from Tkinter import *
from threading import Thread
import traceback

from time import sleep


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.text = StringVar()
        self.text.set("fuck yea")
        self.grid_label = Label(textvariable=self.text)
        self.grid_label.pack()
        self.i=0
        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        #self.grid_label.bind('<Key-Return>', self.increment_grid)

    def set_text(self, text):
        print "Setting text to {}".format(text)
        self.text.set(text)
        print "Set text successfully"


def keyboard_thread(app):
    keep_running = True
    while keep_running:
        try:
            key = raw_input("Send a keyboard command: ")
            if not key:
                continue
            elif ("quit" == key):
                # TODO: We should really use atexit for all this. This is
                # a short-term fix to not take down the simulator with us
                print "Received shutdown command. Exiting now"
                keep_running = False
                app.quit()
            else:
                app.set_text(key)
        except:
            traceback.print_exc()

        sleep(.1)


root = Tk()
app = App(master=root)

keyboard_thread = Thread(target=keyboard_thread, args=(app,), name="KeyboardListeningThread")
keyboard_thread.setDaemon(True)
keyboard_thread.start()

app.mainloop()
root.destroy()
