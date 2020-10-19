# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\mchan\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\scipy\\.libs', 'C:\\Users\\mchan\\Documents\\pythondemo\\resources', 'C:\\Users\\mchan\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages', 'C:\\Users\\mchan\\Documents\\pythondemo'],
             binaries=[],
             datas=[('C:\\Users\\mchan\\Documents\\pythondemo\\resources', 'resources' )],
             hiddenimports=['clr'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
