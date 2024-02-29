from property_management.settings import username,api_key
import africastalking


# Initialize SDK for sending sms
# username='ibgaro'
# api_key='865baf274be090d0dc27361d749af03196c63c93082231e14b1866ab3f7db16e'
africastalking.initialize(username,api_key)


def send_sms(message, recipients):
    """send sms notifications"""
    sms = africastalking.SMS
    sender = "softsearch"
    #no sender ID
    return sms.send(message, recipients)