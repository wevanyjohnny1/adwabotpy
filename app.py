
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gsheet_func import *

from dateutil.parser import parse


app = Flask(__name__)
count=0

@app.route("/sms", methods=['POST'])
def reply():
    
    incoming_msg = request.form.get('Body').lower()
    response = MessagingResponse()
    print(incoming_msg)
    message=response.message()
    responded = False
    words = incoming_msg.split('@')
    if "oi" in incoming_msg:
        reply = "Oi! \nDeseja iniciar um relatório?"
        message.body(reply)
        responded = True

    if len(words) == 1 and "sim" in incoming_msg:
        reminder_string = "Digite a data do culto.\n\n"\
        "*Date @* Data do culto "
        message.body(reminder_string)
        responded = True
    if len(words) == 1 and "não" in incoming_msg:
        reply="Ok. Have a nice day!"
        message.body(reply)
        responded = True
    
    elif len(words) != 1:
        input_type = words[0].strip().lower()
        input_string = words[1].strip()
        if input_type == "date":
            reply="Digite o código do templo.\n\n"\
            "*Reminder @* código do templo"
            set_reminder_date(input_string)
            message.body(reply)
            responded = True
        if input_type == "reminder":
            print("Amém")
            reply="Relatório enviado com sucesso!"
            set_reminder_body(input_string)
            message.body(reply)
            responded = True
        
    if not responded:
        print("why", input_type)
        message.body('Incorrect request format. Please enter in the correct format')
    
    return str(response)
    
def set_reminder_date(msg):
    p= parse(msg)
    date=p.strftime('%d/%m/%Y')
    save_reminder_date(date)
    return 0
    
def set_reminder_body(msg):
    save_reminder_body(msg)
    return 0
    
     
    return reminder_message


if __name__ == "__main__":
    app.run(debug=True)
    
