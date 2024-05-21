import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

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
                    main_image_array[i, j, k] = (main_image_array[i, j, k] & ~1) | watermark_image_array[i, j]
        
        global watermarked_image
        watermarked_image = Image.fromarray(main_image_array)
        watermarked_image_thumbnail = watermarked_image.copy()
        watermarked_image_thumbnail.thumbnail((200, 200))
        watermarked_image_thumbnail = ImageTk.PhotoImage(watermarked_image_thumbnail)
        watermarked_image_label.config(image=watermarked_image_thumbnail)
        watermarked_image_label.image = watermarked_image_thumbnail
    else:
        messagebox.showerror("Error", "Please select both main image and watermark image")

# Fungsi untuk mendownload gambar hasil
def download_image():
    if watermarked_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if save_path:
            watermarked_image.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully")
    else:
        messagebox.showerror("Error", "No watermarked image to save")

# Inisialisasi antarmuka Tkinter
root = tk.Tk()
root.title("Image Watermarking with LSB")

# Label dan tombol untuk memilih gambar utama
main_image_label = tk.Label(root)
main_image_label.pack()
select_main_image_button = tk.Button(root, text="Select Main Image", command=select_main_image)
select_main_image_button.pack()

# Label dan tombol untuk memilih gambar watermark
watermark_image_label = tk.Label(root)
watermark_image_label.pack()
select_watermark_image_button = tk.Button(root, text="Select Watermark Image", command=select_watermark_image)
select_watermark_image_button.pack()

# Tombol untuk menyisipkan watermark
embed_watermark_button = tk.Button(root, text="Embed Watermark", command=embed_watermark)
embed_watermark_button.pack()

# Label untuk menampilkan gambar yang telah disisipi watermark
watermarked_image_label = tk.Label(root)
watermarked_image_label.pack()

# Tombol untuk mendownload hasil gambar
download_button = tk.Button(root, text="Download Watermarked Image", command=download_image)
download_button.pack()

# Jalankan aplikasi Tkinter
root.mainloop()
