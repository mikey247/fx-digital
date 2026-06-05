"""Find the dominant colour(s) in an image.

The logic is split into small, stateless functions so each one can be tested
in isolation: the channel rounding and the colour counting never touch the
filesystem, so tests can feed them known values and assert on known results.
"""

from collections import Counter

from PIL import Image

# Colours excluded from the count by default. These are compared *after*
# rounding, so they match the exact black/white buckets, not near-black or
# near-white shades.

DEFAULT_IGNORE = {
    (0, 0, 0),        # black
    (255, 255, 255),  # white
}


def round_channel(value):
    bucketed = round(value / 10) * 10
    return min(255, max(0, bucketed))


def round_colour(rgb):
    r, g, b = rgb
    return (round_channel(r), round_channel(g), round_channel(b))


def load_image(image_path):
    return Image.open(image_path).convert("RGB")


def count_colours(pixels, ignore=None):
    ignore = ignore or set()
    counts = Counter()

    for pixel in pixels:
        rounded = round_colour(pixel)
        if rounded in ignore:
            continue
        counts[rounded] += 1

    return counts


def dominant_colours(image, top_n=1, ignore=DEFAULT_IGNORE):
    """Return the top_n most frequent colours as [(colour, count), ...].

    most_common(n) uses a heap internally (O(k log n)), which beats fully
    sorting the dictionary when n is small.
    """
    counts = count_colours(image.get_flattened_data(), ignore=ignore)
    return counts.most_common(top_n)


# img = load_image("test.png")
# print(dominant_colours(img, top_n=5))