from logger import get_logger
from models.chats import ChatMessage
from utils.common import CommonsDep
from datastores.datastore_factory import get_datastore_client

logger = get_logger(__name__)


def create_chat(user_id, history, chat_name):
    # Chat is created upon the user's first question asked
    logger.info(f"New chat entry in chats table for user {user_id}")
    
    # Insert a new row into the chats table
    new_chat = {
        "user_id": user_id,
        "history": history, # Empty chat to start
        "chat_name": chat_name
    }
    insert_response = get_datastore_client().table('chats').insert(new_chat).execute()
    logger.info(f"Insert response {insert_response.data}")

    return(insert_response)

def update_chat(chat_id, history):
    if not chat_id:
        logger.error("No chat_id provided")
        return
    get_datastore_client().table("chats").update(
        { "history": history}).match({"chat_id": chat_id}).execute()
    logger.info(f"Chat {chat_id} updated")
    

def get_chat_name_from_first_question( chat_message: ChatMessage):
    # Step 1: Get the summary of the first question        
    # first_question_summary = summarize_as_title(chat_message.question)
    # Step 2: Process this summary to create a chat name by selecting the first three words
    chat_name = ' '.join(chat_message.question.split()[:3])

    return chat_name
