from config import PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY
import pushover

# PUSHOVER
pushover.init(PUSHOVER_APP_TOKEN)
pushover_client = pushover.Client(PUSHOVER_USER_KEY)
