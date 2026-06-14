"""
Focus Primer  ·  Premium Edition
==================================
A calm, premium desktop focus companion.
Inspired by Headspace · Arc Browser · Apple Fitness

Phases  :  Fixate  →  Ujjayi Breath  →  Focus Timer
Design  :  Deep midnight · Glass surfaces · Large typography · Fluid 60 fps
"""

import tkinter as tk
import math
import struct
import wave
import os
import tempfile
import threading

# ─────────────────────────────────────────────────────────────────────────────
# PALETTE  (user-specified)
# ─────────────────────────────────────────────────────────────────────────────
BG       = "#020B18"   # deep midnight
SURFACE  = "#0E1D35"   # glass surface
SURF2    = "#142540"   # lighter surface
SURF3    = "#1D3050"   # chip hover / selected dim
PRIMARY  = "#4A90E2"   # vivid blue
ACCENT   = "#8CC8FF"   # bright accent
TEXT     = "#F5FAFF"   # near-white
TEXT2    = "#7A9FCC"   # muted blue
TEXT3    = "#2D4A6A"   # very muted
SUCCESS  = "#5FD1A5"   # teal green
DANGER   = "#FF6B6B"   # red
WARN     = "#FFB86B"   # amber

# ─────────────────────────────────────────────────────────────────────────────
# AUDIO  — pure-Python WAV, no external deps
# ─────────────────────────────────────────────────────────────────────────────

def _make_chime_wav() -> str:
    sr, dur, freq = 44100, 1.8, 432.0
    n      = int(sr * dur)
    samps  = []
    for i in range(n):
        t   = i / sr
        env = math.exp(-2.2 * t)
        s   = (env * math.sin(2 * math.pi * freq * t)
             + env * 0.40 * math.sin(4 * math.pi * freq * t)
             + env * 0.12 * math.sin(6 * math.pi * freq * t))
        samps.append(struct.pack("<h", max(-32768, min(32767, int(s * 0.42 * 32767)))))
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(b"".join(samps))
    return tmp.name


def play_chime(path: str):
    try:
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except ImportError:
        threading.Thread(
            target=lambda: os.system(f'aplay -q "{path}" 2>/dev/null'),
            daemon=True,
        ).start()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def lerp(c1: str, c2: str, t: float) -> str:
    """Linear colour interpolation between two hex colours."""
    t  = max(0.0, min(1.0, t))
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1 + (r2 - r1) * t),
        int(g1 + (g2 - g1) * t),
        int(b1 + (b2 - b1) * t),
    )


def mmss(s: int) -> str:
    m, s = divmod(max(0, s), 60)
    return f"{m:02d}:{s:02d}"


def rrect(cv, x0, y0, x1, y1, r: int = 14, **kw):
    """Smoothed rounded rectangle drawn as a polygon on a Canvas."""
    pts = [
        x0 + r, y0,  x1 - r, y0,
        x1, y0,       x1, y0 + r,
        x1, y1 - r,  x1, y1,
        x1 - r, y1,  x0 + r, y1,
        x0, y1,       x0, y1 - r,
        x0, y0 + r,  x0, y0,
    ]
    return cv.create_polygon(pts, smooth=True, **kw)


def _ghost_btn(parent, text: str, cmd, danger: bool = False) -> tk.Button:
    """Minimal ghost/text-only button for secondary actions."""
    fg  = DANGER if danger else TEXT2
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=BG, fg=fg,
        activebackground=SURF2, activeforeground=fg,
        font=("Segoe UI", 11), relief="flat", bd=0,
        padx=18, pady=8, cursor="hand2",
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=SURF2))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG))
    return btn


def _slabel(parent, text: str) -> tk.Label:
    """Small spaced section heading label."""
    return tk.Label(parent, text=text, bg=parent["bg"],
                    fg=TEXT3, font=("Segoe UI", 8, "bold"))


# ─────────────────────────────────────────────────────────────────────────────
# CHIP GROUP  — premium preset selector
# ─────────────────────────────────────────────────────────────────────────────

class ChipGroup(tk.Frame):
    """
    A horizontal row of pill-shaped selectable option chips.
    Selected chip is filled PRIMARY; unselected chips are SURF3 with dim border.
    """
    H   = 34     # chip height
    GAP = 7      # gap between chips

    def __init__(self, parent, options: list, default_idx: int = 0,
                 on_change=None, bg: str = None):
        bg = bg or parent["bg"]
        super().__init__(parent, bg=bg)
        self._opts = options    # [(label, value), ...]
        self._sel  = default_idx
        self._cb   = on_change
        self._cvs  = []

        for i, (lbl, _val) in enumerate(options):
            w = max(56, len(lbl) * 10 + 24)
            cv = tk.Canvas(self, bg=bg, highlightthickness=0,
                           width=w, height=self.H, cursor="hand2")
            cv.pack(side="left", padx=(0 if i == 0 else self.GAP, 0))
            self._cvs.append((cv, lbl, w))
            cv.bind("<Button-1>", lambda e, idx=i: self._pick(idx))
            cv.bind("<Configure>", lambda e, idx=i: self._draw(idx))

        self._redraw()

    def _pick(self, idx: int):
        self._sel = idx
        self._redraw()
        if self._cb:
            self._cb(self._opts[idx][1])

    def _redraw(self):
        for i in range(len(self._cvs)):
            self._draw(i)

    def _draw(self, i: int):
        cv, lbl, w = self._cvs[i]
        h   = self.H
        sel = (i == self._sel)
        r   = h // 2          # full pill radius
        cv.delete("all")
        bg_col = PRIMARY if sel else SURF3
        fg_col = TEXT    if sel else TEXT2
        # pill body
        rrect(cv, 1, 1, w - 1, h - 1, r=r, fill=bg_col, outline="")
        # subtle border on unselected
        if not sel:
            rrect(cv, 1, 1, w - 1, h - 1, r=r, fill="", outline=SURF2, width=1)
        cv.create_text(w // 2, h // 2, text=lbl,
                       fill=fg_col, font=("Segoe UI", 10, "bold"))

    def value(self):
        return self._opts[self._sel][1]


# ─────────────────────────────────────────────────────────────────────────────
# ANIMATED TOGGLE SWITCH
# ─────────────────────────────────────────────────────────────────────────────

class Toggle(tk.Canvas):
    """Smooth animated pill toggle switch."""
    W, H = 52, 28

    def __init__(self, parent, value: bool = True, on_change=None, bg: str = None):
        bg = bg or parent["bg"]
        super().__init__(parent, bg=bg, width=self.W, height=self.H,
                         highlightthickness=0, cursor="hand2")
        self._val    = value
        self._cb     = on_change
        self._anim_t = 1.0 if value else 0.0
        self._draw()
        self.bind("<Button-1>", self._toggle)

    def _toggle(self, _e=None):
        self._val = not self._val
        self._animate()
        if self._cb:
            self._cb(self._val)

    def _animate(self):
        target = 1.0 if self._val else 0.0
        diff   = target - self._anim_t
        if abs(diff) < 0.08:
            self._anim_t = target
            self._draw()
        else:
            self._anim_t += 0.12 if diff > 0 else -0.12
            self._draw()
            self.after(14, self._animate)

    def _draw(self):
        self.delete("all")
        t    = self._anim_t
        w, h = self.W, self.H
        r    = h // 2
        bg   = lerp(SURF3, PRIMARY, t)
        rrect(self, 0, 0, w, h, r=r, fill=bg, outline="")
        # thumb position slides from left to right
        tx = int(r + t * (w - 2 * r))
        self.create_oval(tx - r + 3, 3, tx + r - 3, h - 3,
                         fill=TEXT, outline="")

    def value(self) -> bool:
        return self._val


# ─────────────────────────────────────────────────────────────────────────────
# START SCREEN  — premium onboarding
# ─────────────────────────────────────────────────────────────────────────────

class StartScreen(tk.Frame):
    _FIXATE_OPTS  = [("20s", 20),  ("45s", 45),  ("1.5m", 90), ("3m", 180)]
    _FOCUS_OPTS   = [("15m", 900), ("25m", 1500), ("45m", 2700), ("90m", 5400)]
    _BREATH_OPTS  = [("4",  4),   ("6",  6),    ("8",  8),   ("12", 12)]
    _BSEC_OPTS    = [("3s", 3),   ("4s", 4),    ("5s", 5),   ("6s", 6)]

    def __init__(self, master, on_start):
        super().__init__(master, bg=BG)
        self._on_start = on_start
        self._t        = 0.0
        self._alive    = True
        self._btn_hover = False
        self._build()
        self._orb_tick()

    def _build(self):
        self.columnconfigure(0, weight=1)

        # ── ambient orb (drawn behind title via canvas) ───────────────────────
        self._orb_cv = tk.Canvas(self, bg=BG, highlightthickness=0, height=160)
        self._orb_cv.grid(row=0, column=0, sticky="ew")

        # ── title block ───────────────────────────────────────────────────────
        tk.Label(self, text="Focus Primer", bg=BG, fg=TEXT,
                 font=("Segoe UI", 38, "bold")).grid(row=1, column=0, pady=(0, 4))
        tk.Label(self, text="Calm your mind.  Begin deep work.",
                 bg=BG, fg=TEXT2,
                 font=("Segoe UI", 13, "italic")).grid(row=2, column=0, pady=(0, 18))

        # ── glass settings card ───────────────────────────────────────────────
        card = tk.Frame(self, bg=SURFACE, padx=28, pady=22,
                        highlightbackground=SURF2, highlightthickness=1)
        card.grid(row=3, column=0, sticky="ew", padx=40)
        card.columnconfigure(0, weight=1)

        # Fixate duration
        _slabel(card, "FIXATE DURATION").pack(anchor="w", pady=(0, 7))
        self._fixate_chips = ChipGroup(card, self._FIXATE_OPTS, default_idx=1, bg=SURFACE)
        self._fixate_chips.pack(anchor="w", pady=(0, 16))

        # Focus duration
        _slabel(card, "FOCUS DURATION").pack(anchor="w", pady=(0, 7))
        self._focus_chips = ChipGroup(card, self._FOCUS_OPTS, default_idx=1, bg=SURFACE)
        self._focus_chips.pack(anchor="w", pady=(0, 18))

        # Divider
        tk.Frame(card, bg=SURF2, height=1).pack(fill="x", pady=(0, 16))

        # Ujjayi toggle row
        tog_row = tk.Frame(card, bg=SURFACE)
        tog_row.pack(fill="x", pady=(0, 4))
        self._breath_toggle = Toggle(tog_row, value=True,
                                     on_change=self._breath_changed, bg=SURFACE)
        self._breath_toggle.pack(side="left")
        tk.Label(tog_row, text="Ujjayi Breathing",
                 bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 12)).pack(side="left", padx=(12, 0))

        # Breath sub-settings (collapsible)
        self._breath_sub = tk.Frame(card, bg=SURFACE)
        self._breath_sub.pack(fill="x", pady=(10, 0))

        _slabel(self._breath_sub, "CYCLES").pack(anchor="w", pady=(0, 6))
        self._breath_chips = ChipGroup(self._breath_sub, self._BREATH_OPTS,
                                       default_idx=1, bg=SURFACE)
        self._breath_chips.pack(anchor="w", pady=(0, 12))

        _slabel(self._breath_sub, "PACE").pack(anchor="w", pady=(0, 6))
        self._bsec_chips = ChipGroup(self._breath_sub, self._BSEC_OPTS,
                                     default_idx=1, bg=SURFACE)
        self._bsec_chips.pack(anchor="w")

        # ── begin button (canvas-drawn for glow effect) ───────────────────────
        self._btn_cv = tk.Canvas(self, bg=BG, highlightthickness=0, height=76)
        self._btn_cv.grid(row=4, column=0, sticky="ew", padx=40, pady=(20, 4))
        self._btn_cv.bind("<Configure>", lambda e: self._draw_btn())
        self._btn_cv.bind("<Button-1>",  self._start)
        self._btn_cv.bind("<Enter>",
                          lambda e: (setattr(self, "_btn_hover", True),  self._draw_btn()))
        self._btn_cv.bind("<Leave>",
                          lambda e: (setattr(self, "_btn_hover", False), self._draw_btn()))

        tk.Label(self, text="Your session begins immediately",
                 bg=BG, fg=TEXT3,
                 font=("Segoe UI", 10)).grid(row=5, column=0, pady=(0, 22))

    # ── breath toggle ──────────────────────────────────────────────────────────

    def _breath_changed(self, val: bool):
        if val:
            self._breath_sub.pack(fill="x", pady=(10, 0))
        else:
            self._breath_sub.pack_forget()

    # ── begin button ──────────────────────────────────────────────────────────

    def _draw_btn(self, hover: bool = None):
        if hover is not None:
            self._btn_hover = hover
        cv  = self._btn_cv
        w   = cv.winfo_width()  or 460
        h   = cv.winfo_height() or 76
        by0 = 10
        by1 = h - 10
        bh  = by1 - by0
        col = lerp(PRIMARY, ACCENT, 0.28 if self._btn_hover else 0.0)
        cv.delete("all")
        # multi-layer glow
        for i in range(5, 0, -1):
            g   = i * 7
            gc  = lerp(BG, col, 0.06 * (6 - i) / 5)
            rrect(cv, -g, by0 - g, w + g, by1 + g,
                  r=bh // 2 + g, fill=gc, outline="")
        # button pill
        rrect(cv, 0, by0, w, by1, r=bh // 2, fill=col, outline="")
        cv.create_text(w // 2, (by0 + by1) // 2, text="Begin Session",
                       fill=TEXT, font=("Segoe UI", 15, "bold"))

    # ── ambient orb animation ─────────────────────────────────────────────────

    def _orb_tick(self):
        if not self._alive:
            return
        self._t += 0.020
        cv = self._orb_cv
        w  = cv.winfo_width()  or 540
        h  = cv.winfo_height() or 160
        cx, cy = w // 2, h // 2
        cv.delete("all")

        base_r = 48
        pulse  = math.sin(self._t) * 0.10 + 1.0
        r      = base_r * pulse

        # outer ambient haze rings
        for i in range(4, 0, -1):
            ratio = i / 4
            rr    = r * (1.2 + ratio * 2.0)
            col   = lerp(BG, PRIMARY, ratio * 0.12)
            stip  = "gray12" if ratio > 0.6 else ("gray25" if ratio > 0.3 else "gray50")
            cv.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                           fill=col, outline="", stipple=stip)

        # main glow layers (14)
        for i in range(14, 0, -1):
            ratio  = i / 14
            lr     = r * (0.3 + 2.4 * ratio)
            if ratio < 0.25:
                col = lerp("#cce8ff", PRIMARY, ratio / 0.25)
            else:
                col = lerp(PRIMARY, BG, (ratio - 0.25) / 0.75)
            stip = ""
            if ratio > 0.75:  stip = "gray12"
            elif ratio > 0.55: stip = "gray25"
            elif ratio > 0.40: stip = "gray50"
            cv.create_oval(cx - lr, cy - lr, cx + lr, cy + lr,
                           fill=col, outline="", stipple=stip)

        # bright centre
        cr = r * 0.38
        cv.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                       fill="#d8f0ff", outline="")

        # 3 small orbiting particles
        for i, (rf, sp, ph) in enumerate([(1.7, 0.28, 0.0),
                                           (2.3, 0.17, 2.09),
                                           (2.0, 0.44, 4.19)]):
            ang = self._t * sp + ph
            orb = r * rf
            px  = cx + math.cos(ang) * orb
            py  = cy + math.sin(ang) * orb
            cv.create_oval(px - 2, py - 2, px + 2, py + 2,
                           fill=ACCENT, outline="")

        self.after(33, self._orb_tick)

    # ── start ─────────────────────────────────────────────────────────────────

    def _start(self, _e=None):
        self._alive = False
        self._on_start(
            fixate_s      = self._fixate_chips.value(),
            focus_s       = self._focus_chips.value(),
            breath_on     = self._breath_toggle.value(),
            breath_sec    = self._bsec_chips.value(),
            breath_cycles = self._breath_chips.value(),
        )

    def destroy(self):
        self._alive = False
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────
# FIXATE SCREEN  — immersive concentric-circle focal point
# ─────────────────────────────────────────────────────────────────────────────

class FixateScreen(tk.Frame):
    """
    Five concentric ambient rings + 18-layer central glow orb
    + five orbital particles with motion trails.
    Timer and breathing hints sit at the bottom, out of the way.
    """

    _ORBITS = [
        (2.0, 0.38, 0.00, 3),
        (2.8, 0.22, 2.09, 2),
        (2.4, 0.52, 4.19, 2),
        (3.3, 0.16, 1.05, 2),
        (1.7, 0.64, 3.14, 3),
    ]

    def __init__(self, master, duration_s: int, on_done, on_skip, on_stop):
        super().__init__(master, bg=BG)
        self.duration  = duration_s
        self.remaining = duration_s
        self.on_done   = on_done
        self.on_skip   = on_skip
        self.on_stop   = on_stop
        self._running  = True
        self._t        = 0.0
        self._build()
        self._tick_count()
        self._tick_anim()

    def _build(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # full-bleed canvas
        self.cv = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.cv.grid(row=0, column=0, sticky="nsew")

        # bottom status bar
        bar = tk.Frame(self, bg=BG)
        bar.grid(row=1, column=0, pady=(0, 8))

        self._cd_var = tk.StringVar(value=mmss(self.duration))
        tk.Label(bar, textvariable=self._cd_var,
                 bg=BG, fg=TEXT3, font=("Segoe UI", 14)).pack(side="left", padx=16)

        self._hint_var = tk.StringVar(value="settle your gaze …")
        tk.Label(bar, textvariable=self._hint_var,
                 bg=BG, fg=TEXT3,
                 font=("Segoe UI", 11, "italic")).pack(side="left", padx=8)

        # minimal button row
        bf = tk.Frame(self, bg=BG)
        bf.grid(row=2, column=0, pady=(0, 22))
        _ghost_btn(bf, "Skip Phase →", self._skip).pack(side="left", padx=10)
        _ghost_btn(bf, "Stop",         self._stop, danger=True).pack(side="left", padx=10)

    # ── drawing ───────────────────────────────────────────────────────────────

    def _draw(self):
        cv = self.cv
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 4 or h < 4:
            return
        cx, cy = w // 2, h // 2

        base_r = min(w, h) * 0.13
        pulse  = math.sin(self._t * 0.65) * 0.10 + 1.0
        r      = base_r * pulse

        # ── 5 large concentric ambient rings ─────────────────────────────────
        for i in range(5, 0, -1):
            rr  = base_r * (2.0 + i * 1.1)
            col = lerp(BG, SURF2, (6 - i) * 0.03)
            cv.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                           fill="", outline=col, width=1)

        # ── 18-layer radial glow ──────────────────────────────────────────────
        for i in range(18, 0, -1):
            ratio  = i / 18
            layer_r = r * (0.26 + 3.4 * ratio)
            if ratio < 0.22:
                col = lerp("#d8f2ff", PRIMARY, ratio / 0.22)
            else:
                col = lerp(PRIMARY, BG, (ratio - 0.22) / 0.78)
            stip = ""
            if ratio > 0.80:  stip = "gray12"
            elif ratio > 0.60: stip = "gray25"
            elif ratio > 0.44: stip = "gray50"
            cv.create_oval(cx - layer_r, cy - layer_r,
                           cx + layer_r, cy + layer_r,
                           fill=col, outline="", stipple=stip)

        # ── orbital particles with 3-step trails ─────────────────────────────
        for (rf, sp, ph, sz) in self._ORBITS:
            orb_r = base_r * rf
            angle = self._t * sp + ph
            for step in range(3, 0, -1):
                ta  = angle - step * 0.19
                tx  = cx + math.cos(ta) * orb_r
                ty  = cy + math.sin(ta) * orb_r
                tc  = lerp(BG, ACCENT, (3 - step) / 3 * 0.22)
                tsz = max(1, sz - 1)
                cv.create_oval(tx - tsz, ty - tsz, tx + tsz, ty + tsz,
                               fill=tc, outline="")
            px = cx + math.cos(angle) * orb_r
            py = cy + math.sin(angle) * orb_r
            cv.create_oval(px - sz, py - sz, px + sz, py + sz,
                           fill=ACCENT, outline="")

        # ── bright centre dot ─────────────────────────────────────────────────
        cr = r * 0.30
        cv.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                       fill="#e4f4ff", outline="")

    # ── breathing hint ────────────────────────────────────────────────────────

    _HINTS    = ["breathe in …", "hold …", "breathe out …", "rest …"]
    _HINT_DUR = [4, 2, 5, 1]

    def _update_hint(self):
        elapsed = self.duration - self.remaining
        cyc     = sum(self._HINT_DUR)
        pos     = elapsed % cyc
        acc     = 0
        for i, d in enumerate(self._HINT_DUR):
            acc += d
            if pos < acc:
                self._hint_var.set(self._HINTS[i])
                break

    # ── ticks ─────────────────────────────────────────────────────────────────

    def _tick_anim(self):
        if not self._running:
            return
        self._t += 1 / 60
        self._draw()
        self.after(16, self._tick_anim)

    def _tick_count(self):
        if not self._running:
            return
        self._cd_var.set(mmss(self.remaining))
        self._update_hint()
        if self.remaining <= 0:
            self._running = False
            self.on_done()
            return
        self.remaining -= 1
        self.after(1000, self._tick_count)

    # ── actions ───────────────────────────────────────────────────────────────

    def _skip(self):
        self._running = False
        self.on_skip()

    def _stop(self):
        self._running = False
        self.on_stop()

    def destroy(self):
        self._running = False
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────
# BREATH SCREEN  — large immersive breathing orb
# ─────────────────────────────────────────────────────────────────────────────

class BreathScreen(tk.Frame):
    """
    Full-canvas breathing orb occupying 60-70% of screen.
    Orb expands on inhale (SUCCESS glow) and contracts on exhale.
    INHALE / EXHALE label + per-second countdown inside the orb.
    Ripple rings spawn at each inhale peak.
    Cycle dots below show progress.
    """

    STEP_MS     = 33
    MIN_R       = 80
    MAX_R       = 175
    RIPPLE_LIFE = 2.5

    def __init__(self, master, breath_sec: int, cycles: int,
                 on_done, on_skip, on_stop):
        super().__init__(master, bg=BG)
        self.breath_sec   = max(1, breath_sec)
        self.total        = cycles
        self.on_done      = on_done
        self.on_skip      = on_skip
        self.on_stop      = on_stop
        self._running     = True
        self._state       = "in"
        self._progress    = 0.0
        self._count       = 0
        self._after_id    = None
        self._ripples     = []   # [start_r, age_secs]
        self._build()
        self._tick()

    def _build(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.cv = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.cv.grid(row=0, column=0, sticky="nsew")

        # cycle progress dots
        self._dots_cv = tk.Canvas(self, bg=BG, highlightthickness=0, height=22)
        self._dots_cv.grid(row=1, column=0, pady=(4, 0))
        self._dots_cv.bind("<Configure>", lambda _e: self._draw_dots())

        bf = tk.Frame(self, bg=BG)
        bf.grid(row=2, column=0, pady=(8, 24))
        _ghost_btn(bf, "Skip Phase →", self._skip).pack(side="left", padx=10)
        _ghost_btn(bf, "Stop",         self._stop, danger=True).pack(side="left", padx=10)

    # ── cycle dots ────────────────────────────────────────────────────────────

    def _draw_dots(self):
        cv = self._dots_cv
        cv.delete("all")
        w  = cv.winfo_width() or 300
        h  = 22
        r  = 5
        gap = 14
        n  = self.total
        total_w = n * 2 * r + (n - 1) * gap
        x0 = (w - total_w) // 2
        for i in range(n):
            x   = x0 + i * (2 * r + gap) + r
            col = SUCCESS if i < self._count else TEXT3
            cv.create_oval(x - r, h // 2 - r, x + r, h // 2 + r,
                           fill=col, outline="")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _centre(self):
        w = self.cv.winfo_width()  or 300
        h = self.cv.winfo_height() or 450
        return w // 2, h // 2

    # ── animation tick ────────────────────────────────────────────────────────

    def _tick(self):
        if not self._running:
            return

        step           = self.STEP_MS / 1000.0
        self._progress += step / self.breath_sec

        if self._progress >= 1.0:
            self._progress = 0.0
            if self._state == "in":
                self._state = "out"
                self._ripples.append([float(self.MAX_R), 0.0])
            else:
                self._state = "in"
                self._count += 1
                self._draw_dots()

        # age and prune ripples
        self._ripples = [
            [sr, age + step]
            for sr, age in self._ripples
            if age + step < self.RIPPLE_LIFE
        ]

        eased = (1 - math.cos(self._progress * math.pi)) / 2

        if self._state == "in":
            r          = self.MIN_R + (self.MAX_R - self.MIN_R) * eased
            label_text = "INHALE"
            brightness = eased
        else:
            r          = self.MAX_R - (self.MAX_R - self.MIN_R) * eased
            label_text = "EXHALE"
            brightness = 1.0 - eased

        # per-second countdown inside orb
        cd = max(1, math.ceil((1.0 - self._progress) * self.breath_sec))

        self._draw_frame(r, label_text, cd, brightness)

        if self._count >= self.total:
            self._running = False
            self.after(600, self.on_done)
            return

        self._after_id = self.after(self.STEP_MS, self._tick)

    def _draw_frame(self, r: float, label: str, cd: int, brightness: float):
        cv = self.cv
        cv.delete("all")
        cx, cy = self._centre()

        # ── ambient haze ──────────────────────────────────────────────────────
        for i in range(3):
            rr   = r * (2.4 - i * 0.35)
            col  = lerp(BG, SUCCESS, (0.05 + i * 0.04) * brightness)
            stip = ("gray12", "gray25", "gray50")[i]
            cv.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                           fill=col, outline="", stipple=stip)

        # ── ripple rings ──────────────────────────────────────────────────────
        for sr, age in self._ripples:
            frac = age / self.RIPPLE_LIFE
            rr   = sr + frac * self.MAX_R * 1.4
            fade = 1.0 - frac
            col  = lerp(BG, SUCCESS, fade * 0.55)
            lw   = max(1, int(3 * (1.0 - frac)))
            cv.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                           fill="", outline=col, width=lw)

        # ── orb glow layers (8) ───────────────────────────────────────────────
        for i in range(8, 0, -1):
            ratio = i / 8
            lr    = r * (0.88 + 0.36 * ratio)
            if ratio < 0.28:
                base = lerp("#d8fff4", SUCCESS, ratio / 0.28)
            else:
                base = lerp(SUCCESS, BG, (ratio - 0.28) / 0.72)
            col  = lerp(BG, base, brightness * 0.65 + 0.35)
            stip = ""
            if ratio > 0.65: stip = "gray25"
            elif ratio > 0.48: stip = "gray50"
            cv.create_oval(cx - lr, cy - lr, cx + lr, cy + lr,
                           fill=col, outline="", stipple=stip)

        # ── orb body ──────────────────────────────────────────────────────────
        fill_col    = lerp(lerp(BG, SUCCESS, 0.12), lerp(BG, SUCCESS, 0.30), brightness)
        outline_col = lerp(lerp(SUCCESS, BG, 0.45), SUCCESS, brightness)
        lw          = 2 + brightness * 3.0
        cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                       fill=fill_col, outline="")
        cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                       fill="", outline=outline_col, width=lw)

        # ── in-orb text ───────────────────────────────────────────────────────
        tcol = lerp(TEXT3, TEXT, brightness * 0.75 + 0.25)
        cv.create_text(cx, cy - 22,
                       text=label, fill=tcol,
                       font=("Segoe UI", 17, "bold"))
        cv.create_text(cx, cy + 22,
                       text=str(cd), fill=tcol,
                       font=("Segoe UI", 42, "bold"))

    # ── actions ───────────────────────────────────────────────────────────────

    def _skip(self):
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self.on_skip()

    def _stop(self):
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self.on_stop()

    def destroy(self):
        self._running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────
# FOCUS SCREEN  — premium circular arc timer with live stats
# ─────────────────────────────────────────────────────────────────────────────

class FocusScreen(tk.Frame):
    """
    Massive circular arc ring counting down.
    Timer text (52px) centred in the ring.
    Three stat chips below: Streak · Today · Sessions.
    """

    ARC_FPS = 30

    def __init__(self, master, duration_s: int, chime_path: str,
                 on_done, on_stop, stats: dict):
        super().__init__(master, bg=BG)
        self.duration   = duration_s
        self.remaining  = duration_s
        self.chime_path = chime_path
        self.on_done    = on_done
        self.on_stop    = on_stop
        self._stats     = stats
        self._running   = True
        self._pulse_t   = 0.0
        self._build()
        self._tick_count()
        self._tick_anim()

    def _build(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # large canvas for arc
        self.cv = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.cv.grid(row=0, column=0, sticky="nsew")

        # ── stat chips row ────────────────────────────────────────────────────
        sf = tk.Frame(self, bg=BG)
        sf.grid(row=1, column=0, pady=(4, 6))

        self._streak_lbl = self._stat_chip(sf, str(self._stats["streak"]),
                                            "Streak", WARN)
        self._streak_lbl.pack(side="left", padx=8)

        self._today_lbl = self._stat_chip(sf,
                                           f"{self._stats['total_s'] // 60}m",
                                           "Today", TEXT2)
        self._today_lbl.pack(side="left", padx=8)

        self._sess_lbl = self._stat_chip(sf, str(self._stats["sessions"]),
                                          "Sessions", TEXT2)
        self._sess_lbl.pack(side="left", padx=8)

        # ── buttons ───────────────────────────────────────────────────────────
        bf = tk.Frame(self, bg=BG)
        bf.grid(row=2, column=0, pady=(6, 26))
        _ghost_btn(bf, "Finish Early", self._finish).pack(side="left", padx=10)
        _ghost_btn(bf, "Stop",         self._stop, danger=True).pack(side="left", padx=10)

    @staticmethod
    def _stat_chip(parent, value: str, label: str, value_color: str) -> tk.Frame:
        box = tk.Frame(parent, bg=SURFACE, padx=18, pady=10,
                       highlightbackground=SURF2, highlightthickness=1)
        tk.Label(box, text=value, bg=SURFACE, fg=value_color,
                 font=("Segoe UI", 18, "bold")).pack()
        tk.Label(box, text=label, bg=SURFACE, fg=TEXT3,
                 font=("Segoe UI", 9)).pack()
        return box

    # ── drawing ───────────────────────────────────────────────────────────────

    def _draw(self):
        cv = self.cv
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 4 or h < 4:
            return
        cx, cy   = w // 2, h // 2
        md       = min(w, h)
        R        = md * 0.36

        progress = 1.0 - (self.remaining / self.duration)

        # ── ambient pulse ─────────────────────────────────────────────────────
        pulse = math.sin(self._pulse_t * 0.38) * 0.5 + 0.5
        pr    = R * (1.16 + 0.08 * pulse)
        pc    = lerp(BG, SURF2, 0.7 * pulse)
        cv.create_oval(cx - pr, cy - pr, cx + pr, cy + pr,
                       fill="", outline=pc, width=1, dash=(2, 12))

        # ── track ring ────────────────────────────────────────────────────────
        cv.create_oval(cx - R, cy - R, cx + R, cy + R,
                       fill="", outline=SURF2, width=10)

        # ── progress arc (clockwise from 12 o'clock) ──────────────────────────
        if progress > 0.0:
            arc_col = lerp(PRIMARY, ACCENT, progress * 0.55)
            cv.create_arc(cx - R, cy - R, cx + R, cy + R,
                          start=90, extent=-360.0 * progress,
                          style=tk.ARC, outline=arc_col, width=10)

        # ── inner decorative ring ─────────────────────────────────────────────
        ri = R * 0.78
        cv.create_oval(cx - ri, cy - ri, cx + ri, cy + ri,
                       fill="", outline=SURF2, width=1, dash=(2, 14))

        # ── timer text ────────────────────────────────────────────────────────
        tcol = lerp(TEXT2, TEXT, 0.5)
        cv.create_text(cx, cy - 18,
                       text=mmss(self.remaining),
                       fill=tcol, font=("Segoe UI", 52, "bold"))
        cv.create_text(cx, cy + 32,
                       text="remaining",
                       fill=TEXT3, font=("Segoe UI", 12))

    # ── ticks ─────────────────────────────────────────────────────────────────

    def _tick_anim(self):
        if not self._running:
            return
        self._pulse_t += 1 / self.ARC_FPS
        self._draw()
        self.after(int(1000 / self.ARC_FPS), self._tick_anim)

    def _tick_count(self):
        if not self._running:
            return
        # accrue focus time for today stat
        self._stats["total_s"] += 1
        total_m = self._stats["total_s"] // 60
        self._today_lbl.winfo_children()[0].config(text=f"{total_m}m")
        if self.remaining <= 0:
            self._running = False
            play_chime(self.chime_path)
            self.after(1500, self.on_done)
            return
        self.remaining -= 1
        self.after(1000, self._tick_count)

    # ── actions ───────────────────────────────────────────────────────────────

    def _finish(self):
        self._running = False
        play_chime(self.chime_path)
        self.after(1500, self.on_done)

    def _stop(self):
        self._running = False
        self.on_stop()

    def destroy(self):
        self._running = False
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────
# DONE SCREEN  — elegant completion celebration
# ─────────────────────────────────────────────────────────────────────────────

class DoneScreen(tk.Frame):

    _ORBS = [
        (0.18, 0.55, 0.80, 26, PRIMARY),
        (0.50, 0.50, 0.48, 36, SURF2),
        (0.82, 0.55, 1.05, 22, SUCCESS),
        (0.35, 0.45, 0.65, 16, ACCENT),
        (0.65, 0.60, 0.92, 18, PRIMARY),
    ]

    def __init__(self, master, on_restart, on_quit, stats: dict):
        super().__init__(master, bg=BG)
        self._t     = 0.0
        self._alive = True
        self._stats = stats
        self._build(on_restart, on_quit)
        self._tick()

    def _build(self, on_restart, on_quit):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        # floating orbs canvas
        self._cv = tk.Canvas(self, bg=BG, highlightthickness=0, height=110)
        self._cv.grid(row=0, column=0, sticky="ew")

        tk.Label(self, text="Well done.", bg=BG, fg=TEXT,
                 font=("Segoe UI", 42, "bold")).grid(row=1, column=0, pady=(0, 8))
        tk.Label(self, text="Your session is complete.",
                 bg=BG, fg=TEXT2,
                 font=("Segoe UI", 15)).grid(row=2, column=0, pady=(0, 30))

        # stats summary chips
        sf = tk.Frame(self, bg=BG)
        sf.grid(row=3, column=0, pady=(0, 36))

        for val, label, col in [
            (str(self._stats["sessions"]), "Sessions Today",  TEXT),
            (f"{self._stats['total_s'] // 60}m", "Focus Time", SUCCESS),
            (str(self._stats["streak"]),  "Session Streak",   WARN),
        ]:
            box = tk.Frame(sf, bg=SURFACE, padx=22, pady=14,
                           highlightbackground=SURF2, highlightthickness=1)
            box.pack(side="left", padx=10)
            tk.Label(box, text=val, bg=SURFACE, fg=col,
                     font=("Segoe UI", 24, "bold")).pack()
            tk.Label(box, text=label, bg=SURFACE, fg=TEXT3,
                     font=("Segoe UI", 9)).pack()

        # buttons
        bf = tk.Frame(self, bg=BG)
        bf.grid(row=4, column=0, pady=(0, 40), sticky="s")

        new_btn = tk.Button(
            bf, text="New Session",
            bg=PRIMARY, fg=TEXT,
            activebackground=ACCENT, activeforeground=TEXT,
            font=("Segoe UI", 13, "bold"), relief="flat", bd=0,
            padx=26, pady=11, cursor="hand2", command=on_restart,
        )
        new_btn.pack(side="left", padx=12)
        new_btn.bind("<Enter>", lambda e: new_btn.config(bg=lerp(PRIMARY, ACCENT, 0.3)))
        new_btn.bind("<Leave>", lambda e: new_btn.config(bg=PRIMARY))

        _ghost_btn(bf, "Quit", on_quit).pack(side="left", padx=12)

    def _tick(self):
        if not self._alive:
            return
        self._t += 0.032
        cv = self._cv
        w  = cv.winfo_width()  or 540
        h  = cv.winfo_height() or 110
        cv.delete("all")
        for i, (fx, fy, spd, rad, col) in enumerate(self._ORBS):
            x = w * fx + math.sin(self._t * spd + i * 1.3) * 16
            y = h * fy + math.cos(self._t * spd * 0.8 + i) * 8
            cv.create_oval(x - rad, y - rad, x + rad, y + rad,
                           fill=col, outline="", stipple="gray50")
        self.after(40, self._tick)

    def destroy(self):
        self._alive = False
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION ROOT  — session state + routing
# ─────────────────────────────────────────────────────────────────────────────

class FocusPrimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Focus Primer")
        self.configure(bg=BG)
        self.minsize(480, 600)
        self.geometry("540x740")
        self._center()

        self._chime        = _make_chime_wav()
        self._current      = None

        # session stats — persist for the lifetime of the process
        self._stats = {"sessions": 0, "total_s": 0, "streak": 0}

        # session config (set by start screen)
        self._focus_s       = 1500
        self._breath_on     = True
        self._breath_sec    = 4
        self._breath_cycles = 6

        self._show_start()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h   = 540, 740
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _swap(self, frame: tk.Frame):
        if self._current:
            self._current.destroy()
        self._current = frame
        frame.pack(fill="both", expand=True)

    # ── screen transitions ────────────────────────────────────────────────────

    def _show_start(self):
        self._swap(StartScreen(self, on_start=self._start_session))

    def _start_session(self, fixate_s: int, focus_s: int,
                        breath_on: bool, breath_sec: int, breath_cycles: int):
        self._focus_s       = focus_s
        self._breath_on     = breath_on
        self._breath_sec    = breath_sec
        self._breath_cycles = breath_cycles
        self._swap(FixateScreen(
            self,
            duration_s=fixate_s,
            on_done=self._after_fixate,
            on_skip=self._after_fixate,
            on_stop=self._show_start,
        ))

    def _after_fixate(self):
        if self._breath_on:
            self._to_breath()
        else:
            self._to_focus()

    def _to_breath(self):
        self._swap(BreathScreen(
            self,
            breath_sec=self._breath_sec,
            cycles=self._breath_cycles,
            on_done=self._to_focus,
            on_skip=self._to_focus,
            on_stop=self._show_start,
        ))

    def _to_focus(self):
        self._swap(FocusScreen(
            self,
            duration_s=self._focus_s,
            chime_path=self._chime,
            on_done=self._show_done,
            on_stop=self._show_start,
            stats=self._stats,
        ))

    def _show_done(self):
        self._stats["sessions"] += 1
        self._stats["streak"]   += 1
        self._swap(DoneScreen(
            self,
            on_restart=self._show_start,
            on_quit=self.destroy,
            stats=self._stats,
        ))

    def destroy(self):
        try:
            os.unlink(self._chime)
        except Exception:
            pass
        super().destroy()


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    FocusPrimer().mainloop()
