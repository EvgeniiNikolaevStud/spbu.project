from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import eel


eel.init("web")

@eel.expose
def get_id(login, password, user_link):
    options = webdriver.ChromeOptions()
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
    #options.add_argument('headless')

    url = "https://vk.com/login"

    driver = webdriver.Chrome(
        executable_path="/Users/nevgenikolaev/Desktop/parserF/chromedriver/chromedriver 2",
        options=options
    )
    #user_link = input('Вставьте ссылку на страницу пользователя: ')
    #user_link = "https://vk.com/nevgenikolaev"
    def scroll_down(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def add_friends(friends_set, friend_id, driver):
        driver.get(f"https://vk.com/friends?id={friend_id}&section=all")

        scroll_down(driver)

        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        friends_s = soup1.find_all("div", {"class": "friends_user_row"})

        for fs in friends_s:
            friends_set.add(fs["id"][16:])


    try:
        driver.get(url = url)
        time.sleep(0.5)

        email_input = driver.find_element(By.ID, "index_email") 
        email_input.clear()
        email_input.send_keys(login)
        time.sleep(5)


        button1 = driver.find_element(By.CLASS_NAME, "FlatButton__in")
        button1.click()
        time.sleep(3)

        # password_In = driver.find_element(By.CLASS_NAME, "vkc__PureButton__button")
        # password_In.click()
        # time.sleep(1000)

        #code_input = driver.find_element(By.CLASS_NAME, "vkc__TextField__input")
        #code_input.send_keys(input('Введите код:'))
        #time.sleep(2)

        #button_code = driver.find_element(By.CLASS_NAME, "vkuiButton__in")
        #button_code.click()
        #time.sleep(2)

        password_input = driver.find_element(By.NAME, "password") 
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(5)

        button2 = driver.find_element(By.CLASS_NAME, "vkuiButton__in")
        button2.click()
        time.sleep(15)
    
        driver.get(user_link)
        time.sleep(1)

        # getting page owner id
        body = driver.page_source
        body = body.split('<a href="/albums')[2]
        id = body[0:body.index('"')]
        print(id)

        driver.get(f"https://vk.com/friends?id={id}&section=all")

        time.sleep(2)
        scroll_down(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        friends = soup.find_all("div", {"class": "friends_user_row"})

        # no-repeat friends
        final_ids = set()

        # friends of the user we need
        friends_ids_set = set()
        for friend in friends:
            final_ids.add(friend["id"][16:])
            friends_ids_set.add(friend["id"][16:])


        for f_id in friends_ids_set:
            add_friends(final_ids, f_id, driver)
            with open('finalIds.txt', 'w') as f:
                f.write(final_ids.__str__())

        time.sleep(10)
        print('Работа выполнена!')

    
    except Exception as ex:
        print(ex)
    finally:
        driver.close()    
        driver.quit()


eel.start("index.html", size=(700, 700))