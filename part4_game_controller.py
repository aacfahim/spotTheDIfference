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

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_load_image(self):
        """Handle the Load Image button click."""
        filetypes = [
            ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("All Files", "*.*"),
        ]
        filepath = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=filetypes,
        )
        if not filepath:
            return

        success = self.image_processor.load_image(filepath)
        if not success:
            messagebox.showerror(
                "Load Error",
                f"Could not load the image:\n{filepath}\n\n"
                "Please choose a valid JPG, PNG, or BMP file.",
            )
            return

        # Reset game state for the new image
        self.game_state.new_image(self.image_processor.get_difference_regions())

        # Enable reveal button and re-render
        self.btn_reveal.configure(state=tk.NORMAL)
        self.renderer.render(self.image_processor, self.game_state)
        self._refresh_status()

    def _on_image_click(self, image_x: int, image_y: int):
        """
        Handle a player click on the modified canvas.

        Delegates validation to GameState, then re-renders and updates status.

        Args:
            image_x (int): X coordinate in image space.
            image_y (int): Y coordinate in image space.
        """
        result = self.game_state.process_click(image_x, image_y)

        # Re-render to show new circles
        self.renderer.render(self.image_processor, self.game_state)
        self._refresh_status()

        if result["complete"]:
            self._show_completion_dialog()
        elif result["locked"] and result["mistake"]:
            self._show_locked_dialog()

    def _on_reveal(self):
        """Handle the Reveal Differences button click."""
        if self.image_processor.original_rgb is None:
            return

        self.game_state.reveal_all()
        self.renderer.render(self.image_processor, self.game_state)
        self._refresh_status()

        remaining_was = self.game_state.get_remaining()
        messagebox.showinfo(
            "Differences Revealed",
            "All remaining differences have been marked in blue.\n"
            "Load a new image to continue playing!",
        )

    # ------------------------------------------------------------------
    # UI update helpers
    # ------------------------------------------------------------------

    def _refresh_status(self):
        """Update all status indicators to reflect current game state."""
        # Status text
        self.lbl_status.configure(text=self.game_state.get_status_message())

        # Top-right score
        self.lbl_score_top.configure(
            text=f"Total Score: {self.game_state.total_score}"
        )

        # Mistake dot indicators
        mistakes = self.game_state.mistakes
        for i, dot in enumerate(self._mistake_dots):
            if i < mistakes:
                dot.configure(text="●", fg="#cc3333")
            else:
                dot.configure(text="○", fg="#444466")

        # Colour status label based on state
        if self.game_state.is_complete:
            self.lbl_status.configure(fg="#44dd66")
        elif self.game_state.is_locked:
            self.lbl_status.configure(fg="#dd4444")
        else:
            self.lbl_status.configure(fg="#a0a0cc")

    def _show_completion_dialog(self):
        """Show a congratulatory pop-up when all differences are found."""
        messagebox.showinfo(
            "🎉 Congratulations!",
            f"You found all {GameState.TOTAL_DIFFERENCES} differences!\n\n"
            f"Total Score so far: {self.game_state.total_score}\n\n"
            "Load a new image to keep playing.",
        )

    def _show_locked_dialog(self):
        """Show a lockout pop-up when 3 mistakes are reached."""
        messagebox.showwarning(
            "❌ Too Many Mistakes",
            f"You made {GameState.MAX_MISTAKES} mistakes.\n"
            f"You found {GameState.TOTAL_DIFFERENCES - self.game_state.get_remaining()} "
            f"of {GameState.TOTAL_DIFFERENCES} differences.\n\n"
            "No more guesses allowed for this image.\n"
            "Use the Reveal button or load a new image.",
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        """Start the Tkinter main event loop."""
        # Centre the window on screen
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

        self.root.mainloop()
