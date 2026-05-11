"""
HIT137 Assignment 3 - Part 4: Game Controller / GUI
Member 4 Responsibility: GameController class
Builds the main Tkinter window and wires everything together:
  - Toolbar with Load Image and Reveal buttons
  - Status bar displaying score, mistakes, remaining differences
  - Pop-up dialogs for completion and lockout events
  - Delegates image processing to ImageProcessor
  - Delegates game logic to GameState
  - Delegates rendering to CanvasRenderer
"""

import tkinter as tk
from tkinter import filedialog, messagebox

# Import the three sibling modules (Members 1, 2, 3)
from part1_image_processor import ImageProcessor
from part2_game_state import GameState
from part3_canvas_renderer import CanvasRenderer


class GameController:
    """
    Top-level controller that composes ImageProcessor, GameState, and
    CanvasRenderer into a working Tkinter application.

    Demonstrates class interaction, inheritance placeholder (see _AppWindow),
    and polymorphism-ready structure.
    """

    APP_TITLE = "Spot the Difference - HIT137 Assignment 3"
    WINDOW_BG = "#1a1a2e"

    def __init__(self):
        """
        Constructor: create the root window, instantiate collaborator objects,
        and build the full GUI layout.
        """
        # --- Root window ---------------------------------------------------
        self.root = tk.Tk()
        self.root.title(self.APP_TITLE)
        self.root.configure(bg=self.WINDOW_BG)
        self.root.resizable(False, False)

        # --- Collaborators (composition over inheritance for separation) ----
        self.image_processor = ImageProcessor(
            max_display_width=580, max_display_height=480
        )
        self.game_state = GameState()

        # --- Build GUI sections --------------------------------------------
        self._build_header()
        self._build_toolbar()

        # Canvas area frame
        canvas_frame = tk.Frame(self.root, bg=self.WINDOW_BG, padx=16, pady=8)
        canvas_frame.pack()

        self.renderer = CanvasRenderer(
            parent_frame=canvas_frame,
            canvas_width=600,
            canvas_height=500,
        )
        self.renderer.set_click_callback(self._on_image_click)
        self.renderer.clear()

        self._build_status_bar()
        self._build_footer()

    # ------------------------------------------------------------------
    # GUI construction
    # ------------------------------------------------------------------

    def _build_header(self):
        """Build the decorative title header."""
        header = tk.Frame(self.root, bg="#0d0d1f", pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🔍  SPOT  THE  DIFFERENCE",
            font=("Courier New", 20, "bold"),
            bg="#0d0d1f",
            fg="#e0c060",
        ).pack()

        tk.Label(
            header,
            text="HIT137  ·  Group Assignment 3",
            font=("Courier New", 9),
            bg="#0d0d1f",
            fg="#666688",
        ).pack()

    def _build_toolbar(self):
        """Build the toolbar row with Load Image and Reveal buttons."""
        toolbar = tk.Frame(self.root, bg="#12122a", pady=8, padx=20)
        toolbar.pack(fill=tk.X)

        btn_style = {
            "font": ("Courier New", 11, "bold"),
            "relief": tk.FLAT,
            "padx": 18,
            "pady": 6,
            "cursor": "hand2",
        }

        self.btn_load = tk.Button(
            toolbar,
            text="📂  Load Image",
            bg="#2d5a27",
            fg="#ccffcc",
            activebackground="#3a7a30",
            command=self._on_load_image,
            **btn_style,
        )
        self.btn_load.pack(side=tk.LEFT, padx=(0, 12))

        self.btn_reveal = tk.Button(
            toolbar,
            text="👁  Reveal Differences",
            bg="#1a3a6e",
            fg="#aaccff",
            activebackground="#2244aa",
            command=self._on_reveal,
            state=tk.DISABLED,
            **btn_style,
        )
        self.btn_reveal.pack(side=tk.LEFT)

        # Score display (top-right of toolbar)
        self.lbl_score_top = tk.Label(
            toolbar,
            text="Total Score: 0",
            font=("Courier New", 12, "bold"),
            bg="#12122a",
            fg="#e0c060",
        )
        self.lbl_score_top.pack(side=tk.RIGHT, padx=8)

    def _build_status_bar(self):
        """Build the status bar displayed below the canvases."""
        status_frame = tk.Frame(self.root, bg="#0d0d1f", pady=8)
        status_frame.pack(fill=tk.X)

        self.lbl_status = tk.Label(
            status_frame,
            text="Load an image to start playing.",
            font=("Courier New", 11),
            bg="#0d0d1f",
            fg="#a0a0cc",
            wraplength=1260,
            justify=tk.CENTER,
        )
        self.lbl_status.pack()

        # Mistake indicators (3 dots)
        mistake_frame = tk.Frame(status_frame, bg="#0d0d1f")
        mistake_frame.pack(pady=4)

        tk.Label(
            mistake_frame,
            text="Mistakes: ",
            font=("Courier New", 10),
            bg="#0d0d1f",
            fg="#888888",
        ).pack(side=tk.LEFT)

        self._mistake_dots = []
        for _ in range(GameState.MAX_MISTAKES):
            dot = tk.Label(
                mistake_frame,
                text="○",
                font=("Courier New", 14),
                bg="#0d0d1f",
                fg="#444466",
            )
            dot.pack(side=tk.LEFT, padx=4)
            self._mistake_dots.append(dot)

    def _build_footer(self):
        """Build a subtle footer."""
        footer = tk.Frame(self.root, bg="#0a0a18", pady=4)
        footer.pack(fill=tk.X)

        tk.Label(
            footer,
            text="Click on the Modified image to identify differences  |  Max 3 mistakes per image",
            font=("Courier New", 8),
            bg="#0a0a18",
            fg="#333355",
        ).pack()
