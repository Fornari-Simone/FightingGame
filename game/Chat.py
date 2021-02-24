# region Imports
from tkinter import Tk, LEFT, TOP, messagebox, END, Label
from tkinter.constants import DISABLED, NORMAL, X
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import Dialog
from tkinter.ttk import Entry, Button
from udp.packet import NICK_LEN, Packet
from udp.custom_udp import UDP_P2P
from datetime import datetime
from typing import Tuple

# endregion


class Chat:
    """
    Creates the main window of the chat
    """

    def __init__(self, ip, nick, udp) -> None:

        # region Root creation
        self.root = Tk()
        self.root.geometry("700x412")  # set the windows' dimensions
        self.root.resizable(0, 0)  # disable the resizing of the window
        self.root.title("Chat")  # set the title of the window
        # endregion

        self.ipDest = ip
        self.username = nick

        #self.root.withdraw()  # makes the window invisible
        #self.__input()  # handles the user input
        #self.root.wm_deiconify()  # makes the window reappear

        # region Widget creation
        self.record = ScrolledText(self.root, state=DISABLED)
        self.record.pack(side=TOP, fill=X)

        self.message = Entry(self.root, width=100)
        self.message.bind(
            "<Return>", lambda _: self.__send()
        )  # bind the send function with the enter key
        self.message.pack(side=LEFT)

        self.enterBtn = Button(self.root, text="ENTER", command=self.__send, width=15)
        self.enterBtn.pack(side=LEFT)
        # endregion

        #self.udpp2p = UDP_P2P(self.ipDest, 6000, 6000)  # creates the UDP class
        self.udpp2p = udp
        self.t = self.udpp2p.receptionThread(
            self.__receive, lambda _: ()
        )  # initialize the reception thread
        self.t.start()

        self.root.protocol(
            "WM_DELETE_WINDOW", self.__onWindowClose
        )  # intercepts the window closing

        self.root.mainloop()

    def __input(self) -> None:
        """
        Shows an `InputDialog` to get user input.\n
        If the input is invalid the function is recalled.
        """

        self.username, self.ipDest = InputDialog(self.root).result

        if not self.username or len(self.username) > NICK_LEN:
            messagebox.showerror(
                "Input Error", "Invalid Username. Max size is 16 characters"
            )
            self.__input()

        if not UDP_P2P.checkIP(self.ipDest):
            messagebox.showerror("Input Error", "Invalid IP")
            self.__input()

    def __send(self) -> None:
        """
        Handles the press of the enter `Button`, sending the user message.\n
        If an error occurs an error dialog shows up
        """

        if len(self.message.get().strip()) > 0:
            try:
                self.udpp2p.transmission("CHA", "01", self.username, self.message.get())

                self.__addMsg(f"\n(YOU): {self.message.get().strip()}")
                self.message.delete(0, END)
            except Exception as e:
                messagebox.showerror("Input Error", e)

    def __receive(self, data: Packet, addr: Tuple[str, int], time: datetime) -> None:
        """
        Callback function for the reception thread that handles the received data, address and time of reception

        ### Arguments
            `data {Packet}`:
                `summary`: the data received
            `addr {Tuple[str, int]}`:
                `summary`: the source address and port
                example: (192.168.0.1, 6000)
            `time {datetime}`:
                `summary`: the time of the packet reception
        """

        n = UDP_P2P.latency(
            datetime.strptime(time.strftime("%H%M%S%f"), "%H%M%S%f"),
            datetime.strptime(data.time + "000", "%H%M%S%f"),
        )

        self.__addMsg(
            f"\n(Username: {data.nick.strip()} - Address: {addr[0]} - Latency: {n}ms):\n{data.msg.strip()}"
        )

    def __addMsg(self, msg: str) -> None:
        """
        Utility function to add text to the disabled `ScrolledText` area and scrolls down

        ### Arguments
            `msg {str}`:
                `summary`: the string to insert
        """

        self.record.configure(state=NORMAL)
        self.record.insert(END, msg)
        self.record.configure(state=DISABLED)
        self.record.see(END)

    def __onWindowClose(self):
        """
        Handles the closing of the main window to close the sending socket and to stop the reception thread
        """

        self.udpp2p.closeSockSend()
        self.udpp2p.stopThread()
        self.root.destroy()


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
