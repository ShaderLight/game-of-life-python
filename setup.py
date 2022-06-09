import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "logging", "json", "tkinter"], "include_files":["glider.ico"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TheGameOfLife",
    version="1.0",
    description="The game of life in Python",
    options={"build_exe": build_exe_options},
    executables=[Executable("run.py", base=base)],
)