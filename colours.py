import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.colors as mcolors

# Convert hex color strings to RGB tuples
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Convert CSS4 color dict to RGB values
colors = {name: hex_to_rgb(hex_code) for name, hex_code in mcolors.CSS4_COLORS.items()}

def get_nearest_color_name(rgb):
    min_dist = float('inf')
    nearest_color = "Unknown"
    for color_name, color_rgb in colors.items():
        dist = np.linalg.norm(np.array(rgb) - np.array(color_rgb))
        if dist < min_dist:
            min_dist = dist
            nearest_color = color_name
    return nearest_color

def open_image():
    global img_original, img_display, photo, img_width, img_height
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    img_original = cv2.imread(file_path)
    img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)

    max_width, max_height = 800, 600
    h, w, _ = img_original.shape
    scale = min(max_width / w, max_height / h, 1)

    img_width = int(w * scale)
    img_height = int(h * scale)

    img_display = cv2.resize(img_original, (img_width, img_height), interpolation=cv2.INTER_AREA)

    img_pil = Image.fromarray(img_display)
    photo = ImageTk.PhotoImage(img_pil)

    canvas.config(width=img_width, height=img_height)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    color_label.config(text="Image loaded. Click on image to get color name.")

def get_pixel_color(event):
    global img_original, img_width, img_height

    if img_original is None:
        return

    x_display, y_display = event.x, event.y
    h_orig, w_orig, _ = img_original.shape

    scale_x = img_width / w_orig
    scale_y = img_height / h_orig

    x_orig = int(x_display / scale_x)
    y_orig = int(y_display / scale_y)

    if x_orig >= w_orig or y_orig >= h_orig or x_orig < 0 or y_orig < 0:
        return

    pixel_color = img_original[y_orig, x_orig]
    color_name = get_nearest_color_name(pixel_color)

    color_label.config(text=f"RGB: {pixel_color[0]}, {pixel_color[1]}, {pixel_color[2]}    Name: {color_name}")

# Tkinter setup
root = Tk()
root.title("Color Identifier")

img_original = None
photo = None
img_display = None
img_width, img_height = 0, 0

btn = Button(root, text="Open Image", command=open_image)
btn.pack(pady=10)

canvas = Canvas(root)
canvas.pack()

color_label = Label(root, text="Load an image and click on it to see color", font=("Arial", 14), bg="white", fg="black")
color_label.pack(pady=10)

canvas.bind("<Button-1>", get_pixel_color)

root.mainloop()
