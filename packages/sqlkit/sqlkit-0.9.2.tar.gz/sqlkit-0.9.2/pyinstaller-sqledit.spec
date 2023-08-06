# -*- mode: python -*-
# spec file for pyinstaller. Read README.pyinstaller for more info 

import os
import sys

ROOT = os.path.dirname(sys.argv[1]) + '/'

#sqlkit = Tree(ROOT + 'sqlkit', prefix='sqlkit')
icon = Tree(ROOT + 'sqlkit/layout', excludes='*.py')
locale = Tree(ROOT + 'sqlkit/locale', prefix='sqlkit/locale')
demo = Tree(ROOT + 'demo', prefix='demo',
            excludes= ROOT + 'demo/layout')

a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'),
              os.path.join(HOMEPATH,'support/useUnicode.py'),
              ROOT + '/bin/sqledit'],
             pathex=[os.path.abspath(os.path.dirname(sys.argv[0]))]
             )

pyz = PYZ(a.pure )
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/sqledit', 'sqledit'),
          debug=False,
          strip=True,
          upx=True,
          console=1 )

coll = COLLECT( exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                demo,
                icon,
                locale,
                #sqlkit,
                strip=False,
                upx=True,
                name=os.path.join('pyinstaller', 'sqledit')
                )
