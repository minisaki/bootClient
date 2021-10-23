
def like_post_by_id(driver, id_baiviet):
    try:
        driver.get("https://m.facebook.com/reactions/picker/?ft_id=" + id_baiviet + "&amp;")
        list_links = driver.find_elements_by_tag_name('a')
        for item in list_links:
            val = item.get_attribute("href")
            if 'reaction_type=7' in val:
                driver.get(val)
                print("react thanh cong")
                break
        return True
    except:
        return False
