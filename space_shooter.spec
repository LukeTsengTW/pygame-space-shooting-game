# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the pygame space-shooter game.
# Build with:  .venv\Scripts\pyinstaller.exe space_shooter.spec
#
# onedir + windowed (no console). All runtime assets are bundled and a
# runtime hook (pyinstaller_runtime_hook.py) chdir's into the bundle so the
# game's relative asset paths keep working unchanged.

datas = [
    ('img', 'img'),
    ('music', 'music'),
    ('sound_effect', 'sound_effect'),
    ('font.ttf', '.'),
    ('icon.png', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyinstaller_runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SpaceShooter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SpaceShooter',
)
