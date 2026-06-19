from config.stages import get_stage

STAGE = get_stage()
SERVICE_CONVERSATION_URL = "/api/conversations"
SERVICE_MESSAGES_URL = "/api/messages"

class Endpoints:
    get_conversations_list = f"{STAGE}{SERVICE_CONVERSATION_URL}"
    create_conversation = f"{STAGE}{SERVICE_CONVERSATION_URL}"
    find_or_create_dm = lambda self, username: f"{STAGE}{SERVICE_CONVERSATION_URL}/dm/{username}"
    get_conversation = lambda self, conversation_id: f"{STAGE}{SERVICE_CONVERSATION_URL}/{conversation_id}"
    get_conversation_messages = lambda self, conversation_id: f"{STAGE}{SERVICE_CONVERSATION_URL}/{conversation_id}/messages"
    create_messages = lambda self, conversation_id: f"{STAGE}{SERVICE_CONVERSATION_URL}/{conversation_id}/messages"
    remove_message = lambda self, message_id: f"{STAGE}{SERVICE_MESSAGES_URL}/{message_id}"
    mark_conversation_read = lambda self, conversation_id: f"{STAGE}{SERVICE_CONVERSATION_URL}/{conversation_id}/read"
