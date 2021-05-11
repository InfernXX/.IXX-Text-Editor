from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
from pathlib import Path
import argparse
import Validity_Check as VC
#Making the Root Variable into a callable function, then calling it once.
def Define_Root():
    global Rt, Init_RT
    Rt = Tk()
    Init_RT = True
Define_Root()
#Establishing the Root Variable and the Exit Code Variable for ease of use.
global ExitCode
ExitCode = "Normal_Exit"

#Run a Validation Check
VC.Check()

#Grab all the different Config Settings
F = open("Config.txt", "r")
C_Con = F.read().split("\n")
F.close()

#Function for the internal Script to stop the program without raising issues.
def Force_Quit():
    global Rt, Init_RT
    Rt.destroy()
    Init_RT = False
def Force_Quit_Menu():
    global Rt, Init_RT, ExitCode
    Rt.destroy()
    Init_RT = False
    ExitCode = "Normal_Exit"

#Startup File Command for when I eventually get that working.
def Startup_File(File):
    #Open the File
    TFile = open(File, "r")
    Contents = TFile.read()
    #Add File to Text-Box
    MText.insert(END, Contents)
    #Close the Open File
    TFile.close()
    #Updating Status Bars to match
    Name = File
    SBar.config(text=f"Ready. {Name}        ")
    Name = os.path.basename(Name)
    Rt.title(f"{Name} - IXX Text Editor") 

#Theme Handler for Ease of Reading for Main Function
def Theme_Handler(Theme_Config):
    For_Run = 1
    while For_Run > 0:
        try:
            F = open(Theme_Config, "r")
            Theme_Con_Mast = F.read().split("::")
            F.close()
            if Theme_Con_Mast[1] == "":
                Theme_Con = open("Basic.IXXTC", "r").read().split("\n")
            else:
                Theme_Con = open(Theme_Con_Mast[1], "r").read().split("\n")
            For_Run -= 1
        except FileNotFoundError:
            F = open(Theme_Config, "w")
            F.write("Active Theme::Basic.IXXTC")
            F.close()
    return Theme_Con


#Set Variable for Global Opened File Name 
global OpenG_Name #OpenGlobal_Name
OpenG_Name = False

global Selected
Selected = False

#New File Creation Fucntion
def NewFile(e):
    #Delete Previous Contents
    MText.delete("1.0", END)
    #Update Status Bars
    Rt.title("New File - IXX Text Editor")
    SBar.config(text="New File        ")
    
    global OpenG_Name #OpenGlobal_Name
    OpenG_Name = False

#Open Selected File Function
def OpenFile(e):
    #Delete Previous Contents
    MText.delete("1.0", END)
    #Grab Filename
    TFile = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File", filetypes=(("IXX Standard Files", "*.IXXF"), ("IXX Config Files", "*.IXXC"), ("IXX Theme Config Files", "*.IXXTC"), ("IXX Validation Files", "*.IXXVF"), ("IXX Log Files", "IXXLF"), ("IXX Special Files", "*.IXXS"), ("Text Files", "*.txt"), ("All Files", "*.*")))
    
    #Checkto See if a File Name is Present 
    if TFile:
        #Make File Name Global for Later Access
        global OpenG_Name #OpenGlobal_Name
        OpenG_Name = TFile
        OpenedFile = True
    else:
        OpenedFile = False
        NewFile(False)
        TFile = "New File"
    #Update Status Bars
    Name = TFile
    SBar.config(text=f"{Name}        ")
    Name = os.path.basename(Name)
    Rt.title(f"{Name} - IXX Text Editor")
    #Circumventing Exceptions caused by the cancelation of OpenFile
    if OpenedFile != False:
        #Open the File
        TFile = open(TFile, "r")
        Contents = TFile.read()
        #Add File to Text-Box
        MText.insert(END, Contents)
        #Close the Open File
        TFile.close()

#Save Current File As
def SaveFileAs(e):
    TFile = filedialog.asksaveasfilename(defaultextension=".*", initialdir=os.getcwd(), title="Save File", filetypes=(("IXX Standard Files", "*.IXXF"), ("IXX Config Files", "*.IXXC"), ("IXX Theme Config Files", "*.IXXTC"), ("IXX Validation Files", "*.IXXVF"), ("IXX Log Files", "IXXLF"), ("IXX Special Files", "*.IXXS"), ("Text Files", "*.txt"), ("All Files", "*.*")))
    if TFile:
        #Update Status Bars
        Name = TFile
        SBar.config(text=f"Saved: {Name}        ")
        Name = os.path.basename(Name)
        Rt.title(f"{Name} - IXX Text Editor")

        #Save the File
        TFile = open(TFile, "w")
        TTV = MText.get(1.0, END)
        FinVar = ""
        Stage_Two = TTV.split("\n")
        Count = 0
        for i in Stage_Two:
            if Count == len(Stage_Two)-1:
                pass
            else:
                FinVar += i
            Count += 1

        TFile.write(FinVar)
        #Close the File
        TFile.close()

#Save File Function
def SaveFile(e):
    global OpenG_Name #OpenGlobal_Name
    if OpenG_Name:
        #Save the File
        TFile = open(OpenG_Name, "w")
        TTV = MText.get(1.0, END)
        FinVar = ""
        Stage_Two = TTV.split("\n")
        Count = 0
        for i in Stage_Two:
            if Count == len(Stage_Two)-1:
                pass
            else:
                FinVar += i
            Count += 1
        TFile.write(FinVar)
        #Close the File
        TFile.close()
        #Put Status Update or Popup Code
        SBar.config(text=f"Saved: {OpenG_Name}        ")
    else:
        SaveFileAs(False)

#Cut Text Function
def CutText(e):
    global Selected
    #Check to see if we used keyboard Shortcuts
    if e:
        Selected = Rt.clipboard_get()
    else:
        if MText.selection_get():
            #Grab Selected Text from Text Box
            Selected = MText.selection_get()
            #Delete Selected Text from Text Box
            MText.delete("sel.first", "sel.last")
            #Clear the clipboard then append 
            Rt.clipboard_clear()
            Rt.clipboard_append(Selected)

#Copy Text Function
def CopyText(e):
    global Selected
    #Check to see if we used keyboard shortcuts
    if e:
        Selected = Rt.clipboard_get()

    if MText.selection_get():
        #Grab Selected Text from Text Box
        Selected = MText.selection_get()
        #Clear the clipboard then append 
        Rt.clipboard_clear()
        Rt.clipboard_append(Selected)

#Paste Text Function
def PasteText(e):
    global Selected
    #Check to see if we used keyboard shortcuts
    if e:
        Selected = Rt.clipboard_get()
    else: 
        if Selected:
            position = MText.index(INSERT)
            MText.insert(position, str(Selected))

#Check to see if the opened file has any text in it to avoid unessecary hassle.
def Theme_Change_Text_Saver_Checker():
    TTV = MText.get(1.0, END)
    FinVar = ""
    Stage_Two = TTV.split("\n")
    Count = 0
    for i in Stage_Two:
        if Count == len(Stage_Two)-1:
            pass
        else:
            FinVar += i
        Count += 1
    if FinVar == "":
        return False
    else:
        return True

#Grab new Theme and Apply it, it will restart the program, well exit it and the master script will restart it.
def Theme_Change(Theme):
    global Rt
    #Open Theme File and append the new theme to it.
    ThFile = open(C_Con[1].split(":")[1], "w")
    NewTheme = "Active Theme::"+Theme
    ThFile.write(NewTheme)
    ThFile.close()
    global ExitCode
    ExitCode = "Theme_Change_Exit"
    SaveNeeded = Theme_Change_Text_Saver_Checker()
    if SaveNeeded == True:
        SaveFile(False)
        Force_Quit()
    else:
        Force_Quit()

#Add a new Theme to the Index of Custom Themes
def AddTheme(e):
    CThFile = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File", filetypes=(("IXX Theme Config Files", "*.IXXTC"), ("All Files", "*.*")))
    #Creating the file as well as Appending it to the Index.
    if CThFile:
        F = open(CThFile, "r")
        Read_File = F.read()
        F.close()
        Theme = open(os.path.join(os.path.join(os.getcwd(),"Custom Themes"), os.path.basename(CThFile)), "w")
        Theme.write(Read_File)
        Theme.close()
        IndexAppend = open(C_Con[2].split(":")[1], "a")
        IndexAppend.write("\n")
        IndexAppend.write(os.path.join(os.path.join(os.getcwd(),"Custom Themes"), os.path.basename(CThFile)))
        IndexAppend.close()
    else:
        pass

#Open the "Template.txt" file for Custom Templates
def OpenTemplate(e):
    os.startfile("Template.txt")

def DEV_Print_Text_All():
    FinVar = MText.get(1.0, END)
    print(FinVar)

def DEV_Print_Text_Selected():
    Selected = MText.selection_get()
    print(Selected)

#Function for Master File
def Anima(Prelaunch, DEV):
    global MFrame, TScroll, HScroll, MMenu, Rt, FMenu, EMenu, TMenu, SBar, MText
    
    #Checking the Root and Calling the Root Function if needed.
    if Init_RT == True:
        pass
    else:
        Define_Root()

    #Establising the Theme.
    Theme_Con = Theme_Handler(C_Con[1].split(":")[1])
    Theme_Dict = {"Font":Theme_Con[0].split(":")[1], "F.Size":int(Theme_Con[1].split(":")[1]), "H.B.Colour":Theme_Con[2].split(":")[1].lower(), "H.T.Colour":Theme_Con[3].split(":")[1].lower()}

    #Grab the Config for Text Wrapping.
    TWrap = C_Con[0].split(":")
    #Syncronising True and False Statements for the list.
    Temp_ToF_TWarp = TWrap.pop(1)
    if Temp_ToF_TWarp == "true" or Temp_ToF_TWarp == "t" or Temp_ToF_TWarp == "T":
        TWrap.append("True")
    elif Temp_ToF_TWarp == "false" or Temp_ToF_TWarp == "f" or Temp_ToF_TWarp == "F":
        TWrap.append("False")
    else:
        TWrap.append(Temp_ToF_TWarp) 

    #Widnow Size Config
    WindY = int(C_Con[3].split(":")[1])
    WindX = C_Con[4].split(":")[1]

    #Check for Custom Themes Folder and create if needed
    Check = Path(os.path.join(os.getcwd(),"Custom Themes")).is_dir()
    if Check:
        pass
    else:
        os.mkdir(os.path.join(os.getcwd(),"Custom Themes"))

    if Prelaunch != "":
        Rt.title(os.path.basename(Prelaunch)+" - IXX Text Editor")
    else:
        Rt.title("Untitled - IXX Text Editor")
    Rt.iconbitmap("Assets/Text Editor Icon.ico")

    #Padding Correction depedning on TWarp Config Setting.
    if TWrap[1] == "True":
        Rt.geometry(WindX+"x"+str(WindY))
    elif TWrap == "False":
        Rt.geometry(WindX+"x"+str(WindY+20))
    else:
        Rt.geometry(WindX+"x"+str(WindY))

    #Create Main Frame
    MFrame = Frame(Rt)
    MFrame.pack(pady=5)

    #Create Scrollbar For Text Box
    TScroll = Scrollbar(MFrame)
    TScroll.pack(side=RIGHT, fill=Y)

    #Horizontal Scrollbar
    if TWrap[1] == "False":
        HScroll = Scrollbar(MFrame, orient="horizontal")
        HScroll.pack(side=BOTTOM, fill=X)


    #Create Text Box
    if TWrap[1] == "True":
        MText = Text(MFrame, width= 97, height=25, font=(Theme_Dict["Font"], Theme_Dict["F.Size"]), selectbackground=Theme_Dict["H.B.Colour"], selectforeground=Theme_Dict["H.T.Colour"], undo=True, yscrollcommand=TScroll.set)
    elif TWrap[1] == "False":
        MText = Text(MFrame, width= 97, height=25, font=(Theme_Dict["Font"], Theme_Dict["F.Size"]), selectbackground=Theme_Dict["H.B.Colour"], selectforeground=Theme_Dict["H.T.Colour"], undo=True, yscrollcommand=TScroll.set, wrap="none", xscrollcommand=HScroll.set)
    else:
        MText = Text(MFrame, width= 97, height=25, font=(Theme_Dict["Font"], Theme_Dict["F.Size"]), selectbackground=Theme_Dict["H.B.Colour"], selectforeground=Theme_Dict["H.T.Colour"], undo=True, yscrollcommand=TScroll.set)
    MText.pack()

    #Configure Scrollbar
    TScroll.config(command=MText.yview)
    if TWrap[1] == "False":
        HScroll.config(command=MText.xview)

    #Create Menu
    MMenu = Menu(Rt)
    Rt.config(menu=MMenu)

    #Add File Menu
    FMenu = Menu(MMenu, tearoff=False)
    MMenu.add_cascade(label="File", menu=FMenu)
    FMenu.add_command(label="New", command=lambda: NewFile(False), accelerator="(Crtl+n)")
    FMenu.add_command(label="Open", command=lambda: OpenFile(False), accelerator="(Crtl+o)")
    FMenu.add_command(label="Save", command=lambda: SaveFile(False), accelerator="(Crtl+s)")
    FMenu.add_command(label="Save As          ", command=lambda: SaveFileAs(False), accelerator="(Crtl+d)")
    FMenu.add_separator()
    FMenu.add_command(label="Exit", command=Force_Quit_Menu, accelerator="(Alt+f4)")

    #Add Edit Menu
    EMenu = Menu(MMenu, tearoff=False)
    MMenu.add_cascade(label="Edit", menu=EMenu)
    EMenu.add_command(label="Cut", command=lambda: CutText(False), accelerator="(Crtl+x)")
    EMenu.add_command(label="Copy", command=lambda: CopyText(False), accelerator="(Crtl+c)")
    EMenu.add_command(label="Paste          ", command=lambda: PasteText(False), accelerator="(Crtl+v)")
    EMenu.add_separator()
    EMenu.add_command(label="Undo", command=MText.edit_undo, accelerator="(Crtl+z)")
    EMenu.add_command(label="Redo", command=MText.edit_redo, accelerator="(Crtl+y)")

    #Get Custom Theme Index
    try:
        Custom_Themes = open(C_Con[2].split(":")[1], "r").read().split("\n")
    except FileNotFoundError:
        F = open(C_Con[2].split(":")[1], "w")
        F.close()
        Custom_Themes = []

    #Add Theme Menu
    TMenu = Menu(MMenu, tearoff=False)
    MMenu.add_cascade(label="Theme", menu=TMenu)
    TMenu.add_command(label="Basic", command=lambda: Theme_Change("Basic.IXXTC"))
    TMenu.add_command(label="C-Blue White", command=lambda: Theme_Change("C-Blue White.IXXTC"))
    TMenu.add_command(label="T-Purple White", command=lambda: Theme_Change("T-Purple White.IXXTC"))
    TMenu.add_separator()
    for Themes in Custom_Themes:
        if Themes == "":
            pass
        else:
            Theme = os.path.basename(os.path.join(os.path.join(os.getcwd(),"Custom Themes"), Themes))
            TMenu.add_command(label=Theme.replace(".IXXTC", "").replace("\\", ""), command=lambda: Theme_Change((os.path.join(os.path.join(os.getcwd(),"Custom Themes"), Themes))))
    TMenu.add_separator()
    TMenu.add_command(label="Add New Theme          ", command=lambda: AddTheme(False), accelerator="(Ctrl+t)")
    TMenu.add_command(label="Open Template.txt", command=lambda: OpenTemplate(False))

    #Dev Testing
    if DEV == True:
        DEVMenu = Menu(MMenu, tearoff=False)
        MMenu.add_cascade(label="Developer Tools", menu=DEVMenu)
        DEVMenu.add_command(label="Print Entire Text", command=DEV_Print_Text_All)
        DEVMenu.add_command(label="Print Selected Text", command=DEV_Print_Text_Selected)


    #Add Status Bar to Bottom of App
    if TWrap[1] == "True":
        SBar = Label(Rt, text="Ready        ", anchor=E)
        SBar.pack(fill=X, side=BOTTOM, ipady=5)
    elif TWrap[1] == "False":
        SBar = Label(Rt, text="Ready        ", anchor=E)
        SBar.pack(fill=X, side=BOTTOM, ipady=15)
    else:
        SBar = Label(Rt, text="Ready        ", anchor=E)
        SBar.pack(fill=X, side=BOTTOM, ipady=5)

    #Edit Bindings
    Rt.bind("<Control-x>", CutText)
    Rt.bind("<Control-c>", CopyText)
    Rt.bind("<Control-v>", PasteText)
    Rt.bind("<Control-s>", SaveFile)
    Rt.bind("<Control-n>", NewFile)
    Rt.bind("<Control-o>", OpenFile)
    Rt.bind("<Control-d>", SaveFileAs)
    Rt.bind("<Control-t>", AddTheme)

    #If Prelaunch, then open file and add
    if Prelaunch != "":
        Startup_File(Prelaunch)
    else:
        pass
    Rt.mainloop()
    return ExitCode