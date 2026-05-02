#!/usr/bin/env python3
"""
Generate favicon variants from icon-512.svg using manual PNG generation
"""
from PIL import Image, ImageDraw
import io

def create_favicon_from_svg_concept(size):
    """
    Recreate the icon design at specified size
    Based on icon-512.svg design (beige bg, red geometric shapes)
    """
    # Create image with beige background
    img = Image.new('RGBA', (size, size), '#E8E0D0')
    draw = ImageDraw.Draw(img)
    
    # Calculate proportions (based on 512px reference)
    scale = size / 512
    
    # Colors
    red = '#8B1A1A'
    red_alpha = (139, 26, 26, 26)  # 10% opacity for fill
    
    # Main square (120, 120, 392, 392 in 512px)
    square_margin = int(120 * scale)
    square_size = int(272 * scale)
    square_end = square_margin + square_size
    
    # Draw main square
    draw.rectangle(
        [(square_margin, square_margin), (square_end, square_end)],
        outline=red,
        width=max(1, int(4 * scale))
    )
    
    # Center point
    center = size // 2
    
    # Draw center circle (r=80 in 512px)
    circle_radius = int(80 * scale)
    draw.ellipse(
        [(center - circle_radius, center - circle_radius),
         (center + circle_radius, center + circle_radius)],
        outline=red,
        width=max(1, int(4 * scale))
    )
    
    # Draw diamond shape inside circle (176, 256, 336, 256 points)
    diamond_offset = int(80 * scale)
    diamond_points = [
        (center, center - diamond_offset),  # top
        (center + diamond_offset, center),  # right
        (center, center + diamond_offset),  # bottom
        (center - diamond_offset, center),  # left
    ]
    draw.polygon(diamond_points, fill=red_alpha, outline=red, width=max(1, int(2 * scale)))
    
    return img

# Generate 32x32 favicon
print("Generating favicon-32x32.png...")
img_32 = create_favicon_from_svg_concept(32)
img_32.save('favicon-32x32.png', 'PNG')
print("✓ Generated favicon-32x32.png")

# Generate 16x16 favicon
print("Generating favicon-16x16.png...")
img_16 = create_favicon_from_svg_concept(16)
img_16.save('favicon-16x16.png', 'PNG')
print("✓ Generated favicon-16x16.png")

# Generate ICO with both sizes
print("Generating favicon.ico...")
img_32.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)], append_images=[img_16])
print("✓ Generated favicon.ico (multi-size)")

print("\n✓ All favicons generated from icon-512.svg design")
