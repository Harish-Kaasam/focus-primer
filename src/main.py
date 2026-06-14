import os
import sys
import json
import math
import struct
import wave
import tempfile
import threading
import webview

# Resolve asset path helper for PyInstaller bundles
def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

class FocusAPI:
    def __init__(self):
        self.stats_file = os.path.join(os.path.abspath("."), "focus_stats.json")
        self.cached_beep_path = self._generate_beep_wav()

    def _generate_beep_wav(self) -> str:
        """Generates a short sine-wave beep WAV file without external dependencies."""
        sample_rate = 44100
        duration = 0.35  # seconds
        frequency = 520.0  # Hz
        num_samples = int(sample_rate * duration)
        samples = []

        for i in range(num_samples):
            t = i / sample_rate
            # Smooth attack and decay envelope
            envelope = math.sin(math.pi * t / duration)
            val = envelope * math.sin(2 * math.pi * frequency * t)
            packed_sample = struct.pack("<h", int(val * 32767 * 0.5))
            samples.append(packed_sample)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.close()
        
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(samples))
            
        return tmp.name

    def play_beep(self):
        """Play generated beep asynchronously on a cross-platform background thread."""
        def run():
            try:
                import winsound
                winsound.PlaySound(self.cached_beep_path, winsound.SND_FILENAME)
            except ImportError:
                # Unix fallback sound player
                os.system(f'aplay -q "{self.cached_beep_path}" 2>/dev/null || paplay "{self.cached_beep_path}" 2>/dev/null')
        
        threading.Thread(target=run, daemon=True).start()

    def get_stats(self):
        """Reads stats file or returns defaults."""
        if not os.path.exists(self.stats_file):
            defaults = {
                "current_streak": 0,
                "today_focus_mins": 0,
                "total_focus_mins": 0,
                "last_active_date": ""
            }
            self._write_stats(defaults)
            return defaults
        
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {
                "current_streak": 0,
                "today_focus_mins": 0,
                "total_focus_mins": 0,
                "last_active_date": ""
            }

    def record_session(self, duration_mins):
        """Logs completed session minutes and increments current streak metrics."""
        from datetime import date
        today_str = str(date.today())
        stats = self.get_stats()

        stats["total_focus_mins"] += duration_mins
        
        # Simple daily streak tracker
        last_date = stats.get("last_active_date", "")
        if last_date == today_str:
            stats["today_focus_mins"] += duration_mins
        else:
            # New active day
            stats["today_focus_mins"] = duration_mins
            stats["current_streak"] += 1
            stats["last_active_date"] = today_str

        self._write_stats(stats)
        return stats

    def _write_stats(self, data):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing stats: {e}")

def main():
    api = FocusAPI()
    html_path = get_asset_path("index.html")
    
    # Run pywebview desktop frame configuration
    window = webview.create_window(
        "Focus Primer",
        url=html_path,
        js_api=api,
        width=1000,
        height=700,
        resizable=True,
        background_color="#020818"
    )
    webview.start()

if __name__ == "__main__":
    main()
