from PIL import ImageTk, Image
from customtkinter import (CTk, CTkLabel, CTkToplevel)

class ImagePreview(CTkToplevel):
    def __init__(self, master, img: ImageTk.PhotoImage):
        super().__init__(self, master, img)
        self.title("Image Preview")
        self.geometry(f"{img.width}x{img.height}")
        self.resizable(width=False, height=False)
        
        self.image_preview = CTkLabel(self, image=img, width=img.width, height=img.height)
        self.image_preview.place(x=0, y=0)