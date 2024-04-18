from customtkinter import *
from PIL import ImageTk, Image
from text_reg import Model
from CTkMessagebox import CTkMessagebox

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("TextReg with Tesseract")
        self.geometry("1600x900")
        self.resizable(width=False, height=False)
        
        # Create btn used to open image
        self.btn_open_img = CTkButton(self, text="Open image...", command=self.handle_open_img)
        self.btn_open_img.place(x=100, y=10)
        
        # Create btn used to start converting
        self.btn_convert_img = CTkButton(self, text="Convert Img to Text", command=self.handle_conversion)
        self.btn_convert_img.place(x=100, y=60)
        
        # Setup advanced settings
        self.btn_advanced_setting = CTkButton(self, text="Advanced settings...", command=self.handle_setting_window)
        self.btn_advanced_setting.place(x=100, y=110)
        
        # Create a TextBox showing the result
        self.result = CTkTextbox(self, width=500, height=550, fg_color="#e8e8e8", text_color="#000000")
        self.result.place(x=20, y=200)
        
        # Create a Label indicate the state of the process
        self.process_state = CTkLabel(self, text="Pending")
        self.process_state.place(x=20, y=160)
        
        self.image_frame = CTkLabel(self, image=None, height=IMG_SIZE[0], width=IMG_SIZE[1], fg_color="#494949")
        self.image_frame.place(x=550, y=50)
            
        self.img_path = ""
        
    def handle_open_img(self) -> None:
        self.img_path = filedialog.askopenfilename(title="Open")
        print(self.img_path)
        global IMG_SIZE
        with Image.open(self.img_path) as img:
            size_x = int(IMG_SIZE[1] * SCALE) if int(IMG_SIZE[1] * SCALE) < 1024 else 1024
            size_y = int(IMG_SIZE[0] * SCALE) if int(IMG_SIZE[0] * SCALE) < 720 else 720
            img = img.resize(size=(size_x, size_y))
            img = ImageTk.PhotoImage(img)
            self.image_frame.configure(image=img)

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
        
        self.kernel_x = CTkEntry(self, placeholder_text=str(KERNEL_SHAPE[0]), width=75)
        self.kernel_y = CTkEntry(self, placeholder_text=str(KERNEL_SHAPE[1]), width=75)
        self.kernel_x.place(x=130, y=30)
        self.kernel_y.place(x=210, y=30)
        self.lb_kernel = CTkLabel(self, text="Kernel size: ")
        self.lb_kernel.place(x=30, y=30)
        
        self.cb_reverse = CTkCheckBox(self, text="Reverse text after converting", variable=REVERSE, onvalue="True", offvalue="False")
        self.cb_reverse.place(x=30, y=70)
        
        self.lb_scale = CTkLabel(self, text="Scale: ")
        self.lb_scale.place(x=30, y=110)
        self.slider_scale = CTkSlider(self, from_=0.1, to=2.0, command=self.handle_slider_scale)
        self.slider_scale.place(x=130, y=115)
        self.lb_slider_scale = CTkLabel(self, text=str(SCALE)[0:4], width=40)
        self.lb_slider_scale.place(x=330, y=110)
        
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
                
    def handle_slider_scale(self, value):
        global SCALE
        SCALE = value
        self.lb_slider_scale.configure(text=str(SCALE)[0:4])
        print(SCALE)
        
   
if __name__ == "__main__":
    KERNEL_SHAPE: tuple = (20, 20)
    IMG_SIZE: tuple = (728, 1024)
    SCALE: float = 1.0
    app = App()
    REVERSE: StringVar = StringVar(app, value="False")
    app.mainloop()