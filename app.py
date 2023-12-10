from PIL import Image, ImageDraw
import sys
from flask import Flask, render_template
from moviepy.editor import *
import random
import os

if not os.path.exists('static'):
    os.makedirs('static')
    
arr = [ f"static/frame{i}.png" for i in range (100)]

for i in range(100):
    img = Image.new('RGB', (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    center = (random.randint(200, 600), random.randint(200, 500))
    radius = random.randint(1, 100)
    fill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline="black", width=2, fill = fill)
    img.save(f"static/frame{i}.png")

clip = ImageSequenceClip(arr, fps = 5)

clip.write_videofile("static/video.mp4")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
