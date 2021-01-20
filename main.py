import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
import html2text

import difflib

import discord
from discord import Webhook, RequestsWebhookAdapter, File


WEBHOOK_ID = '789550588991766529'
WEBHOOK_TOKEN = 'wAI4hHXY2g7TOIaJWlEEEjqWqJ-sAE-_LN-dUlVNWHl35AEM2N2GqaQoemJ6tXTNNSqh'

debug_id = '801236245815492619'
debug_token = 'syX4rGvf8MCEXqG_6w1JqN0NzdqE6dI-voGggyFrTF8Ms2cVBjWT6fJNmRoae5XPRRje'

# https://discord.com/api/webhooks/801236245815492619/syX4rGvf8MCEXqG_6w1JqN0NzdqE6dI-voGggyFrTF8Ms2cVBjWT6fJNmRoae5XPRRje

WEBHOOK_URL = 'https://discord.com/api/webhooks/789550588991766529/wAI4hHXY2g7TOIaJWlEEEjqWqJ-sAE-_LN-dUlVNWHl35AEM2N2GqaQoemJ6tXTNNSqh'

# Create webhook
webhook = Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN,adapter=RequestsWebhookAdapter())
debug_hook = Webhook.partial(debug_id, debug_token,adapter=RequestsWebhookAdapter())


WAIT = 60

h = html2text.HTML2Text()
h.ignore_links = True


# url = 'http://127.0.0.1:5500/'
url = 'https://vaccine.ucihealth.org/'

response = urlopen(url).read()

currtext = h.handle(response.decode()).strip().split('\n')

currentHash = hashlib.sha224(response).hexdigest()


def get_diff(currtext, newtext):

    report = []

    if len(currtext) > len(newtext):
        line_c = len(currtext)

        # print(line_c)

        for i in range(line_c):
            if currtext[i] in newtext:
                pass
                # print('found text')
            else:
                report.append('REMOVED: ' + currtext[i])
                # print('REMOVED:', currtext[i])
    else:
        line_c = len(newtext)

        # print(line_c)

        for i in range(line_c):
            if newtext[i] in currtext:
                pass
                # print('found text')
            else:
                report.append('ADD: ' + newtext[i])
                # print('ADD:', newtext[i])

    return '\n'.join(report)

# exit()

webhook.send('This is a new watcher. Started on a more stable server', username='Vaccine Watcher')

while True:


    response = urlopen(url).read()
    currentHash = hashlib.sha224(response).hexdigest()
    time.sleep(WAIT)
    response = urlopen(url).read()

    newtext = h.handle(response.decode()).strip().split('\n')
    newHash = hashlib.sha224(response).hexdigest()

    if newHash == currentHash:
        debug_hook.send('SAME!', username='Vaccine Watcher')
        # print('SAME!')
        continue

    else:
        message = "Link: " + url + '\n' + get_diff(currtext, newtext)

        print(message)

        webhook.send(message, username='Vaccine Watcher')

        response = urlopen(url).read()

        currtext = h.handle(response.decode()).strip().split('\n')

        currentHash = hashlib.sha224(response).hexdigest()
        time.sleep(WAIT)
        continue
