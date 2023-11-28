import random
from email.message import EmailMessage
import ssl
import smtplib
from config import emailSender, emailPassword
from groups import groups

def genRandomPair(group):
    pairing = {}
    remaining = dict(group)

    for person, email in remaining.items():

        choices = [p for p in remaining.keys() if p != person and p not in pairing.values()]
        
        if not choices:
            return genRandomPair(group)
        
        recipient = random.choice(choices)

        pairing[person, email] = recipient

    return pairing

def sendEmail(emailReceiver, emailBody):
    email = EmailMessage()
    email['From'] = emailSender
    email['To'] = emailReceiver
    email['Subject'] = "🎁 You've Got a Secret Santa Assignment! 🎅"
    email.add_alternative(emailBody, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(emailSender, emailPassword)
        smtp.sendmail(emailSender, emailReceiver, email.as_string())

    print("Email to "+ emailReceiver + " was sent successfully")

masterGroup = {}

for groupName, groupMembers in groups.items():
    groupPairs = genRandomPair(groupMembers)
    masterGroup.update(groupPairs)

for person, recipient in masterGroup.items():

    body = f"""<p>Hi {person[0]},</p>
    <p>It's time for some holiday magic!</p>
    <p><b>🎁 Your Secret Santa Assignment: {recipient}! 🎁</b></p>
    <p>Now it's time to use your little christmas spirit and think of a gift. No christmas list this year. You're on your own. Show me what you got. This is your time to SHINE! ⭐</p>

    <p>Jingle bells, Batman smells, don't disappoint me this year,</p>
    <p>Santa</p>
    <img src="https://media.istockphoto.com/id/1175686088/photo/closeup-photo-of-funny-funky-wild-vocalist-screaming-in-microphone-wearing-fur-coat-gloves.jpg?s=612x612&w=0&k=20&c=rPAvTuNZ8EhQIW8E963tVRlbCN3scZ2gqJEJccNvYWY=">"""
    
    print("Sending email to " + person[0] + " at " + person[1])
    sendEmail(person[1], body)