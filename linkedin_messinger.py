from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import os
from dotenv import load_dotenv
import pandas as pd
import pickle
import subprocess


class LinkedInMessageSender:
    def __init__(self, email, password):
        subprocess.Popen(f'google-chrome --remote-debugging-port=9222  --user-data-dir=.data_dir'.split()) 
        self.email = email
        self.password = password
        self.options = webdriver.ChromeOptions()
        user_data = r"C:\Users\jenni\AppData\Local\Google\Chrome\User Data"
        self.options.add_argument(f'--user-data-dir={user_data}')
        self.options.add_argument(f'profile-directory=Default')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

    #링크드인 로그인
    def login(self):
        self.driver.get('https://www.linkedin.com')
        self.driver.find_element(By.XPATH, '//*[@type="text"]').send_keys(self.email)
        self.driver.find_element(By.XPATH, '//*[@type="password"]').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()
        self.driver.implicitly_wait(1)
        print("login success")
        page = self.driver.page_source
        print(page)


    #메시지 전송
    def send_message(self, profile_url, message):
        # cookies = pickle.load(open("./cookies.pkl", "rb"))
        self.driver.get(profile_url)
        time.sleep(15)
        message_button= self.driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button/span')
        message_button.click()
        self.driver.implicitly_wait(1)
        print("message button clicked")
        try:
            title = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/input')
            content = self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[3]/form/div[3]/div/div/div[1]')
            title.send_keys(message['title'])
            content.send_keys(message['content'])
            time.sleep(5)
            send_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/div[3]/div[3]/form/footer/div[2]')
            send_button.click()
        except:
            content =  self.driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/div[3]/div/div[1]/div[1]')
            content.send_keys(message['content'])
            time.sleep(5)
            send_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[2]/div[1]')
            send_button.click()
            time.sleep(3)
            delete_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/aside[1]/div[2]/div[1]/header/div[4]/button[3]')
            time.sleep(3)
            delete_button.click()
        print("message sent")

    def close(self):
        self.driver.quit()

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    load_dotenv('./credentials/.env')
    # 계정 정보 입력
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    # 인재 정보
    data = {
        'talent_name': ['이준하', '조재신'],
        'profile_url': ['https://www.linkedin.com/in/leejunha/', 'https://www.linkedin.com/in/jaeshincho/'],
        'chatbot_link': ['https://ca7afd07c45230a631.gradio.live', 'https://ca7afd07c45230a631.gradio.live'],
    }


    df = pd.DataFrame(data)


    for i, r in df.iterrows():
    # 이메일 설정
        talent_name = r['talent_name']
        profile_url = r['profile_url']
        chatbot_link = r['chatbot_link']
        # hooking_message = 'chatgpt_generated_message'
    
        #메시지 내용 작성
        with open('./templates/message_template.txt', 'r', encoding = 'utf-8') as f:
            content = f.read()
            content = content.format(talent_name=talent_name, chatbot_link=chatbot_link)

    
        # 메시지 정보
        message = {
            'title': f'안녕하세요, {talent_name}님 삼정 KPMG입니다',
            'content': content
        }
    
        # LinkedIn 메시지 보내기
        sender = LinkedInMessageSender(email, password)
        # sender.login()
        sender.send_message(profile_url, message)
        #sender.close()
