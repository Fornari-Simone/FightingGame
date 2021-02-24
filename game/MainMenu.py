# region Imports

from tkinter import PhotoImage, Tk, messagebox, Label
from tkinter import Entry, Button, Frame
from tkinter.simpledialog import Dialog
from tkinter.constants import ACTIVE
from tkinter.font import nametofont
from udp.custom_udp import UDP_P2P
from udp.packet import NICK_LEN
from datetime import datetime
from threading import Thread
from game.const import Game
from game.Chat import Chat
import urllib.request
import socket

# endregion Imports


class MainMenu:
    # region DocString
    """
    Class to display the main menu of the game
    """
    # endregion

    def __init__(self, gameloop) -> None:
        # region DocString
        """
        Creates a `MainMenu` object

        ### Arguments
            `gameloop {function(bool, str, str, str, str, UDP_P2P): str}`:
                `summary`: a fuction to start the pygame loop
        """
        # endregion

        self.gameloop = gameloop

        # region Root setup

        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title("Fighting Game")

        # endregion

        # region Widget setup

        startBtn_img = PhotoImage(file="img/Menu/StartGame.png")
        Button(
            self.root,
            image=startBtn_img,
            command=self.__start,
            borderwidth=0,
            highlightthickness=0,
        ).grid(row=0, column=0, columnspan=2, sticky="n")

        controls_img = PhotoImage(file="img/Menu/Controls.png")
        Button(
            self.root,
            image=controls_img,
            command=self.__info,
            borderwidth=0,
            highlightthickness=0,
        ).grid(row=1, column=0, sticky="w")

        quit_img = PhotoImage(file="img/Menu/QUIT.png")
        Button(
            self.root,
            image=quit_img,
            command=self.root.destroy,
            borderwidth=0,
            highlightthickness=0,
        ).grid(row=1, column=1, sticky="e")

        Label(
            self.root,
            text=f"""
Private IP:  {socket.gethostbyname(socket.gethostname())} 
Public IP:  {urllib.request.urlopen('https://ident.me').read().decode('utf8')}""",
            # socket.gethostbyname(socket.gethostname()) -> Private IP
            # urllib.request.urlopen('https://ident.me').read().decode('utf8') -> Public IP
            font=f"{Game.FONT} 19 bold",
        ).grid(row=2, column=0, columnspan=2, sticky="w")

        # endregion

        # region Center window

        self.root.geometry(
            f"+{(self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)}+{(self.root.winfo_screenheight() // 2 - self.root.winfo_reqheight() // 2)}"
        )

        # endregion

        self.root.mainloop()

    def __start(self) -> None:
        # region DocString
        """
        Method that starts the game. First the user is prompted to input a username and an IP for the connection,\n
        then a character must be selected and the connection with the other user starts.
        """
        # endregion

        self.root.withdraw()
        try:
            self.__input()
            udp = UDP_P2P(self.ipDest, 6000, 6000)
            wait = WaitingWindow(self.ipDest)

            while wait.is_alive():

                # region Enstablish connection with other player

                udp.transmission(Game.APP, Game.VERSION, self.username, "connection")
                rdata, _, _ = udp.singleReceive(1)
                if rdata is not None and rdata.msg == "connection":
                    udp.transmission(
                        Game.APP, Game.VERSION, self.username, "connection"
                    )
                    stime = udp.transmission(
                        Game.APP, Game.VERSION, self.username, self.character
                    )
                    rdata, _, _ = udp.singleReceive(None)
                    if rdata is not None and rdata.msg == "connection":
                        rdata, _, _ = udp.singleReceive(None)
                    imPlayer1 = stime < datetime.strptime(
                        f"{rdata.time}000", "%H%M%S%f"
                    )
                    wait.stop()

                    # endregion

                    chat = Chat(self.ipDest, rdata.nick, udp, self.root)

                    # region Start pygame loop

                    gamestate = self.gameloop(
                        imPlayer1,
                        self.character,
                        self.username,
                        rdata.msg,
                        rdata.nick,
                        udp,chat
                    )

                    # endregion

                    # region Handle window exit cause

                    if gamestate == "Quitted":
                        messagebox.showinfo(
                            "Quitting", "The other player left the game"
                        )
                    elif gamestate == "Win":
                        messagebox.showinfo("Results", "YOU WIN!")
                    elif gamestate == "Lost":
                        messagebox.showinfo("Results", "YOU LOST!")

                    # endregion

        except Exception as e:
            print(e)
            pass
        finally:
            self.root.wm_deiconify()

    def __info(self) -> None:
        # region DocString
        """
        Method that shows an info dialog with a list of the key bindings
        """
        # endregion

        self.root.withdraw()

        # region Info dialog

        messagebox.showinfo(
            "CONTROLS",
            "Jump: Up Arrow\nMove to Left: Left Arrow\nMove to Right: Right Arrow\nNormal Attack: Z\nCharged Attack: X",
        )

        # endregion

        self.root.wm_deiconify()

    def __input(self) -> None:
        # region DocString
        """
        Shows an `InputDialog` and a `CharacterDialog` to get user input.\n
        If the input is invalid the function is recalled.
        """
        # endregion

        self.username, self.ipDest = InputDialog(self.root).result

        # region Check if username is valid

        if not self.username or len(self.username) > NICK_LEN:
            messagebox.showerror(
                "Input Error", "Invalid Username. Max size is 16 characters"
            )
            self.__input()

        # endregion

        # region Check if IP is valid

        if not UDP_P2P.checkIP(self.ipDest):
            messagebox.showerror("Input Error", "Invalid IP")
            self.__input()

        # endregion

        self.character = CharacterDialog(self.root).character


class WaitingWindow(Thread):
    # region DocString
    """
    Class to display a waiting window in a separate thread
    """
    # endregion

    def __init__(self, other: str) -> None:
        # region DocString
        """
        Creates a `WaitingWindow` object and starts the thread

        ### Arguments
            `other {str}`:
                `summary`: the ip of the remote player
        """
        # endregion

        super(WaitingWindow, self).__init__()
        self.other = other
        self.daemon = True
        self.start()

    def run(self) -> None:
        # region DocString
        """
        Method overridden from `Thread`
        """
        # endregion

        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)

        # region Widget setup

        Label(
            self.root, text=f"Waiting for {self.other}...", font=f"{Game.FONT} 20 bold"
        ).pack()
        Button(
            self.root, text="Cancel", command=self.stop, font=f"{Game.FONT} 20 bold"
        ).pack()

        # endregion

        self.root.mainloop()

    def stop(self) -> None:
        # region DocString
        """
        Method to destroy the window
        """
        # endregion

        self.root.quit()


class InputDialog(Dialog):
    # region DocString
    """
    Creates an input dialog with two `Entry` widgets, one for the username and one for the destination IP
    """
    # endregion

    def body(self, master: Tk) -> Entry:
        # region DocString
        """
        Handles the creation of the widgets in the window

        ### Arguments
            `master {Tk}`:
                `summary`: the parent window

        ### Returns
            `Entry`: the focused widget
        """
        # endregion

        self.resizable(0, 0)

        # region Widget setup

        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=20)
        self.option_add("*Font", default_font)

        Label(master, text="Username:").grid(row=0)
        Label(master, text="Connect to IP:").grid(row=1)

        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2 = Entry(master)
        self.e2.grid(row=1, column=1)

        # endregion

        return self.e1

    def apply(self) -> None:
        # region DocString
        """
        Implemented method to load the result of the input
        """
        # endregion

        self.result = [self.e1.get(), self.e2.get()]


class CharacterDialog(Dialog):
    # region DocString
    """
    Creates an input dialog with two `Button` widgets, one for each selectable character
    """
    # endregion

    def buttonbox(self) -> None:
        # region DocString
        """
        Overridden from `Dialog`. Creates the body of the dialog
        """
        # endregion

        self.resizable(0, 0)
        self.focus()

        box = Frame(self)

        # region Widget setup

        ichigoimg = PhotoImage(file="img/Profili/Ichigo.png")
        btn = Button(
            box,
            image=ichigoimg,
            command=lambda: self.__choice("Ichigo"),
            default=ACTIVE,
            borderwidth=0,
        )
        btn.image = ichigoimg
        btn.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        vegethimg = PhotoImage(file="img/Profili/Vegeth.png")
        btn = Button(
            box, image=vegethimg, command=lambda: self.__choice("Vegeth"), borderwidth=0
        )
        btn.image = vegethimg
        btn.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        # endregion

        box.pack()

    def __choice(self, char: str) -> None:
        # region DocString
        """
        Method that closes the dialog when a character is selected

        ### Arguments
            `char {str}`:
                `summary`: the character chosen
        """
        # endregion

        self.ok()
        self.character = char
