# region Imports
from socket import AF_INET, SOCK_DGRAM, socket
from typing import Callable, Tuple
from datetime import datetime
from threading import Thread
from packet import Packet
from re import match

# endregion


class UDP_P2P:
    """
    Class to handles p2p connections via the UDP protocol

    ### Attributes
        `ipDest {str}`:
            `summary`: the destination IP
        `sendPort {int}`:
            `summary`: the destination port
        `recvPort {int}`:
            `summary`: the source port
        `sockSend {socket}`:
            `summary`: the destination socket
        `sockRecv {socket}`:
            `summary`: the source socket
    """

    def __init__(self, ipDest: str, sendPort: int, recvPort: int) -> None:
        """
        Creates a `UDP_P2P` object

        ### Arguments
            `ipDest {str}`:
                `summary`: the destination IP
            `sendPort {int}`:
                `summary`: the destination port
            `recvPort {int}`:
                `summary`: the source port
        """

        self.ipDest = ipDest
        self.sendPort = sendPort
        self.sockSend = socket(AF_INET, SOCK_DGRAM)
        self.sockRecv = socket(AF_INET, SOCK_DGRAM)
        self.sockRecv.bind(("", recvPort))

        self.stop_flag = False

    def transmission(self, app: str, ver: str, nick: str, msg: str) -> None:
        """
        Handles the transmission of a `Packet` object

        ### Arguments
            `app {str}`:
                `summary`: the name of the application from which the packet is sent
            `ver {str}`:
                `summary`: the version of the application
            `nick {str}`:
                `summary`: the username of the user in the application
            `msg {str}`:
                `summary`: the message to send

        ### Raises
            `Exception`: if the packet is invalid (check the `Packet` class for more)
        """

        try:
            p = Packet(
                app,
                ver,
                nick,
                msg,
            )
            self.sockSend.sendto(p.bytes, (self.ipDest, self.sendPort))
        except Exception as e:
            raise e

    def receptionThread(
        self,
        f: Callable[[Packet, Tuple[str, int]], None],
        onErr: Callable[[Exception], None],
    ) -> Thread:
        """
        Creates a `Thread` object that runs the reception method

        ### Arguments
            `f {function (Packet, (str, int)): None}`:
                `summary`: a function to handle the received data (data, (address, port))
            `onErr {function (Exception): None}`:
                `summary`: a function to handle the raise of an exception

        ### Returns
            `Thread`: the thread that runs the reception method with `f` and `onErr` as arguments.\n
            \t\tThe thread is a deamon
        """
        self.stop_flag = False

        t = Thread(target=self.reception, args=(f, onErr, lambda: self.stop_flag))
        t.daemon = True
        return t

    def reception(
        self,
        f: Callable[[Packet, Tuple[str, int], datetime], None],
        onErr: Callable[[Exception], None],
        stop: Callable[[], bool],
    ) -> None:
        """
        Handles the reception of data with an infinite loop when the method is called

        ### Arguments
            `f {function (Packet, (str, int)): None}`:
                `summary`: a function to handle the received data (data, (address, port))
            `onErr {function (Exception): None}`:
                `summary`: a function to handle the raise of an exception
            `stop {function (): bool}`:
                `summary`: a function to stop the loop. If returns true the cycle is interrupted\n
                \t\tand the source socket is closed, otherwise the cycle continues
        """

        while True:
            if stop():
                break

            try:
                data, addr = self.sockRecv.recvfrom(130)
                time = datetime.now()
                data = Packet(data)
                f(data, addr, time)
            except Exception as e:
                onErr(e)

        self.__closeSockRecv()

    def stopThread(self) -> None:
        """
        A method to stop a running thread from `receptionThread`
        """

        self.stop_flag = True

    def closeSockSend(self) -> None:
        """
        A method to close the destination socket
        """

        self.sockSend.close()

    def __closeSockRecv(self) -> None:
        """
        A method to close the source socket.\n
        You shouldn't use this method since its automatically called\n
        at the end of the cycle in the `reception` method
        """

        self.sockRecv.close()

    def latency(t1: datetime, t2: datetime) -> int:
        """
        A static utility method that calculates the difference in milliseconds between two times

        ### Arguments
            `t1 {datetime}`:
                `summary`: the most recent time
            `t2 {datetime}`:
                `summary`: the least recent time

        ### Returns
            `int`: the number of milliseconds between the two tmes
        """

        return int((t1 - t2).total_seconds() * 1000)

    def checkIP(ip: str) -> bool:
        """
        A static utility method to check if an ip in valid

        ### Arguments
            `ip {str}`:
                `summary`: the ip to check

        ### Returns
            `bool`: True if the ip is valid, False otherwise
        """

        return match(
            r"^((1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])$",
            ip,
        )
