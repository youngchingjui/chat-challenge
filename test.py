import unittest
from unittest.mock import patch, MagicMock
from main import process_input, call_streaming_server
import http.client

# Copied from real_agent.py
mock_random_strings = [
    "Quality solutions lead to satisfied customers.",
    "Correctness is the foundation of customer trust.",
    "A well-done job is the best way to keep customers happy.",
    "Quality over speed: happy customers appreciate accuracy.",
    "The right solution is worth more than a quick fix.",
    "Excellence in service creates loyal customers.",
    "When quality is prioritized, customer satisfaction follows.",
    "Correct answers build lasting relationships.",
    "A commitment to quality ensures happy customers.",
    "Precision in service leads to customer confidence.",
    "Quality work speaks louder than quick fixes.",
    "Happy customers are those who receive the right solutions.",
    "In service, correctness is key to customer happiness.",
    "Quality service is the best customer retention strategy.",
    "A satisfied customer values quality above all.",
    "Delivering the right solution fosters customer loyalty.",
    "Quality assurance is the path to customer delight.",
    "Correctness in service builds a strong reputation.",
    "Happy customers are those who receive accurate solutions.",
    "In the end, quality is what keeps customers coming back.",
]


# Expected response chunks from product_info_bot.py
response_chunks = [
    b"<p>Smart toaster that reads your mind to determine the perfect toasting level.</p>",
    b"<p>Includes AI-powered bread recognition and interdimensional crumb tray.</p>",
    b"<p>CAUTION: May pick up breakfast desires from neighbors within 50 feet.</p>",
]


class TestMain(unittest.TestCase):

    @patch("builtins.print")
    def test_process_input_real_person(self, mock_print):
        process_input("real person")
        # Check if the printed message is one of the random strings
        printed_message = mock_print.call_args[0][0]
        self.assertIn(printed_message, mock_random_strings)

    @patch("builtins.print")
    def test_process_input_other(self, mock_print):
        process_input("other input")
        mock_print.assert_called_with("You entered: other input")


if __name__ == "__main__":
    unittest.main()
