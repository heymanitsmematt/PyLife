#append the evolve directory to the namespace
import sys
sys.path.append('/home/matthew/life/evolve')

from Tkinter import Tk, BOTH, Text, W, N, E, S, Canvas
from ttk import Button, Frame, Style, Label
from beings import Beings
from timer import Timer

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

        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, pad=7)
        self.rowconfigure(3, weight=1)

        lbl = Label(self, text="PyLife")
        lbl.grid(sticky=W, pady=5, padx=25)


        world = Canvas(self, background="#7474DB")
        world.grid(row=1, column=0, columnspan=3, rowspan=8, padx=5, sticky=E+W+N+S)
        
        sbtn = Button(self, text="Stop")
        sbtn.grid(row=1, column=4, pady = 5, sticky=E)

        bbox = Text(self, height=20, width=36)
        bbox.grid(row=3, column = 4, padx=5, sticky=E+W+N+S)

        bbox1 = Text(self, height=11, width=36)
        bbox1.grid(row=4, column=4, padx=5, sticky=E+W+N+S)

        cbtn = Button(self, text="Close", command=self.parent.destroy)
        cbtn.grid(row=9, column=4, pady=5)

        hbtn = Button(self, text="Configure Universe")
        hbtn.grid(row=9, column=0, padx=5)

        timelbl = Text(self, height=1, width=10)
        timelbl.grid(row=2, column=4, pady=5 )
        
        abtn = Button(self, text="Start", command=Beings(world, 4, 10, sbtn, bbox, bbox1, timelbl).live)
        abtn.grid(row=1, column=4, pady=5, sticky=W)

    def close(self):
        self.parent.destroy




def main():
    root = Tk()
    root.geometry("%dx%d+%d+%d" % (990, 750, ((root.winfo_screenwidth()/2)-990), ((root.winfo_screenheight()/2-750))))
    ex = Evolution(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()
