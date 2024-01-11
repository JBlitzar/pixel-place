from flask import Flask, jsonify, Response, send_file
from PIL import Image
import time
from io import BytesIO

app = Flask(__name__)

# Initialize a 100x100 white image
image = Image.new('RGB', (100, 100), 'white')

toggle_count = 0
last_toggle_time = 0

@app.route('/')
def main_img():
    temp_filename = "temp_image.png"
    image.save(temp_filename)
    return send_file(temp_filename, mimetype='image/png', as_attachment=True, download_name='image.png')


@app.route('/togglepixel/<int:x>/<int:y>')
def toggle_pixel(x, y):
    global toggle_count, last_toggle_time

    current_time = time.time()

    if current_time - last_toggle_time > 30:
        # Reset if more than 30 seconds have passed since the last toggle
        toggle_count = 0

    toggle_count += 1
    last_toggle_time = current_time

    if toggle_count == 2:
        print("togglecount == 2!")
        # Toggle the pixel in the image
        pixel_color = image.getpixel((x, y))
        new_color = (0, 0, 0) if pixel_color == (255, 255, 255) else (255, 255, 255)
        image.putpixel((x, y), new_color)
        toggle_count = 0  # Reset the toggle count after successful toggle

        temp_filename = "temp_image.png"
        image.save(temp_filename)
        # Return blue 1x1 pixel
        return send_file("blue.png", mimetype='image/png', as_attachment=True, download_name='image.png')

    # Return red 1x1 pixel
    red_pixel = Image.new('RGB', (1, 1), 'red')
    return send_file("red.png", mimetype='image/png', as_attachment=True, download_name='red.png')

if __name__ == '__main__':
    app.run(debug=True)
