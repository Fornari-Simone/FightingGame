# region Imports

from datetime import datetime
from typing import Union

# endregion

# region Constants

APP_LEN = 3
VER_LEN = 2
NICK_LEN = 16
TIME_LEN = 9
MSG_LEN = 100
PKT_LEN = APP_LEN + VER_LEN + NICK_LEN + TIME_LEN + MSG_LEN

# endregion


class Packet:
    # region DocString
    """
    Represents a standard packet. If any of the attributes excedes its maximum an `Exception` is raised

    ### Attributes
        `app {str}`:
            `summary`: the name of the application from which the packet is sent. Max 3 characters
        `ver {str}`:
            `summary`: the version of the application. Max 2 characters
        `nick {str}`:
            `summary`: the username of the user in the application. Max 16 characters
        `time {str}`:
            `summary`: the time when the packet is sent in the 'HHmmSSsss' format. Max 9 characters
            `example`: 102030213 (Sent at 10:20:30.213)
        `msg {str}`:
            `summary`: the message to send. Max 100 characters
        `bytes {bytes}`:
            `summary`: the packet divided in bytes
    """
    # endregion

    def __init__(self, *fields: Union[tuple[str, str, str, str], tuple[bytes]]) -> None:
        # region DocString
        """
        Creates a `Packet` object

        ### Arguments
            `fields {(str, str, str, str) | (bytes)}`:
                `summary`: a tuple with either the four fields (APP, VER, NICK, MSG)\n
                or the bytes representation of a preexisting packet.\n
                The TIME field is omitted since its automatically calculated inside the constructor\n
                for more precise latency calculations

        ### Raises
            `Exception`: if any of the arguments are over their maximum length\n
            or if wrong parameters are passed
        """
        # endregion

        self.app = ""
        self.ver = ""
        self.nick = ""
        self.time = ""
        self.msg = ""
        self.bytes = b""

        # region If the single fields are passed

        if len(fields) == 4:
            self.app = Packet.__check(fields[0], APP_LEN, "APP")
            self.ver = Packet.__check(fields[1], VER_LEN, "VER")
            self.nick = Packet.__check(fields[2], NICK_LEN, "NICK")
            self.time = datetime.now().strftime("%H%M%S%f")[:-3]

            if len(fields[3]) > MSG_LEN:
                raise Exception(f"MSG field is too long. Max is {MSG_LEN} characters")
            else:
                self.msg = fields[3]

            self.bytes = bytes(
                self.app + self.ver + self.nick + self.time + self.msg, "utf-8"
            )

        # endregion

        # region If the byte representation is passed

        elif len(fields) == 1:
            if len(fields[0]) > PKT_LEN:
                raise Exception(f"Invalid Buffer. Max is {PKT_LEN} bytes")
            else:
                self.bytes = fields[0]

                self.app = str(fields[0][0:APP_LEN], encoding="utf-8")
                self.ver = str(fields[0][APP_LEN : APP_LEN + VER_LEN], encoding="utf-8")
                self.nick = str(
                    fields[0][APP_LEN + VER_LEN : APP_LEN + VER_LEN + NICK_LEN],
                    encoding="utf-8",
                )
                self.time = str(
                    fields[0][
                        APP_LEN
                        + VER_LEN
                        + NICK_LEN : APP_LEN
                        + VER_LEN
                        + NICK_LEN
                        + TIME_LEN
                    ],
                    encoding="utf-8",
                )
                self.msg = str(
                    fields[0][APP_LEN + VER_LEN + NICK_LEN + TIME_LEN :],
                    encoding="utf-8",
                )

        # endregion

        # region Otherwise

        else:
            raise Exception(
                "Invalid Arguments. Must be (str, str, str, str) or (bytes)"
            )

        # endregion

    def __check(str: str, length: int, lbl: str) -> str:
        # region DocString
        """
        Static method to check if a string isn't over the specified length and pads it to that length

        ### Arguments
            `str {str}`:
                `summary`: the string to check
            `length {int}`:
                `summary`: the maximum length of the string
            `lbl {str}`:
                `summary`: the string identifier to display in the exception message

        ### Returns
            `str`: the padded string

        ### Raises
            `Exception`: if the string is too long
        """
        # endregion

        if len(str) > length:
            raise Exception(f"{lbl} field is too long. Max is {length} characters")
        else:
            return str.rjust(length)