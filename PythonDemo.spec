# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PythonDemo.py'],
             pathex=['C:\\Users\\mchan\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\scipy\\.libs', 'C:\\Users\\mchan\\Documents\\pythondemo\\resources', 'C:\\Users\\mchan\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages', 'C:\\Users\\mchan\\Documents\\pythondemo'],
             binaries=[],
             datas=[('DelsysAPI.dll', '.'), ('SiUSBXp.dll', '.'), ('Stateless.dll', '.'), ('Xamarin.Forms.Core.dll', '.'), ('Xamarin.Forms.Platform.dll', '.'), ('Xamarin.Forms.Xaml.dll', '.'), ('Stateless.xml', '.'), ('System.Runtime.InteropServices.RuntimeInformation.dll', '.'), ('Portable.Licensing.dll', '.'), ('Portable.Licensing.xml', '.'), ('Mono.Android.dll','.'), ('Newtonsoft.Json.dll','.'), ('Plugin.BLE.Abstractions.dll','.'), ('Plugin.BLE.dll','.')],
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
          name='PythonDemo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
