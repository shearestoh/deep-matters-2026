#!/usr/bin/env python3
"""
Generate LinkedIn share images for Deep Matters: Foundations conference speakers.
Each image includes: speaker photo, conference logo, affiliation logo, name, and event details.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
import json
import os
from pathlib import Path

# Configuration
CONFERENCE_NAME = "Deep Matters: Foundations"
CONFERENCE_DATE = "May 16, 2025"
CONFERENCE_LOCATION = "Imperial College London"
OUTPUT_DIR = "linkedin_images"
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 627  # LinkedIn recommended size

# Speaker data (extracted from speakers-config.js)
SPEAKERS = {
    "hassan-sirelkhatim": {
        "name": "Hassan Sirelkhatim",
        "affiliation": "NVIDIA",
        "image": "images/hassan-sirelkhatim.jpeg",
        "logo": None  # Add nvidia-logo.png if available
    },
    "peter-coveney": {
        "name": "Prof. Peter Coveney",
        "affiliation": "UCL",
        "image": "images/peter-coveney.jpg",
        "logo": None  # Add ucl-logo.png if available
    },
    "james-gin": {
        "name": "James Gin-Pollock",
        "affiliation": "Orbital Materials",
        "image": "images/james-gin.jpg",
        "logo": None  # Add orbital-logo.png if available
    },
    "kevin-jablonka": {
        "name": "Dr. Kevin Maik Jablonka",
        "affiliation": "University of Jena",
        "image": "images/kevin-jablonka.jpg",
        "logo": None  # Add jena-logo.png if available
    },
    "steven-kench": {
        "name": "Dr. Steven Kench",
        "affiliation": "Polaron",
        "image": "images/steven-kench.jpg",
        "logo": "images/polaron-logo.png"
    },
    "sina-samangooei": {
        "name": "Dr. Sina Samangooei",
        "affiliation": "CuspAI",
        "image": "images/sina-samangooei.jpg",
        "logo": None  # Add cuspai-logo.png if available
    },
    "lei-ge": {
        "name": "Lei Ge",
        "affiliation": "Imperial College London",
        "image": "images/lei-ge.JPG",
        "logo": "images/imperial-logo.png"
    }
}

# Colors (matching website theme)
COLOR_BG = "#ffffff"
COLOR_ACCENT = "#fab22b"
COLOR_TEXT_PRIMARY = "#1f2937"
COLOR_TEXT_SECONDARY = "#6b7280"


def get_font(size, bold=False):
    """Get a font with fallback options."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    
    paths = bold_paths if bold else font_paths
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def create_circular_thumbnail(image_path, size=300):
    """Create a circular thumbnail from an image."""
    img = Image.open(image_path).convert("RGB")
    
    # Crop to square from center
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    img = img.crop((left, top, right, bottom))
    
    # Resize
    img = img.resize((size, size), Image.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    return output


def add_border_to_circle(img, border_width=8, border_color="#fab22b"):
    """Add a border around a circular image."""
    size = img.size[0]
    new_size = size + border_width * 2
    
    # Create new image with border
    bordered = Image.new('RGBA', (new_size, new_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bordered)
    
    # Draw border circle
    draw.ellipse((0, 0, new_size, new_size), fill=border_color)
    
    # Paste original image in center
    bordered.paste(img, (border_width, border_width), img)
    
    return bordered


def generate_speaker_image(speaker_id, speaker_data, conference_logo_path="images/logo.png"):
    """Generate a LinkedIn share image for a speaker."""
    
    # Create canvas
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Add gradient background accent
    for i in range(IMAGE_HEIGHT // 3):
        alpha = int(30 * (1 - i / (IMAGE_HEIGHT // 3)))
        color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
        draw.rectangle([(0, i), (IMAGE_WIDTH, i + 1)], fill=color)
    
    # Load and add conference logo (top left)
    try:
        logo = Image.open(conference_logo_path)
        logo_height = 80
        logo_width = int(logo.width * (logo_height / logo.height))
        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
        
        # Add white background for logo
        logo_bg = Image.new('RGB', (logo_width + 40, logo_height + 40), COLOR_BG)
        logo_bg.paste(logo, (20, 20), logo if logo.mode == 'RGBA' else None)
        img.paste(logo_bg, (40, 40))
    except Exception as e:
        print(f"Could not load conference logo: {e}")
    
    # Add speaker photo (centered vertically, left side)
    try:
        speaker_photo = create_circular_thumbnail(speaker_data["image"], size=280)
        speaker_photo = add_border_to_circle(speaker_photo, border_width=6, border_color=COLOR_ACCENT)
        
        photo_x = 150
        photo_y = (IMAGE_HEIGHT - speaker_photo.height) // 2
        img.paste(speaker_photo, (photo_x, photo_y), speaker_photo)
    except Exception as e:
        print(f"Could not load speaker photo for {speaker_id}: {e}")
    
    # Right side content area
    right_x = 500
    
    # Conference details
    font_conference = get_font(32, bold=True)
    font_date = get_font(20)
    font_name = get_font(42, bold=True)
    font_affiliation = get_font(26)
    
    y_position = 120
    
    # Conference name
    draw.text((right_x, y_position), CONFERENCE_NAME, 
              fill=COLOR_TEXT_PRIMARY, font=font_conference)
    y_position += 45
    
    # Date and location
    date_text = f"{CONFERENCE_DATE} • {CONFERENCE_LOCATION}"
    draw.text((right_x, y_position), date_text, 
              fill=COLOR_TEXT_SECONDARY, font=font_date)
    y_position += 80
    
    # Accent line
    draw.rectangle([(right_x, y_position), (right_x + 300, y_position + 4)], 
                   fill=COLOR_ACCENT)
    y_position += 40
    
    # Speaker name
    draw.text((right_x, y_position), speaker_data["name"], 
              fill=COLOR_TEXT_PRIMARY, font=font_name)
    y_position += 55
    
    # Affiliation
    draw.text((right_x, y_position), speaker_data["affiliation"], 
              fill=COLOR_TEXT_SECONDARY, font=font_affiliation)
    y_position += 50
    
    # Add affiliation logo if available
    if speaker_data.get("logo") and os.path.exists(speaker_data["logo"]):
        try:
            affiliation_logo = Image.open(speaker_data["logo"])
            logo_height = 50
            logo_width = int(affiliation_logo.width * (logo_height / affiliation_logo.height))
            # Cap width at 200px
            if logo_width > 200:
                logo_width = 200
                logo_height = int(affiliation_logo.height * (logo_width / affiliation_logo.width))
            
            affiliation_logo = affiliation_logo.resize((logo_width, logo_height), Image.LANCZOS)
            img.paste(affiliation_logo, (right_x, y_position), 
                     affiliation_logo if affiliation_logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Could not load affiliation logo for {speaker_id}: {e}")
    
    return img


def main():
    """Generate LinkedIn images for all speakers."""
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generating LinkedIn share images for {len(SPEAKERS)} speakers...")
    print(f"Output directory: {output_path.absolute()}")
    
    for speaker_id, speaker_data in SPEAKERS.items():
        try:
            img = generate_speaker_image(speaker_id, speaker_data)
            output_file = output_path / f"{speaker_id}-linkedin.png"
            img.save(output_file, "PNG", quality=95, optimize=True)
            print(f"✓ Generated: {output_file}")
        except Exception as e:
            print(f"✗ Error generating image for {speaker_id}: {e}")
    
    print(f"\nDone! Generated {len(SPEAKERS)} images in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
