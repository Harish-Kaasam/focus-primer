# Focus Primer

> **Prepare · Breathe · Focus**

[![Release](https://img.shields.io/github/v/release/your-username/focus-primer?color=4A90E2&label=release)](https://github.com/your-username/focus-primer/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/your-username/focus-primer)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](file:///LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Focus Primer is a premium, distraction-free desktop focus companion app designed to prepare your mind for cognitive tasks using science-backed visual fixation and breathing exercises.

## The Science

Focus Primer divides prep into distinct phases:
1. **Gaze Fixation**: Anchoring your visual field on a single point triggers a focus reflex in the brain, narrowing your attention window.
2. **Ujjayi Breathing**: Controlled breathing cycles activate your parasympathetic nervous system, lowering heart rate and raising focus confidence.
3. **Deep Work block**: A dedicated focus timer for you to execute your tasks.

---

## Screen Highlights

| 01. Session Setup | 02. Fixation Mode |
| :---: | :---: |
| ![Setup](screenshots/01-session-setup.png) | ![Fixation](screenshots/02-fixation.png) |
| **03. Breathing Phase** | **04. Focus Session** |
| ![Breathing](screenshots/03-breathing.png) | ![Focus](screenshots/04-focus.png) |

---

## Features

- **Gaze Fixation Guide**: Concentric rotating paths with custom target focus points.
- **Ujjayi Breathing Visuals**: Pulsing teal indicators synced to custom inhale/exhale cycles.
- **Clockwise SVG Timer**: Clean countdown circle.
- **Daily Streak Metrics**: Tracks sessions and total focused hours.
- **Dark Luxury Styling**: Translucent panels with background mountain outlines.

---

## Installation & Setup

Download the pre-compiled installer from our [Releases](https://github.com/your-username/focus-primer/releases) page.

Alternatively, run from source:
```bash
# Clone the repository
git clone https://github.com/your-username/focus-primer.git
cd focus-primer

# Install requirements
pip install pywebview pyinstaller

# Run
python src/main.py
```

## Tech Stack

| Technology | Usage |
| :--- | :--- |
| **Python 3** | App wrapper, statistics logic, wave sound generators |
| **PyWebview** | HTML display frame |
| **HTML/CSS/JS** | Single-page UI layout |
| **PyInstaller** | Executable compiler |

## Architecture & Animations
Focus Primer handles background stats via a local JSON file (`focus_stats.json`) and communications using Pywebview's asynchronous API bridges.
Animations use CSS transforms (300ms–800ms) for smooth visual flows.

- [Detailed Architecture Plan](docs/ARCHITECTURE.md)
- [Design Token System Specs](docs/DESIGN_SYSTEM.md)
- [Installation Detailed Steps](docs/INSTALLATION.md)
- [User Walkthrough Guide](docs/USER_GUIDE.md)

---

## License

This project is licensed under the [MIT License](LICENSE).
