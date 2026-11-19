
"""Homework 4 - Problem 3: Fade to Black and White."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def image_load(filename):
    """Load a color image."""
    return plt.imread(filename)


def convert_bw(img):
    """Convert an RGB image to grayscale using NumPy."""
    average = np.mean(img, axis=2).astype(np.uint8)

    # Repeat the grayscale values across RGB channels.
    return np.broadcast_to(
        average[:, :, np.newaxis], img.shape
    ).copy()


def image_gen(filename, steps):
    """Generate a transition from color to grayscale and back."""
    original = image_load(filename)
    grayscale = convert_bw(original)

    for i in range(steps + 1):
        alpha = i / steps
        frame = (
            (1 - alpha) * original + alpha * grayscale
        )
        yield frame.astype(np.uint8)

    for i in range(steps - 1, -1, -1):
        alpha = i / steps
        frame = (
            (1 - alpha) * original + alpha * grayscale
        )
        yield frame.astype(np.uint8)


def main():
    """Display the animated color-to-grayscale transition."""
    filename = Path(__file__).parent / "florida-keys-800-480.jpg"

    if not filename.exists():
        print("Image not found:", filename)
        print("Put the JPG file in the same folder as this Python file.")
        return

    original = image_load(filename)
    frames = list(image_gen(filename, 30))

    fig, ax = plt.subplots()
    picture = ax.imshow(original)
    ax.set_title("Fade to Black and White")
    ax.axis("off")

    def update(frame):
        picture.set_data(frame)
        return (picture,)

    animation = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=50,
        blit=True,
        repeat=True,
    )

    plt.show()


if __name__ == "__main__":
    main()
