# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Laptop Battery Test
"""

import sys
from pathlib import Path

block_cipher = None

# Get the absolute path to the project directory
project_dir = Path(SPECPATH).resolve()

a = Analysis(
    ['main.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        # Include test files if needed
        ('test_files', 'test_files'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'pyautogui',
        'psutil',
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
    [],
    exclude_binaries=True,
    name='LaptopBatteryTest',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LaptopBatteryTest',
)

# macOS specific: Create app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='LaptopBatteryTest.app',
        icon=None,  # Add icon path here if you have one: 'assets/icon.icns'
        bundle_identifier='com.duyluan.laptopbatterytest',
        info_plist={
            'CFBundleName': 'Laptop Battery Test',
            'CFBundleDisplayName': 'Laptop Battery Test',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
            'LSMinimumSystemVersion': '12.0',
        },
    )
