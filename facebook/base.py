from bot_service.resrc_service import get_facebook_user
from http.cookies import SimpleCookie
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .like import like_post_by_id
from .group import post_group
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import re
from threading import Thread


class Facebook(Thread):
    def __init__(self, driver_type=1, target=None, driver_path="",
                 facebook_id="", cookie="", username=None, password=None):
        Thread.__init__(self)
        self.driver_type = driver_type
        self.driver_path = driver_path
        self.cookie = cookie
        self.facebook_id = facebook_id
        self.username = username
        self.password = password
        self.action_script = None
        self.facebook_action_list = []
        self.driver = None
        self.get_driver()
        self.flag = False
        self.target = target
        self.name = target

    def get_driver(self):
        if self.driver_type == 1:
            self.driver = webdriver.Firefox(executable_path='./driver/firefox/geckodriver')

        if self.driver_type == 2:
            options = Options()
            options.add_argument('--headless')
            self.driver = webdriver.Firefox(executable_path='./driver/firefox/geckodriver', options=options)

    def set_action_list(self, action_script_list):
        # get action list
        self.facebook_action_list = action_script_list

    def exe_action_script(self):
        for action in self.facebook_action_list:
            # exc
            pass
        pass

    def update_status_to_server(self):
        pass

    def logging_account(self):
        pass

    def login(self):
        self.driver.get("https://mbasic.facebook.com/")
        rawdata = self.cookie
        cookie = SimpleCookie()
        cookie.load(rawdata)

        for key, morsel in cookie.items():
            self.driver.add_cookie({'name': key, 'value': morsel.value})

        self.driver.get("https://mbasic.facebook.com/")
        # cookies = self.driver.get_cookies()
        # print(cookies)
        # string_cookie = ''
        # facebook_id = ''
        # for cookie in cookies:
        #     temp = cookie['name'] + '=' + cookie['value'] + ';'
        #     if cookie['name'] == 'c_user':
        #         facebook_id = cookie['value']
        #     string_cookie += temp
        # print(string_cookie)
        # print(facebook_id)
        #
        # self.driver.get("https://m.facebook.com/")
        # self.driver.get("https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed")
        # string_source = self.driver.page_source
        # self.driver.close()
        # print(type(string_source))
        # token = re.findall(r'accessToken\\\":\\\"(.*)\\\",\\\"use', string_source)
        # user_name = re.findall(r'aria-label=\\\"(.{3,50}),', string_source)
        #
        # print(token[0])
        # print(user_name[0])

    def login_by_user(self):
        self.driver.get('https://m.facebook.com/')
        txt_email = self.driver.find_element_by_xpath('//*[@id="m_login_email"]')
        txt_email.send_keys(self.username)
        time.sleep(5)
        txt_pass = self.driver.find_element_by_name('pass')
        txt_pass.send_keys(self.password)
        time.sleep(5)
        n_login = self.driver.find_element_by_xpath('//*[@value = "Đăng nhập"]')
        print(n_login)
        n_login.click()
        time.sleep(120)
        cookies = self.driver.get_cookies()
        print(cookies)
        string_cookie = ''
        facebook_id = ''
        for cookie in cookies:
            temp = cookie['name'] + '=' + cookie['value'] + ';'
            if cookie['name'] == 'c_user':
                facebook_id = cookie['value']
            string_cookie += temp

        self.driver.get("https://m.facebook.com/")
        self.driver.get("https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed")
        string_source = self.driver.page_source
        self.driver.close()
        print(type(string_source))
        token = re.findall(r'accessToken\\\":\\\"(.*)\\\",\\\"use', string_source)
        user_name = re.findall(r'aria-label=\\\"(.{3,50}),', string_source)

        print(string_cookie)
        print(facebook_id)
        print(token[0])
        print(user_name[0])
        return string_cookie, facebook_id, token[0], user_name[0]

        # self.driver.get("https://www.facebook.com/")

    def logout(self):
        self.driver.close()

    def export_cookie_to_file(self, save_path):
        pass

    def update_cookie_to_server(self):
        pass

    def get_facebook_user_account(self):
        data_user = get_facebook_user()
        if data_user['is_email']:
            self.username = data_user['email']
        else:
            self.username = data_user['phone']

        self.cookie = data_user['cookie']

    def like_facebook_post_by_id(self, id_baiviet):
        return like_post_by_id(self.driver, id_baiviet)

    def new_feed_scoll(self, h=0, m=0, s=0):
        # ve trang chu
        self.driver.get("https://www.facebook.com/")
        s0 = 0

        s0 += h*60*60
        s0 += m*60
        s0 += s

        actions = ActionChains(self.driver)
        while s0 >= 0 and self.flag is False:
            actions.send_keys(Keys.SPACE).perform()
            time_sleep_random = random.randint(1, 10)
            time.sleep(time_sleep_random)
            s0 -= time_sleep_random
            print("chay done")

    def post_status_group(self, id_post):
        print(id_post)
        return post_group(driver=self.driver, id_post=id_post)

    def run(self):
        print(f' bat dau thead {self.name}')
        self.login()







