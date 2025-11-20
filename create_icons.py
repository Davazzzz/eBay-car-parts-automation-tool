"""Generate app icons for PWA"""
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    # Create a gradient background
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)

    # Draw a simple car icon representation
    # Draw a rectangle for car body
    car_width = int(size * 0.6)
    car_height = int(size * 0.3)
    x1 = (size - car_width) // 2
    y1 = int(size * 0.45)
    x2 = x1 + car_width
    y2 = y1 + car_height

    draw.rectangle([x1, y1, x2, y2], fill='white', outline='white')

    # Draw wheels
    wheel_radius = int(size * 0.08)
    wheel1_x = x1 + int(car_width * 0.25)
    wheel2_x = x2 - int(car_width * 0.25)
    wheel_y = y2

    draw.ellipse([wheel1_x - wheel_radius, wheel_y - wheel_radius,
                  wheel1_x + wheel_radius, wheel_y + wheel_radius],
                 fill='white')
    draw.ellipse([wheel2_x - wheel_radius, wheel_y - wheel_radius,
                  wheel2_x + wheel_radius, wheel_y + wheel_radius],
                 fill='white')

    # Draw dollar sign
    dollar_size = int(size * 0.15)
    dollar_x = size // 2
    dollar_y = int(size * 0.25)

    try:
        font = ImageFont.truetype("arial.ttf", dollar_size)
    except:
        font = ImageFont.load_default()

    draw.text((dollar_x, dollar_y), "$", fill='white', font=font, anchor='mm')

    # Save
    img.save(filename, 'PNG')
    print(f"Created {filename}")

if __name__ == '__main__':
    create_icon(192, 'static/icon-192.png')
    create_icon(512, 'static/icon-512.png')
    print("Icons created successfully!")
