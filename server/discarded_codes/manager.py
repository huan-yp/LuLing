

from dataStructure import *


class SystemManager():
    """管理器, 实际处理来自 qq 的命令请求并给出返回信息
    将来自 qq 的对话请求转为命令行字符串并返回
    """
    
    ACC = AccessManager() # 不支持手动修改的模型权限信息(即角色信息和机器人副本信息)(只能通过 System Manager 的接口修改)
    CON = ConfigManager() # 支持手动修改 json 的配置信息(包括 qq 号和机器人的对应信息)(最好通过 System Manager 的接口修改)

    def __init__():
        pass
    
    def save(self):
        self.ACC.save()
        self.CON.save()
    
    def bind_account(self, qq:str, type:str, character_name:str, bot_name:str, create=False):
        """将一个 qq 号或者群号绑定到一个机器人副本
        Args:
            qq (str): qq 号或群号
            type (str):
                values:
                    "group": 表示群聊
                    "friend": 表示好友
            character (str): 角色名, 如果为 None 表示解除绑定
            bot_name (str): 机器人副本名
        """
        if character_name is None:
            pass
        character = self.ACC.find_character_by_name(character_name)
        if character == None:
            return False, f"No such character:{character_name}"
        bot = character.find_bot_by_name(bot_name)
        if bot == None:
            if create:
                self.create_bot(character_name, bot_name)
            else:
                return False, f"No such bot copy in character {character_name}:{bot_name}"
        if type == 'group':
            target = self.CON.GROUP_BOTS
        elif type == 'friend':
            target = self.CON.FRIEND_BOTS
        if qq in target.keys():
            _cn = target[qq]['character_name']
            _bn = target[qq]['bot_name']
            res = True, f"{type} qq_id{qq}'s bot has been replaced to {character_name} {bot_name}, instead of {_cn} {_bn}"
        else:
            res = True, f"{type} qq_id{qq}'s bot has been set to {character_name} {bot_name}"
        target[qq]['character_name'] = character_name
        target[qq]['bot_name'] = bot_name
        return res
    
    def create_bot(self, character_name, bot_name):
        character = self.ACC.find_character_by_name(character_name)
        if character == None:
            raise ValueError(f"No such character:{character_name}")
        bot = character.find_bot_by_name(bot_name)
        if bot != None
    
    def process_request(self, chat:Chat) -> dict:
        result = {}
        
    
    @property
    def SERVER_DEBUG(self):
        return self.CON.SERVER_DEBUG

    @SERVER_DEBUG.setter
    def SERVER_DEBUG(self, value):
        self.CON.SERVER_DEBUG = bool(value)
        
G = SystemManager()