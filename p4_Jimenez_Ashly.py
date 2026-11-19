
"""Homework 4 - Problem 4: Miniature Effect."""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from image_blur import image_load, image_save, img_blur


def img_miniature(img):
    """Create a miniature effect by blurring the top and bottom."""
    height, width = img.shape[:2]

    # Blur the image using the provided function.
    weights = np.ones((15, 15))
    blurred = img_blur(img, weights)

    # Keep the center sharp.
    result = img.copy()
    center = height // 2
    focus = height // 6
    transition = max(1, height // 8)

    for row in range(height):
        distance = abs(row - center)
        amount = np.clip(
            (distance - focus) / transition, 0, 1
        )

        result[row] = (
            (1 - amount) * img[row]
            + amount * blurred[row]
        ).astype(img.dtype)

    return result


def main():
    """Load the image, apply the effect, and save the result."""
    folder = Path(__file__).resolve().parent
    filename = folder / "florida-keys-800-480.jpg"

    if not filename.exists():
        print("Image not found:", filename)
        return

    # Load the original image.
    original = image_load(str(filename))

    # Convert RGBA to RGB if necessary.
    if original.ndim == 3 and original.shape[2] == 4:
        original = original[:, :, :3]

    # Apply miniature effect.
    miniature = img_miniature(original)

    # Save the modified image.
    output = folder / "miniature_effect.png"
    image_save(str(output), miniature)

    # Display both images.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(miniature)
    plt.title("Miniature Effect")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("Miniature effect saved successfully!")


if __name__ == "__main__":
    main()
