# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

BANGTAL_HOME = "C:/Program Files (x86)/Bosornd/Bangtal/"


a = Analysis(['Tetris.py'],
             pathex=['.'],
             binaries=[],
             datas=[(BANGTAL_HOME + 'bin/bangtal.dll', './'),
             		(BANGTAL_HOME + 'res', 'res'), ('Images', 'Images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tetris',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Tetris')
