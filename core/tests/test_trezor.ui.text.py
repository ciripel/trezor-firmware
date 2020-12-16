import mock
from common import *

from trezor import ui
from trezor.ui import text, display

if False:
    from typing import List, Tuple


class TestTextSpan(unittest.TestCase):
    def lines(self, span: text.Span) -> List[Tuple[str, int, bool]]:
        result = []
        while True:
            should_continue = span.next_line()
            substr = span.string[span.start : span.start + span.length]
            result.append((substr, span.width, span.word_break))
            if not should_continue:
                break
        return result

    def checkSpanWithoutWidths(
        self, span: text.Span, expected: List[Tuple[str, bool]]
    ) -> None:
        expected_with_calculated_widths = [
            (string, ui.display.text_width(string, span.font), word_break)
            for string, word_break in expected
        ]
        self.assertListEqual(self.lines(span), expected_with_calculated_widths)

    def test_basic(self):
        span = text.Span("hello")
        self.checkSpanWithoutWidths(
            span,
            [("hello", False)],
        )

        span.reset("world", start=0, font=ui.NORMAL)
        self.checkSpanWithoutWidths(
            span,
            [("world", False)],
        )

        span.reset("", start=0, font=ui.NORMAL)
        self.checkSpanWithoutWidths(
            span,
            [("", False)],
        )

    def test_two_lines(self):
        line_width = display.text_width("hello world", ui.NORMAL) - 1
        span = text.Span("hello world", line_width=line_width)
        self.checkSpanWithoutWidths(
            span,
            [
                ("hello", False),
                ("world", False),
            ],
        )

    def test_newlines(self):
        span = text.Span("hello\nworld")
        self.checkSpanWithoutWidths(
            span,
            [
                ("hello", False),
                ("world", False),
            ],
        )

        span = text.Span("\nhello\nworld\n")
        self.checkSpanWithoutWidths(
            span,
            [
                ("", False),
                ("hello", False),
                ("world", False),
                ("", False),
            ],
        )

    def test_break_words(self):
        line_width = display.text_width("hello w", ui.NORMAL) + text.DASH_WIDTH
        span = text.Span("hello world", line_width=line_width, break_words=True)
        self.checkSpanWithoutWidths(
            span,
            [
                ("hello w", True),
                ("orld", False),
            ],
        )

    def test_long_word(self):
        line_width = display.text_width("establishme", ui.NORMAL) + text.DASH_WIDTH
        span = text.Span(
            "Down with the establishment!", line_width=line_width, break_words=False
        )
        self.checkSpanWithoutWidths(
            span,
            [
                ("Down with", False),
                ("the", False),
                ("establishme", True),
                ("nt!", False),
            ],
        )


if __name__ == "__main__":
    unittest.main()