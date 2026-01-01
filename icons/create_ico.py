from PIL import Image
from pathlib import Path

def create_ico(png_path, output_path):
    png_path = Path(png_path)
    output_path = Path(output_path)
    
    if not png_path.exists():
        print(f"Error: {png_path} not found")
        return

    img = Image.open(png_path)
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Created {output_path}")

if __name__ == "__main__":
    create_ico("icons/app_icon.png", "icons/app_icon.ico")
