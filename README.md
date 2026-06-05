# Image Dominant Color Finder

## Program to find the dominant colour of an uploaded image

## Strategy

- Research how pixels of an image can be read programatically(Python)
- Decode pixel's RGB value
- Round that value to the nearest multiple of 10
- Register it with a Dictionary(HashTable) with the RGB value, and frequency as key-value pairs, increment where it's been seen before.

## Additional Features

### Implement efficiency optimisations such as using a dictionary or hash map to count occurrences of each colour

- This will be my default implementation, using dictionaries to keep count, O(1) insert, O(1) search.

### Add functionality to ignore certain colours (like white or black) if desired

- Have a list of RGB values(blacklist), to check before running the frequency update process.

### Provide an option to return the top N dominant colours instead of just one

- Sort the pixel-RGB register dictionary and return a split of [:n]
