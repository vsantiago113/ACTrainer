from PIL import Image, ImageTk
from ReadWriteMemory import ReadWriteMemory
import tkinter as tk
from tkinter import ttk
import sys


class ACTrainer:

    def __init__(self, parent):
        rwm = ReadWriteMemory()
        self.process = rwm.get_process_by_name('ac_client.exe')
        self.process.open()
        self.health_pointer = None
        self.ammo_pointer = None
        self.grenade_pointer = None
        self.health = 0
        self.ammo = 0
        self.grenade = 0

        def grenade_func():
            """Add more grenades in the game and update the value on the GUI"""
            try:
                self.en_grenade = self.entry_grenade.get()
                if self.en_grenade.strip() == '':
                    pass
                else:
                    self.process.write(self.grenade_pointer, int(self.en_grenade))
                    self.entry_grenade.delete(0, tk.END)
            except AttributeError:
                self.entry_grenade.delete(0, tk.END)

        def health_func():
            """
            A toggle function to turn ON or OFF infinite health.
            """
            if self.infinite_health_button['text'].endswith('OFF'):
                self.infinite_health_button.config(text='Infinite Health: ON')
            else:
                self.infinite_health_button.config(text='Infinite Health: OFF')

        def ammo_func():
            """
            A toggle function to turn ON or OFF infinite ammo.
            """
            if self.infinite_ammo_button['text'].endswith('OFF'):
                self.infinite_ammo_button.config(text='Infinite Ammo: ON')
            else:
                self.infinite_ammo_button.config(text='Infinite Ammo: OFF')

        def timer():
            """This is the TIMER function that runs every 100 milliseconds and update the health, ammo and grenade."""
            # START POINTERS FOR HEALTH, AMMO AND GRENADE
            self.health_pointer = self.process.get_pointer(0x004e4dbc, offsets=[0xf4])
            self.ammo_pointer = self.process.get_pointer(0x004df73c, offsets=[0x378, 0x14, 0x0])
            self.grenade_pointer = self.process.get_pointer(0x004df73c, offsets=[0x35c, 0x14, 0x0])
            # END POINTERS

            self.p_label.config(text='Game Online')

            self.health = self.process.read(self.health_pointer)
            self.health_label.config(text=self.health)

            self.ammo = self.process.read(self.ammo_pointer)
            self.ammo_label.config(text=self.ammo)

            self.grenade = self.process.read(self.grenade_pointer)
            self.grenade_label.config(text=self.grenade)

            if self.infinite_health_button['text'].endswith('ON'):
                self.process.write(self.health_pointer, 100)

            if self.infinite_ammo_button['text'].endswith('ON'):
                self.process.write(self.ammo_pointer, 20)

            parent.after(100, timer)

        self.p_label = tk.Label(parent, text='Game Offline', font=('Microsoft Sans Serif', 16), bg='black', fg='white')
        self.p_label.place(x=12, y=9)

        self.health_label = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24), bg='black', fg='white')
        self.health_label.place(x=53, y=128)

        self.ammo_label = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24), bg='black', fg='white')
        self.ammo_label.place(x=53, y=219)

        self.grenade_label = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24), bg='black', fg='white')
        self.grenade_label.place(x=225, y=168)

        self.infinite_health_button = ttk.Button(parent, text='Infinite Health: OFF', command=health_func)
        self.infinite_health_button.place(w=115, h=35, x=12, y=175)

        self.infinite_ammo_button = ttk.Button(parent, text='Infinite Ammo: OFF', command=ammo_func)
        self.infinite_ammo_button.place(w=115, h=35, x=12, y=268)

        self.entry_grenade = ttk.Entry(parent)
        self.entry_grenade.place(w=100, h=20, x=182, y=217)

        self.grenade_button = ttk.Button(parent, text='Insert Grenades', command=grenade_func)
        self.grenade_button.place(w=100, h=60, x=182, y=245)
        timer()


def main():
    root = tk.Tk()
    w = 300
    h = 315
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(width=False, height=False)
    root.title('AssaultCube Trainer')
    root.wm_iconbitmap('icon.ico')
    root.configure(background='#000')
    image = Image.open('AssaultCubeTutorialTrainer.jpg')
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, bg='#000')
    label.image = photo
    label.pack()
    ACTrainer(root)

    root.mainloop()
    sys.exit(1)


if __name__ == '__main__':
    main()
