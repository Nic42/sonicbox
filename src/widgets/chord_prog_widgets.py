from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from widgets.drum_machine_widgets import DMPlayButton
from widgets.synth_widgets import SynthButton


Builder.load_file('ui/chord_prog_screen.kv')


class ChordProgScreen(Screen):
    pass


class ChordsPanel(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.playing = False
        self.current_column_number = -1
        self.dt = 0
        self.column_event = None

        self.reset_current_column_number()

    def reset_current_column_number(self):
        self.current_column_number = len(self.children) - 1

    def update_current_column_number(self):
        self.current_column_number -= 1
        if self.current_column_number < 0:
            self.reset_current_column_number()

    @property
    def curr_column(self):
        return self.children[self.current_column_number]

    def play_curr_column(self):
        self.curr_column.add_overlay()
        self.curr_column.send_chord()

    def column_callback(self, dt):
        self.curr_column.remove_overlay()
        self.update_current_column_number()
        self.play_curr_column()

    def play(self, dt):
        if not self.playing:
            self.play_curr_column()
            self.column_event = Clock.schedule_interval(
                self.column_callback, dt)
            self.dt = dt
            self.playing = True
        elif dt != self.dt:
            self.column_event.cancel()
            self.column_event = Clock.schedule_interval(
                self.column_callback, dt)
            self.dt = dt

    def stop(self):
        self.column_event.cancel()
        self.curr_column.remove_overlay()
        self.reset_current_column_number()
        self.playing = False


class ChordsColumn(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

    def add_overlay(self):
        self.canvas.add(Color(0, 0.5, 0, 0.4, group='overlay'))
        self.canvas.add(Rectangle(size=self.size, pos=self.pos,
                                  group='overlay'))
        self.canvas.ask_update()

    def remove_overlay(self):
        self.canvas.remove_group('overlay')
        self.canvas.ask_update()

    def get_chosen_chord_data(self):
        key = self.parent.key.replace('#', 's')
        degree = self.key_degree.lower()

        return [
            self.parent.synth,
            key,
            self.parent.key_type,
            degree,
        ]

    def send_chord(self):
        self.app.sender.send_message(
            '/chord-prog',
            self.get_chosen_chord_data(),
        )


class ChordsSpinner(Spinner):
    pass


class CPPlayButton(DMPlayButton):

    def on_release(self):
        dt = (60 / int(self.bpm_value))
        self.panel.play(dt)


class KeysButton(SynthButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bottom_sheet = self._create_bottom_sheet('keys')


class KeyTypesButton(SynthButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bottom_sheet = self._create_bottom_sheet('key_types')
