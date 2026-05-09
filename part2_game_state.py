"""
HIT137 Assignment 3 - Part 2: Game State Management

Written by: Tufayel Ahmed - S397780
Responsibility: GameState class

Handles all game logic:
  - click validation against difference regions
  - score tracking (cumulative across images)
  - mistake counting and lockout (max 3 per image)
  - found/unfound region tracking
  - reveal logic
"""

"""


class GameState:
    """
    Manages the state of the spot-the-difference game.

    Encapsulates all game rules so that the GUI layer only needs to call
    high-level methods and read simple properties.

    Attributes:
        total_score  (int): Cumulative count of differences found across all images.
        mistakes     (int): Number of wrong clicks for the current image.
        is_locked    (bool): True when the player has reached MAX_MISTAKES.
        is_complete  (bool): True when all 5 differences for the current image are found.
    """

    MAX_MISTAKES = 3
    TOTAL_DIFFERENCES = 5
    CLICK_TOLERANCE = 30  # pixels – proximity radius around region centre

    def __init__(self):
        """
        Constructor: initialise a fresh game with zeroed counters.
        """
        self.total_score: int = 0
        self.mistakes: int = 0
        self.is_locked: bool = False
        self.is_complete: bool = False

        # Internal list mirroring ImageProcessor.difference_regions,
        # extended with a 'found' flag.
        self._regions: list = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def new_image(self, difference_regions: list):
        """
        Reset per-image state for a freshly loaded image.

        Called by the GUI whenever a new image is loaded.
        Preserves total_score across images.

        Args:
            difference_regions (list): List of region dicts from ImageProcessor,
                each with keys 'x', 'y', 'w', 'h', 'type'.
        """
        self.mistakes = 0
        self.is_locked = False
        self.is_complete = False

        # Deep-copy regions and add 'found' flag
        self._regions = [
            {**region, "found": False} for region in difference_regions
        ]

    def process_click(self, click_x: int, click_y: int) -> dict:
        """
        Validate a player's click against known difference regions.

        Args:
            click_x (int): X coordinate of the click on the modified image.
            click_y (int): Y coordinate of the click on the modified image.

        Returns:
            dict with keys:
                'hit'     (bool)  – True if an unfound difference was clicked.
                'mistake' (bool)  – True if this click counted as a mistake.
                'locked'  (bool)  – True if max mistakes now reached.
                'complete'(bool)  – True if all differences now found.
                'region'  (dict|None) – The matched region, or None.
        """
        if self.is_locked or self.is_complete:
            return {
                "hit": False,
                "mistake": False,
                "locked": self.is_locked,
                "complete": self.is_complete,
                "region": None,
            }

        matched_region = self._find_matching_region(click_x, click_y)

        if matched_region is not None:
            matched_region["found"] = True
            self.total_score += 1
            self.is_complete = self._check_all_found()
            return {
                "hit": True,
                "mistake": False,
                "locked": False,
                "complete": self.is_complete,
                "region": matched_region,
            }
        else:
            self.mistakes += 1
            if self.mistakes >= self.MAX_MISTAKES:
                self.is_locked = True
            return {
                "hit": False,
                "mistake": True,
                "locked": self.is_locked,
                "complete": False,
                "region": None,
            }

    def reveal_all(self) -> list:
        """
        Mark all unfound differences as revealed (for the Reveal button).

        Returns:
            list: The regions that were NOT yet found (now marked found).
        """
        unrevealed = [r for r in self._regions if not r["found"]]
        for region in unrevealed:
            region["found"] = True
            region["revealed"] = True  # extra flag so GUI can colour them blue
        self.is_locked = True  # prevent further clicks after reveal
        return unrevealed

    def get_remaining(self) -> int:
        """Return the number of differences not yet found in the current image."""
        return sum(1 for r in self._regions if not r["found"])

    def get_found_regions(self) -> list:
        """Return all regions the player has successfully found (not revealed)."""
        return [r for r in self._regions if r.get("found") and not r.get("revealed")]

    def get_revealed_regions(self) -> list:
        """Return regions that were revealed via the Reveal button (blue circles)."""
        return [r for r in self._regions if r.get("revealed")]

    def get_all_regions(self) -> list:
        """Return the full list of regions (with found/revealed flags)."""
        return self._regions

    def get_status_message(self) -> str:
        """
        Return a human-readable status string for the current game state.

        Returns:
            str: Status text to display in the GUI.
        """
        if self.is_complete:
            return "🎉 All differences found! Load a new image to continue."
        if self.is_locked:
            remaining = self.get_remaining()
            return (
                f"❌ Too many mistakes! {remaining} difference(s) not found. "
                "Load a new image to restart."
            )
        return (
            f"Remaining: {self.get_remaining()}  |  "
            f"Mistakes: {self.mistakes}/{self.MAX_MISTAKES}  |  "
            f"Total Score: {self.total_score}"
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _find_matching_region(self, cx: int, cy: int):
        """
        Find an unfound region whose centre is within CLICK_TOLERANCE of (cx, cy).

        Args:
            cx (int): Click x.
            cy (int): Click y.

        Returns:
            dict | None: The matched region dict, or None.
        """
        for region in self._regions:
            if region["found"]:
                continue

            # Region centre
            rx = region["x"] + region["w"] // 2
            ry = region["y"] + region["h"] // 2

            distance = ((cx - rx) ** 2 + (cy - ry) ** 2) ** 0.5
            if distance <= self.CLICK_TOLERANCE:
                return region

            # Also accept click inside the bounding box itself
            if (
                region["x"] <= cx <= region["x"] + region["w"]
                and region["y"] <= cy <= region["y"] + region["h"]
            ):
                return region

        return None

    def _check_all_found(self) -> bool:
        """Return True if every region has been found."""
        return all(r["found"] for r in self._regions)
    

