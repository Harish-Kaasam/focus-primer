# Focus Primer Architecture

Focus Primer uses a lightweight, local-first hybrid architecture pairing a local Python runner with a modern HTML/CSS/JS frontend environment via **pywebview**.

## System Overview

```
 ┌──────────────────────┐               ┌───────────────────────┐
 │                      │  pywebview    │                       │
 │    Python Backend    ├──────────────>│    HTML/CSS/JS UI     │
 │    (main.py)         │   Bridge      │    (index.html)       │
 │                      │<──────────────┤                       │
 └──────────┬───────────┘               └───────────────────────┘
            │
            ├──────────────> [focus_stats.json]
            │
            └──────────────> [Chime WAV Speaker]
```

### Components

1. **Python Backend (`main.py`)**:
   - Manages the parent operating system window frame configurations.
   - Generates and writes sound buffers using pure standard library elements.
   - Exposes a `FocusAPI` object to the JS environment for statistics persistence storage.

2. **Frontend UI (`index.html`)**:
   - Handles the entire presentation layer using inline standard web assets.
   - Runs UI layout, state flow routers, visual concentric SVG shapes, and scaling loops in JS.

3. **Bridge API**:
   - Communicates asynchronously via window injection hooks (`pywebview.api`).
