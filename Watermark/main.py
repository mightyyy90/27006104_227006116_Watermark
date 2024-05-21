import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

# Inisialisasi global variabel
main_image = None
watermark_image = None
test_image = None

# Fungsi untuk memilih gambar utama
def select_main_image():
    global main_image, main_image_path
    main_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if main_image_path:
        main_image = Image.open(main_image_path)
        main_image_thumbnail = main_image.copy()
        main_image_thumbnail.thumbnail((200, 200))
        main_image_thumbnail = ImageTk.PhotoImage(main_image_thumbnail)
        main_image_label.config(image=main_image_thumbnail)
        main_image_label.image = main_image_thumbnail

# Fungsi untuk memilih gambar watermark
def select_watermark_image():
    global watermark_image, watermark_image_path
    watermark_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if watermark_image_path:
        watermark_image = Image.open(watermark_image_path).convert("1")  # Convert to 1-bit image
        watermark_image_thumbnail = watermark_image.copy()
        watermark_image_thumbnail.thumbnail((200, 200))
        watermark_image_thumbnail = ImageTk.PhotoImage(watermark_image_thumbnail)
        watermark_image_label.config(image=watermark_image_thumbnail)
        watermark_image_label.image = watermark_image_thumbnail

# Fungsi untuk menyisipkan watermark menggunakan metode LSB
def embed_watermark():
    if main_image and watermark_image:
        main_image_array = np.array(main_image.convert("RGB"))
        watermark_image_array = np.array(watermark_image)

        watermark_height, watermark_width = watermark_image_array.shape
        main_height, main_width, _ = main_image_array.shape

        if main_height < watermark_height or main_width < watermark_width:
            messagebox.showerror("Error", "Watermark size should be smaller than main image")
            return

        for i in range(watermark_height):
            for j in range(watermark_width):
                for k in range(3):  # Iterate over R, G, B channels
                    main_image_array[i, j, k] = (main_image_array[i, j, k] & 0xFE) | (watermark_image_array[i, j] & 0x01)

        watermarked_image = Image.fromarray(main_image_array)
        watermarked_image.save("watermarked_image.png")
        messagebox.showinfo("Success", "Watermark embedded and saved as watermarked_image.png")
    else:
        messagebox.showerror("Error", "Please select both main image and watermark image")

# Fungsi untuk memilih gambar yang ingin diperiksa
def select_image():
    global test_image, test_image_path
    test_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if test_image_path:
        test_image = Image.open(test_image_path)
        test_image_thumbnail = test_image.copy()
        test_image_thumbnail.thumbnail((200, 200))
        test_image_thumbnail = ImageTk.PhotoImage(test_image_thumbnail)
        test_image_label.config(image=test_image_thumbnail)
        test_image_label.image = test_image_thumbnail

# Fungsi untuk mendeteksi watermark menggunakan metode LSB
def detect_watermark():
    if test_image:
        test_image_array = np.array(test_image.convert("RGB"))
        watermark_size = (100, 100)  # Assuming watermark size is known

        if test_image_array.shape[0] < watermark_size[0] or test_image_array.shape[1] < watermark_size[1]:
            messagebox.showerror("Error", "The image is smaller than the expected watermark size")
            return

        watermark_area = test_image_array[0:watermark_size[0], 0:watermark_size[1]]

        extracted_watermark = np.zeros((watermark_size[0], watermark_size[1]), dtype=np.uint8)
        for i in range(watermark_size[0]):
            for j in range(watermark_size[1]):
                extracted_watermark[i, j] = watermark_area[i, j, 0] & 1

        extracted_watermark_image = Image.fromarray((extracted_watermark * 255).astype(np.uint8), 'L')

        extracted_watermark_display = ImageTk.PhotoImage(extracted_watermark_image)
        extracted_watermark_label.config(image=extracted_watermark_display)
        extracted_watermark_label.image = extracted_watermark_display
        result_label.config(text="Watermark detected and displayed below")
    else:
        messagebox.showerror("Error", "Please select an image to check for watermark")

# Inisialisasi antarmuka Tkinter
root = tk.Tk()
root.title("Steganografi Watermark")
root.configure(bg="white")

# Frame untuk embed watermark
frame_embed = tk.Frame(root, padx=100, pady=20, bg="white")
frame_embed.grid(row=0, column=0, padx=10, pady=10, sticky="n")

embed_title_label = tk.Label(frame_embed, text="Embed Watermark", font=("Arial", 36), bg="white")
embed_title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

main_image_label = tk.Label(frame_embed, bg="white")
main_image_label.grid(row=1, column=0, padx=10, pady=10)
select_main_image_button = tk.Button(frame_embed, text="Select Main Image", command=select_main_image, width=20)
select_main_image_button.grid(row=2, column=0, padx=10, pady=10)

watermark_image_label = tk.Label(frame_embed, bg="white")
watermark_image_label.grid(row=1, column=1, padx=10, pady=10)
select_watermark_image_button = tk.Button(frame_embed, text="Select Watermark Image", command=select_watermark_image, width=20)
select_watermark_image_button.grid(row=2, column=1, padx=10, pady=10)

embed_watermark_button = tk.Button(frame_embed, text="Embed Watermark", command=embed_watermark, width=20)
embed_watermark_button.grid(row=3, column=0, columnspan=2, pady=20)

# Frame untuk detect watermark
frame_detect = tk.Frame(root, padx=100, pady=20, bg="white")
frame_detect.grid(row=0, column=1, padx=10, pady=10, sticky="n")

detect_title_label = tk.Label(frame_detect, text="Detect Watermark", font=("Arial", 36), bg="white")
detect_title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

test_image_label = tk.Label(frame_detect, bg="white")
test_image_label.grid(row=1, column=0, padx=10, pady=10)
select_image_button = tk.Button(frame_detect, text="Select Image to Check", command=select_image, width=20)
select_image_button.grid(row=2, column=0, padx=10, pady=10)

detect_watermark_button = tk.Button(frame_detect, text="Detect Watermark", command=detect_watermark, width=20)
detect_watermark_button.grid(row=2, column=1, padx=10, pady=10)

result_label = tk.Label(frame_detect, text="", bg="white")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

extracted_watermark_label = tk.Label(frame_detect, bg="white")
extracted_watermark_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Jalankan aplikasi Tkinter
root.mainloop()
