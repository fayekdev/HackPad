import os
import sys
import pywinctl as pwc
import json
import time
import serial
import threading
import pyautogui
import requests
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


import asyncio
# Windows native Media Controls API integration
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager


try:
    import pygetwindow as gw
except ImportError:
    gw = None

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

CONFIG_FILE = "profiles.json"
SERIAL_PORT = "COM15"  # <-- Change this to your exact USB COM Port
BAUD_RATE = 115200

def load_profiles():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f: return json.load(f)
        except Exception: pass
    return {"Default": {"buttons": {}, "encoder": {}}}

class HackPadSystemTracker:
    def __init__(self):
        self.profiles = load_profiles()
        self.current_profile_name = "Default"
        self.running = True
        self.pc_link_active = False 
        
        self.joystick_x = 512
        self.joystick_y = 512
        self.buttons_state = [0] * 16
        self.encoder_pos = 0
        
        self.DEADZONE = 40
        self.CENTER = 512
        self.CURSOR_SPEED_MODIFIER = 0.04

        self.speaker_volume = None
        self.microphone_volume = None
        self.current_song_title = "Idle"  # Declared cleanly in init
        
        self.weather_state = "Sunny"
        self.temp_state = "21C"
        
        # Sequentially call everything exactly once on startup
        self.init_system_audio()
        self.start_weather_thread()
        self.start_media_tracking_thread()


    def init_system_audio(self):
        try:
            devices = AudioUtilities.GetDeviceEnumerator()
            speakers = getattr(devices, "GetDefaultAudioEndpoint")(0, 0) 
            self.speaker_volume = cast(speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
            
            microphones = getattr(devices, "GetDefaultAudioEndpoint")(1, 0) 
            self.microphone_volume = cast(microphones.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
            
            print("[+] Audio subsystem hooks attached successfully.")
        except Exception as e: 
            print(f"[-] Sound hardware hook failed: {e}")

    async def get_windows_media_properties(self):
        """Pulls metadata strings directly out of the active Windows system audio session."""
        try:
            sessions = await MediaManager.request_async()
            current_session = sessions.get_current_session()
            if current_session:
                info = await current_session.try_get_media_properties_async()
                if info:
                    title = info.title if info.title else "Unknown"
                    artist = info.artist if info.artist else "Unknown"
                    combined = f"{title} - {artist}"
                    
                    # Truncate clean layouts for your small device screen dimensions
                    if len(combined) > 14:
                        return combined[:13] + ".."
                    return combined
            return "No Media"
        except Exception:
            return "Idle"

    def run_media_update_loop(self):
        """Asynchronous tracking adapter thread bridge."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while self.running:
            self.current_song_title = loop.run_until_complete(self.get_windows_media_properties())
            time.sleep(2.0)  # Throttled polling to conserve system resources

    def start_media_tracking_thread(self):
        """Dispatches media tracker to its own independent worker background thread."""
        threading.Thread(target=self.run_media_update_loop, daemon=True).start()


    def fetch_live_weather(self):
        """Fetches and parses precise JSON weather data from wttr.in silently in the background."""
        # Moving this flag out of the while loop ensures it prints exactly once on startup
        print("[+] Weather tracking system background thread initialized.")
        
        spoof_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        while self.running:
            try:
                response = requests.get("https://wttr.in", headers=spoof_headers, timeout=(3.5, 5))
                if response.status_code == 200:
                    data = response.json()
                    conditions_list = data.get('current_condition', [])
                    
                    if isinstance(conditions_list, list) and len(conditions_list) > 0:
                        current = conditions_list[0]
                        
                        feels_like_c = current.get('FeelsLikeC', '21')
                        self.temp_state = f"{feels_like_c}C"
                        
                        desc_text = "sunny"
                        desc_list = current.get('weatherDesc', [])
                        if isinstance(desc_list, list) and len(desc_list) > 0:
                            desc_text = desc_list[0].get('value', 'sunny').lower()
                        
                        if any(word in desc_text for word in ["rain", "drizzle", "shower", "thunderstorm", "sleet"]):
                            self.weather_state = "Rainy"
                        elif any(word in desc_text for word in ["cloud", "overcast", "mist", "fog", "haze"]):
                            self.weather_state = "Cloudy"
                        elif any(word in desc_text for word in ["wind", "gale", "storm", "blizzard", "snow"]):
                            self.weather_state = "Windy"
                        else:
                            self.weather_state = "Sunny"
                            
                        # Removed the cyclic success print statement to prevent console pollution
            except Exception:
                # Silently drop exceptions to protect terminal readability
                pass
                
            time.sleep(900)

          
    def start_weather_thread(self):
        threading.Thread(target=self.fetch_live_weather, daemon=True).start()

    def get_pc_telemetry(self):
        vol_state = "normal"
        if self.speaker_volume:
            try:
                if getattr(self.speaker_volume, "GetMute")(): vol_state = "low"
                else:
                    cv = getattr(self.speaker_volume, "GetMasterVolumeLevelScalar")() * 100
                    vol_state = "low" if cv < 25 else "loud" if cv > 70 else "normal"
            except Exception: pass

        mic_state = "on"
        if self.microphone_volume:
            try: mic_state = "off" if getattr(self.microphone_volume, "GetMute")() else "on"
            except Exception: pass

        return vol_state, mic_state, self.weather_state, self.temp_state

    def get_active_window(self):
        """Fetches raw focused window text and passes it entirely to the parser profile engine."""
        if sys.platform.startswith("win32") and gw is not None:
            try:
                active_window = gw.getActiveWindow()
                if active_window and active_window.title:
                    return active_window.title.strip()
            except Exception: pass
        return "Default"

    def determine_profile(self, window_title):
        """Scans raw window text strings against available profile identifiers."""
        if not window_title or window_title == "Default":
            return "Default"
            
        for profile_name in self.profiles.keys():
            if profile_name == "Default":
                continue
            # Scans window title string for keywords (e.g. searching 'chrome' inside 'Google Chrome')
            if profile_name.lower() in window_title.lower(): 
                return profile_name
        return "Default"


    def send_display_update(self, serial_conn):
        t = time.localtime()
        time_str = f"{t.tm_hour:02d}:{t.tm_min:02d}"
        date_str = f"{time.strftime('%b %d')}"
        vol_state, mic_state, weather_state, temp_state = self.get_pc_telemetry()
        
        app_name = self.current_profile_name
        song_name = self.current_song_title
        
        # 1. Safely extract and verify the 'todos' data type from your loaded configuration dictionary
        raw_todos = self.profiles.get("todos", ["", "", "", ""])
        
        # 2. Re-instantiate it cleanly as an explicit list of strings to satisfy strict linter checking
        todos_list: list[str] = list(raw_todos) if isinstance(raw_todos, list) else ["", "", "", ""]

        # 3. Secure safety padding to prevent out-of-bounds screen array faults
        while len(todos_list) < 4:
            todos_list.append("")
            
        # 4. Extract directly using safe tuple unpacking to circumvent raw integer index collection flags
        t1, t2, t3, t4 = todos_list[0], todos_list[1], todos_list[2], todos_list[3]
        
        data_frame = (
            f"DATA:|APP:{app_name}|WEA:{weather_state}|TMP:{temp_state}"
            f"|SND:{vol_state}|MIC:{mic_state}|SNG:{song_name}"
            f"|DAT:{date_str}|TIM:{time_str}|T1:{t1}|T2:{t2}|T3:{t3}|T4:{t4}\n"
        )
        serial_conn.write(data_frame.encode('utf-8'))

    def execute_macro(self, macro_string):
        if not macro_string: return
        if "+" in macro_string and not macro_string.endswith("\\n"):
            pyautogui.hotkey(*macro_string.split("+"))
        else:
            if macro_string.endswith("\n") or macro_string.endswith("\\n"):
                pyautogui.write(macro_string.replace("\\n", "").replace("\n", ""))
                pyautogui.press('enter')
            else: pyautogui.write(macro_string)

    def process_hardware_inputs(self, json_data, serial_conn):
        try:
            data = json.loads(json_data)
            self.joystick_x = data.get("joyX", 512)
            self.joystick_y = data.get("joyY", 512)
            
            new_buttons = data.get("buttons", [0] * 16)
            new_encoder = data.get("encoder", 0)
            
            window_title = self.get_active_window()
            self.current_profile_name = self.determine_profile(window_title)

            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, 'r') as f:
                        self.profiles = json.load(f)
                except Exception:
                    pass
            active_map = self.profiles.get(self.current_profile_name, self.profiles.get("Default", {}))

            for i in range(16):
                if self.buttons_state[i] == 0 and new_buttons[i] == 1:
                    macro = active_map.get("buttons", {}).get(str(i), "")
                    self.execute_macro(macro)
            
            self.buttons_state = new_buttons

            if new_encoder != self.encoder_pos:
                diff = new_encoder - self.encoder_pos
                encoder_map = active_map.get("encoder", {"clockwise": "scroll_up", "counter_clockwise": "scroll_down"})
                action = encoder_map["clockwise"] if diff > 0 else encoder_map["counter_clockwise"]
                if action == "zoom_in": pyautogui.hotkey('ctrl', '+')
                elif action == "zoom_out": pyautogui.hotkey('ctrl', '-')
                else: pyautogui.scroll(120 if diff > 0 else -120)
                self.encoder_pos = new_encoder

            self.send_display_update(serial_conn)
        except Exception: pass

    def run_cursor_loop(self):
        while self.running:
            if self.pc_link_active:
                dx = self.joystick_x - self.CENTER
                dy = self.joystick_y - self.CENTER
                move_x = int(dx * self.CURSOR_SPEED_MODIFIER) if abs(dx) > self.DEADZONE else 0
                move_y = int(dy * self.CURSOR_SPEED_MODIFIER) if abs(dy) > self.DEADZONE else 0
                if move_x != 0 or move_y != 0:
                    try: pyautogui.moveRel(move_x, move_y)
                    except Exception: pass
            time.sleep(0.01)

class TrackerService:
    def __init__(self):
        self.tracker = HackPadSystemTracker()
        self.thread = None
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.tracker.run_cursor_loop,
            daemon=True
        ).start()

        self.thread = threading.Thread(
            target=self.serial_loop,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False
        self.tracker.running = False

    def serial_loop(self):
        while self.running:
            try:
                with serial.Serial(
                    SERIAL_PORT,
                    BAUD_RATE,
                    timeout=0.1
                ) as ser:

                    self.tracker.pc_link_active = True

                    while self.running:

                        ser.write(b"HELLO\n")

                        if ser.in_waiting:
                            line = ser.readline().decode(
                                "utf-8",
                                errors="ignore"
                            ).strip()

                            if line.startswith("{") and line.endswith("}"):
                                self.tracker.process_hardware_inputs(
                                    line,
                                    ser
                                )

                        time.sleep(0.05)

            except (
                serial.SerialException,
                FileNotFoundError,
                KeyboardInterrupt,
            ):
                self.tracker.pc_link_active = False
                time.sleep(2)


