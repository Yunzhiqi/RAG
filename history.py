import os
import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage,message_to_dict,messages_from_dict
import config

class ChatHistory(BaseChatMessageHistory):
    def __init__(self,session_id,store_path):
        self.session_id=session_id
        self.store_path=store_path

        os.makedirs(store_path, exist_ok=True)
        self.history_path = os.path.join(store_path, f"{session_id}.json")
        return
    
    def add_messages(self, messages):
        all_messages=list(self.messages)
        all_messages.extend(messages)  
        j_messages=[]
        for m in all_messages:
            j_messages.append(message_to_dict(m))
        with open(self.history_path,'w',encoding='utf-8') as f:
            json.dump(j_messages,f,ensure_ascii=False,indent=2)
        return
    @property
    def messages(self):
        try:
            with open(self.history_path,'r',encoding='utf-8') as f:
                j_messages=json.load(f)
                return messages_from_dict(j_messages)
        except FileNotFoundError:
            return []
        
    def clear(self):
        with open(self.history_path,'w',encoding='utf-8') as f:
            json.dump([],f)
        return
    
def get_history(session_id):
    return ChatHistory(session_id,config.chat_history_path)