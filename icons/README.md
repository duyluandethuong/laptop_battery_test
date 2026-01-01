# App Icon Setup

This directory should contain your app icon file.

## Icon File Format

macOS requires icons in the `.icns` format. The icon file should be named `app_icon.icns` and placed in this directory.

## How to Create an .icns File

### Option 1: Using macOS Icon Composer (Recommended)

1. **Create your icon image**:
   - Design your icon at 1024x1024 pixels (or larger, square)
   - Save as PNG format
   - Name it `app_icon.png`

2. **Convert to .icns using macOS tools**:
   ```bash
   # Create an iconset directory
   mkdir app_icon.iconset
   
   # Generate all required sizes
   sips -z 16 16     app_icon.png --out app_icon.iconset/icon_16x16.png
   sips -z 32 32     app_icon.png --out app_icon.iconset/icon_16x16@2x.png
   sips -z 32 32     app_icon.png --out app_icon.iconset/icon_32x32.png
   sips -z 64 64     app_icon.png --out app_icon.iconset/icon_32x32@2x.png
   sips -z 128 128   app_icon.png --out app_icon.iconset/icon_128x128.png
   sips -z 256 256   app_icon.png --out app_icon.iconset/icon_128x128@2x.png
   sips -z 256 256   app_icon.png --out app_icon.iconset/icon_256x256.png
   sips -z 512 512   app_icon.png --out app_icon.iconset/icon_256x256@2x.png
   sips -z 512 512   app_icon.png --out app_icon.iconset/icon_512x512.png
   sips -z 1024 1024 app_icon.png --out app_icon.iconset/icon_512x512@2x.png
   
   # Convert iconset to icns
   iconutil -c icns app_icon.iconset
   
   # Clean up
   rm -rf app_icon.iconset
   ```

3. **Move the .icns file here**:
   ```bash
   mv app_icon.icns icons/app_icon.icns
   ```

### Option 2: Using Online Converters

1. Create your icon image (1024x1024 PNG)
2. Use an online converter like:
   - https://cloudconvert.com/png-to-icns
   - https://convertio.co/png-icns/
3. Download the .icns file and place it in this directory as `app_icon.icns`

### Option 3: Using Image2icon App

1. Download Image2icon from the Mac App Store (free)
2. Drag your PNG image into Image2icon
3. Export as .icns
4. Place the file in this directory as `app_icon.icns`

### Option 4: Using Python Script

A helper script is provided below to automate the conversion:

```python
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
        subprocess.run([
            'sips', '-z', str(size), str(size),
            str(png_path), '--out', str(output_file)
        ], check=True)
        print(f"  Created {filename} ({size}x{size})")
    
    print(f"Converting iconset to {output_path}...")
    subprocess.run([
        'iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)
    ], check=True)
    
    # Clean up
    import shutil
    shutil.rmtree(iconset_dir)
    
    print(f"✓ Successfully created {output_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python create_icns.py <input.png> [output.icns]")
        sys.exit(1)
    
    create_icns(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

Save this as `create_icns.py` and run:
```bash
python create_icns.py your_icon.png icons/app_icon.icns
```

## Icon Design Guidelines

- **Size**: Start with at least 1024x1024 pixels
- **Format**: PNG with transparency
- **Style**: 
  - Simple, recognizable design
  - Works well at small sizes (16x16)
  - Avoid fine details that won't be visible when scaled down
- **Background**: Can be transparent or solid color
- **Content**: Should represent your app (robot hand, control interface, etc.)

## After Creating the Icon

Once you have `app_icon.icns` in this directory, the build scripts will automatically use it when you rebuild the app.




















