from config.action_config import FacebookAction
from facebook.base import Facebook
from connect_socket.connect import connect_socket
from config.base_config import SERVER_DOMAIN
import websocket
import requests
import threading

facebook_accout_run = {}
threads =[]
def run_facebook_process(message_data):
    global facebook_accout_run
    # phân tích action mà server gửi về rồi thực hiện nó
    if message_data["action"] == FacebookAction.LOGIN.value:
        ids = message_data["facebook_id"]
        if len(ids) > 0 and len(ids) == 1:
            fb_id = ids[0]
            cookie = message_data["data"]["cookie"][0][fb_id]
            fb = Facebook(cookie=cookie)
            fb.login()
            facebook_accout_run[fb_id] = fb
        else:
            for index,fb_id in enumerate(ids):
                try:                    
                    cookie = message_data["data"]["cookie"][index][fb_id]
                    fb = Facebook(target=fb_id, cookie=cookie)
                    fb.start()
                    threads.append(fb)
                    facebook_accout_run[fb_id] = fb
                except KeyboardInterrupt:
                    break
            for t in threads:
                t.join()

    if message_data["action"] == FacebookAction.LOGOUT.value:
        ids = message_data["facebook_id"]
        if len(ids) <= 1:
            fb = facebook_accout_run[ids[0]]
            fb.logout()
        else:
            for fb_id in ids:
                fb = facebook_accout_run[fb_id]
                fb.logout()

    if message_data["action"] == FacebookAction.LIKE.value:
        try:
            id_post = message_data["data"]["id_post"]
            fb_id = message_data["facebook_id"]
            fb = facebook_accout_run[fb_id]
            fb.like_facebook_post_by_id(id_baiviet=id_post)
        except:
            cookie = message_data["data"]["cookie"]
            fb = Facebook(cookie=cookie)
            fb.login()
            fb_id = message_data["facebook_id"]
            facebook_accout_run[fb_id] = fb

            id_post = message_data["data"]["id_post"]
            fb_id = message_data["facebook_id"]
            fb = facebook_accout_run[fb_id]
            fb.like_facebook_post_by_id(id_baiviet=id_post)

    if message_data["action"] == FacebookAction.NEW_FEED.value:
        try:
            fb_id = message_data["facebook_id"]
            fb = facebook_accout_run[fb_id]
            if not fb.flag:
                fb.flag = True
            else:
                fb.flag = False

            fb.new_feed_scoll(s=30)
        except:
            fb.new_feed_scoll(s=30)

    if message_data["action"] == FacebookAction.COMMENT.value:
        pass

    if message_data["action"] == FacebookAction.GET_COOKIE.value:
        print(f'xu li lay cokie {message_data}')
        fb = Facebook(username=message_data['data']['userName'], password=message_data['data']['passWord'])
        # fb.login_by_user()
        cookie, facebook_id, token, user = fb.login_by_user()
        facebook_accout_run[facebook_id] = fb
        print(cookie, facebook_id, token, user)
        data = {
            'username': message_data.data['userName'],
            'password': message_data['passWord'],
            'userid': facebook_id,
            'cookie': cookie,
            'user': user,
            'token': token,
        }
        r = requests.post(f'http://{SERVER_DOMAIN}/api/', data)
        print(r.status_code)

    if message_data["action"] == FacebookAction.POST_GROUP.value:
        fb_id = message_data["facebook_id"]
        print(fb_id)
        id_post = message_data["data"]["post_id"]
        print(id_post)
        fb = facebook_accout_run[fb_id]
        fb.post_status_group(id_post=id_post)


def run_youtube_process():
    pass


def run_tiktok_process():
    pass
