import os
import sys
import json
import time
import serial
import threading
import asyncio
import webbrowser

import pyautogui
import requests

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
)

try:
    import pygetwindow as gw
except ImportError:
    gw = None


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

CONFIG_FILE = "profiles.json"
SERIAL_PORT = "COM15"
BAUD_RATE = 115200


def load_profiles():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

    return {
        "Default": {
            "buttons": {},
            "encoder": {},
            "joystick": {},
            "todos": ["", "", "", ""]
        }
    }


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

        self.current_song_title = "Idle"

        self.weather_state = "Sunny"
        self.temp_state = "21C"

        self.init_system_audio()
        self.start_weather_thread()
        self.start_media_tracking_thread()

    def init_system_audio(self):
        try:
            devices = AudioUtilities.GetDeviceEnumerator()

            speakers = getattr(
                devices,
                "GetDefaultAudioEndpoint"
            )(0, 0)

            self.speaker_volume = cast(
                speakers.Activate(
                    IAudioEndpointVolume._iid_,
                    CLSCTX_ALL,
                    None
                ),
                POINTER(IAudioEndpointVolume)
            )

            microphones = getattr(
                devices,
                "GetDefaultAudioEndpoint"
            )(1, 0)

            self.microphone_volume = cast(
                microphones.Activate(
                    IAudioEndpointVolume._iid_,
                    CLSCTX_ALL,
                    None
                ),
                POINTER(IAudioEndpointVolume)
            )

            print("[+] Audio subsystem hooks attached successfully.")

        except Exception as e:
            print(f"[-] Sound hardware hook failed: {e}")

    async def get_windows_media_properties(self):
        try:
            sessions = await MediaManager.request_async()
            current_session = sessions.get_current_session()

            if current_session:
                info = await current_session.try_get_media_properties_async()

                if info:
                    title = info.title if info.title else "Unknown"
                    artist = info.artist if info.artist else "Unknown"

                    combined = f"{title} - {artist}"

                    if len(combined) > 14:
                        return combined[:13] + ".."

                    return combined

            return "No Media"

        except Exception:
            return "Idle"

    def run_media_update_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            while self.running:
                self.current_song_title = loop.run_until_complete(
                    self.get_windows_media_properties()
                )

                time.sleep(2.0)

        finally:
            loop.close()

    def start_media_tracking_thread(self):
        threading.Thread(
            target=self.run_media_update_loop,
            daemon=True
        ).start()

    def fetch_live_weather(self):
        print(
            "[+] Weather tracking system background thread initialized."
        )

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
        }

        while self.running:
            try:
                response = requests.get(
                    "https://wttr.in?format=j1",
                    headers=headers,
                    timeout=(3.5, 5)
                )

                if response.status_code == 200:
                    data = response.json()

                    conditions = data.get(
                        "current_condition",
                        []
                    )

                    if isinstance(conditions, list) and conditions:
                        current = conditions[0]

                        feels_like = current.get(
                            "FeelsLikeC",
                            "21"
                        )

                        self.temp_state = f"{feels_like}C"

                        desc_text = "sunny"

                        descriptions = current.get(
                            "weatherDesc",
                            []
                        )

                        if (
                            isinstance(descriptions, list)
                            and descriptions
                        ):
                            desc_text = descriptions[0].get(
                                "value",
                                "sunny"
                            ).lower()

                        if any(
                            word in desc_text
                            for word in [
                                "rain",
                                "drizzle",
                                "shower",
                                "thunderstorm",
                                "sleet"
                            ]
                        ):
                            self.weather_state = "Rainy"

                        elif any(
                            word in desc_text
                            for word in [
                                "cloud",
                                "overcast",
                                "mist",
                                "fog",
                                "haze"
                            ]
                        ):
                            self.weather_state = "Cloudy"

                        elif any(
                            word in desc_text
                            for word in [
                                "wind",
                                "gale",
                                "storm",
                                "blizzard",
                                "snow"
                            ]
                        ):
                            self.weather_state = "Windy"

                        else:
                            self.weather_state = "Sunny"

            except Exception:
                pass

            time.sleep(900)

    def start_weather_thread(self):
        threading.Thread(
            target=self.fetch_live_weather,
            daemon=True
        ).start()

    def get_pc_telemetry(self):
        vol_state = "normal"
        
        if self.speaker_volume:
            try:
                if getattr(self.speaker_volume, "GetMute")():

                    vol_state = "low"
                else:
                    volume = (
                        getattr(
                        self.speaker_volume, 
                        "GetMasterVolumeLevelScalar"
                        )
                    )

                    if volume < 25:
                        vol_state = "low"
                    elif volume > 70:
                        vol_state = "loud"
                    else:
                        vol_state = "normal"

            except Exception:
                pass

        mic_state = "on"

        if self.microphone_volume:
            try:
                mic_state = (
                    "off"
                    if getattr(
                        self.microphone_volume, 
                        "GetMute"
                    )
                    else "on"
                )

            except Exception:
                pass

        return (
            vol_state,
            mic_state,
            self.weather_state,
            self.temp_state
        )

    def get_active_window(self):
        if (
            sys.platform.startswith("win32")
            and gw is not None
        ):
            try:
                active_window = gw.getActiveWindow()

                if (
                    active_window
                    and active_window.title
                ):
                    return active_window.title.strip()

            except Exception:
                pass

        return "Default"

    def determine_profile(self, window_title):
        if (
            not window_title
            or window_title == "Default"
        ):
            return "Default"

        for profile_name in self.profiles.keys():

            if profile_name == "Default":
                continue

            if (
                profile_name.lower()
                in window_title.lower()
            ):
                return profile_name

        return "Default"

    def reload_profiles(self):
        if not os.path.exists(CONFIG_FILE):
            return

        try:
            with open(
                CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                data = json.load(f)

            if isinstance(data, dict):
                self.profiles = data

        except Exception:
            pass

    def get_active_profile(self):
        profile = self.profiles.get(
            self.current_profile_name
        )

        if isinstance(profile, dict):
            return profile

        profile = self.profiles.get("Default", {})

        if isinstance(profile, dict):
            return profile

        return {}

    def send_display_update(self, serial_conn):
        try:
            t = time.localtime()

            time_str = (
                f"{t.tm_hour:02d}:{t.tm_min:02d}"
            )

            date_str = time.strftime("%b %d")

            (
                vol_state,
                mic_state,
                weather_state,
                temp_state
            ) = self.get_pc_telemetry()

            app_name = self.current_profile_name
            song_name = self.current_song_title

            active_profile = self.get_active_profile()

            raw_todos = active_profile.get(
                "todos",
                ["", "", "", ""]
            )

            if isinstance(raw_todos, list):
                todos_list = [
                    str(item)
                    for item in raw_todos[:4]
                ]
            else:
                todos_list = []

            while len(todos_list) < 4:
                todos_list.append("")

            t1, t2, t3, t4 = todos_list

            data_frame = (
                f"DATA:"
                f"|APP:{app_name}"
                f"|WEA:{weather_state}"
                f"|TMP:{temp_state}"
                f"|SND:{vol_state}"
                f"|MIC:{mic_state}"
                f"|SNG:{song_name}"
                f"|DAT:{date_str}"
                f"|TIM:{time_str}"
                f"|T1:{t1}"
                f"|T2:{t2}"
                f"|T3:{t3}"
                f"|T4:{t4}"
                f"\n"
            )
            print(data_frame.strip())
            serial_conn.write(
                data_frame.encode("utf-8")
            )

        except Exception as e:
            print(
                f"[-] Display update error: {e}"
            )

    def execute_macro(self, action):

        if not action:
            return

        if isinstance(action, dict):

            action_type = action.get(
                "type",
                ""
            )

            if action_type == "shortcut":

                keys = action.get(
                    "keys",
                    []
                )

                if keys:
                    pyautogui.hotkey(*keys)

                return

            if action_type == "text":

                text = action.get(
                    "text",
                    ""
                )

                if text:
                    pyautogui.write(text)

                return

            if action_type == "program":

                program = action.get(
                    "program",
                    ""
                )

                args = action.get(
                    "args",
                    ""
                )

                if not program:
                    return

                try:
                    if args:
                        os.system(
                            f'"{program}" {args}'
                        )
                    else:
                        os.startfile(program)

                except Exception as e:
                    print(
                        f"[-] Program action failed: {e}"
                    )

                return

            if action_type == "website":

                url = action.get(
                    "url",
                    ""
                )

                if url:
                    try:
                        webbrowser.open(url)
                    except Exception as e:
                        print(
                            f"[-] Website action failed: {e}"
                        )

                return

            return

        if isinstance(action, str):

            if "+" in action and not action.endswith("\\n"):

                pyautogui.hotkey(
                    *action.split("+")
                )

                return

            if (
                action.endswith("\n")
                or action.endswith("\\n")
            ):

                pyautogui.write(
                    action
                    .replace("\\n", "")
                    .replace("\n", "")
                )

                pyautogui.press("enter")

                return

            pyautogui.write(action)

    def execute_encoder_action(self, action, direction):
        if not action:
            return

        if isinstance(action, dict):
            self.execute_macro(action)
            return

        if action == "scroll_up":
            pyautogui.scroll(120)
            return

        if action == "scroll_down":
            pyautogui.scroll(-120)
            return

        if action == "zoom_in":
            pyautogui.hotkey(
                "ctrl",
                "+"
            )
            return

        if action == "zoom_out":
            pyautogui.hotkey(
                "ctrl",
                "-"
            )
            return

        self.execute_macro(action)

    def process_joystick(self, joystick_map):
        if not isinstance(joystick_map, dict):
            return

        center_x = joystick_map.get(
            "center_x",
            self.CENTER
        )

        center_y = joystick_map.get(
            "center_y",
            self.CENTER
        )

        deadzone = joystick_map.get(
            "deadzone",
            self.DEADZONE
        )

        speed = joystick_map.get(
            "speed",
            self.CURSOR_SPEED_MODIFIER
        )

        self.CENTER = center_x
        self.DEADZONE = deadzone
        self.CURSOR_SPEED_MODIFIER = speed

        self.joystick_x = self.joystick_x
        self.joystick_y = self.joystick_y

    def process_hardware_inputs(
        self,
        json_data,
        serial_conn
    ):
        try:
            data = json.loads(json_data)

            self.joystick_x = int(
                data.get(
                    "joyX",
                    512
                )
            )

            self.joystick_y = int(
                data.get(
                    "joyY",
                    512
                )
            )

            new_buttons = data.get(
                "buttons",
                [0] * 16
            )

            if not isinstance(new_buttons, list):
                new_buttons = [0] * 16

            new_buttons = (
                new_buttons[:16]
                + [0] * (16 - len(new_buttons))
            )

            new_encoder = int(
                data.get(
                    "encoder",
                    0
                )
            )

            window_title = self.get_active_window()

            detected_profile = self.determine_profile(
                window_title
            )

            self.current_profile_name = (
                detected_profile
            )

            self.reload_profiles()

            active_map = self.get_active_profile()

            buttons_map = active_map.get(
                "buttons",
                {}
            )

            if not isinstance(buttons_map, dict):
                buttons_map = {}

            for i in range(16):

                if (
                    self.buttons_state[i] == 0
                    and new_buttons[i] == 1
                ):

                    action = buttons_map.get(
                        str(i),
                        ""
                    )

                    self.execute_macro(action)

            self.buttons_state = new_buttons

            if new_encoder != self.encoder_pos:

                diff = (
                    new_encoder
                    - self.encoder_pos
                )

                encoder_map = active_map.get(
                    "encoder",
                    {}
                )

                if not isinstance(
                    encoder_map,
                    dict
                ):
                    encoder_map = {}

                if diff > 0:
                    action = encoder_map.get(
                        "clockwise",
                        "scroll_up"
                    )

                    direction = "clockwise"

                else:
                    action = encoder_map.get(
                        "counter_clockwise",
                        "scroll_down"
                    )

                    direction = "counter_clockwise"

                self.execute_encoder_action(
                    action,
                    direction
                )

                self.encoder_pos = new_encoder

            

        except json.JSONDecodeError:
            pass

        except Exception as e:
            print(
                f"[-] Hardware input error: {e}"
            )

    def run_cursor_loop(self):
        while self.running:

            if self.pc_link_active:

                dx = (
                    self.joystick_x
                    - self.CENTER
                )

                dy = (
                    self.joystick_y
                    - self.CENTER
                )

                move_x = (
                    int(
                        dx
                        * self.CURSOR_SPEED_MODIFIER
                    )
                    if abs(dx) > self.DEADZONE
                    else 0
                )

                move_y = (
                    int(
                        dy
                        * self.CURSOR_SPEED_MODIFIER
                    )
                    if abs(dy) > self.DEADZONE
                    else 0
                )

                if (
                    move_x != 0
                    or move_y != 0
                ):
                    try:
                        pyautogui.moveRel(
                            move_x,
                            move_y
                        )
                    except Exception:
                        pass

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
        self.tracker.running = True

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
        self.tracker.pc_link_active = False

    def serial_loop(self):
        while self.running:
            try:
                with serial.Serial(
                SERIAL_PORT,
                BAUD_RATE,
                timeout=0.1
            ) as ser:

                    self.tracker.pc_link_active = True

                    print(f"[+] HackPad connected on {SERIAL_PORT}")

                    last_display_update = 0

                    while self.running:

                        now = time.time()

                        if now - last_display_update >= 0.5:
                            self.tracker.send_display_update(ser)
                            last_display_update = now

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