import time

from kivy.clock import Clock


class TimerLogic:
    def __init__(self):
        self.timer_event = None
        self.running = False
        self.update_callback = None
        self.start_time = 0
        self.end_time = 0

    def validate_input(self, instance, value):
        """Validate that input is within range 0-300"""
        if value:
            try:
                time_value = int(value)
                if time_value < 0:
                    instance.text = "0"
                elif time_value > 300:
                    instance.text = "300"
            except ValueError:
                instance.text = ""

    def start_timer(self, time_value, callback):
        """
        Start the countdown timer

        Args:
            time_value: Initial time value in seconds
            callback: Function to call on each timer update -
                      gets passed (current_value, is_finished)
        """
        if self.timer_event:
            self.timer_event.cancel()

        self.start_time = time.time()
        self.end_time = self.start_time + float(time_value)
        self.update_callback = callback

        remaining = self.end_time - self.start_time

        self.update_callback(remaining, False)

        self.timer_event = Clock.schedule_interval(self._update_timer, 0.05)
        self.running = True

    def _update_timer(self, dt):
        """Update the timer (called by Clock scheduler)"""
        current_time = time.time()
        remaining = max(0.0, self.end_time - current_time)

        remaining = round(remaining, 1)

        is_finished = remaining <= 0
        self.update_callback(remaining, is_finished)

        if is_finished:
            self.timer_event.cancel()
            self.running = False
            return False

        return True
