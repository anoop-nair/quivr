import time

from logger import get_logger
from models.users import User
from utils.common import CommonsDep
from datastores.datastore_factory import get_datastore_client

logger = get_logger(__name__)

def create_user(email, date):
    logger.info(f"New user entry in db document for user {email}")

    return(get_datastore_client().table("users").insert(
        {"email": email, "date": date, "requests_count": 1}).execute())

def update_user_request_count(email, date, requests_count):
    logger.info(f"User {email} request count updated to {requests_count}")
    get_datastore_client().table("users").update(
        { "requests_count": requests_count}).match({"email": email, "date": date}).execute()
    
def fetch_user_id_from_credentials(credentials):
    user = User(email=credentials.get('email', 'none'))

    # Fetch the user's UUID based on their email
    response = get_datastore_client().from_('users').select('user_id').filter("email", "eq", user.email).execute()

    userItem = next(iter(response.data or []), {})

    if userItem == {}: 
        date = time.strftime("%Y%m%d")
        create_user_response = create_user(email= user.email, date=date)
        user_id = create_user_response.data[0]['user_id']

    else: 
        user_id = userItem['user_id']

    return user_id

