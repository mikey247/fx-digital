import pytest
from collections import Counter
from PIL import Image

import colors
from colors import round_channel, round_colour, count_colours, dominant_colours, DEFAULT_IGNORE

class TestRoundChannel:
    def test_rounds_down(self):
        assert round_channel(123) == 120

    def test_rounds_up(self):
        assert round_channel(126) == 130
 
    def test_zero(self):
        assert round_channel(0) == 0

    def test_clamps_255_to_255(self):
        # 255 would bucket to 260 without the clamp
        assert round_channel(255) == 255

    def test_low_value_clamps_to_zero(self):
        # 1 rounds down to 0 — stays at 0, not negative
        assert round_channel(1) == 0

    def test_exact_multiple(self):
        assert round_channel(100) == 100

    def test_bankers_rounding_rounds_to_even(self):
        # Python's round() uses banker's rounding: 0.5 rounds to nearest even
        # 5/10 = 0.5 → rounds to 0 (even), not 10
        assert round_channel(5) == 0
        # 15/10 = 1.5 → rounds to 2 (even), so 20
        assert round_channel(15) == 20

class TestRoundColour:
    def test_rounds_all_channels(self):
        assert round_colour((123, 64, 255)) == (120, 60, 255)

    def test_pure_black_stays_black(self):
        assert round_colour((0, 0, 0)) == (0, 0, 0)

    def test_pure_white_stays_white(self):
        assert round_colour((255, 255, 255)) == (255, 255, 255)

class TestCountColours:
    def test_counts_pixels(self):
        # 204 rounds down to 200, 53 rounds up to 50
        pixels = [(204, 0, 0), (204, 0, 0), (0, 53, 0)]
        result = count_colours(pixels)
        assert result[(200, 0, 0)] == 2
        assert result[(0, 50, 0)] == 1

    def test_rounding_groups_similar_colours(self):
        # Both round to (250, 0, 0) and should be counted as one bucket
        pixels = [(251, 0, 0), (249, 0, 0)]
        result = count_colours(pixels)
        assert result[(250, 0, 0)] == 2

    def test_ignore_filters_colours(self):
        pixels = [(0, 0, 0), (255, 255, 255), (255, 0, 0)]
        result = count_colours(pixels, ignore=DEFAULT_IGNORE)
        assert (0, 0, 0) not in result
        assert (255, 255, 255) not in result
        # 255 clamps to 255 after rounding up to 260
        assert result[(255, 0, 0)] == 1

    def test_empty_pixels_returns_empty_counter(self):
        assert count_colours([]) == Counter()

    def test_no_ignore_counts_black_and_white(self):
        pixels = [(0, 0, 0), (255, 255, 255)]
        result = count_colours(pixels, ignore=set())
        assert result[(0, 0, 0)] == 1
        assert result[(255, 255, 255)] == 1

def make_image(pixels):
    """Create an in-memory RGB image from a flat list of (R, G, B) tuples."""
    img = Image.new("RGB", (len(pixels), 1))
    img.putdata(pixels)
    return img


class TestDominantColours:
    def test_returns_most_frequent_colour(self):
        pixels = [(255, 0, 0)] * 5 + [(0, 0, 255)] * 2
        img = make_image(pixels)
        result = dominant_colours(img, top_n=1)
        assert result[0][0] == (255, 0, 0)

    def test_top_n_returns_correct_count(self):
        pixels = [(255, 0, 0)] * 5 + [(0, 255, 0)] * 3 + [(0, 0, 255)] * 1
        img = make_image(pixels)
        result = dominant_colours(img, top_n=2)
        assert len(result) == 2

    def test_results_ordered_by_frequency(self):
        pixels = [(255, 0, 0)] * 5 + [(0, 0, 255)] * 2
        img = make_image(pixels)
        result = dominant_colours(img, top_n=2)
        assert result[0][1] > result[1][1]
    
    def test_tie__breaks_by_insert_order(self):
        pixels = [(255, 0, 0)] * 5 + [(0, 255, 0)] * 5 + [(0, 0, 255)] * 5
        img = make_image(pixels)
        result = dominant_colours(img, top_n=2)
        # Both have same count, but (255, 0, 0) was seen first in the image
        assert result[0][0] == (255, 0, 0)
        assert result[1][0] == (0, 255, 0)

    def test_ignores_black_and_white_by_default(self):
        pixels = [(0, 0, 0)] * 10 + [(255, 0, 0)] * 2
        img = make_image(pixels)
        result = dominant_colours(img, top_n=1)
        assert result[0][0] == (255, 0, 0)

    def test_top_n_larger_than_distinct_colours(self):
        pixels = [(255, 0, 0)] * 5 + [(0, 255, 0)] * 3
        img = make_image(pixels)
        result = dominant_colours(img, top_n=5)
        assert len(result) == 2
        assert result[0][0] == (255, 0, 0)

    def test_top_n_zero_returns_empty_list(self):
        pixels = [(255, 0, 0)] * 5
        img = make_image(pixels)
        result = dominant_colours(img, top_n=0)
        assert result == []
