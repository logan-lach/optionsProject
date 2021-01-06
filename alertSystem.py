import os
import smtplib

class alertSystem:

    def __init__(self):
        self.messages = []

    def addMessage(self,message):
        self.messages.append(message)

    def sendMessages(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            e = os.environ.get('EMAIL_ADDRESS')
            p = os.environ.get('EMAIL_PASSWORD')
            print(e)
            print(p)

            smtp.login(e,p)

            subject = 'Recent options Alerts'
            body = str(''.join(self.messages))

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(e,'lwlach123@gmail.com',str(msg))

a = alertSystem()
a.addMessage('This is a test!')
a.sendMessages()


