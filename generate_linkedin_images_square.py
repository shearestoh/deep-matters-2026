#!/usr/bin/env python3
"""
Generate square (1:1) LinkedIn share images for Deep Matters: Foundations conference speakers.
Each image includes: speaker photo, conference logo, affiliation logo, name, and event details.
Optimized for Instagram and LinkedIn square format (1080x1080).
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from pathlib import Path

# Configuration
CONFERENCE_NAME = "Deep Matters: Foundations"
CONFERENCE_DATE = "May 16, 2025"
CONFERENCE_LOCATION = "Imperial College London"
OUTPUT_DIR = "linkedin_images"
IMAGE_SIZE = 1080  # Square format

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
COLOR_DARK = "#1f1f1f"
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


def create_rounded_square_thumbnail(image_path, size=350, radius=25):
    """Create a rounded square thumbnail from an image."""
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
    
    # Create rounded rectangle mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    return output


def add_border_to_square(img, border_width=6, border_color="#fab22b", radius=30):
    """Add a border around a rounded square image."""
    size = img.size[0]
    new_size = size + border_width * 2
    
    # Create new image with border
    bordered = Image.new('RGBA', (new_size, new_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bordered)
    
    # Draw border rounded rectangle
    draw.rounded_rectangle((0, 0, new_size, new_size), radius=radius, fill=border_color)
    
    # Paste original image in center
    bordered.paste(img, (border_width, border_width), img)
    
    return bordered


def generate_speaker_image(speaker_id, speaker_data, conference_logo_path="images/logo.png"):
    """Generate a square LinkedIn share image for a speaker."""
    
    # Create canvas with dark top section and light bottom section
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Dark top section (about 22% of image)
    dark_section_height = 240
    draw.rectangle([(0, 0), (IMAGE_SIZE, dark_section_height)], fill=COLOR_DARK)
    
    # Load and add conference logo (top left)
    logo_y = 35
    try:
        logo = Image.open(conference_logo_path)
        logo_height = 70
        logo_width = int(logo.width * (logo_height / logo.height))
        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
        
        # Add logo
        img.paste(logo, (50, logo_y), logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Could not load conference logo: {e}")
    
    # Conference details in top section
    font_conference = get_font(28, bold=True)
    font_date = get_font(17)
    
    conf_y = logo_y + 10
    
    # Conference name (in white on dark background)
    draw.text((50, conf_y + 90), CONFERENCE_NAME, 
              fill="#ffffff", font=font_conference)
    
    # Date and location
    date_text = f"{CONFERENCE_DATE} • {CONFERENCE_LOCATION}"
    draw.text((50, conf_y + 125), date_text, 
              fill="#a0a0a0", font=font_date)
    
    # Add speaker photo (centered, overlapping the dark/light sections)
    photo_size = 350
    try:
        speaker_photo = create_rounded_square_thumbnail(speaker_data["image"], size=photo_size)
        speaker_photo = add_border_to_square(speaker_photo, border_width=6, border_color=COLOR_ACCENT)
        
        photo_x = (IMAGE_SIZE - speaker_photo.width) // 2
        photo_y = dark_section_height - 50  # Overlap into light section
        img.paste(speaker_photo, (photo_x, photo_y), speaker_photo)
    except Exception as e:
        print(f"Could not load speaker photo for {speaker_id}: {e}")
    
    # Bottom section content
    font_name = get_font(44, bold=True)
    font_affiliation = get_font(26)
    
    # Calculate text positions (below the photo)
    text_start_y = photo_y + speaker_photo.height + 40
    
    # Speaker name (centered)
    name_bbox = draw.textbbox((0, 0), speaker_data["name"], font=font_name)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (IMAGE_SIZE - name_width) // 2
    
    draw.text((name_x, text_start_y), speaker_data["name"], 
              fill=COLOR_TEXT_PRIMARY, font=font_name)
    
    # Affiliation (centered)
    affil_bbox = draw.textbbox((0, 0), speaker_data["affiliation"], font=font_affiliation)
    affil_width = affil_bbox[2] - affil_bbox[0]
    affil_x = (IMAGE_SIZE - affil_width) // 2
    
    draw.text((affil_x, text_start_y + 55), speaker_data["affiliation"], 
              fill=COLOR_TEXT_SECONDARY, font=font_affiliation)
    
    # Add affiliation logo if available (centered below text)
    if speaker_data.get("logo") and os.path.exists(speaker_data["logo"]):
        try:
            affiliation_logo = Image.open(speaker_data["logo"])
            logo_height = 55
            logo_width = int(affiliation_logo.width * (logo_height / affiliation_logo.height))
            # Cap width at 220px
            if logo_width > 220:
                logo_width = 220
                logo_height = int(affiliation_logo.height * (logo_width / affiliation_logo.width))
            
            affiliation_logo = affiliation_logo.resize((logo_width, logo_height), Image.LANCZOS)
            
            logo_x = (IMAGE_SIZE - logo_width) // 2
            logo_y = text_start_y + 110
            
            img.paste(affiliation_logo, (logo_x, logo_y), 
                     affiliation_logo if affiliation_logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Could not load affiliation logo for {speaker_id}: {e}")
    
    # Add a subtle accent line at the bottom
    accent_line_y = IMAGE_SIZE - 15
    line_width = 250
    line_x = (IMAGE_SIZE - line_width) // 2
    draw.rectangle([(line_x, accent_line_y), (line_x + line_width, accent_line_y + 4)], 
                   fill=COLOR_ACCENT)
    
    return img


def main():
    """Generate LinkedIn images for all speakers."""
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    print(f"Generating square (1080x1080) LinkedIn share images for {len(SPEAKERS)} speakers...")
    print(f"Output directory: {output_path.absolute()}")
    
    for speaker_id, speaker_data in SPEAKERS.items():
        try:
            img = generate_speaker_image(speaker_id, speaker_data)
            output_file = output_path / f"{speaker_id}-linkedin-square.png"
            img.save(output_file, "PNG", quality=95, optimize=True)
            print(f"✓ Generated: {output_file}")
        except Exception as e:
            print(f"✗ Error generating image for {speaker_id}: {e}")
    
    print(f"\nDone! Generated {len(SPEAKERS)} square images in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
