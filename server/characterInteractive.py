import requests
import os
import re

import constants as C

from global_attributes import G


def decode_message(message_string:str):
    """将获取到的 HTTPS body 解码为 ResponseChain
    Returns:
        [{"text":"t1", id: "123"}, {"text":"t2", id: "124"}, ]
    """
    re_pattern = re.compile("\"speech\": \"[\s\S]+?\"")
    message_string = message_string.replace("false", "False")
    message_string = message_string.replace("true", "True")
    message_string = f"({message_string})"
    message_string = message_string.replace("\n", ",")
    message_string = message_string.replace("{\"text\":\"", "{\"text\":u\"")
    message_string = re_pattern.sub("\"speech\": \"hhh\"", message_string)
    message_string = re.sub(" {100,}", " ", message_string)
    message_string = message_string.replace(",,", ",")
    reponse = eval(message_string)
    messages = []
    for reply in reponse:
        if reply["is_final_chunk"]:
            messages += reply['replies']
    return messages


class RequestError(BaseException):
    
    def __init__(self, response:requests.Response) -> None:
        self.response = response
        super().__init__(f"StatuCode:{response.status_code}")


class MessageChain():
    """交流消息链, 顺序重要
    """
    def __init__(self, response_chain):
        """
            response_chain (回应链): [{"text":"t1", id: "123"}, {"text":"t2", id: "124"}, ]
        """
        self.current_message = 0
        self.messages = []
        for response in response_chain:
            self.messages.append((response["text"], response["id"]))
    
    def get_text_by_id():
        pass
    
    def merge(self, response_chain):
        for response in response_chain:
            self.messages.append((response["text"], response["id"]))
        
    def rate_current(self, score):
        pass
    
    def rate_id(self, id, score):
        pass
    
    @property
    def current_text(self):
        return self.messages[self.current_message][0]
      
    
class Bot():
    
    def __init__(self, his, char, tgt) -> None:
        self.history = his # history_external_id
        self.character = char # character_external_id
        self.tgt = tgt # tgt
        self.current_interaction = None # MessageChain
        pass
    
    def chat(self, text):
        if not G.bot_online:
            return C.OFFLINE_MESSAGE
        if C.SERVER_DEBUG:
            return "Test Message"
        data = C.CHAT_TEMPLATE_DATA
        data["history_external_id"] = self.history
        data["character"] = self.character
        data["tgt"] = self.tgt
        data["text"] = text
        response = requests.post(f"{C.URL}/chat/streaming/", headers=C.CHAT_TEMPLATE_HEADERS, data=data, proxies=C.PROXY)
        if response.status_code == 200:
            self.current_interaction = MessageChain(decode_message(response.text))
            return self.current_interaction.current_text
        
        raise RequestError(response)
    
    def change(self):
        pass
    
    def rate(self, score):
        pass
    
    
main_bot = Bot(
    his = "wFOiVjQkIE9cjwwhWck_6Kgx4HQ1Fh3Tm_9XrDA65R0", 
    char = "_MwkwWt5TV1x1St4IljM8jurRqRgkJ7meEiMzBSiASo",
    tgt = "internal_id:215124:b2e7e158-bbb0-45cc-a2d4-0f0b6f690133"
    )   



# print(main_bot.chat("leaf:It seems that you use chinese with an translation API, Feel free to use English, We can understand."))