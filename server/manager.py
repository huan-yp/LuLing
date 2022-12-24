
import functools
import re
import argparse

import constants as C

from global_attributes import G
from characterInteractive import Bot, main_bot




class AccessProcessor():
    """权限管理
    """
    def __init__(self) -> None:
        self.super_admins = ["3051561876", ] # 权限等级为 2
        self.admins = [] # 权限等级为 1
        self.blacklist = []
        
    def get_access_level_by_id(self, qq):
        if qq in self.super_admins:
            return 100
        if qq in self.admins:
            return 10
        if qq in self.blacklist:
            return 0
            
        return 1

    def set_access(self, qq, access):
        pass


def authorization_decorator(level=1):
    """权限管理修饰器
    Info:
        函数必须传入命名参数 user
    Args:
        level: 该操作的需求权限等级.
    """
    def decorator(fun):
        @functools.wraps(fun)
        def warpped_function(*args, **kwargs):
            if 'user' not in kwargs:
                raise ValueError("named argument 'user' required")
            user = kwargs['user']
            if G.access_processor.get_access_level_by_id(user) < level:
                return f"User {user} has no access for this operation"
            return fun(*args, **kwargs)
        return warpped_function
    return decorator


def abstract_command(text:str):
    """识别是否是鹿灵CLI命令

    Args:
        text (_type_): _description_
    Returns:
        二元组
        (False, None): 不是鹿灵CLI命令
        (True, [arg1, arg1, ...]): 是鹿灵CLI命令, 参数为 arg1, arg2
        (True, "some info"): 是鹿灵CLI命令, 参数不合法
    """
    escapes = "\"\\"
    match = re.search("/cmd[\s]", text)
    if match == None:
        return (False, None)
    start_index = match.span()[1]
    cmds = text[start_index:]
    i = 0
    exist = 0
    cmd = ""
    result = []
    while i < len(cmds):
        char = cmds[i]
        if char == '\\':
            if i + 1 == len(cmds):
                return (True, "Unmatched escape character")
            i += 1
            if cmds[i] not in escapes:
                return (True, f"Unmatched escape character \\{cmds[i]}")
            cmd += cmds[i]
        elif char == '\"':
            if exist:
                if len(cmd) == 0:
                    return (True, "empty argument")
                exist = 0
                result.append(cmd)
                cmd = ""
            else:
                exist = 1
        elif char == ' ':
            if exist:
                cmd += char
            else:
                if len(cmd):
                    result.append(cmd)
                cmd = ""
        else:
            cmd += char
        i += 1
    if len(cmd):
        result.append(cmd)
    return (True, result)
    

class CommandProcessor():
    """处理命令
    """
    def __init__(self, bot:Bot) -> None:
        self.bot = bot
        # self.parser = argparse.ArgumentParser(prog="LuLing CLI", description="CLI for LuLing AI management")
    
    def do_command(self, user, args):
        command = args[0]
        if command == "help":
            return self.help(user=user)
        if command == "offline":
            return self.offline(user=user)
        if command == 'online':
            return self.online(user=user)
        
    @authorization_decorator(level=1)
    def help(self, user):
        return C.HELP_INFO
        
    @authorization_decorator(level=10)
    def online(self, user):
        G.bot_online = True
        return C.ONLINE_MESSAGE
    
    @authorization_decorator(level=10)
    def offline(self, user):
        G.bot_online = False
        return C.OFFLINE_MESSAGE
    

class MainProcessor():
    """消息处理器
    """
    def __init__(self, ) -> None:
        self.command_processor = CommandProcessor(main_bot) 
        self.bot = main_bot
    
    @authorization_decorator(level=1)
    def chat(self, user, text):
        return self.bot.chat(text)
    
    def process(self, text, user):
        is_cmd, args = abstract_command(text)
        if not is_cmd:
            return self.chat(user=user, text=text)
        else:
            if isinstance(args, str):
                return args
            return self.command_processor.do_command(user, args)
    
    
if __name__ == "__main__":
    print(abstract_command("/cmd set access 13214342 2"))
