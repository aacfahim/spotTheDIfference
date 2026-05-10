"""
HIT137 Assignment 3 - Part 3: Canvas Rendering
Member 3 Responsibility: CanvasRenderer class
Handles all visual rendering on Tkinter canvases:
  1. Displaying original and modified images side by side
  2. Drawing red circles (found differences) on both canvases
  3. Drawing blue circles (revealed differences) on both canvases
  4. Mapping canvas click coordinates to image coordinates
  5. Refreshing canvases whenever game state changes
"""

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2


class CanvasRenderer:
    """
    Manages rendering of two side-by-side Tkinter canvases.

    Inherits from object (implicit). Interacts with:
        1. ImageProcessor  (to get RGB image arrays)
        2. GameState       (to know which regions to mark)

    The renderer is purely presentational — it never modifies game state.
    """

    # Circle drawing constants
    CIRCLE_RADIUS = 28        # pixels on the displayed image
    CIRCLE_THICKNESS = 3      # line width
    COLOUR_FOUND = (220, 30, 30)      # red  (R, G, B) – found by player
    COLOUR_REVEALED = (30, 100, 220)  # blue (R, G, B) – revealed by button

    def __init__(
        self,
        parent_frame: tk.Widget,
        canvas_width: int = 620,
        canvas_height: int = 520,
    ):
        """
        Constructor: create the two canvases inside parent_frame.

        Args:
            parent_frame  (tk.Widget): The Tkinter frame that owns the canvases.
            canvas_width  (int):       Width of each individual canvas in pixels.
            canvas_height (int):       Height of each individual canvas in pixels.
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Build layout 
        # Left canvas: original image (reference only, no click handler)
        self._left_label = tk.Label(
            parent_frame,
            text="Original",
            font=("Courier New", 11, "bold"),
            bg="#1a1a2e",
            fg="#e0e0e0",
        )
        self._left_label.grid(row=0, column=0, pady=(0, 4))

        self.canvas_original = tk.Canvas(
            parent_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#0f0f23",
            highlightthickness=2,
            highlightbackground="#4444aa",
            cursor="arrow",
        )
        self.canvas_original.grid(row=1, column=0, padx=(0, 12))

        # Right canvas: modified image (accepts clicks)
        self._right_label = tk.Label(
            parent_frame,
            text="Modified  ← Click here",
            font=("Courier New", 11, "bold"),
            bg="#1a1a2e",
            fg="#e0c060",
        )
        self._right_label.grid(row=0, column=1, pady=(0, 4))

        self.canvas_modified = tk.Canvas(
            parent_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#0f0f23",
            highlightthickness=2,
            highlightbackground="#aa8800",
            cursor="crosshair",
        )
        self.canvas_modified.grid(row=1, column=1, padx=(12, 0))

        # Internal state
        self._tk_image_original = None   # keep references to prevent GC
        self._tk_image_modified = None
        self._click_callback = None       # set by GameController

        # Image offsets (for centring images smaller than the canvas)
        self._offset_x = 0
        self._offset_y = 0

        # Register click handler on modified canvas only
        self.canvas_modified.bind("<Button-1>", self._on_canvas_click)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_click_callback(self, callback):
        """
        Register a function to be called when the modified canvas is clicked.

        The callback receives (image_x: int, image_y: int) in image coordinates.

        Args: callback (callable): Function(image_x, image_y) -> None.
        """
        self._click_callback = callback

    def render(self, image_processor, game_state):
        """
        Re-render both canvases from current image and game state.

        Draws:
            1. The original and modified images (from ImageProcessor)
            2. Red circles for player-found differences
            3. Blue circles for revealed differences

        Args:
            image_processor: ImageProcessor instance (with loaded images).
            game_state:       GameState instance (with region flags).
        """
        if image_processor.original_rgb is None:
            return

        # Build annotated RGB arrays from fresh BGR copies
        orig_bgr = image_processor.get_original_bgr()
        mod_bgr = image_processor.get_modified_bgr()

        # Draw circles on both images
        for region in game_state.get_found_regions():
            cx, cy = self._region_centre(region)
            cv2.circle(orig_bgr, (cx, cy), self.CIRCLE_RADIUS,
                       self._bgr(self.COLOUR_FOUND), self.CIRCLE_THICKNESS)
            cv2.circle(mod_bgr, (cx, cy), self.CIRCLE_RADIUS,
                       self._bgr(self.COLOUR_FOUND), self.CIRCLE_THICKNESS)

        for region in game_state.get_revealed_regions():
            cx, cy = self._region_centre(region)
            cv2.circle(orig_bgr, (cx, cy), self.CIRCLE_RADIUS,
                       self._bgr(self.COLOUR_REVEALED), self.CIRCLE_THICKNESS)
            cv2.circle(mod_bgr, (cx, cy), self.CIRCLE_RADIUS,
                       self._bgr(self.COLOUR_REVEALED), self.CIRCLE_THICKNESS)

        orig_rgb = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB)
        mod_rgb = cv2.cvtColor(mod_bgr, cv2.COLOR_BGR2RGB)

        # Convert to PhotoImage and display
        self._tk_image_original = self._numpy_to_photoimage(orig_rgb)
        self._tk_image_modified = self._numpy_to_photoimage(mod_rgb)

        # Calculate centred offsets
        h, w = orig_rgb.shape[:2]
        self._offset_x = (self.canvas_width - w) // 2
        self._offset_y = (self.canvas_height - h) // 2

        self._draw_on_canvas(self.canvas_original, self._tk_image_original)
        self._draw_on_canvas(self.canvas_modified, self._tk_image_modified)

    def clear(self):
        """Clear both canvases (called before loading a new image)."""
        self.canvas_original.delete("all")
        self.canvas_modified.delete("all")
        self._show_placeholder(self.canvas_original, "Load an image to begin")
        self._show_placeholder(self.canvas_modified, "Modified image will appear here")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _on_canvas_click(self, event: tk.Event):
        """
        Handle a click event on the modified canvas.

        Translates canvas pixel coordinates to image coordinates and
        calls the registered callback (if any).
        """
        if self._click_callback is None:
            return

        image_x = event.x - self._offset_x
        image_y = event.y - self._offset_y

        # Ignore clicks outside the image bounds
        if image_x < 0 or image_y < 0:
            return

        self._click_callback(image_x, image_y)

    def _draw_on_canvas(self, canvas: tk.Canvas, photo_image: ImageTk.PhotoImage):
        """Clear a canvas and draw a PhotoImage centred on it."""
        canvas.delete("all")
        canvas.create_image(
            self.canvas_width // 2,
            self.canvas_height // 2,
            anchor=tk.CENTER,
            image=photo_image,
        )

    def _numpy_to_photoimage(self, rgb_array: np.ndarray) -> ImageTk.PhotoImage:
        """Convert an RGB numpy array to a Tkinter-compatible PhotoImage."""
        pil_image = Image.fromarray(rgb_array)
        return ImageTk.PhotoImage(pil_image)

    def _show_placeholder(self, canvas: tk.Canvas, message: str):
        """Display a placeholder text message on an empty canvas."""
        canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=message,
            fill="#555577",
            font=("Courier New", 13),
        )

    @staticmethod
    def _region_centre(region: dict) -> tuple:
        """Return the (x, y) centre pixel of a region dict."""
        cx = region["x"] + region["w"] // 2
        cy = region["y"] + region["h"] // 2
        return cx, cy

    @staticmethod
    def _bgr(rgb_tuple: tuple) -> tuple:
        """Convert an RGB colour tuple to BGR for OpenCV drawing."""
        r, g, b = rgb_tuple
        return (b, g, r)
