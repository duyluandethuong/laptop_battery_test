#!/usr/bin/env python3
"""Convert PNG to ICNS format for macOS app icons."""

import subprocess
import sys
import os
from pathlib import Path

def create_icns(png_path, output_path=None):
    """Convert a PNG image to ICNS format."""
    png_path = Path(png_path)
    if not png_path.exists():
        print(f"Error: {png_path} not found")
        return False
    
    if output_path is None:
        output_path = png_path.with_suffix('.icns')
    else:
        output_path = Path(output_path)
    
    iconset_dir = png_path.with_suffix('.iconset')
    if iconset_dir.exists():
        import shutil
        shutil.rmtree(iconset_dir)
    iconset_dir.mkdir(exist_ok=True)
    
    sizes = [
        (16, 'icon_16x16.png'),
        (32, 'icon_16x16@2x.png'),
        (32, 'icon_32x32.png'),
        (64, 'icon_32x32@2x.png'),
        (128, 'icon_128x128.png'),
        (256, 'icon_128x128@2x.png'),
        (256, 'icon_256x256.png'),
        (512, 'icon_256x256@2x.png'),
        (512, 'icon_512x512.png'),
        (1024, 'icon_512x512@2x.png'),
    ]
    
    print(f"Creating iconset from {png_path}...")
    for size, filename in sizes:
        output_file = iconset_dir / filename
        try:
            subprocess.run([
                'sips', '-z', str(size), str(size),
                str(png_path), '--out', str(output_file)
            ], check=True, capture_output=True)
            print(f"  ✓ Created {filename} ({size}x{size})")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to create {filename}: {e}")
            return False
    
    print(f"Converting iconset to {output_path}...")
    try:
        subprocess.run([
            'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting to ICNS: {e}")
        return False
    
    # Clean up
    import shutil
    shutil.rmtree(iconset_dir)
    
    print(f"✓ Successfully created {output_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python create_icns.py <input.png> [output.icns]")
        print("\nExample:")
        print("  python create_icns.py my_icon.png icons/app_icon.icns")
        sys.exit(1)
    
    success = create_icns(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit(0 if success else 1)




















