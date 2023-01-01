

from threading import Lock

class GlobalAttr():
    statu = 'waiting'
    lock = Lock()
    access_processor = None
    bot_online = True
    main_processor = None
    translator = None


G = GlobalAttr()

