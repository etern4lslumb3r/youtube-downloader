from distutils.core import setup
import py2exe
import sys

if len(sys.argv) == 1:
    sys.argv.append("py2exe")

setup( options = {"py2exe": {"compressed": 1, "optimize": 2, "ascii": 1, "bundle_files": 3}},
       zipfile = None,
       
       
       #Can use windows or console,replace my_file.py with py file you want to make exe off.
       #If not run in same folder give path /mydir/my_file.py
       windows = [{"script": 'youtube-downloader.py'}])