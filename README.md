
A desktop game where you find 5 hidden differences between two side-by-side images.  
Built with **Python**, **OpenCV**, and **Tkinter**.

<img width="1246" height="698" alt="2026-05-11_17-57-07" src="https://github.com/user-attachments/assets/e1ee511f-6f1f-41b7-8f2c-f38d3fbe6621" />


---

## 👥 Group Information

| | |
|---|---|
| **Group Name** | SYDN 05 |
| **Unit** | HIT137 |
| **Assignment** | Group Assignment 3  |

| Name | Student ID |
|------|-----------|
| Ashfaq Afzal Chowdhury | S399270 |
| Mahinur Rahman | S398451 |
| Tufayel Ahmed | S397780 |
| Ahnaf Hasnain Nahiun | S400103 |

---

## 📋 Table of Contents

- [Group Information](#-group-information)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [How to Run](#how-to-run)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Requirements

| Tool | Version |
|------|---------|
| Python | 3.10 or newer (3.13 recommended) |
| opencv-python-headless | latest |
| Pillow | latest |
| Tkinter | built-in with Python |

---

## Installation

### Windows

**Step 1 — Install Python**

1. Go to https://www.python.org/downloads/
2. Download the latest **Python 3.13** Windows installer
3. Run the installer — ✅ **check "Add Python to PATH"** before clicking Install

**Step 2 — Open Command Prompt and install dependencies**

```bash
pip install opencv-python-headless Pillow
```

**Step 3 — Done!** Jump to [How to Run](#how-to-run).

---

### macOS

> ⚠️ **Do NOT use the built-in system Python** (`/usr/bin/python3`).  
> It is outdated and will cause errors. Use the official python.org installer instead.

**Step 1 — Install Python from python.org**

1. Go to https://www.python.org/downloads/macos/
2. Download the latest **Python 3.13** macOS `.pkg` installer
3. Open and install it (this also installs Tkinter automatically)

**Step 2 — Open Terminal and install dependencies**

```bash
python3.13 -m pip install opencv-python-headless Pillow
```

**Step 3 — Done!** Jump to [How to Run](#how-to-run).

---

### Linux

**Step 1 — Install Python and Tkinter**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Step 2 — Install dependencies**

```bash
pip3 install opencv-python-headless Pillow
```

**Step 3 — Done!** Jump to [How to Run](#how-to-run).

---

## How to Run

### Step 1 — Make sure all files are in the same folder

```
your-folder/
├── main.py
├── part1_image_processor.py
├── part2_game_state.py
├── part3_canvas_renderer.py
└── part4_game_controller.py
```

### Step 2 — Open a terminal / command prompt in that folder

**Windows:**
- Open File Explorer → navigate to the folder
- Click the address bar → type `cmd` → press Enter

**macOS/Linux:**
- Open Terminal and type `cd` followed by the folder path, e.g.:
```bash
cd "/Users/yourname/Desktop/assignment 3/files"
```

### Step 3 — Run the program

**Windows:**
```bash
python main.py
```

**macOS (python.org install):**
```bash
python3.13 main.py
```

**Linux:**
```bash
python3 main.py
```

A window will open and the game is ready to play! 🎉

---

## How to Play

### 1. Load an Image
Click the **📂 Load Image** button in the top-left toolbar.  
Choose any image file from your computer in `.jpg`, `.jpeg`, `.png`, or `.bmp` format.

```
✅ Supported formats: JPG, JPEG, PNG, BMP
```

### 2. Two Images Appear Side by Side

| Left Image | Right Image |
|-----------|------------|
| **Original** — for reference only | **Modified** — click here to play |

The modified image has **5 hidden differences** introduced automatically by the program.

### 3. Find the Differences
- Click anywhere on the **right (Modified)** image where you think a difference is
- If correct → a **🔴 red circle** appears on both images marking the difference
- If wrong → it counts as a **mistake**

### 4. Track Your Progress
The status bar at the bottom shows:
```
Remaining: 3  |  Mistakes: 1/3  |  Total Score: 2
```

| Indicator | Meaning |
|-----------|---------|
| **Remaining** | How many differences are still unfound |
| **Mistakes** | Wrong clicks for the current image (max 3) |
| **Total Score** | Cumulative differences found across all images |

### 5. Load Another Image
Once you finish (or run out of mistakes), load a new image to keep playing.  
Your **Total Score carries over** between images.

---

## Game Rules

```
🎯  Find all 5 differences in the Modified image
🖱️  Click on the Modified image (right side) only
🔴  Red circle = correctly found difference
🔵  Blue circle = difference revealed by the Reveal button
❌  Maximum 3 mistakes allowed per image
🏆  Score is cumulative across all images loaded
```

### Mistake System
- Every click that does **not** land near a difference = 1 mistake
- At **3 mistakes** → all clicking is disabled for that image
- A warning message appears telling you how many differences you found
- You can then use **Reveal** or load a new image

### Winning an Image
- Find all **5 differences** → a congratulations pop-up appears 🎉
- Load another image to continue building your score

### Reveal Button
- Click **👁 Reveal Differences** at any time
- All unfound differences are marked with **🔵 blue circles** on both images
- Clicking is disabled after revealing
- Load a new image to continue

---

## Project Structure

| File | Class | Member | Role |
|------|-------|--------|------|
| `main.py` | — | All | Entry point — run this file |
| `part1_image_processor.py` | `ImageProcessor` | Member 1 | OpenCV image loading, scaling, generating 5 differences |
| `part2_game_state.py` | `GameState` | Member 2 | Click validation, scoring, mistakes, lockout, reveal |
| `part3_canvas_renderer.py` | `CanvasRenderer` | Member 3 | Tkinter canvas display, circle drawing, click mapping |
| `part4_game_controller.py` | `GameController` | Member 4 | Main window, toolbar, status bar, dialogs |

### Difference Types (5 alteration methods)

| Type | Effect |
|------|--------|
| Colour Shift | Hue shifted in a region — subtle but findable |
| Blur | Gaussian blur applied to a patch |
| Brightness | Region made brighter or darker |
| Noise | Salt-and-pepper noise added to a patch |
| Invert Patch | Partial colour channel inversion |

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'cv2'`
```bash
pip install opencv-python-headless
# or on macOS:
python3.13 -m pip install opencv-python-headless
```

### `ModuleNotFoundError: No module named '_tkinter'`

**macOS:** Install Python from https://www.python.org/downloads/macos/ (includes Tkinter)

**Linux:**
```bash
sudo apt install python3-tk
```

**Windows:** Reinstall Python from python.org and ensure "tcl/tk" option is checked during install

### `ModuleNotFoundError: No module named 'PIL'`
```bash
pip install Pillow
```

### `macOS 26 required` or `libexpat` error
You are using the wrong Python. Use the python.org installer:
1. Download from https://www.python.org/downloads/macos/
2. Install Python 3.13
3. Run with `python3.13 main.py`

### Window doesn't open / crashes immediately
- Make sure **all 5 Python files** are in the **same folder**
- Make sure you are running `main.py` and not one of the part files
- Check that both `opencv-python-headless` and `Pillow` are installed

### Images look distorted
The program automatically scales images to fit the window while preserving aspect ratio. Very small images (under 100×100px) may look stretched — use larger photos for best results.

---

## Tips for Best Experience

- Use **clear, colourful photos** — differences are easier to spot and more fun
- Differences are **subtle by design** — inspect carefully before clicking!
- You can load the **same image multiple times** — differences are randomised each load
- Build your **Total Score** by playing through multiple images in one session

---

*HIT137 — Group Assignment 3 | Group SYDN 05 | Charles Darwin University*
