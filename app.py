import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    message_text = ""

                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    except Exception, e:
                        log(e)

                    if(message_text!=""):

                        url4 = "http://abdul.in.th/abdul-api/askme"
                        frm = "fb-%s" % sender_id
                        payload ={"b":os.environ["BOT_ID"],"f":frm,"t":message_text,"k":os.environ["BOT_ACCESS_TOKEN"],"p":os.environ["PAGE_ACCESS_TOKEN"],"l":""}

                        ans = ""
                        try:
                            response = requests.post(url4,data=payload)
                            data = json.loads(response.text)
                            xans = data['answer'][0]['content']
                            ans = "%s" % xans
                        except Exception, e:
                            log("there are some errors")

                        ans = ans.encode('utf8')

                        if(len(ans)>1000):
                            ans = ans[:999]

                        send_message(sender_id, ans)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
