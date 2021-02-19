# region Imports

from tkinter import Tk, LEFT, TOP, Toplevel, messagebox, END, Label
import tkinter
from tkinter.constants import ACTIVE, CENTER, DISABLED, NORMAL, RIGHT, X
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import Dialog
from tkinter.ttk import Entry, Button, Frame
from tkinter.font import Font, nametofont
from packet import NICK_LEN, Packet
from custom_udp import UDP_P2P
from datetime import datetime
from typing import Tuple

# endregion Imports


class MainMenu:
    def __init__(self, gameloop) -> None:
        self.gameloop = gameloop

        # region Root creation
        self.root = Tk()
        self.root.geometry("400x400")  # set the windows' dimensions
        self.root.resizable(0, 0)  # disable the resizing of the window
        self.root.title("Fighting Game")  # set the title of the window
        # endregion

        # region Widget creation
        self.startBtn = Button(
            self.root, text="Start Game", command=self.__start, width=15
        )
        self.startBtn.grid(row=0, column=0, columnspan=2)
        self.infoBtn = Button(self.root, text="Info", command=self.__info, width=15)
        self.infoBtn.grid(row=1, column=0)
        self.quitBtn = Button(self.root, text="Quit", command=self.__quit, width=15)
        self.quitBtn.grid(row=1, column=1)
        # endregion

        self.root.mainloop()

    def __start(self):
        self.root.withdraw()
        try:
            self.__input()
            udp = UDP_P2P(self.ipDest, 6000, 6000)
            while True:
                udp.transmission("CBG", "01", self.username, "connection")
                rdata, _, _ = udp.singleReceive()
                if rdata.msg == "connection":
                    udp.transmission("CBG", "01", self.username, "connection")
                    stime = udp.transmission("CBG", "01", self.username, self.character)
                    rdata, _, _ = udp.singleReceive()
                    if rdata.msg == "connection":
                        rdata, _, _ = udp.singleReceive()
                    imPlayer1 = stime < datetime.strptime(
                        rdata.time + "000", "%H%M%S%f"
                    )
                    break
            self.gameloop(imPlayer1, self.character, rdata.msg, udp)
        except:
            pass
        finally:
            self.root.wm_deiconify()

    def __info(self):
        self.root.withdraw()
        # newWindow = Tk()
        # newWindow.geometry("600x600")
        # newWindow.title("Commands")
        # Label(newWindow, text="Command\n\nArrow Up --> Jump\nArrow Left --> Move to Left\nArrow Right --> Move to Right\nz --> Normal Attack\nx --> Charged Attack").pack()
        # # entry = Entry(newWindow)
        # # entry.pack()
        # # entry.insert(
        # #     "end",
        # #     "Arrow Up --> Jump\nArrow Left --> Move to Left\nArrow Right --> Move to Right\nz --> Normal Attack\nx --> Charged Attack",
        # # )
        # Button(newWindow, text="Go to Menu", command=lambda : self.__destroyInfo(newWindow)).pack()
        messagebox.showinfo(
            "CONTROLS",
            "Jump: Up Arrow\nMove to Left: Left Arrow\nMove to Right: Right Arrow\nNormal Attack: Z\nCharged Attack: X",
        )
        self.root.wm_deiconify()

    def __destroyInfo(self, new):
        new.destroy()
        self.root.wm_deiconify()

    def __quit(self):
        self.root.destroy()

    def __input(self) -> None:
        """
        Shows an `InputDialog` to get user input.\n
        If the input is invalid the function is recalled.
        """

        self.username, self.ipDest = InputDialog(self.root).result
        self.character = CharacterDialog(self.root).character

        if not self.username or len(self.username) > NICK_LEN:
            messagebox.showerror(
                "Input Error", "Invalid Username. Max size is 16 characters"
            )
            self.__input()

        if not UDP_P2P.checkIP(self.ipDest):
            messagebox.showerror("Input Error", "Invalid IP")
            self.__input()


class InputDialog(Dialog):
    """
    Creates an input dialog with two `Entry` widgets, one for the username and one for the destination IP
    """

    def body(self, master: Tk) -> Entry:
        """
        Handles the creation of the widgets in the window

        ### Arguments
            `master {Tk}`:
                `summary`: the parent window

        ### Returns
            `Entry`: the focused widget
        """

        Label(master, text="Username:").grid(row=0)
        Label(master, text="Connect to IP:").grid(row=1)

        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2 = Entry(master)
        self.e2.grid(row=1, column=1)

        return self.e1

    def apply(self) -> None:
        """
        Implemented method to load the result of the input
        """

        self.result = [self.e1.get(), self.e2.get()]


class CharacterDialog(Dialog):
    """
    Creates an input dialog with two `Entry` widgets, one for the username and one for the destination IP
    """

    def buttonbox(self):
        """add standard button box.
        override if you do not want the standard buttons
        """

        box = Frame(self)

        w = Button(
            box,
            text="Ichigo",
            width=10,
            command=lambda: self.__choice("Ichigo"),
            default=ACTIVE,
        )
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(
            box, text="Vegeth", width=10, command=lambda: self.__choice("Vegeth")
        )
        w.pack(side=LEFT, padx=5, pady=5)

        box.pack()

    def __choice(self, char):
        self.ok()
        self.character = char