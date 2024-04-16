from customtkinter import *
from PIL import ImageTk, Image
from text_reg import Model
from CTkMessagebox import ctkmessagebox
import codecs

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title = "TextReg with Tesseract"
        self.geometry("1024x576")
        self.resizable(width=False, height=False)
        
        # Setting up image_frame size
        self.img_size = (540, 304)
        
        # Create btn used to open image
        self.btn_open_img = CTkButton(self, text="Open image...", command=self.handle_open_img)
        self.btn_open_img.place(x=40, y=10)
        
        # Create btn used to start converting
        self.btn_convert_img = CTkButton(self, text="Convert img to text", command=self.handle_conversion)
        self.btn_convert_img.place(x=40, y=60)
        
        # Create a TextBox showing the result
        self.result = CTkTextbox(self, width=350, height=200, fg_color="#e8e8e8", text_color="#000000")
        self.result.place(x=20, y=300)
        
        self.img_path = ""
        
        
    def handle_open_img(self) -> None:
        self.img_path = filedialog.askopenfilename(title="Open")
        print(self.img_path)
        img = Image.open(self.img_path).resize(self.img_size)
        img = ImageTk.PhotoImage(img)
        self.image_frame = CTkLabel(self, image=img, height=self.img_size[0], width=self.img_size[1])
        self.image_frame.place(x=450)

    def handle_conversion(self) -> None:
        # Create OCR Model
        if self.img_path != "":
            self.result.delete("1.0", END)
            with open("./test/recognized.txt", errors='ignore') as file:
                self.model = Model(self.img_path)
                self.model.predict()
                content = file.readlines()
                content.reverse()
                for line in content:
                    self.result.insert(END, line)
                self.img_path = ""
        else:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()