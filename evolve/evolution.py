#append the evolve directory to the namespace
import sys
sys.path.append('/home/matthew/life/evolve')

from Tkinter import Tk, BOTH, Text, W, N, E, S, Canvas, Toplevel
from ttk import Button, Frame, Style, Label
from beings import Beings
from config import WorldConfiguration
from timer import Timer

#debugging
import pdb


class Evolution(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent

        self.initUI()
        

    def configure(self):
        self.conf = Toplevel(self)
        self.conf.wm_title("Configure Universe")

        self.wc.reconfigure(self)
    

    def initUI(self):
        #create initial Beings object (not instantiated until live is called)
        self.wc = WorldConfiguration()

        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, pad=7)
        self.rowconfigure(3, weight=1)

        lbl = Label(self, text="PyLife")
        lbl.grid(sticky = W, padx=25, pady=5)

        self.world = Canvas(self, background="#7474DB")
        self.world.grid(row=1, column=0, columnspan=3, rowspan=8, padx=5, sticky=E+W+N+S)
        
        self.sbtn = Button(self, text="Stop")
        self.sbtn.grid(row=1, column=4, pady = 5, sticky=E)

        self.bbox = Text(self, height=20, width=36)
        self.bbox.grid(row=3, column = 4, padx=5, sticky=E+W+N+S)

        self.bbox1 = Text(self, height=11, width=36)
        self.bbox1.grid(row=4, column=4, padx=5, sticky=E+W+N+S)

        self.cbtn = Button(self, text="Close", command=self.parent.destroy)
        self.cbtn.grid(row=9, column=4, pady=5)

        self.cnfbtn = Button(self, text="Configure Universe")
        self.cnfbtn.grid(row=9, column=0, padx=5)

        self.timelbl = Text(self, height=1, width=10)
        self.timelbl.grid(row=2, column=4, pady=5 )
       

        b = Beings(self)
        abtn = Button(self, text="Start", command=b.live)  #Beings(cnfbtn, world, 4, 10, sbtn, bbox, bbox1, timelbl).live)
        abtn.grid(row=1, column=4, pady=5, sticky=W)

        self.cnfbtn.config(command=b.configure)

    def close(self):
        self.parent.destroy



def main():
    root = Tk()
    root.geometry("%dx%d+%d+%d" % (990, 750, ((root.winfo_screenwidth()/2)-990), ((root.winfo_screenheight()/2-750))))
    ex = Evolution(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()
