from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from zipfile import ZipFile
import os, sys, platform

system = platform.platform()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# The window class
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class reader(Frame):

    def __init__(self):
        
        super().__init__()
        
        self.manga = 0

        self.path = os.path.join(os.getcwd(), "cache")

        self.images = []

        self.cur_site = 0
        
        self.pack()

        self.panel = Label(self)

        load_button = Button(self, text="Load E-Book", command=self.loadBook)
        print_button = Button(self, text="Print Filename", command=self.printFile)
        next_button = Button(self, text = "NEXT PAGE", command=lambda: self.loadImage(1))
        prev_button = Button(self, text = "PREV PAGE", command=lambda: self.loadImage(-1))
        
        prev_button.pack(side="bottom")
        next_button.pack(side=BOTTOM)
        load_button.pack(side=LEFT)
        print_button.pack(side=LEFT)
        
        self.loadBook()

    def loadBook(self):

        os.system("del /Q /S cache")

        self.manga =  filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("Manga or Comic Files",".cbr .cbz"),("all files","*.*")))

        if (self.manga != 0):
            if(self.manga[-4::] == ".cbz"):
                book = ZipFile(self.manga, 'r')
                book.extractall(self.path)
                book.close()
            if(self.manga[-4::] == ".cbr"):
                if ( "Windows" in system):
                    os.system("unrar x -ep {} {}\\".format(self.manga,self.path))
                else:
                    os.system("unrar x -ep {} {}/".format(self.manga,self.path))

            for file in os.scandir(self.path):
                self.images.append(file.name)

            self.initImage()

    def printFile(self):
        print(self.manga)

    def loadImage(self, num):

        self.cur_site = self.cur_site + num

        if(self.cur_site < 0):
            self.cur_site = 0

        if(self.cur_site > len(self.images)):
            self.cur_site = len(self.images)

        tmp_img = Image.open(os.path.join("cache",self.images[self.cur_site]))
        tmp_img = tmp_img.resize((750,990))
        img = ImageTk.PhotoImage(tmp_img)

        self.panel.configure(image=img)
        self.panel.image = img
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def initImage(self):
        tmp_img = Image.open(os.path.join("cache",self.images[self.cur_site]))
        tmp_img = tmp_img.resize((750,990))
        img = ImageTk.PhotoImage(tmp_img)

        self.panel.configure(image=img)
        self.panel.image = img
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")


        


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# The main shit
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create the folder we're going to untar the book into
os.system("mkdir cache")

root = Tk()

app = reader()

root.mainloop()

#clear the cache

if ("Windows" in system):
    os.system("del /Q /S cache")
else:
    os.system("rm -rf cache")
