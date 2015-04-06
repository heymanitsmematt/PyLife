#append the evolve directory to the namespace
import sys
sys.path.append('/home/matthew/life/evolve')

from Tkinter import Tk, BOTH, Text, W, N, E, S, Canvas
from ttk import Button, Frame, Style, Label
from beings import Beings

#debugging
import pdb


class Evolution(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.parent.title = ("Evolution")

        self.initUI()

    def initUI(self):
        #create initial Beings object (not instantiated until live is called)

        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="PyLife")
        lbl.grid(sticky=W, pady=5, padx=25)

        world = Canvas(self, background="#7474DB")
        world.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+N+S)
        
        sbtn = Button(self, text="Stop")
        sbtn.grid(row=2, column=3)

        abtn = Button(self, text="Start", command=Beings(world, 7, 9, sbtn).live)
        abtn.grid(row=1, column=3, pady=5)

        cbtn = Button(self, text="Close", command=self.parent.destroy)
        cbtn.grid(row=5, column=3, pady=4)

        hbtn = Button(self, text="Configure Universe")
        hbtn.grid(row=5, column=0, padx=5)

        
        wbtn = Button(self, text="Step")
        wbtn.grid(row=3, column=3, sticky=N)

    def close(self):
        self.parent.destroy




def main():
    root = Tk()
    root.geometry("%dx%d+%d+%d" % (790, 550, ((root.winfo_screenwidth()/2)-790), ((root.winfo_screenheight()/2-550))))
    ex = Evolution(root)
    root.mainloop()

if __name__ == '__main__':
    main()
