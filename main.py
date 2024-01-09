
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, Frame
from tkinter import N, S, E, W, END
import os
from PIL import Image, ImageTk
import tkinter as tk
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By

pyt=os.getcwd()

def download_images(keyword, num_images):
    driver_path = "путь_к_драйверу"

    # Создать экземпляр драйвера
    driver = webdriver.Chrome(driver_path) 

    url = f"https://www.google.com/search?q={keyword}&tbm=isch"
    driver.get(url)

    num_scrolls = num_images // 400  
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    image_elements = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

    output_folder = f'{pyt}\image\{keyword}'
    os.makedirs(output_folder, exist_ok=True)

    for i, image_element in enumerate(image_elements[:num_images]):
        image_element.click()
        time.sleep(2)

        open_image_element = driver.find_element(By.CSS_SELECTOR, ".iPVvYb")
        image_url = open_image_element.get_attribute("src")

        response = requests.get(image_url)
        with open(os.path.join(output_folder, f"image_{i+1}.jpg"), "wb") as f:
            f.write(response.content)



    driver.quit()

def browse_folders():
    folder_path = fr"{pyt}\image"  
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    folder_listbox.delete(0, END)
    for folder in folders:
        folder_listbox.insert(END, folder)

def browse_images(event):
    selected_folder = folder_listbox.get(folder_listbox.curselection())  
    folder_path = os.path.join(fr"{pyt}\image", selected_folder)  
    file_listbox.delete(0, END)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                img = Image.open(file_path)
                file_listbox.insert(END, file_name)
            except (OSError, Image.UnidentifiedImageError):
                pass




def on_download_button_click():
    keyword = keyword_entry.get()
    num_images = int(num_images_entry.get())

    download_images(keyword, num_images)

    folder_path = fr"{pyt}\image"
    folder_listbox.delete(0, END)
    for folder in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, folder)):
            folder_listbox.insert(END, folder)

root = Tk()
root.title("Google Image Downloader")

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - 400
h = h // 2 - 300
root.geometry(f'900x600+{w}+{h}')


folder_frame = Frame(root)
folder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


folder_listbox = Listbox(folder_frame, width=30)
folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
folder_listbox.bind("<<ListboxSelect>>", browse_images)

folder_scrollbar = Scrollbar(folder_frame, orient="vertical")
folder_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
folder_listbox.config(yscrollcommand=folder_scrollbar.set)
folder_scrollbar.config(command=folder_listbox.yview)


file_frame = Frame(root)
file_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


file_listbox = Listbox(file_frame, width=30)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)




file_scrollbar = Scrollbar(file_frame, orient="vertical")
file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=file_scrollbar.set)
file_scrollbar.config(command=file_listbox.yview)


refresh_button = Button(root, text="Refresh", command=browse_folders)
refresh_button.pack(side=tk.BOTTOM)


keyword_label = Label(root, text="Keyword:")
keyword_label.pack()
keyword_entry = Entry(root)
keyword_entry.pack()


num_images_label = Label(root, text="Number of Images:")
num_images_label.pack()
num_images_entry = Entry(root)
num_images_entry.pack()


download_button = Button(root, text="Download", command=on_download_button_click)
download_button.pack()

browse_folders()

root.mainloop()
