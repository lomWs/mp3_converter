from mp3_Downloader import Mp3_Downloader as YTdownloader
from tkinter import filedialog
import tkinter
import tkinter.messagebox
import customtkinter

#SET SOME PREFERENCES
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


######## APP CLASS ########

class App(customtkinter.CTk):
    
    #### Costructor #### 
    def __init__(self):
        super().__init__()
        self.download_path = "" 
        # configure window
        self.title("Mp3 Converter.py")
        self.minsize(920,320)
        self.maxsize(920,320)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1, 2,3), weight=0)
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=250,height=1000, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mp3 Converter", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.download_btn_event,width=200,text="Download")
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=(40,10))
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.directory_btn_event,width=200,text="Directory")
        self.sidebar_button_2.grid(row=5, column=0, padx=20, pady=(0,52))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w",width=200)
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,width=200, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        
        # entry labels
        self.entry_1 = customtkinter.CTkEntry(self, placeholder_text="1)Singer-Title",height=35,width=600)
        self.entry_1.grid(row=1, column=1, columnspan=1, padx=(20, 20), pady=(0, 10), sticky="nsew")

        self.entry_2 = customtkinter.CTkEntry(self, placeholder_text="2)Singer-Title",height=35)
        self.entry_2.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")
      
        self.entry_3 = customtkinter.CTkEntry(self, placeholder_text="3)Singer-Title",height=35)
        self.entry_3.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")
     
        self.entry_4 = customtkinter.CTkEntry(self, placeholder_text="4)Singer-Title",height=35)
        self.entry_4.grid(row=4, column=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")
       
        self.entry_5 = customtkinter.CTkEntry(self, placeholder_text="5)Singer-Title",height=35)
        self.entry_5.grid(row=5, column=1, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")
      

        

    #### Event method for appearance button #### 
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    #### Event method for download button #### 
    def download_btn_event(self):
        flags = [False]*5
        threads = []
        #maybe it doesn't the best way to check if the thread is started
        if(self.entry_1.get() != "" ):
            bot1 = YTdownloader(self.entry_1.get(),self.download_path)
            threads.append(bot1)
            flags[0]=True
        if(self.entry_2.get() != ""):
            bot2 = YTdownloader(self.entry_2.get(),self.download_path)
            threads.append(bot2)
            flags[1]=True
        if(self.entry_3.get() != ""):
            bot3 = YTdownloader(self.entry_3.get(),self.download_path)
            threads.append(bot3)
            flags[2]=True
        if(self.entry_4.get() != ""):
            bot4 = YTdownloader(self.entry_4.get(),self.download_path)
            threads.append(bot4)
            flags[3]=True
        if(self.entry_5.get() != ""):
            bot5 = YTdownloader(self.entry_5.get(),self.download_path)
            threads.append(bot5)
            flags[4]=True
            
        #start the threads
        [t.start() for t in threads]
        #join the threads
        [t.join() for t in threads]

        
        if flags[0]==True:
            if bot1.download_status():
                flags[0]="DOWNLOADED"
            else:
                flags[0]="NO"
        if flags[1]==True:
            if bot2.download_status():
                flags[1]="DOWNLOADED"
            else:
                flags[1]="NO"
        if flags[2]==True:
            if bot3.download_status():
                flags[2]="DOWNLOADED"
            else:
                flags[2]="NO"
        if flags[3]==True:
            if bot4.download_status():
                flags[3]="DOWNLOADED"
            else:
                flags[3]="NO"
        if flags[4]==True:
            if bot5.download_status():
                flags[4]="DOWNLOADED"
            else:
                flags[4]="NO"
        
        
        if self.check_all_download(flags):
            tkinter.messagebox.showinfo(title="Success", message="Downloads completed")
        else:
            tkinter.messagebox.showerror(title="Error", message="Something went wrong")
            
    
    #### Check method for download #### 
    def check_all_download(self,list):
        for i in range(len(list)):
            if list[i] ==  "NO":
                return False
        return True            

            
    #### Event method for directory button ####        
    def directory_btn_event(self):   
        folder_selected = filedialog.askdirectory()
        
        self.download_path = folder_selected.replace('/','\\')
        print(self.download_path)
        
    
        



