"""
Main Entry Point

# Group Name: SYDN 05 | HIT 137 Software Now | Assignment 3: Spot-the-Difference Game
==============================================================================
# Group Members:
# Ashfaq Afzal Chowdhury - S399270
# Mahinur Rahman - S398451
# Tufayel Ahmed - S397780
# Ahnaf Hasnain Nahiun - S400103

=======================================
Run this file to launch the Spot-the-Difference application.

    python main.py

Dependencies
------------
    pip install opencv-python Pillow

File / Class structure
----------------------
    main.py                   ← this file (entry point)
    part1_image_processor.py  ← ImageProcessor  (Member 1)
    part2_game_state.py       ← GameState        (Member 2)
    part3_canvas_renderer.py  ← CanvasRenderer   (Member 3)
    part4_game_controller.py  ← GameController   (Member 4)

OOP design summary
------------------
    Class              Inherits    Key responsibilities
    ────────────────── ─────────── ──────────────────────────────────────────
    ImageProcessor     object      OpenCV load, scale, generate 5 differences
    GameState          object      Click validation, scoring, mistakes, reveal
    CanvasRenderer     object      Tkinter canvas rendering, click events
    GameController     object      GUI layout, event wiring, dialog management

    Encapsulation  – internal state held in private (_-prefixed) attributes
    Inheritance    – each class inherits from object (Python default)
    Polymorphism   – alteration types dispatched via string keys (_apply_alteration)
    Class interaction – GameController composes all three other classes
"""

from part4_game_controller import GameController


def main():
    """Application entry point."""
    app = GameController()
    app.run()


if __name__ == "__main__":
    main()
