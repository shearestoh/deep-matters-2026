#!/usr/bin/env python3
"""
Generate circular profile images for Deep Matters: Foundations conference speakers.
Simple circular avatars with golden border.
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

# Configuration
OUTPUT_DIR = "speaker_avatars"
AVATAR_SIZE = 400  # Size of the circular avatar

# Speaker data (extracted from speakers-config.js)
SPEAKERS = {
    "hassan-sirelkhatim": {
        "name": "Hassan Sirelkhatim",
        "image": "images/hassan-sirelkhatim.jpeg",
    },
    "peter-coveney": {
        "name": "Prof. Peter Coveney",
        "image": "images/peter-coveney.jpg",
    },
    "james-gin": {
        "name": "James Gin-Pollock",
        "image": "images/james-gin.jpg",
    },
    "kevin-jablonka": {
        "name": "Dr. Kevin Maik Jablonka",
        "image": "images/kevin-jablonka.jpg",
    },
    "steven-kench": {
        "name": "Dr. Steven Kench",
        "image": "images/steven-kench.jpg",
    },
    "sina-samangooei": {
        "name": "Dr. Sina Samangooei",
        "image": "images/sina-samangooei.jpg",
    },
    "lei-ge": {
        "name": "Lei Ge",
        "image": "images/lei-ge.JPG",
    },
    "ronan-docherty": {
        "name": "Ronan Docherty",
        "image": "images/ronan-docherty.jpg",
    },
    "francesco-ferroni": {
        "name": "Dr. Francesco Ferroni",
        "image": "images/francesco-ferroni.jpg",
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
    """Generate circular avatars for all speakers."""
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generating circular avatars for {len(SPEAKERS)} speakers...")
    print(f"Output directory: {output_path.absolute()}")
    print(f"Avatar size: {AVATAR_SIZE}x{AVATAR_SIZE} pixels\n")
    
    for speaker_id, speaker_data in SPEAKERS.items():
        try:
            avatar = create_circular_avatar(
                speaker_data["image"], 
                size=AVATAR_SIZE,
                border_width=8,
                border_color=COLOR_ACCENT
            )
            output_file = output_path / f"{speaker_id}-avatar.png"
            avatar.save(output_file, "PNG", quality=95, optimize=True)
            print(f"✓ Generated: {output_file.name} - {speaker_data['name']}")
        except Exception as e:
            print(f"✗ Error generating avatar for {speaker_id}: {e}")
    
    print(f"\nDone! Generated {len(SPEAKERS)} circular avatars in {OUTPUT_DIR}/")
    print("All avatars have transparent backgrounds and can be used on any background color.")


if __name__ == "__main__":
    main()
