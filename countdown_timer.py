from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from timer_logic import TimerLogic


class CountdownTimer(BoxLayout):
    def __init__(self, **kwargs):
        super(CountdownTimer, self).__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 20

        self.timer_logic = TimerLogic()

        self._setup_ui()

        self._connect_events()

    def _setup_ui(self):
        """Create and add all UI elements"""
        self.input_label = Label(text="Enter time (0-300 seconds):", size_hint=(1, 0.2))
        self.time_input = TextInput(
            multiline=False,
            input_filter="int",
            size_hint=(1, 0.2),
            halign="center",
        )

        self.start_button = Button(text="Start", size_hint=(1, 0.2))

        self.timer_label = Label(text="0.0", font_size=40, size_hint=(1, 0.4))

        self.add_widget(self.input_label)
        self.add_widget(self.time_input)
        self.add_widget(self.start_button)
        self.add_widget(self.timer_label)

    def _connect_events(self):
        """Connect UI elements to their event handlers"""
        self.time_input.bind(text=self.validate_input)
        self.start_button.bind(on_press=self.start_countdown)

    def validate_input(self, instance, value):
        """Validate that input is within range 0-300"""
        self.timer_logic.validate_input(instance, value)

    def start_countdown(self, instance):
        """Start the countdown timer"""
        if not self.time_input.text:
            return

        time_value = float(self.time_input.text)
        if time_value <= 0:
            return

        def timer_callback(value, is_finished):
            """Callback function for timer updates"""
            self.timer_label.text = f"{value:.1f}"
            self.start_button.disabled = not is_finished

        self.timer_logic.start_timer(time_value, timer_callback)
        self.start_button.disabled = True
