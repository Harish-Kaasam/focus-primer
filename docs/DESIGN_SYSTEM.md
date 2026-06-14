# Design System

A documentation of colors, typography scales, layout, and visual components.

## Colors

| Variable | Value | Description |
| :--- | :--- | :--- |
| `--bg-primary` | `#020B18` | Deep midnight main background |
| `--bg-secondary`| `#081223` | Gradient mid-level backdrop |
| `--bg-elevated` | `#0E1D35` | Glass container fills |
| `--primary-blue`| `#4A90E2` | Interactive visual highlights |
| `--breathing-teal`| `#5FD1A5`| Breathing guide orb color |
| `--warm-accent` | `#FFB86B` | Daily streak fire indicator |
| `--danger`      | `#FF6B6B` | Terminate session actions |

## Typography

- **Font Family**: Segoe UI Variable, Inter, sans-serif
- **H1 Display**: `clamp(40px, 5vw, 56px)` bold
- **Title (Screen Headers)**: `24px` uppercase, letter-spacing `2px`, color Text Secondary
- **Active Countdown Timer**: `clamp(64px, 9vw, 96px)` bold
- **Body Text**: `18px`, color Text Secondary
- **Captions**: `14px`, color Text Muted

## UI Elements

- **Glass Cards**: Backdrop filter blur `16px`, background `rgba(255,255,255,0.06)`, border `1px solid rgba(255,255,255,0.12)`, radius `16px`.
- **Begin Button**: Blue gradient pill track, padding `16px`, hover `Primary Hover` (#5DA2F5).
- **Breathing Orb**: Scaled smoothly from `0.85` (Exhale) to `1.0` (Inhale) centered inside wave overlays.
