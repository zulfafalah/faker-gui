# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Faker GUI Windows executable.
This file provides fine-grained control over the build process.

You can use this spec file instead of command-line arguments:
pyinstaller faker_gui.spec
"""

block_cipher = None


a = Analysis(
    ['faker_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('example_ddl.sql', '.'),
        ('example_config.json', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'faker',
        'faker.providers',
    ],
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
    name='FakerGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .ico file path here if you have one
)
