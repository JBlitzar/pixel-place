from flask import Flask, jsonify, Response, send_file
from PIL import Image
import time
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize a 100x100 white image
size = 100
image = Image.new('RGB', (size, size), 'white')

toggle_count = 0
last_toggle_time = 0
temp_filename = "/tmp/temp_image.png"
@app.route('/')
def main_img():
    print("get /")
    image.save(temp_filename)
    return send_file(temp_filename, mimetype='image/png', as_attachment=True, download_name='image.png')


@app.route('/togglepixel/<int:x>/<int:y>')
def toggle_pixel(x, y):
    referrer = request.headers.get('Referer')

    global toggle_count, last_toggle_time

    current_time = time.time()

    if current_time - last_toggle_time > 30:
        # Reset if more than 30 seconds have passed since the last toggle
        toggle_count = 0

    toggle_count += 1
    last_toggle_time = current_time

    if toggle_count == 2 or referrer == "https://www.desmos.com/" and x < size and y < size:
        # Toggle the pixel in the image
        pixel_color = image.getpixel((x, y))
        new_color = (0, 0, 0) if pixel_color == (255, 255, 255) else (255, 255, 255)
        image.putpixel((x, y), new_color)
        toggle_count = 0  # Reset the toggle count after successful toggle

        image.save(temp_filename)
        # Return blue 1x1 pixel
        return send_file("blue.png", mimetype='image/png', as_attachment=True, download_name='image.png')

    # Return red 1x1 pixel
    red_pixel = Image.new('RGB', (1, 1), 'red')
    return send_file("red.png", mimetype='image/png', as_attachment=True, download_name='red.png')

if __name__ == '__main__':
    app.run(debug=True)
