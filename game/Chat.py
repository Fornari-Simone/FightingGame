# region imports

from pygame_gui.core.interfaces.manager_interface import IUIManagerInterface
from pygame_gui.elements import UITextBox, UITextEntryLine, UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_TEXT_ENTRY_FINISHED
from pygame_gui.core.ui_container import UIContainer
from pygame import Rect, USEREVENT
from udp.custom_udp import UDP_P2P
from typing import Tuple, Union
from pygame.event import Event
from udp.packet import Packet
from datetime import datetime
from game.const import Game

# endregion


class Chat(UIContainer):
    # region Docstring
    """
    Class to display the game chat
    """
    # endregion

    def __init__(
        self,
        size: tuple[int, int],
        manager: IUIManagerInterface,
        udp: UDP_P2P,
        username: str,
    ) -> None:
        # region Docstring
        """
        Creates a `Chat` object

        ### Arguments
            `size {(int, int)}`:
                `summary`: the size of the chat window
            `manager {UIManager}`:
                `summary`: the UIManager that manages this element.
            `udp {UDP_P2P}`:
                `summary`: the udp object
            `username {str}`:
                `summary`: the username of this host
        """
        # endregion
        super().__init__(relative_rect=Rect((Game.SIZE[0], 0), size), manager=manager)

        # region Element creation

        self.textbox = UITextBox(
            html_text="",
            relative_rect=Rect((0, 0), (size[0], size[1] - 25)),
            manager=manager,
            container=self,
        )

        self.entryline = UITextEntryLine(
            relative_rect=Rect((0, size[1] - 28), (size[0] - 50, 20)),
            manager=manager,
            container=self,
        )
        self.entryline.set_text_length_limit(100)

        self.enterbtn = UIButton(
            text="Enter",
            relative_rect=Rect((size[0] - 50, size[1] - 28), (50, 30)),
            manager=manager,
            container=self,
        )

        # endregion

        self.record = ""
        self.size = size
        self.udp = udp
        self.username = username

    def process_event(self, event: Event) -> Union[bool, None]:
        # region Docstring
        """
        Overridden method to handle the gui events

        ### Arguments
            `event {Event}`:
                `summary`: the fired event

        ### Returns
            `bool | None`: return if the event has been handled
        """
        # endregion

        handled = super().process_event(event)
        if event.type != USEREVENT:
            return

        if (
            event.user_type == UI_TEXT_ENTRY_FINISHED
            and event.ui_element == self.entryline
        ) or (
            event.user_type == UI_BUTTON_PRESSED and event.ui_element == self.enterbtn
        ):
            self.__send()
            handled = True

        return handled

    def __send(self) -> None:
        # region Docstring
        """
        Handles the press of the enter `UIButton`, sending the user message.\n
        """
        # endregion

        if len(self.entryline.get_text().strip()) > 0:
            self.udp.transmission(
                "CHA", "01", self.username, self.entryline.get_text().strip()
            )
            self.__addmsg(f"<b>(YOU): </b><br>{self.entryline.get_text().strip()}<br>")
            self.entryline.set_text("")

    def receive(self, data: Packet, addr: Tuple[str, int], time: datetime) -> None:
        # region Docstring
        """
        Method that handles the received data, address and time of reception

        ### Arguments
            `data {Packet}`:
                `summary`: the data received
            `addr {Tuple[str, int]}`:
                `summary`: the source address and port
                example: (192.168.0.1, 6000)
            `time {datetime}`:
                `summary`: the time of the packet reception
        """
        # endregion

        n = UDP_P2P.latency(
            datetime.strptime(time.strftime("%H%M%S%f"), "%H%M%S%f"),
            datetime.strptime(data.time + "000", "%H%M%S%f"),
        )

        self.record += f"<b>({data.nick.strip()} - {addr[0]} - {n}ms): </b><br>{data.msg.strip()}<br>"

    def update(self, time_delta: float) -> None:
        # region Docstring
        """
        Overridden method to update the element

        ### Arguments
            `time_delta {float}`:
                `summary`: the time passed between frames, measured in seconds.
        """
        # endregion

        super().update(time_delta)
        if self.record != self.textbox.html_text:
            self.textbox.kill()
            self.textbox = UITextBox(
                html_text=self.record,
                relative_rect=Rect((0, 0), (self.size[0], self.size[1] - 25)),
                container=self,
                manager=self.ui_manager,
            )

    def __addmsg(self, msg: str) -> None:
        # region Docstring
        """
        Method to insert text in the `UITextBox` element

        ### Arguments
            `msg {str}`:
                `summary`: the text to insert
        """
        # endregion
        self.record += msg
        self.textbox.kill()
        self.textbox = UITextBox(
            html_text=self.record,
            relative_rect=Rect((0, 0), (self.size[0], self.size[1] - 25)),
            container=self,
            manager=self.ui_manager,
        )
