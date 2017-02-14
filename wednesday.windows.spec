# -*- mode: python -*-
a = Analysis(['wednesday/ui.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.win32/main', 'wednesday.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )

from os import listdir
from os.path import isfile, join

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('wednesday'))
