from functools import lru_cache
from twilio.rest import Client
from app.config.settings import settings
from app.utils.logger import logger


class TwilioActionResult:
    """Result of a Twilio SMS or Call action"""
    def __init__(self, phone_number: str, status: str, sid: str = None, error: str = None):
        self.phone_number = phone_number
        self.status = status
        self.sid = sid
        self.error = error


class TwilioService:
    """Simplified Twilio service for SMS and Voice calls"""
    
    def __init__(self, account_sid: str, auth_token: str, messaging_service_sid: str, phone_number: str = None):
        self.client = Client(account_sid, auth_token)
        self.messaging_service_sid = messaging_service_sid
        self.phone_number = phone_number
        self.account_sid = account_sid

    def send_sms(self, to: str, message: str) -> TwilioActionResult:
        """Send SMS using Twilio Messaging Service"""
        try:
            msg = self.client.messages.create(
                body=message,
                messaging_service_sid=self.messaging_service_sid,
                to=to,
            )
            logger.info(f"✅ SMS sent to {to}: {msg.sid}")
            return TwilioActionResult(
                phone_number=to,
                status="success",
                sid=msg.sid,
            )
        except Exception as e:
            logger.error(f"❌ SMS failed to {to}: {str(e)}")
            return TwilioActionResult(
                phone_number=to,
                status="failed",
                error=str(e),
            )

    def make_call(self, to: str, message: str) -> TwilioActionResult:
        """Make voice call using Twilio"""
        try:
            # Get available phone numbers from account
            if not self.phone_number:
                # Try to get a phone number from the account
                incoming_numbers = self.client.incoming_phone_numbers.list(limit=1)
                if incoming_numbers:
                    from_number = incoming_numbers[0].phone_number
                    logger.info(f"Using Twilio number: {from_number}")
                else:
                    logger.warning("No Twilio phone number found - call may fail on trial account")
                    from_number = None
            else:
                from_number = self.phone_number
            
            # Create TwiML for voice message
            twiml = f'<Response><Say voice="alice">{message}</Say></Response>'
            
            # Make the call
            if from_number:
                call = self.client.calls.create(
                    twiml=twiml,
                    to=to,
                    from_=from_number
                )
                logger.info(f"📞 Call initiated to {to}: {call.sid}")
                return TwilioActionResult(
                    phone_number=to,
                    status="success",
                    sid=call.sid,
                )
            else:
                logger.error("No valid Twilio phone number available for calls")
                return TwilioActionResult(
                    phone_number=to,
                    status="failed",
                    error="No Twilio phone number configured",
                )
                
        except Exception as e:
            logger.error(f"❌ Call failed to {to}: {str(e)}")
            return TwilioActionResult(
                phone_number=to,
                status="failed",
                error=str(e),
            )


@lru_cache(maxsize=1)
def get_twilio_service() -> TwilioService:
    """Get Twilio service instance with credentials from environment"""
    account_sid = (settings.twilio_account_sid or "").strip()
    auth_token = (settings.twilio_auth_token or "").strip()
    messaging_service_sid = (settings.twilio_messaging_service_sid or "").strip()
    phone_number = (settings.twilio_phone_number or "").strip() if settings.twilio_phone_number else None

    missing_vars = []
    if not account_sid:
        missing_vars.append("TWILIO_ACCOUNT_SID")
    if not auth_token:
        missing_vars.append("TWILIO_AUTH_TOKEN")
    if not messaging_service_sid:
        missing_vars.append("TWILIO_MESSAGING_SERVICE_SID")

    if missing_vars:
        missing = ", ".join(missing_vars)
        raise RuntimeError(f"Missing required environment variables: {missing}")

    return TwilioService(
        account_sid=account_sid,
        auth_token=auth_token,
        messaging_service_sid=messaging_service_sid,
        phone_number=phone_number,
    )
