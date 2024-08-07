import customtkinter as ctk
from PIL import Image  # Make sure to import Image from PIL
from Automation import AutomationRpa,AutomationRpaAlphaProject,AutomationRpaAlphaProject1,AutomationRpa1
import os
import tkinter as tk
from UpdatePhotos import UpdatePhotosAlphaProject,UpdatePhotosProjetoTerra,UpdatePhotosProjetoTerra1,UpdatePhotosAlphaProject1

# ---------------------------------------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self, title, size):
        # Main Setup --------------------------------------------------
        super().__init__()
        self.title(title)
        ctk.set_default_color_theme("green") 
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Initial frame
        self.current_frame = None
        self.show_frame(Rpa1)

        # Run ---------------------------------------------------------
        self.mainloop()

    def show_frame(self, frame_class):
        """Method to switch frames"""
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# ---------------------------------------------------------------------------------------------------
class Rpa1(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent)
        self.menu = Menu(self, parent.show_frame)
        self.main = Main1(self)

# ---------------------------------------------------------------------------------------------------
class Rpa2(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent)
        self.menu = Menu(self, parent.show_frame)
        self.main = Main2(self)

# ---------------------------------------------------------------------------------------------------
class Rpa3(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent)
        self.menu = Menu(self, parent.show_frame)
        self.main = Main3(self)

# ---------------------------------------------------------------------------------------------------
class Menu(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.show_frame_callback = show_frame_callback
        self.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        self.create_widget()

    def create_widget(self):
        # Widgets -----------------------------------------------------
        image_path = "icon.png"
        absolute_image_path = os.path.abspath(image_path)
        print(f"Loading image from: {absolute_image_path}")

        try:
            self.label_Icon_image = ctk.CTkImage(Image.open(image_path), size=(150, 80))
        except Exception as e:
            print(f"Error loading image: {e}")
            self.label_Icon_image = None

        if self.label_Icon_image:
            _Icon = ctk.CTkLabel(master=self, image=self.label_Icon_image, text="")
        else:
            _Icon = ctk.CTkLabel(master=self, text="Image not found")

        btn1SideFrame = ctk.CTkButton(self, text='Projeto Terra', command=lambda: self.show_frame_callback(Rpa1), fg_color='#8db600', corner_radius=10, font=('Helvetica', 14, 'bold'))
        btn2SideFrame = ctk.CTkButton(self, text='Projeto Alpha', command=lambda: self.show_frame_callback(Rpa2), fg_color='#8db600', corner_radius=10, font=('Helvetica', 14, 'bold'))
        btn3SideFrame = ctk.CTkButton(self, text='RPA 3 Automation', command=lambda: self.show_frame_callback(Rpa3), fg_color='#8db600', corner_radius=10, font=('Helvetica', 14, 'bold'))
        label2SideFrame = ctk.CTkLabel(self, text='Created By: BI Team', fg_color='gray', text_color='white', font=('Helvetica', 12, 'bold'), corner_radius=10)

        # Layout ------------------------------------------------------
        _Icon.place(relx=0.1, rely=0.02, relwidth=0.8, relheight=0.2)
        btn1SideFrame.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        btn2SideFrame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.12)
        btn3SideFrame.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.12)
        label2SideFrame.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.1)


# ---------------------------------------------------------------------------------------------------
class Main1(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        self.submain1 = SubMain1(self)
        self.submain2 = SubMain2(self)

# ---------------------------------------------------------------------------------------------------
class Main2(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        self.submain1 = SubMainAlpha1(self)
        self.submain2 = SubMainAlpha2(self)

# ---------------------------------------------------------------------------------------------------
class Main3(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        # self.submain1 = SubMain1(self)
        # self.submain2 = SubMain2(self)

# ---------------------------------------------------------------------------------------------------
class SubMain1(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0, rely=0, relwidth=1, relheight=0.4)
        self.create_widget(parent)

    def create_widget(self, parent):
        # Widgets -----------------------------------------------------
        lbl1 = ctk.CTkLabel(self, text='Projeto Terra', text_color='#55682f', font=('Helvetica', 18, 'bold'))
        lbl2 = ctk.CTkLabel(self, text='Download Path:',  text_color='gray', font=('Helvetica', 14,'bold'))
        lbl4 = ctk.CTkLabel(self, text='ChromeDriver:',  text_color='gray', font=('Helvetica', 14,'bold'))
        driverEntry =ctk.CTkEntry(self)
        #if self.ExistPath() ==  True:
            #arrayInputs = VerifyPaths()
           # self.entry_var1 = tk.StringVar(value=arrayInputs[0])
           # etr1 = ctk.CTkEntry(self,textvariable=self.entry_var1)
            #self.entry_var2 = tk.StringVar(value=arrayInputs[1])
           #etr2 = ctk.CTkEntry(self,textvariable=self.entry_var2)
        #else:
        etr1 = ctk.CTkEntry(self)
        etr2 = ctk.CTkEntry(self)
            #etr3 = ctk.CTkEntry(self)
            
        
        
        lbl3 = ctk.CTkLabel(self, text='Output Path:',  text_color='gray', font=('Helvetica', 14,'bold'))
        btn1 = ctk.CTkButton(self, text='Start Automation', command=lambda: AutomationRpa1(self,parent.submain2, etr1.get(), etr2.get(),driverEntry.get()), fg_color='#8db600', corner_radius=10,font=('Helvetica', 12, 'bold'))
        btn2 = ctk.CTkButton(self, text='Update Photos', command=lambda: UpdatePhotosProjetoTerra1(self,parent.submain2, etr1.get(), etr2.get(),driverEntry.get()), fg_color='#8db600', corner_radius=10,font=('Helvetica', 12, 'bold'))
        # Layout ------------------------------------------------------
        lbl1.place(relx=0.16, rely=0.05, relwidth=0.7, relheight=0.1)
        lbl2.place(relx=0.02, rely=0.2, relwidth=0.3, relheight=0.1)
        etr1.place(relx=0.31, rely=0.2, relwidth=0.45, relheight=0.1)
        etr2.place(relx=0.31, rely=0.35, relwidth=0.45, relheight=0.1)
        driverEntry.place(relx=0.31, rely=0.50, relwidth=0.45, relheight=0.1)
        #etr3.place(relx=0.31, rely=0.45, relwidth=0.45, relheight=0.1)
        lbl3.place(relx=0.08, rely=0.35, relwidth=0.22, relheight=0.1)
        lbl4.place(relx=0.03, rely=0.50, relwidth=0.30, relheight=0.1)
        btn1.place(relx=0.37, rely=0.65, relwidth=0.3, relheight=0.12)
        btn2.place(relx=0.37, rely=0.80, relwidth=0.3, relheight=0.12)
  

# ---------------------------------------------------------------------------------------------------
inpt = (
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------"
)

class SubMain2(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)
        self.create_widget()

    def create_widget(self):
        # Widgets -----------------------------------------------------
        lbl1 = ctk.CTkLabel(self, text='Status Bar', text_color='#55682f', font=('Helvetica', 18, 'bold'))
        self.text_widget = ctk.CTkTextbox(self, height=200, width=300, fg_color='#474a51', text_color='#00FF00', font=('Helvetica', 12), corner_radius=10)

        # Layout ------------------------------------------------------
        lbl1.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)
        self.text_widget.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
        self.text_widget.insert("end", "----------------------------Status Bar------------------------------\n")

    def insert_text(self, text):
        self.text_widget.insert("end", text + "\n")

# ---------------------------------------------------------------------------------------------------

class SubMainAlpha1(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0, rely=0, relwidth=1, relheight=0.4)
        self.create_widget(parent)

    def create_widget(self, parent):
        # Widgets -----------------------------------------------------
        lbl1 = ctk.CTkLabel(self, text='Projeto Alpha', text_color='#55682f', font=('Helvetica', 18, 'bold'))
        lbl2 = ctk.CTkLabel(self, text='Download Path:',  text_color='gray', font=('Helvetica', 14,'bold'))
        lbl4 = ctk.CTkLabel(self, text='ChromeDriver:',  text_color='gray', font=('Helvetica', 14,'bold'))
        driverEntry =ctk.CTkEntry(self)
        #if self.ExistPath() ==  True:
            #arrayInputs = VerifyPaths()
           # self.entry_var1 = tk.StringVar(value=arrayInputs[0])
           # etr1 = ctk.CTkEntry(self,textvariable=self.entry_var1)
            #self.entry_var2 = tk.StringVar(value=arrayInputs[1])
           #etr2 = ctk.CTkEntry(self,textvariable=self.entry_var2)
        #else:
        etr1 = ctk.CTkEntry(self)
        etr2 = ctk.CTkEntry(self)
            #etr3 = ctk.CTkEntry(self)
            
        
        
        lbl3 = ctk.CTkLabel(self, text='Output Path:',  text_color='gray', font=('Helvetica', 14,'bold'))
        btn1 = ctk.CTkButton(self, text='Start Automation', command=lambda: AutomationRpaAlphaProject1( etr1.get(), etr2.get(),driverEntry.get()), fg_color='#8db600', corner_radius=10,font=('Helvetica', 12, 'bold'))
        btn2 = ctk.CTkButton(self, text='Update Photos', command=lambda: UpdatePhotosAlphaProject1(self,parent.submain2, etr1.get(), etr2.get(),driverEntry.get()), fg_color='#8db600', corner_radius=10,font=('Helvetica', 12, 'bold'))
        # Layout ------------------------------------------------------
        lbl1.place(relx=0.16, rely=0.05, relwidth=0.7, relheight=0.1)
        lbl2.place(relx=0.02, rely=0.2, relwidth=0.3, relheight=0.1)
        etr1.place(relx=0.31, rely=0.2, relwidth=0.45, relheight=0.1)
        etr2.place(relx=0.31, rely=0.35, relwidth=0.45, relheight=0.1)
        driverEntry.place(relx=0.31, rely=0.50, relwidth=0.45, relheight=0.1)
        #etr3.place(relx=0.31, rely=0.45, relwidth=0.45, relheight=0.1)
        lbl3.place(relx=0.08, rely=0.35, relwidth=0.22, relheight=0.1)
        lbl4.place(relx=0.03, rely=0.50, relwidth=0.30, relheight=0.1)
        btn1.place(relx=0.37, rely=0.65, relwidth=0.3, relheight=0.12)
        btn2.place(relx=0.37, rely=0.80, relwidth=0.3, relheight=0.12)
  

# ---------------------------------------------------------------------------------------------------
inpt = (
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------\n"
    "---------------------------------------------------------------------------"
)

class SubMainAlpha2(ctk.CTkFrame):
    def __init__(self, parent):
        # Main Setup --------------------------------------------------
        super().__init__(parent, fg_color='#f0f0f0', border_color='gray', border_width=2)
        self.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)
        self.create_widget()

    def create_widget(self):
        # Widgets -----------------------------------------------------
        lbl1 = ctk.CTkLabel(self, text='Status Bar', text_color='#55682f', font=('Helvetica', 18, 'bold'))
        self.text_widget = ctk.CTkTextbox(self, height=200, width=300, fg_color='#474a51', text_color='#00FF00', font=('Helvetica', 12), corner_radius=10)

        # Layout ------------------------------------------------------
        lbl1.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)
        self.text_widget.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
        self.text_widget.insert("end", "----------------------------Status Bar------------------------------\n")

    def insert_text(self, text):
        self.text_widget.insert("end", text + "\n")

# ---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("Starting application")
    App('Class Based App', (600, 600))
