import os
import sys
import json
import math
import struct
import wave
import tempfile
import threading
import webview

def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

class FocusAPI:
    def __init__(self):
        self.stats_file = os.path.join(os.path.abspath("."), "focus_stats.json")
        self.sounds = {}
        self._pregenerate_sounds()

    def _generate_tone_wav(self, frequency, duration, filename_key, is_two_tone=False) -> str:
        sample_rate = 44100
        volume = 0.3
        
        tmp = tempfile.NamedTemporaryFile(suffix=f"_{filename_key}.wav", delete=False)
        tmp.close()

        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            
            samples = []
            if not is_two_tone:
                num_samples = int(sample_rate * duration)
                for i in range(num_samples):
                    t = i / sample_rate
                    # Soft linear fade-out envelope
                    envelope = 1.0 - (t / duration)
                    val = envelope * math.sin(2 * math.pi * frequency * t)
                    packed = struct.pack("<h", int(val * 32767 * volume))
                    samples.append(packed)
            else:
                # Two tone ascending chime
                half_duration = duration / 2
                num_samples = int(sample_rate * half_duration)
                # First tone
                for i in range(num_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (t / half_duration)
                    val = envelope * math.sin(2 * math.pi * frequency * t)
                    samples.append(struct.pack("<h", int(val * 32767 * volume)))
                # Second tone (ascending: 1.5 * frequency)
                for i in range(num_samples):
                    t = i / sample_rate
                    envelope = 1.0 - (t / half_duration)
                    val = envelope * math.sin(2 * math.pi * (frequency * 1.5) * t)
                    samples.append(struct.pack("<h", int(val * 32767 * volume)))

            wf.writeframes(b"".join(samples))
        
        return tmp.name

    def _pregenerate_sounds(self):
        # 1. Soft single tone chime: 800Hz, 0.4s (Fixate done)
        self.sounds["chime_soft"] = self._generate_tone_wav(800.0, 0.4, "soft")
        # 2. Breathing transition chime: Softer 600Hz, 0.3s
        self.sounds["chime_breath"] = self._generate_tone_wav(600.0, 0.3, "breath")
        # 3. Two tone completed chime: 600Hz then 900Hz
        self.sounds["chime_complete"] = self._generate_tone_wav(600.0, 0.6, "complete", is_two_tone=True)

    def play_sound(self, sound_name):
        """Cross-platform asynchronous sound triggers called by index.html JS."""
        # Check local settings for mute state
        stats = self.get_stats()
        if stats.get("muted", False):
            return

        sound_path = self.sounds.get(sound_name)
        if not sound_path or not os.path.exists(sound_path):
            return

        def run():
            try:
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            except ImportError:
                os.system(f'aplay -q "{sound_path}" 2>/dev/null || paplay "{sound_path}" 2>/dev/null')
        
        threading.Thread(target=run, daemon=True).start()

    def get_stats(self):
        if not os.path.exists(self.stats_file):
            defaults = {
                "current_streak": 0,
                "today_focus_mins": 0,
                "total_focus_mins": 0,
                "last_active_date": "",
                "muted": False
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
                "last_active_date": "",
                "muted": False
            }

    def set_mute_state(self, is_muted):
        stats = self.get_stats()
        stats["muted"] = is_muted
        self._write_stats(stats)
        return stats

    def record_session(self, duration_mins):
        from datetime import date
        today_str = str(date.today())
        stats = self.get_stats()

        stats["total_focus_mins"] += duration_mins
        
        last_date = stats.get("last_active_date", "")
        if last_date == today_str:
            stats["today_focus_mins"] += duration_mins
        else:
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
