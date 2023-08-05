"""
Kung is a utility application like less or more to read files, it approves upon
less and more by adding in syntax highlighting and whatever other features your
browser will support.
"""

#!/usr/bin/env python

from pygments import highlight
from pygments.lexers import (find_lexer_class, get_lexer_for_mimetype,
                             get_lexer_for_filename, guess_lexer,
                             guess_lexer_for_filename, get_lexer_by_name,
                             ClassNotFound as LexerClassNotFound)
from pygments.util import ClassNotFound as MimeClassNotFound
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from webbrowser import open as webopen
import argparse
from mimetypes import guess_type
from tempfile import NamedTemporaryFile
from sys import (stdin, argv)

class Kung():
    """A class to hold state and behaviour."""

    def __init__(self, path, number, filetype, style):
        self.path = path
        self.contents = self.path.read()
        self.linenos = number
        self.filetype = filetype
        self.temp = NamedTemporaryFile(suffix=".html", delete=False)
        self.lexer = self.get_lexer()
        self.style = style
        self.pygment()
        webopen(self.temp.name)
        return None

    def get_lexer(self):
        """
        Get the lexer for the give file at self.path.

        I haven't yet seen a way to clean up the nest try/catches that equally
        effiecient. If someone knows a better way then please fork and make the
        change.
        """

        #user specified filetype
        if self.filetype:
            try:
                return get_lexer_by_name(self.filetype)
            except LexerClassNotFound:
                lexer_class = find_lexer_class(self.filetype)
                try:
                    for alias in lexer_class.aliases:
                        try:
                            return get_lexer_by_name(alias)
                        except LexerClassNotFound:
                            continue
                except (AttributeError, LexerClassNotFound):
                    pass
        #have to guess the filetype/lexer
        try:
            return get_lexer_for_mimetype(guess_type(self.path.name)[0])
        except MimeClassNotFound:
            try:
                return get_lexer_for_filename(self.path.name)
            except LexerClassNotFound:
                try:
                    return guess_lexer_for_filename(self.path.name,
                                                     self.contents)
                except LexerClassNotFound:
                    try:
                        return guess_lexer(self.contents)
                    except LexerClassNotFound:
                        pass
        if not lexer:
            print "Unknown file type, can't add syntax coloring."
            return get_lexer_by_name("Text")

    def pygment(self):
        """Add in the syntax coloring required for the file at self.path."""

        if self.style and not self.style in list(get_all_styles()):
            print "Unknown style %s, using colorful." % self.style
            self.style = "colorful"
        formatter = HtmlFormatter(full=True, style=self.style,
                                  linenos=self.linenos)
        result = highlight(self.contents, self.lexer, formatter)
        self.temp.write(result.encode('utf8'))
        return None

def main():
    """Function to put everything together when called from the terminal."""

    parser = argparse.ArgumentParser(description="more with less")
    parser.add_argument("file", type=argparse.FileType('r'),
                        default=stdin,
                        help="""file to be read (use '-' 
                        as last arg to read from stdin)""")
    parser.add_argument("-nu", "--number", default=False, action="store_true", 
                        help="print the line number in front of each line")
    parser.add_argument("-ft", "--filetype", help="explicity set the filetype")
    parser.add_argument("-st", "--style", default="colorful",
                        help="explicity set the style.")
    try:
        if argv[1] == "-":
            args = parser.parse_args(["-"])
        else:
            args = parser.parse_args()
        Kung(args.file, args.number, args.filetype, args.style)
    except IndexError:
        parser.print_help()
