from twilio.rest import TwilioRestClient
import yaml
import os.path

def send_text(to_number, message):
    try:
        config = yaml.load( open(os.path.expanduser('~/.twilio')) )
        client = TwilioRestClient(config['account_sid'], config['auth_token'])
    
        message = client.sms.messages.create(body=message,
                                             to=to_number, 
                                             from_=config['from_number'])
        return True
    except:
        print "ERROR: Didn't send text"
        return False
        
