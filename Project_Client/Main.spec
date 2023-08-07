# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[('Icon/*.png', 'images'), ('App_Init.py', '.'), ('UI_App.ui', '.'), ('icon_toolbar.py', '.'), ('App_Help.py', '.'), ('App_Active.py', '.'), ('UI_App_Active.ui', '.'), ('App_Active_Screen.py', '.'), ('Network_Control.py', '.'), ('Network_Packet.py', '.'), ('UI_App_Screen.ui', '.'), ('UI_Help_Introduction.ui', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
