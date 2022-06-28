import sys
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import ttk
import sv_ttk
import darkdetect
import tkinter.font as TkFont
from tkinter.filedialog import askdirectory
from tkinter import filedialog




class App(ttk.Frame, ttk.Label):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_00 = tk.BooleanVar(value=True)
        self.var_0 = tk.BooleanVar(value=True)
        self.var_0 = tk.BooleanVar(value=True)
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        
        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)
        
        # Entry
        self.entry = ttk.Entry(self.widgets_frame)
        self.entry.insert(0, "Select .txt file")
        self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
        
        # Entry
        self.entry_1 = ttk.Entry(self.widgets_frame)
        self.entry_1.insert(0, "Select Output Directory")
        self.entry_1.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        
        # Button Function
        def Funcbutton():
            path = filedialog.askopenfilename(title = "Select .txt file", filetypes=[("Text files", "*.txt")])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path)
            self.buttonPath = path
            print(self.buttonPath)
        
        # Button
        self.button = ttk.Button(self.widgets_frame, text="Input", command = Funcbutton)
        self.button.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")
        
        # Button_1 Function
        def Funcbutton_1():
            path = askdirectory(title='Select Output Directory')
            self.entry_1.delete(0, tk.END)
            self.entry_1.insert(0, path)
            self.buttonPath_1 = path
            print(self.buttonPath_1)
        
        # Button_1
        self.button_1 = ttk.Button(self.widgets_frame, text="Output", command = Funcbutton_1)
        self.button_1.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        
        
        # Create a Frame for the Checkbuttons
        self.check_frame = ttk.LabelFrame(self, text="Select & Start", padding=(20, 10))
        self.check_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(140, 10), sticky="nsew"
        )

        # Checkbuttons
        self.check_1 = ttk.Checkbutton(
            self.check_frame, text="Keywords", variable=self.var_0
        )
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.check_frame, text="Images", variable=self.var_1
        )
        self.check_2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        
                
        # Start Functions        
        def FuncStart_worker():
            text = self.var_0.get()
            if text:
                
                print("Process Started")
                
                
            text_1 = self.var_1.get()
            if text_1:
                
                print("Process Ended")
                
            
        def schedule_check(t):
            """
            Schedule the execution of the `check_if_done()` function after
            one second.
            """
            root.after(1000, check_if_done, t)
            
            
        def check_if_done(t):
            # If the thread has finished, re-enable the button and show a message.
            if not t.is_alive():
                self.accentbutton["state"] = "normal"
            else:
                # Otherwise check again after one second.
                schedule_check(t)
                
        def FuncStart():
            t = ""
            if self.accentbutton['text'] == 'Start':
                self.var_00.set(value=True)
                print("True")
                print("Started")
                #self.accentbutton["state"] = "disabled"
                # Start the download in a new thread.
                t = threading.Thread(target=FuncStart_worker)
                t.start()
                # Start checking periodically if the thread has finished.
                schedule_check(t)
                self.accentbutton.config(text="Stop")
            else:
                self.var_00.set(value=False)
                print(self.var_00.get())
                self.accentbutton.config(text="Start")
                
            
        
        # Accentbutton
        self.accentbutton = ttk.Button(
            self.check_frame, text="Start", style="Accent.TButton", command = FuncStart
        )
        self.accentbutton.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

        
        
        
class Gauge(ttk.Label, ttk.Frame):
    
    def __init__(self, parent, **kwargs):
        self.arc = None
        self.im = Image.new('RGBA', (1000, 1000))
        self.min_value = kwargs.get('minvalue') or 0
        self.max_value = kwargs.get('maxvalue') or 100
        self.size = kwargs.get('size') or 200
        self.font = kwargs.get('font') or 'helvetica 100 bold'
        self.background = kwargs.get('background') or '#01bdae'
        self.foreground = kwargs.get('foreground') or '#01bdae'
        
        
        self.arcvariable = tk.IntVar(value='text')
        self.arcvariable.trace_add('write', self.update_arcvariable)
        self.textvariable = tk.StringVar()
        self.textvariable_1 = tk.StringVar()
        if darkdetect.theme() == "Light":
            self.troughcolor = kwargs.get('troughcolor') or '#F5F5F5'
            self.indicatorcolor = kwargs.get('indicatorcolor') or '#005fb8'
        else:
            self.troughcolor = kwargs.get('troughcolor') or '#2d2d2d'
            self.indicatorcolor = kwargs.get('indicatorcolor') or '#5ec8fd'
            
            
        self.setup()
        
        super().__init__(parent, image=self.arc, compound='center',
                        textvariable=self.textvariable, **kwargs)
        
        label = ttk.Label(
            root,
            text='25',
            font=("Courier", 30),
            foreground='#005fb8',
            textvariable=self.textvariable)
        
        label.place(x=145, y=345, anchor='center')
        
        label_1 = ttk.Label(
            root,
            text='Loading...',
            font=("Courier", 12),
            foreground='#808080',
            textvariable = self.textvariable_1)
            
        
        label_1.place(x=140, y=375, anchor='center')
        
        
        if darkdetect.theme() == "Light":
            label.config(foreground= '#005fb8')
        else:
            label.config(foreground= '#5ec8fd')
        
    def setup(self):
        """Setup routine"""
        
                
        
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, 990, 990), 0, 360, self.troughcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.LANCZOS))
        
    def update_arcvariable(self, *args):
        """Redraw the arc image based on variable settings"""
        angle = int(float(self.arcvariable.get())) + 90
        self.im = Image.new('RGBA', (1000, 1000))
        draw = ImageDraw.Draw(self.im)
        draw.arc((0, 0, 990, 990), 0, 360, self.troughcolor, 100)
        draw.arc((0, 0, 990, 990), 90, angle, self.indicatorcolor, 100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size, self.size), Image.LANCZOS))
        self.configure(image=self.arc)
        
# Start Progress

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Alibaba Intelligence")
    root.resizable(False,False)
    
    
    
    
    # Start Progress
    gauge = Gauge(root, padding=20)
    gauge.grid(row=1, column=0)
    # Simply set the theme
    if darkdetect.theme() == "Light":
        sv_ttk.use_light_theme()
    else:
        sv_ttk.use_dark_theme()

    app = App(root)
    app.grid(row=0, column=0)
    
    
    
    gauge.textvariable.set(str(25))
    gauge.textvariable_1.set("Waiting...")
    gauge.arcvariable.set(25)
    
    # End Progress
    # Start ListBox 
    
    # Create a Frame for the Checkbuttons
    check_frame = ttk.LabelFrame(text="Console", padding=(20, 10))
    check_frame.grid(
        row=0, column=1, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
    )
    
    sf= TkFont.Font(family='Courier', size=10, weight='normal')
    lb = tk.Listbox(check_frame,selectbackground="#005fb8",relief='flat', width=60, font=sf)
    lb.pack(side="left", expand=1, fill=tk.BOTH)
    
    
      
        
    
    # End ListBox
    
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    

    root.mainloop()
    