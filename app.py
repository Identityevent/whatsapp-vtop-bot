from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(_name_)

@app.route("/")
def home():
    return "WhatsApp Bot is Running 🚀"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").lower()
    reply = MessagingResponse()
    msg = reply.message()

    if "hello" in incoming_msg:
        msg.body("Hi! I am your VTOP Assistant 🤖")

    elif "attendance" in incoming_msg:
        msg.body("I will fetch your attendance soon")

    elif "marks" in incoming_msg:
        msg.body("I will fetch your marks soon")

    else:
        msg.body("Send: hello, attendance, or marks")

    return str(reply)

if _name_ == "_main_":
    app.run(debug=True)