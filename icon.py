#!/usr/bin/env python3
"""
Create application icon for the Universal Database Importer
"""
from PIL import Image, ImageDraw

def create_app_icon():
    """Create a simple database icon"""
    # Create a 64x64 icon
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw database cylinder
    # Top ellipse
    draw.ellipse([10, 10, 54, 25], fill=(70, 130, 180), outline=(25, 25, 112), width=2)
    
    # Cylinder body
    draw.rectangle([10, 17, 54, 45], fill=(70, 130, 180), outline=None)
    
    # Vertical lines
    draw.line([10, 17, 10, 45], fill=(25, 25, 112), width=2)
    draw.line([54, 17, 54, 45], fill=(25, 25, 112), width=2)
    
    # Bottom ellipse
    draw.ellipse([10, 38, 54, 53], fill=(70, 130, 180), outline=(25, 25, 112), width=2)
    
    # Add some data lines
    draw.line([18, 25, 46, 25], fill=(255, 255, 255), width=1)
    draw.line([18, 30, 46, 30], fill=(255, 255, 255), width=1)
    draw.line([18, 35, 46, 35], fill=(255, 255, 255), width=1)
    
    # Save icon
    img.save('app_icon.png', 'PNG')
    
    # Also create a smaller version for the window
    img_small = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_small.save('app_icon_small.png', 'PNG')
    
    # Create ICO file with multiple sizes
    img.save('app_icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (64, 64)])
    
    print("Icon files created successfully!")

if __name__ == "__main__":
    create_app_icon()