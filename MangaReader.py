from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from zipfile import ZipFile
import os, sys, platform

system = platform.platform()

print(system)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# The window class
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class reader(Frame):

    def __init__(self):
    
        self.manga = 0

        self.path = os.path.join(os.getcwd(), "cache")

        self.images = []

        self.cur_site = 0

        super().__init__()

        

        self.pack()

        self.panel = Label(self)

        load_button = Button(self, text="Load E-Book", command=self.loadBook)
        print_button = Button(self, text="Print Filename", command=self.printFile)
        next_button = Button(self, text = "NEXT PAGE", command=lambda: self.loadImage(1))
        prev_button = Button(self, text = "PREV PAGE", command=lambda: self.loadImage(-1))
        img_button = Button(self, text="Print Images[]", command=lambda: print(self.images))
        
        prev_button.pack(side="bottom")
        next_button.pack(side="bottom")
        load_button.pack(side=LEFT)
        print_button.pack(side=LEFT)
        img_button.pack(side=RIGHT)
        
        self.loadBook()

    def loadBook(self):

        os.system("rm -rf cache")

        self.manga =  filedialog.askopenfilename(initialdir = os.getcwd, title = "Select file", filetypes = (("Manga or Comic Files",".cbr .cbz"),("all files","*.*")))

        if (self.manga != 0):
            if(self.manga[-4::] == ".cbz"):
                book = ZipFile(self.manga, 'r')
                book.extractall(self.path)
                book.close()
            if(self.manga[-4::] == ".cbr"):
                os.system("unrar x -ep {} {}/".format(self.manga,self.path))

            self.images = os.listdir(self.path)
            self.images.sort()

            self.initImage()

    def printFile(self):
        print(self.manga)

    def loadImage(self, num):

        self.cur_site = self.cur_site + num

        if(self.cur_site < 0):
            self.cur_site = 0

        if(self.cur_site > len(self.images)):
            self.cur_site = len(self.images)

        tmp_img = Image.open("cache/{}".format(self.images[self.cur_site]))
        tmp_img = tmp_img.resize((750,990))
        img = ImageTk.PhotoImage(tmp_img)

        self.panel.configure(image=img)
        self.panel.image = img
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def initImage(self):
        tmp_img = Image.open("cache/{}".format(self.images[0]))
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
os.system("rm -rf cache")
