from kivy.app import App
from kivy.core.window import Window

from countdown_timer import CountdownTimer


class CountdownApp(App):
    def build(self):
        Window.size = (400, 250)
        return CountdownTimer()


if __name__ == "__main__":
    CountdownApp().run()
