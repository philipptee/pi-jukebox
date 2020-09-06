from gpiozero import Button

class GpioHandler():
    def __init__(self, phoniebox):
        self._phoniebox = phoniebox
        self._next_btn = Button(5, pull_up=True)
        self._next_btn.when_pressed = self._phoniebox.do_next
        self._previous_btn = Button(6, pull_up=True)
        self._previous_btn.when_pressed = self._phoniebox.do_previous
        self._toggle_btn = Button(13, pull_up=True)
        self._toggle_btn.when_pressed = self._phoniebox.do_toggle
        self._volume_up_btn = Button(16, pull_up=True)  #  Black
        self._volume_up_btn.when_pressed = self.do_volume_up
        self._volume_down_btn = Button(12, pull_up=True)  # White
        self._volume_down_btn.when_pressed = self.do_volume_down

    def do_volume_up(self):
        # Necessary for rotary buttons.
        if self._volume_down_btn.is_pressed:
            self._phoniebox.do_volume_up()

    def do_volume_down(self):
        # Necessary for rotary buttons.
        if self._volume_up_btn.is_pressed:
            self._phoniebox.do_volume_down()
