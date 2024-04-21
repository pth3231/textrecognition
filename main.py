from customtkinter import (CTkFrame, CTk, CTkLabel, CTkTextbox, 
                           CTkCheckBox, CTkButton, CTkToplevel, CTkProgressBar,
                           CTkEntry, CTkSlider, filedialog, END, StringVar)
from PIL import ImageTk, Image
from text_reg import Model
from CTkMessagebox import CTkMessagebox
import subprocess
import webbrowser

class Docs(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btn_github = CTkButton(self, text="Our repo", width=70, command=self.handle_open_repo)
        self.btn_github.place(x=5, y=5)
        self.btn_github = CTkButton(self, text="Bugs", width=50, command=self.handle_bug_report)
        self.btn_github.place(x=80, y=5)
        
    def handle_open_repo(self):
        webbrowser.open("https://github.com/pth3231/textrecognition")
        
    def handle_bug_report(self):
        webbrowser.open("https://github.com/pth3231/textrecognition/issues")

class AdvancedSetting(CTkToplevel):
    def __init__(self, master, FONT_SIZE: int, REVERSE: bool, KERNEL_SHAPE: tuple, SCALE: float):
        super().__init__(master)
        self.geometry('400x400')
        self.title('Textifier')
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
        
        self.lb_font_size = CTkLabel(self, text="Font size:")
        self.lb_font_size.place(x=30, y=150)
        self.font_size = CTkEntry(self, placeholder_text=str(FONT_SIZE), width=75)
        self.font_size.place(x=110, y=150)
        
        self.btn_apply = CTkButton(self, text="Apply", command=self.handle_apply, width=80)
        self.btn_apply.place(x=110, y=360)
        self.btn_ok = CTkButton(self, text="OK", command=self.handle_ok, width=80)
        self.btn_ok.place(x=210, y=360)

    def handle_apply(self) -> None:
        try:
            global KERNEL_SHAPE, FONT_SIZE
            new_kernel_shape = [0, 0]
            new_kernel_shape[0] = int(self.kernel_x.get()) if self.kernel_x.get() != "" else KERNEL_SHAPE[0]
            new_kernel_shape[1] = int(self.kernel_y.get()) if self.kernel_y.get() != "" else KERNEL_SHAPE[1]
            KERNEL_SHAPE = tuple(new_kernel_shape)
            FONT_SIZE = int(self.font_size.get()) if len(self.font_size.get()) != 0 else FONT_SIZE
            print(KERNEL_SHAPE)
            print(FONT_SIZE)
        except:
            print("Wrong format exception")
            CTkMessagebox(self, title="Setting Error", message="Wrong format!")
    
    def handle_ok(self) -> None:
        try:
            global KERNEL_SHAPE, FONT_SIZE
            new_kernel_shape = [0, 0]
            new_kernel_shape[0] = int(self.kernel_x.get()) if self.kernel_x.get() != "" else KERNEL_SHAPE[0]
            new_kernel_shape[1] = int(self.kernel_y.get()) if self.kernel_y.get() != "" else KERNEL_SHAPE[1]
            KERNEL_SHAPE = tuple(new_kernel_shape)
            FONT_SIZE = int(self.font_size.get()) if self.font_size.get() != "" else FONT_SIZE
            print(KERNEL_SHAPE)
            print(FONT_SIZE)
            self.destroy()
        except:
            print("Wrong format exception")
            CTkMessagebox(self, title="Setting Error", message="Wrong format!")
                
    def handle_slider_scale(self, value):
        global SCALE
        SCALE = value
        self.lb_slider_scale.configure(text=str(SCALE)[0:4])
        print(SCALE)

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Textifier')
        self.geometry('1600x824')
        self.resizable(width=False, height=False)
        
        # Create btn used to open image
        self.btn_open_img = CTkButton(self, text="Open", command=self.handle_open_img, width=80)
        self.btn_open_img.place(x=30, y=150)
        
        # Create btn used to start converting
        self.btn_convert_img = CTkButton(self, text="Convert", command=self.handle_conversion, width=80)
        self.btn_convert_img.place(x=130, y=150)
        
        # Setup advanced settings
        self.btn_advanced_setting = CTkButton(self, text="Settings...", command=self.handle_setting_window, width=100)
        self.btn_advanced_setting.place(x=230, y=150)
        
        # Create a TextBox showing the result
        self.result = CTkTextbox(self, width=500, height=560, fg_color="#484848", text_color="#ffffff", font=("Open Sans", FONT_SIZE))
        self.result.place(x=20, y=200)
        
        # Create a Label indicate the state of the process
        self.process_state = CTkLabel(self, text="Pending", justify="right")
        self.process_state.place(x=410, y=775)
        
        # Create a Label in order to show the image
        self.image_frame = CTkLabel(self, image=None, text="Image Preview will be displayed here...", height=IMG_SIZE[0], width=IMG_SIZE[1], fg_color="#494949", font=("Consolas", 16))
        self.image_frame.place(x=550, y=30)
        
        # Title
        self.main_title = CTkLabel(self, text="Textifier", font=("Open Sans", 28), height=50)
        self.main_title.place(x=210, y=50)
        
        # Progress Bar
        self.prog_bar = CTkProgressBar(self, orientation="horizontal", mode="determinate", width=100, height=20)
        self.prog_bar.place(x=550, y=780)
        self.lb_prog_bar = CTkLabel(self, text="0")
        self.lb_prog_bar.place(x=670, y=777.5)
        self.prog_bar.set(0)
        
        # Documentation, Bug report and Updates
        self.docs_frame = Docs(self, width=135, height=40)
        self.docs_frame.place(x=1440, y=770)
        
        self.img_path = ""
        self.window = None
        
    def handle_open_img(self) -> None:
        self.img_path = filedialog.askopenfilename(title="Open...")
        print(self.img_path)
        global IMG_SIZE
        with Image.open(self.img_path, "r") as img:
            size_x = int(IMG_SIZE[1] * SCALE) if int(IMG_SIZE[1] * SCALE) < 1024 else 1024
            size_y = int(IMG_SIZE[0] * SCALE) if int(IMG_SIZE[0] * SCALE) < 728 else 728
            print(f"Size of the result: {(size_x, size_y)}")
            img = ImageTk.PhotoImage(
                img.resize(
                        size=(size_x, size_y)
                    )
                )
            self.image_frame.configure(image=img, text="")

    def handle_conversion(self) -> None:
        # Create OCR Model
        print(f"All stats:\n{KERNEL_SHAPE}\n{REVERSE.get()}")
        
        if self.img_path != "":
            self.result.delete("1.0", END)
            with open("./test/recognized.txt") as file:
                model = Model(img_path=self.img_path, 
                              kernel_shape=KERNEL_SHAPE)
                model.predict()
                content = file.readlines()
                if (REVERSE.get() == "True"):
                    content.reverse()
                i = 1
                self.prog_bar.set(0)
                self.prog_bar.start()
                for line in content:
                    self.prog_bar.set(i / len(content))
                    self.result.insert(END, line) 
                    self.update_idletasks()
                    self.lb_prog_bar.configure(text=str(i / len(content) * 100)[0:3])
                    i += 1
                self.prog_bar.stop()
                self.process_state.configure(text="Successful")
        else:
            self.process_state.configure(text="No imported image")

    def handle_setting_window(self) -> None:
        self.window = AdvancedSetting(self, FONT_SIZE, REVERSE, KERNEL_SHAPE, SCALE)
        self.window.grab_set()

if __name__ == "__main__":
    KERNEL_SHAPE: tuple = (20, 20)
    IMG_SIZE: tuple = (728, 1024)
    SCALE: float = 1.0
    FONT_SIZE: int = 14
    app = App()
    REVERSE: StringVar = StringVar(app, value="False")
    app.mainloop()