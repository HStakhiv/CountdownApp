import unittest
import time
from kivy.base import EventLoop
from timer_logic import TimerLogic


class TimerAccuracyTest(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        EventLoop.ensure_window()

        self.timer_logic = TimerLogic()

        self.test_durations = [1, 5, 10]
        self.acceptable_error_pct = 1

        self.timer_completed = False
        self.reported_values = []
        self.actual_start_time = 0
        self.actual_end_time = 0

    def timer_callback(self, value, is_finished):
        """Callback function for timer updates"""
        self.reported_values.append(value)

        if is_finished:
            self.timer_completed = True
            self.actual_end_time = time.time()

    def test_timer_accuracy(self):
        """Test the accuracy of the timer for different durations"""
        results = []

        for duration in self.test_durations:
            self.timer_completed = False
            self.reported_values = []

            self.actual_start_time = time.time()
            self.timer_logic.start_timer(duration, self.timer_callback)

            start_time = time.time()
            timeout = duration * 1.5

            while not self.timer_completed and (time.time() - start_time) < timeout:
                EventLoop.idle()
                time.sleep(0.01)

            self.assertTrue(
                self.timer_completed, f"Timer did not complete for duration {duration}s"
            )

            actual_duration = self.actual_end_time - self.actual_start_time

            absolute_error = abs(actual_duration - duration)
            percentage_error = (absolute_error / duration) * 100

            tick_count = len(self.reported_values)
            expected_tick_count = int(duration / 0.1)
            tick_count_error = abs(tick_count - expected_tick_count)

            final_reported_value = (
                self.reported_values[-1] if self.reported_values else 0
            )
            final_value_error = abs(final_reported_value)

            results.append(
                {
                    "duration": duration,
                    "actual_duration": actual_duration,
                    "absolute_error": absolute_error,
                    "percentage_error": percentage_error,
                    "tick_count": tick_count,
                    "expected_tick_count": expected_tick_count,
                    "tick_count_error": tick_count_error,
                    "final_reported_value": final_value_error,
                }
            )

            self.assertLessEqual(
                percentage_error,
                self.acceptable_error_pct,
                f"Timer error too high for {duration}s duration: {percentage_error:.2f}%",
            )

        print("\nTimer Accuracy Test Results:")
        print("=" * 60)
        for result in results:
            print(f"Test Duration: {result['duration']}s")
            print(f"  Actual Duration: {result['actual_duration']:.3f}s")
            print(
                f"  Error: {result['absolute_error']:.3f}s ({result['percentage_error']:.2f}%)"
            )
            print(
                f"  Ticks: {result['tick_count']} (expected {result['expected_tick_count']})"
            )
            print(f"  Final Value: {result['final_reported_value']:.3f}")
            print("-" * 40)

    def test_input_validation(self):
        """Test that input validation works correctly"""

        class MockTextInput:
            def __init__(self):
                self.text = ""

        mock_input = MockTextInput()

        mock_input.text = "150"
        self.timer_logic.validate_input(mock_input, mock_input.text)
        self.assertEqual(mock_input.text, "150")

        mock_input.text = "400"
        self.timer_logic.validate_input(mock_input, mock_input.text)
        self.assertEqual(mock_input.text, "300")

        mock_input.text = "-10"
        self.timer_logic.validate_input(mock_input, mock_input.text)
        self.assertEqual(mock_input.text, "0")

        mock_input.text = "abc"
        self.timer_logic.validate_input(mock_input, mock_input.text)
        self.assertEqual(mock_input.text, "")


if __name__ == "__main__":
    unittest.main()
