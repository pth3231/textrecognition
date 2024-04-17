from customtkinter import *
from PIL import ImageTk, Image
from text_reg import Model
from CTkMessagebox import CTkMessagebox

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("TextReg with Tesseract")
        self.geometry("1024x576")
        self.resizable(width=False, height=False)
        
        # Setting up image_frame size
        self.img_size = (540, 420)
        
        # Create btn used to open image
        self.btn_open_img = CTkButton(self, text="Open image...", command=self.handle_open_img)
        self.btn_open_img.place(x=40, y=10)
        
        # Create btn used to start converting
        self.btn_convert_img = CTkButton(self, text="Convert Img to Text", command=self.handle_conversion)
        self.btn_convert_img.place(x=40, y=60)
        
        # Create a TextBox showing the result
        self.result = CTkTextbox(self, width=400, height=350, fg_color="#e8e8e8", text_color="#000000")
        self.result.place(x=20, y=200)
        
        # Create a Label indicate the state of the process
        self.process_state = CTkLabel(self, text="Pending")
        self.process_state.place(x=20, y=160)
        
        # Setup advanced settings
        self.btn_advanced_setting = CTkButton(self, text="Advanced settings...", command=self.handle_setting_window)
        self.btn_advanced_setting.place(x=40, y=110)
                
        self.img_path = ""
        
    def handle_open_img(self) -> None:
        self.img_path = filedialog.askopenfilename(title="Open")
        print(self.img_path)
        with Image.open(self.img_path) as img:
            img = img.resize(self.img_size)
            img = ImageTk.PhotoImage(img)
            self.image_frame = CTkLabel(self, image=img, height=self.img_size[0], width=self.img_size[1])
            self.image_frame.place(x=450)

    def handle_conversion(self) -> None:
        # Create OCR Model
        print(f"All stats:\n{KERNEL_SHAPE}\n{REVERSE.get()}")
        
        if self.img_path != "":
            self.result.delete("1.0", END)
            with open("./test/recognized.txt", errors='ignore') as file:
                self.model = Model(img_path=self.img_path, 
                                   kernel_shape=KERNEL_SHAPE)
                self.model.predict()
                content = file.readlines()
                if (REVERSE.get() == "True"):
                    content.reverse()
                for line in content:
                    self.result.insert(END, line)
                self.process_state.configure(text="Successful")
        else:
            self.process_state.configure(text="No imported image")

    def handle_setting_window(self) -> None:
        window = AdvancedSetting(self)
        window.grab_set()

class AdvancedSetting(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('400x400')
        self.title('Advanced Setting')
        self.resizable(width=False, height=False)
        
        self.kernel_x = CTkEntry(self, placeholder_text=str(KERNEL_SHAPE[0]), width=50)
        self.kernel_y = CTkEntry(self, placeholder_text=str(KERNEL_SHAPE[1]), width=50)
        self.kernel_x.place(x=130, y=30)
        self.kernel_y.place(x=190, y=30)
        self.lb_kernel = CTkLabel(self, text="Kernel size: ")
        self.lb_kernel.place(x=30, y=30)
        
        self.cb_reverse = CTkCheckBox(self, text="Reverse text after converting", variable=REVERSE, onvalue="True", offvalue="False")
        self.cb_reverse.place(x=30, y=70)
        
        self.btn_apply = CTkButton(self, text="Apply", command=self.handle_apply, width=80)
        self.btn_apply.place(x=110, y=360)
        self.btn_ok = CTkButton(self, text="OK", command=self.handle_ok, width=80)
        self.btn_ok.place(x=210, y=360)
        
    def handle_apply(self) -> None:
        if (self.kernel_x.get() != "" and self.kernel_y.get() != ""):
            try: 
                global KERNEL_SHAPE
                KERNEL_SHAPE = (int(self.kernel_x.get()), int(self.kernel_y.get()))
            except:
                print("KERNEL_SHAPE wrong format exception")
                CTkMessagebox(self, title="Setting Error", message="KERNEL_SHAPE wrong format!")
    
    def handle_ok(self) -> None:
        if (self.kernel_x.get() == "" or self.kernel_y.get() == ""):
            self.destroy()
        else:
            try:
                global KERNEL_SHAPE
                KERNEL_SHAPE = (int(self.kernel_x.get()), int(self.kernel_y.get()))
                self.destroy()
            except:
                print("KERNEL_SHAPE wrong format exception")
                CTkMessagebox(self, title="Setting Error", message="KERNEL_SHAPE wrong format!")
   
if __name__ == "__main__":
    app = App()
    REVERSE: StringVar = StringVar(app, value="False")
    KERNEL_SHAPE: tuple = (20, 20)
    app.mainloop()