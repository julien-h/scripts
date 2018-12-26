import requests
import os


def notify(msg, title=None):
    headers = {'Content-type': 'application/json'}
    data = '{"text":"' + msg + '"}'
    url = os.environ['SLACK_NOTIFIER_URL']
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
