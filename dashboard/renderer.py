import requests
import os
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

# Configuration
HA_URL = "http://localhost:8123/api"
ENV_FILE = "/opt/.env"
OUTPUT_PATH = "/opt/pizero/dashboard/latest.png"
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def get_ha_token():
    try:
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith('HOMEASSISTANT_TOKEN'):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception as e:
        print(f"Error reading env file: {e}")
    return None

def fetch_ha_data(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    entities = [
        "sensor.total_solar_power",
        "sensor.geyser_power",
        "sensor.freezer_power",
        "sensor.heat_pump_power"
    ]
    
    data = {}
    for entity in entities:
        try:
            response = requests.get(f"{HA_URL}/states/{entity}", headers=headers)
            if response.status_code == 200:
                data[entity] = response.json()
            else:
                data[entity] = {"state": "N/A", "attributes": {"unit_of_measurement": ""}}
        except Exception as e:
            data[entity] = {"state": "Error", "attributes": {"unit_of_measurement": ""}}
    return data

def render_dashboard(data):
    # Create a 1920x1080 dark image
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(image)
    
    # Fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, 80)
        label_font = ImageFont.truetype(FONT_PATH, 60)
        value_font = ImageFont.truetype(FONT_PATH, 120)
        time_font = ImageFont.truetype(FONT_PATH, 40)
    except Exception as e:
        print(f"Error loading font: {e}")
        # Fallback to default font
        title_font = label_font = value_font = time_font = ImageFont.load_default()
    
    # Draw Title
    draw.text((100, 80), "Home Server Status", font=title_font, fill=(255, 255, 255))
    
    # Draw Date/Time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((100, 180), f"Last Updated: {now}", font=time_font, fill=(150, 150, 150))
    
    # Draw Grid
    items = [
        ("Solar Power", "sensor.total_solar_power", (255, 200, 0)),
        ("Geyser", "sensor.geyser_power", (255, 100, 100)),
        ("Freezers", "sensor.freezer_power", (100, 255, 100)),
        ("Heat Pump", "sensor.heat_pump_power", (100, 100, 255))
    ]
    
    start_x, start_y = 100, 300
    col_width, row_height = 800, 300
    
    for i, (label, entity_id, color) in enumerate(items):
        row = i // 2
        col = i % 2
        x = start_x + col * col_width
        y = start_y + row * row_height
        
        # Draw Box
        draw.rectangle([x, y, x + col_width - 50, y + row_height - 50], outline=(50, 50, 50), width=2)
        
        # Draw Label
        draw.text((x + 20, y + 20), label, font=label_font, fill=(200, 200, 200))
        
        # Draw Value
        entity_data = data.get(entity_id, {})
        state = entity_data.get("state", "N/A")
        unit = entity_data.get("attributes", {}).get("unit_of_measurement", "")
        draw.text((x + 20, y + 100), f"{state} {unit}", font=value_font, fill=color)
        
    # Save Image
    image.save(OUTPUT_PATH)
    print(f"Dashboard saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    token = get_ha_token()
    if token:
        data = fetch_ha_data(token)
        render_dashboard(data)
    else:
        print("Error: Could not find HA token.")
