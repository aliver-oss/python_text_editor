#! ./python_editor/bin/python


from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.application import get_app
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import *
from pygments.styles.solarized import SolarizedDarkStyle
from pygments.styles import get_style_by_name
from prompt_toolkit.styles.pygments import style_from_pygments_cls
import pathlib
import os
import sys

from highlighting import syntax_highlight


class editor:
    def __init__(self, file):
        self.file_name = file

    def run(self):
        """start text editor with the text existing in the file"""

        self.editor_window().run()

    def open_file(self):
        """method resposible for opening a file"""

        # create file if doesn't exists
        try:
            file = open(self.file_name, "x")
            file.close()
        except FileExistsError:
            pass

        self.file_abs_path = os.path.abspath(self.file_name)

        # open file for reading
        if os.path.isfile(self.file_abs_path):
            file = open(self.file_abs_path, "r")
            lines = file.read()
            file.close()
        else:
            self.app.exit("Argument is not a file, please try again")

        return lines

    def editor_window(self):
        """configure the editor window and returns a application class"""
        self.buffer_1 = Buffer() # need the text in another method
        self.text = self.open_file()

        f_ext = pathlib.PurePath(self.file_abs_path).suffix

        # set container(s)
        self.buffer_1.text = self.text 
        style_n = style_from_pygments_cls(get_style_by_name("friendly"))
        container = Window(BufferControl(buffer=self.buffer_1, lexer=syntax_highlight(f_ext)))
        
        # create layout
        layout_editor = Layout(container)

        # make an instance from keybinds method
        key_bind = self.key_binds("")
        
        # define application that will be started
        app = Application(layout=layout_editor, key_bindings=key_bind, full_screen=True, style=style_n)

        return app

    def key_binds(self, keybind):
        """handle keybinds"""
        bindings = KeyBindings()

        @bindings.add("c-s")
        def save(bind):
            self.save()

        @bindings.add("c-z")
        def quit(bind):
            bind.app.exit()
        
        return bindings

    def save(self):
        """save the text to the file"""
        final_text = self.buffer_1.text

        open_file = open(self.file_abs_path, "w")
        open_file.write(final_text)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        program = editor(sys.argv[1])
        program.run()
    else:
        raise Exception("Please provide the file to be opened as an argument\
 to the cli like in the example: python script <file>")