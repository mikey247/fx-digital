# Image Dominant Colour Finder

A Python application that analyses an image and returns its most dominant colours, built as a solution to the FX Digital coding challenge.

## Approach

The core logic lives in `colors.py` and is intentionally split into small, stateless functions so each can be tested in isolation.

**1. Load the image**
PIL opens the file and converts it to RGB, normalising any format (PNG, JPG, WEBP, etc.) including images with alpha channels or palette modes.

**2. Reduce the colour space**
Each pixel's RGB channels are individually rounded to the nearest multiple of 10 using Python's built-in `round()`. This buckets similar colours together so minor variations (e.g. `(253, 0, 0)` and `(248, 0, 0)`) are treated as the same colour rather than inflating the count with near-duplicates.

One non-obvious edge case: `255` rounds up to `260` via Python's banker's rounding, which is then clamped back to `255`. The tests document this explicitly.

**3. Count with a hash map**
A `Counter` (Python's built-in hash map) tallies each rounded colour in a single O(n) pass over the pixels. Membership checks against the ignore list use a `set` for O(1) lookups.

**4. Return the top N**
`Counter.most_common(n)` uses a min-heap internally — O(k log n) — which is faster than sorting the full dictionary when N is small.

## Challenge Two — all three bonus features implemented

| Feature | Implementation |
| --- | --- |
| Hash map for counting | `Counter` in `count_colours()` |
| Ignore colours (black/white) | `DEFAULT_IGNORE` set, passed through as `ignore` param |
| Top N dominant colours | `top_n` parameter + slider in the UI |

## Running the app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The Gradio UI will be available at `http://localhost:7860`. Upload any image, choose how many colours to return with the slider, and click **Find Dominant Colours**.

## Running the tests

```bash
pytest test_colors.py -v
```

Tests cover `round_channel`, `round_colour`, `count_colours`, and `dominant_colours` — including boundary conditions (clamping, banker's rounding, empty input) and the ignore-list behaviour. No file I/O is needed for unit tests; the pure functions are tested directly with plain Python values, and `dominant_colours` is tested using in-memory PIL images.

A GitHub Actions workflow (`.github/workflows/test.yml`) runs the full suite automatically on every push and pull request.

## Project structure

```text
├── colors.py          # Core logic — image loading, rounding, counting
├── main.py            # Gradio UI
├── test_colors.py     # Pytest unit tests
├── test_ui.py         # Playwright tests
├── requirements.txt
└── .github/
    └── workflows/
        └── test.yml   # CI workflow
```

## Use of AI

Claude Code (Anthropic) was used throughout this project — for UI improvements, writing and debugging the test suite, setting up CI, and code review. All generated code was reviewed, understood, and where necessary corrected (e.g. the test suite initially had incorrect expected values for the `255` clamping edge case, which was caught when the tests were run and then fixed).
