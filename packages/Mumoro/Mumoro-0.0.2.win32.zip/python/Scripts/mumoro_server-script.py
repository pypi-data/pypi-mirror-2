#!c:\python\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Mumoro==0.0.2','console_scripts','mumoro_server'
__requires__ = 'Mumoro==0.0.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Mumoro==0.0.2', 'console_scripts', 'mumoro_server')()
    )
