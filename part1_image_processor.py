"""
HIT137 Assignment 3 - Part 1: Image Processing

Written by: Ashfaq Afzal Chowdhury - S399270
Responsibility: ImageProcessor class

Handles all OpenCV image manipulation:
  - loading images from disk
  - scaling images to fit display
  - generating 5 non-overlapping differences using 3+ alteration types
"""

import cv2
import numpy as np
import random


class ImageProcessor:
    """
    Handles all image processing operations using OpenCV.

    Responsibilities:
        - Load and scale images
        - Generate altered copies with exactly 5 hidden differences
        - Track difference regions for game validation
        - Support 3+ distinct alteration types
    """

    # Supported image file formats
    SUPPORTED_FORMATS = [
        ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
        ("JPEG", "*.jpg *.jpeg"),
        ("PNG", "*.png"),
        ("BMP", "*.bmp"),
    ]

    # Alteration type identifiers
    ALT_COLOUR_SHIFT = "colour_shift"
    ALT_BLUR = "blur"
    ALT_BRIGHTNESS = "brightness"
    ALT_NOISE = "noise"
    ALT_INVERT = "invert_patch"

    # All available alteration types (at least 3 required)
    ALL_ALTERATION_TYPES = [
        ALT_COLOUR_SHIFT,
        ALT_BLUR,
        ALT_BRIGHTNESS,
        ALT_NOISE,
        ALT_INVERT,
    ]

    def __init__(self, max_display_width=600, max_display_height=500):
        """
        Constructor: initialise the ImageProcessor with display constraints.

        Args:
            max_display_width  (int): Maximum width for displayed images.
            max_display_height (int): Maximum height for displayed images.
        """
        self.max_display_width = max_display_width
        self.max_display_height = max_display_height

        # Raw BGR originals (OpenCV format)
        self._original_bgr = None
        self._modified_bgr = None

        # RGB versions ready for Tkinter/PIL display
        self.original_rgb = None
        self.modified_rgb = None

        # List of dicts: {'x', 'y', 'w', 'h', 'type'}
        self.difference_regions = []

        # Patch size range (pixels in display-scaled image)
        self._patch_min = 40
        self._patch_max = 80

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_image(self, filepath: str) -> bool:
        """
        Load an image from disk, scale it, and generate the modified copy.

        Args:
            filepath (str): Absolute path to the image file.

        Returns:
            bool: True on success, False if the file could not be read.
        """
        bgr = cv2.imread(filepath)
        if bgr is None:
            return False

        scaled = self._scale_image(bgr)
        self._original_bgr = scaled.copy()
        self.original_rgb = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB)

        self._generate_differences()
        return True

    def get_difference_regions(self) -> list:
        """Return the list of difference region dicts for the current image."""
        return self.difference_regions

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _scale_image(self, bgr_image: np.ndarray) -> np.ndarray:
        """
        Scale an image to fit within display bounds, preserving aspect ratio.

        Args:
            bgr_image (np.ndarray): Source BGR image.

        Returns:
            np.ndarray: Scaled BGR image.
        """
        h, w = bgr_image.shape[:2]
        scale = min(
            self.max_display_width / w,
            self.max_display_height / h,
            1.0,  # never upscale
        )
        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            return cv2.resize(bgr_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return bgr_image.copy()

    def _generate_differences(self):
        """
        Create the modified image by introducing exactly 5 non-overlapping
        differences into a clone of the original.

        Each difference uses a randomly selected alteration type.
        The type and position are randomised on every call.
        """
        self.difference_regions = []
        modified = self._original_bgr.copy()
        h, w = modified.shape[:2]

        attempts_limit = 500
        attempts = 0

        while len(self.difference_regions) < 5 and attempts < attempts_limit:
            attempts += 1

            patch_w = random.randint(self._patch_min, self._patch_max)
            patch_h = random.randint(self._patch_min, self._patch_max)

            x = random.randint(0, max(0, w - patch_w - 1))
            y = random.randint(0, max(0, h - patch_h - 1))

            candidate = {"x": x, "y": y, "w": patch_w, "h": patch_h}

            if not self._overlaps_existing(candidate):
                alt_type = random.choice(self.ALL_ALTERATION_TYPES)
                self._apply_alteration(modified, x, y, patch_w, patch_h, alt_type)
                candidate["type"] = alt_type
                self.difference_regions.append(candidate)

        self._modified_bgr = modified
        self.modified_rgb = cv2.cvtColor(modified, cv2.COLOR_BGR2RGB)

    def _overlaps_existing(self, candidate: dict) -> bool:
        """
        Check whether a candidate region overlaps any already-placed region.

        Args:
            candidate (dict): Region with keys 'x', 'y', 'w', 'h'.

        Returns:
            bool: True if there is any overlap.
        """
        margin = 5  # extra buffer between patches
        cx1 = candidate["x"] - margin
        cy1 = candidate["y"] - margin
        cx2 = candidate["x"] + candidate["w"] + margin
        cy2 = candidate["y"] + candidate["h"] + margin

        for region in self.difference_regions:
            rx1 = region["x"]
            ry1 = region["y"]
            rx2 = region["x"] + region["w"]
            ry2 = region["y"] + region["h"]

            # AABB overlap test
            if cx1 < rx2 and cx2 > rx1 and cy1 < ry2 and cy2 > ry1:
                return True
        return False

    def _apply_alteration(
        self,
        image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        alt_type: str,
    ):
        """
        Apply one of the supported alteration types to a rectangular region
        in-place on the given image.

        Supported types:
            colour_shift   – Shift hue in HSV space (subtle but findable)
            blur           – Apply Gaussian blur to the region
            brightness     – Increase or decrease brightness
            noise          – Add random salt-and-pepper style noise
            invert_patch   – Partially invert colour channels

        Args:
            image    (np.ndarray): BGR image to modify in-place.
            x, y     (int):        Top-left corner of the region.
            w, h     (int):        Width and height of the region.
            alt_type (str):        One of the ALT_* constants.
        """
        roi = image[y : y + h, x : x + w]

        if alt_type == self.ALT_COLOUR_SHIFT:
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV).astype(np.int32)
            shift = random.choice([-40, -30, 30, 40])
            hsv[:, :, 0] = (hsv[:, :, 0] + shift) % 180
            image[y : y + h, x : x + w] = cv2.cvtColor(
                hsv.astype(np.uint8), cv2.COLOR_HSV2BGR
            )

        elif alt_type == self.ALT_BLUR:
            ksize = random.choice([9, 11, 13])
            image[y : y + h, x : x + w] = cv2.GaussianBlur(roi, (ksize, ksize), 0)

        elif alt_type == self.ALT_BRIGHTNESS:
            delta = random.choice([-60, -50, 50, 60])
            adjusted = np.clip(roi.astype(np.int32) + delta, 0, 255).astype(np.uint8)
            image[y : y + h, x : x + w] = adjusted

        elif alt_type == self.ALT_NOISE:
            noisy = roi.copy()
            num_pixels = int(0.08 * w * h)
            for _ in range(num_pixels):
                nx = random.randint(0, w - 1)
                ny = random.randint(0, h - 1)
                noisy[ny, nx] = (
                    [255, 255, 255] if random.random() < 0.5 else [0, 0, 0]
                )
            image[y : y + h, x : x + w] = noisy

        elif alt_type == self.ALT_INVERT:
            # Partially invert: only the blue channel, subtly
            inverted = roi.copy()
            inverted[:, :, 0] = 255 - inverted[:, :, 0]
            blended = cv2.addWeighted(roi, 0.55, inverted, 0.45, 0)
            image[y : y + h, x : x + w] = blended

    def get_original_bgr(self) -> np.ndarray:
        """Return the original BGR image (for drawing circles on a fresh copy)."""
        return self._original_bgr.copy() if self._original_bgr is not None else None

    def get_modified_bgr(self) -> np.ndarray:
        """Return the modified BGR image (for drawing circles on a fresh copy)."""
        return self._modified_bgr.copy() if self._modified_bgr is not None else None
