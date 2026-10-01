#!/usr/bin/env python3
"""
Generate circular profile images for Deep Matters: Foundations conference organizers.
Simple circular avatars with golden border.
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

# Configuration
OUTPUT_DIR = "organizer_avatars"
AVATAR_SIZE = 400  # Size of the circular avatar

# Organizer data (extracted from organizers-config.js)
ORGANIZERS = {
    "lei-ge": {
        "name": "Lei Ge",
        "image": "images/lei-ge.JPG",
    },
    "samuel-cooper": {
        "name": "Dr. Samuel J. Cooper",
        "image": "images/samuel-cooper.jpg",
    }
}

# Colors
COLOR_ACCENT = "#fab22b"  # Golden border


def create_circular_avatar(image_path, size=400, border_width=8, border_color="#fab22b"):
    """Create a circular avatar with border from an image."""
    # Open and convert image
    img = Image.open(image_path).convert("RGB")
    
    # Crop to square from center
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    img = img.crop((left, top, right, bottom))
    
    # Calculate inner size (accounting for border)
    inner_size = size - (border_width * 2)
    
    # Resize to inner size
    img = img.resize((inner_size, inner_size), Image.LANCZOS)
    
    # Create circular mask for the photo
    mask = Image.new('L', (inner_size, inner_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, inner_size, inner_size), fill=255)
    
    # Create output image with transparent background
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw_output = ImageDraw.Draw(output)
    
    # Draw border circle
    draw_output.ellipse((0, 0, size, size), fill=border_color)
    
    # Create circular photo
    circular_photo = Image.new('RGBA', (inner_size, inner_size), (0, 0, 0, 0))
    circular_photo.paste(img, (0, 0))
    circular_photo.putalpha(mask)
    
    # Paste circular photo in the center (with border)
    output.paste(circular_photo, (border_width, border_width), circular_photo)
    
    return output


def main():
    """Generate circular avatars for all organizers."""
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generating circular avatars for {len(ORGANIZERS)} organizers...")
    print(f"Output directory: {output_path.absolute()}")
    print(f"Avatar size: {AVATAR_SIZE}x{AVATAR_SIZE} pixels\n")
    
    for organizer_id, organizer_data in ORGANIZERS.items():
        try:
            avatar = create_circular_avatar(
                organizer_data["image"], 
                size=AVATAR_SIZE,
                border_width=8,
                border_color=COLOR_ACCENT
            )
            output_file = output_path / f"{organizer_id}-avatar.png"
            avatar.save(output_file, "PNG", quality=95, optimize=True)
            print(f"✓ Generated: {output_file.name} - {organizer_data['name']}")
        except Exception as e:
            print(f"✗ Error generating avatar for {organizer_id}: {e}")
    
    print(f"\nDone! Generated {len(ORGANIZERS)} circular avatars in {OUTPUT_DIR}/")
    print("All avatars have transparent backgrounds and can be used on any background color.")


if __name__ == "__main__":
    main()
