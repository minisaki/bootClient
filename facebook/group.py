import requests
import os
import time, random
import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from config.base_config import SERVER_DOMAIN

path = os.path.abspath(os.getcwd())


def get_file_name(path_dir):
    file_name = os.listdir(path_dir)
    print(file_name)
    return file_name


def post_item(driver, id_group, text, file_name, path_dir):
    driver.get('https://mbasic.facebook.com/')
    time.sleep(random.randint(3, 6))
    url = f'https://mbasic.facebook.com/groups/{id_group}/'
    driver.get(url)
    time.sleep(random.randint(3, 6))
    content = driver.find_element_by_name('xc_message')
    time.sleep(random.randint(2, 5))
    for character in text:
        content.send_keys(character)
        time.sleep(0.3)

    time.sleep(random.randint(3, 10))
    photo = driver.find_element_by_name('view_photo')
    photo.click()
    len_list = len(file_name)
    count_filename = math.ceil(len_list / 3)
    start = 0
    for count in range(1, count_filename + 1):
        end = count * 3
        if (len_list - end) <= 0:
            for index in range(start, len_list):
                time.sleep(random.randint(2, 5))
                upload = driver.find_element_by_name(
                    f'file{index + 1 - start}')
                time.sleep(random.randint(2, 5))
                upload.send_keys(f'{path_dir}/{file_name[index]}')
            start = end
            time.sleep(random.randint(3, 5))
            done = driver.find_element_by_name('add_photo_done')
            done.click()
            time.sleep(random.randint(3, 5))
            post = driver.find_element_by_name('view_post')
            post.click()
        else:
            for index in range(start, end):
                time.sleep(random.randint(2, 5))
                upload = driver.find_element_by_name(
                    f'file{index + 1 - start}')
                time.sleep(random.randint(2, 5))
                upload.send_keys(f'{path_dir}/{file_name[index]}')
            start = end
            time.sleep(random.randint(3, 10))
            done = driver.find_element_by_name('add_photo_done')
            done.click()

            time.sleep(random.randint(3, 5))
            addphoto = driver.find_element_by_name('view_photo')
            addphoto.click()

    print(f'post ok {id_group}')
    time.sleep(random.randint(5, 10))

    actions = ActionChains(driver)
    actions.send_keys(Keys.SPACE).perform()
    time.sleep(random.randint(3, 5))
    actions.send_keys(Keys.SPACE).perform()
    time.sleep(random.randint(2, 8))


def post_group(driver, id_post):
    try:
        r = requests.get(f'http://{SERVER_DOMAIN}/api/get_post/?id_post={id_post}')
        print(r.json())
        post = r.json()
        content = post['content']
        group_id = post['group_id'].split(',')
        date = post['added']
        images = post['images']
        print(content)
        print(group_id)
        print(date)
        print(images)
        link_img = f'images/{images[0]["post_id"]}'
        path_dir = os.path.join(path, link_img)
        print(path_dir)
        if not os.path.isdir(path_dir):
            for image in images:
                link = f'http://{SERVER_DOMAIN}{image["file"]}'
                print(link)
                page = requests.get(link, stream=True)

                f_ext = os.path.splitext(link)[-1]
                print(f_ext)
                f_name = f'img_{image["id"]}{f_ext}'
                print(f_name)
                os.makedirs(path_dir, exist_ok=True)
                if page.status_code == 200:
                    print('vao day')
                    with open(f"{path_dir}/{f_name}", 'wb') as f:
                        f.write(page.content)
                else:
                    print('loi roi')
        driver.get(f"https://mbasic.facebook.com/")
        time.sleep(random.randint(2, 8))
        file_name = get_file_name(path_dir)
        print(file_name)
        for id_group in group_id:
            try:
                post_item(driver=driver, id_group=id_group, text=content, file_name=file_name, path_dir=path_dir)
                time.sleep(random.randint(3, 6))
            except:
                print('co loi khi post bai')
                continue

    except NameError:
        print('co loi khi luu hinh')
        return False