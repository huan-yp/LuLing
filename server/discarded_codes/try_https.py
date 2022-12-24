import requests
import httpx
# import os
# import re


# class MessageChain():
#     """交流消息链, 顺序重要
#     """
#     current_message = 0
#     messages = []
#     def __init__(self):
#         pass
    
#     def get_text_by_id():
#         pass
    
#     def move_front():
#         pass
        
#     def move_back():
#         pass


# class ResponseObject():
#     def __init__(self, response_dict) -> None:
            


# def decodeMessage(messageString:str):
#     messageString = messageString.replace("false", "False")
#     messageString = messageString.replace("true", "True")
#     messageString = f"({messageString})"
#     messageString = messageString.replace("\n", ",")
#     # messageString = messageString.replace("{\"text\":\"", "{\"text\":u\"")
#     return eval(messageString)
    
# with open("message.txt", mode="r", encoding="utf-8") as f:
#     response_object = decodeMessage(f.read())
#     print(response_object[-1])    
    
# def make_speech_request(character, history, token, tgt, text):
    

# def 

def get_full_text(response:requests.Response):
    rawbytes = b'' 
    for chunk in response.iter_content(chunk_size=101024): 
        rawbytes += chunk 
    return rawbytes.decode("utf-8")

proxies = {
    'http': 'http://localhost:7890/',
    'https': 'http://localhost:7890/'
}

proxies_httpx = {
    'http://': 'http://localhost:7890/',
    'https://': 'http://localhost:7890/'
}

headers = {
    # "cookie": "_ga=GA1.2.1639721911.1666917686; CookieConsent=true; _gid=GA1.2.1184028167.1671522838; __cuid=e81351332fd9400bbfc2b3eb296a329f; amp_fef1e8=fb4e7547-c602-4944-abc6-2ec6cdd43215R...1gkpflr2u.1gkpflr50.2u.0.2u; __cf_bm=7vnqW0N0.5nzdVCw5Wv9ndWY26ei_6fs0qdAXG03DXk-1671642039-0-AR/95UUsNrtx71Clh+JySboBVyGMHyG3h2JwYCAULidtPtSoZP6LVD6LBif7oEKzl5naIPOq2K5CCDRiWWMw/H7muLdpNG3q7+MCODlK1ZUMU/SPi67OQCfzRlPOtBiUnkKh1z83qhrMzL7h1uoTUjqJs5CRw5v52QWtJfm0akMwwC1xSAGavwNQXoDq8rLXpA==; _gat=1; messages=.eJzty8EKgCAMANBfGTuPiKAv6SgyxNQMW8Hw4N_XbwS7PnjOIfOpt_CVVENJSDMtK-HWY_wk99YGaC2SdqgCQeHoQXg8ExKiJ_v27du3b_-H378xuFqP:1p82Zj:UVoG3fK_RTqLuDg5SCPuGXxU4wT0Vd7-jBD4hQ67vzo; csrftoken=7FAxT6PKgKJktw8ByrTRX2lx9zkL5LOa; sessionid=ibyudi0ofwca8jy5l1wodj9rpkupze29",
    # "Origin": "https://beta.character.ai",
    "Authorization": "Token ccae5043f07315c4bfe312136e9407cbb3725367",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # "Referer": "https://beta.character.ai/chat?char=_MwkwWt5TV1x1St4IljM8jurRqRgkJ7meEiMzBSiASo"
}

data = {
    "history_external_id":"wFOiVjQkIE9cjwwhWck_6Kgx4HQ1Fh3Tm_9XrDA65R0",
    "character_external_id":"_MwkwWt5TV1x1St4IljM8jurRqRgkJ7meEiMzBSiASo",
    "text":"huan_yp:For noodles, I prefer chinese one, especially which from DaZhou.",
    "tgt":"internal_id:215124:b2e7e158-bbb0-45cc-a2d4-0f0b6f690133",
    "ranking_method":"random",
    "staging":False,
    "model_server_address":None,
    "override_prefix":None,
    "override_rank":None,
    "rank_candidates":None,
    "filter_candidates":None,
    "prefix_limit":None,
    "prefix_token_limit":None,
    "livetune_coeff":None,
    "stream_params":None,
    "enable_tti":True,
    "initial_timeout":None,
    "insert_beginning":None,
    "translate_candidates":None,
    "stream_every_n_steps":16,
    "chunks_to_pad":8,
    "is_proactive":False,
    "image_rel_path":"",
    "image_description":"",
    "image_description_type":"",
    "image_origin_type":"",
    "voice_enabled":False,
    "parent_msg_id":None,
    "external_id": "_MwkwWt5TV1x1St4IljM8jurRqRgkJ7meEiMzBSiASo"
}

# with httpx.Client(proxies=proxies_httpx, headers=headers, timeout=40) as client:
#     response = client.post('https://beta.character.ai/chat/streaming/', data=data, timeout=40)
#     print(response.status_code)
#     print(response.headers)
#     print(response.text)
#     print(response.is_closed)
# response = requests.get(url="http://localhost:1145/")
# response = requests.get(url="https://beta.character.ai/", proxies=proxies, headers=headers)
response = requests.post('https://beta.character.ai/chat/streaming/', headers=headers, proxies=proxies, data=data, timeout=40, stream=True)
# response = requests.post('https://beta.character.ai/chat/character/info/', headers=headers, proxies=proxies, data=data, timeout=40, stream=True)
print(response.request.__dict__)
print(response.status_code)
print(response.headers)
print(len(response.text))
print(response.text)
with open("messa.txt", mode="w+") as f:
    f.write(response.text)
    f.write("\n")
    f.write(response.content.decode("utf-8"))