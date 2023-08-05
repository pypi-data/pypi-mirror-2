from Tkinter import *
from playdoh.processtools import *

class PlaydohGUI:
    def __init__(self, master):
        frame = Frame(master)
        self.frame = frame
        self.t = None
        self.process = None
        self.started = False

        Label(text="Number of CPUs").grid(row=0, column=0)
        self.slider_cpu = Scale(master, from_=0, to=multiprocessing.cpu_count(),
                            command = self.callback_cpu,
                            orient=HORIZONTAL)
        self.slider_cpu.set(2)
        self.slider_cpu.grid(row=0,column=1)

        Label(text="Number of GPUs").grid(row=1, column=0)
        self.slider_gpu = Scale(master, from_=0, to=2,
                            command = self.callback_gpu,
                            orient=HORIZONTAL)
        self.slider_gpu.set(1)
        self.slider_gpu.grid(row=1,column=1)
        
        self.textbox = Text(width=35, height=10)
        self.textbox.grid(row=3,columnspan=2)
        
        self.button_launch = Button(master, text="Launch", 
                                    width=12, height=2,
                                    foreground="blue",
                                    font="Arial 12 bold",
                                    command=self.start)
        self.button_launch.grid(row=4,column=0)
        
        self.button_exit = Button(master, text="Stop", 
                                    width=12, height=2,
                                    foreground="red",
                                    font="Arial 12 bold",
                                    command=self.stop)
        self.button_exit.grid(row=4,column=1)
        
        self.button_exit = Button(master, text="Exit", 
                                    width=29, height=2,
                                    font="Arial 11 bold",
                                    command=self.exit)
        self.button_exit.grid(row=5,columnspan=2)
       
    def callback_cpu(self, value):
        if self.started:
            wasstarted = True
            self.stop()
        else:
            wasstarted = False
        self.max_cpu = int(value)
        if wasstarted:
            self.start()

    def callback_gpu(self, value):
        if self.started:
            wasstarted = True
            self.stop()
        else:
            wasstarted = False
        self.max_gpu = int(value)
        if wasstarted:
            self.start()
    
    def refresh(self):
        str = recv_some(self.process).strip()
        if str is not "":
            self.textbox.insert(END, str+"\n")
            self.textbox.see(END)
            text = self.textbox.get(1.0,END)
            if (text[-11:].strip() == "Finished"):
                self.stop()
                time.sleep(.5)
                self.start()
    
    def start(self):
        if self.started:
            self.stop()
#        self.textbox.delete(1.0, END)
        args = [ "python", 
                 "playdoh_console.py", 
                 "max_cpu=%d" % self.max_cpu,
                 "max_gpu=%d" % self.max_gpu]
        self.process = Popen(args, stdin=PIPE, stdout=PIPE)
        self.t = MyTimer(1.0, self.refresh)
        self.t.start()
        self.started = True
        
    def stop(self):
        if self.started:
            if self.t is not None:
                self.t.stop()
            if self.process is not None:
                try:
                    self.process.kill()
                    self.killworkers()
                    self.textbox.insert(END, "Worker stopped.\n")
                except:
                    pass
            self.textbox.see(END)
        self.started = False
            
    def find_processes(self):
        text = self.textbox.get(1.0,END)
        pids = []
        for line in text.split("\n"):
            line = line.strip()
            ids = line.split(',')
            for id in ids:
                try:
                    id = int(id)
                    pids.append(id)
                except:
                    pass
        return pids
    
    def killworkers(self):
        pids = self.find_processes()
        for pid in pids:
            if win32api is not None:
                try:
                    p = win32api.OpenProcess(1, 0, pid)
                    win32api.TerminateProcess(p,0)
                    self.textbox.insert(END, "Process %d terminated\n" % pid)
                except:
                    pass
            else:
                try:
                    os.kill(pid, signal.SIGKILL)
                    self.textbox.insert(END, "Process %d terminated\n" % pid)
                except:
                    pass
        self.textbox.insert(END, "\n")
    
    def exit(self):
        self.stop()
        self.frame.quit()

if __name__ == '__main__':
    root = Tk()
    
    # Window not resizable
    root.resizable(0,0)
    
    # Size of the window
    w = 290
    h = 360
    
    # Centers window on the screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    root.geometry("%dx%d%+d%+d" % (w, h, x, y))
    app = PlaydohGUI(root)
    root.mainloop()
