import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from ReadWriteMemory import rwm

import sys

class AC_Trainer:

    def __init__(self, parent):

        def subGranade():
            try:
                self.enGranade = self.entryGranade.get()
                if self.enGranade.strip() == '':
                    pass
                else:
                    rwm.WriteProcessMemory(self.hProcess, self.GranadeVar, int(self.enGranade))
                    self.entryGranade.delete(0, tk.END)
            except AttributeError:
                self.entryGranade.delete(0, tk.END)

        def infHealthFunc():
            if self.hProcess == None:
                pass
            else:
                if self.InfHealthValue == True:
                    self.InfHealthValue = False
                    return self.InfHealthValue
                else:
                    self.InfHealthValue = True
                    return self.InfHealthValue

        def infAmmoFunc():
            if self.hProcess == None:
                pass
            else:
                if self.InfAmmoValue == True:
                    self.InfAmmoValue = False
                    return self.InfAmmoValue
                else:
                    self.InfAmmoValue = True
                    return self.InfAmmoValue

        def Timer():
            ProcID = rwm.GetProcessIdByName('ac_client.exe')
            self.hProcess = rwm.OpenProcess(ProcID)
            
            if self.hProcess == None:
                self.pLabel.config(text='Game Offline')
                self.HealthLabel.config(text='0x0')
                self.AmmoLabel.config(text='0x0')
                self.GranadeLabel.config(text='0x0')
            else:
                #Address Variale
                self.HealthVar = rwm.getPointer(self.hProcess, 0x004e4dbc, offsets=[0xf4])
                self.MainAmmoVar = rwm.getPointer(self.hProcess, 0x004df73c, offsets=[0x378,0x14,0x0])
                self.GranadeVar = rwm.getPointer(self.hProcess, 0x004df73c, offsets=[0x35c,0x14,0x0])
                
                self.pLabel.config(text='Game Online')
                
                self.Health = rwm.ReadProcessMemory(self.hProcess, self.HealthVar)
                self.HealthLabel.config(text=self.Health)

                self.MainAmmo = rwm.ReadProcessMemory(self.hProcess, self.MainAmmoVar)
                self.AmmoLabel.config(text=self.MainAmmo)

                self.Granade = rwm.ReadProcessMemory(self.hProcess, self.GranadeVar)
                self.GranadeLabel.config(text=self.Granade)

                if self.InfHealthValue == True:
                    rwm.WriteProcessMemory(self.hProcess, self.HealthVar, 100)
                    self.infHealthButton.config(text='Infinite Health: On')
                else:
                    self.infHealthButton.config(text='Infinite Health: OFF')

                if self.InfAmmoValue == True:
                    rwm.WriteProcessMemory(self.hProcess, self.MainAmmoVar, 20)
                    self.infAmmoButton.config(text='Infinite Ammo: On')
                else:
                    self.infAmmoButton.config(text='Infinite Ammo: OFF')
            parent.after(100, Timer)

        self.InfHealthValue = False
        self.InfAmmoValue = False

        self.pLabel = tk.Label(parent, text='Game Offline', font=('Microsoft Sans Serif', 16),
                            bg='black', fg='white')
        self.pLabel.place(x=12, y=9)

        self.HealthLabel = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24),
                            bg='black', fg='white')
        self.HealthLabel.place(x=53, y=128)

        self.AmmoLabel = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24),
                            bg='black', fg='white')
        self.AmmoLabel.place(x=53, y=219)

        self.GranadeLabel = tk.Label(parent, text='0x0', font=('Microsoft Sans Serif', 24),
                            bg='black', fg='white')
        self.GranadeLabel.place(x=225, y=168)

        self.infHealthButton = ttk.Button(parent, text='Infinite Health: OFF', command=infHealthFunc)
        self.infHealthButton.place(w=115, h=35, x=12, y=175)

        self.infAmmoButton = ttk.Button(parent, text='Infinite Ammo: OFF', command=infAmmoFunc)
        self.infAmmoButton.place(w=115, h=35, x=12, y=268)

        self.entryGranade = ttk.Entry(parent)
        self.entryGranade.place(w=100, h=20, x=182, y=217)

        self.GranadeButton = ttk.Button(parent, text='Insert Granades', command=subGranade)
        self.GranadeButton.place(w=100, h=60, x=182, y=245)
        Timer()

def main():
    root = tk.Tk()
    w = 300; h =315
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
    MainWindow = AC_Trainer(root)

    root.mainloop()
    sys.exit(1)

if __name__ == '__main__':
    main()
