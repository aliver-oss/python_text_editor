# implement syntax highlighting and completion depending on the file ext

from pygments import lexers
from prompt_toolkit.lexers import PygmentsLexer


def syntax_highlight(file_ext):
    """return syntax highlight to be used using pygments """
    if file_ext == ".py":
        lexer = PygmentsLexer(lexers.python.PythonLexer)
    elif file_ext == ".c":
        lexer = PygmentsLexer(lexers.c_cpp.CLexer)
    elif file_ext == ".rs":
        lexer = PygmentsLexer(lexers.rust.RustLexer)
    else:
        lexer = None

    return lexer
