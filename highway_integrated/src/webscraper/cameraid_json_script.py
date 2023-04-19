from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from datetime import datetime
import os
import json
import time

#Load the login information from our secrets file
def login(driver):
    #Load in our secrets file
    username = ""
    password = ""
    with open('secrets.json') as f:
        data = json.load(f)
        username = data['username']
        password = data['password']

    #Navigate to the login page
    driver.find_element("id", "menu-my_511").click()
    driver.find_element(By.CLASS_NAME, "dropdown-item").click()
    driver.implicitly_wait(3)
    #Go to the login page
    driver.find_element("id", "UserName").send_keys(username)
    driver.find_element("id", "Password").send_keys(password)
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH, "//input[@type='submit' and @class='expand primary button' and @value='Sign in']").click()


def output_data(driver):
    #Get all the camera names from the table
    time.sleep(6)

    table = driver.find_element("id", "cameraList")
    rows = table.find_elements("css selector", "td.camera_selector")

    #Populate the list of camera ids and names
    ids = []
    names = []
    for row in rows:
        id = row.get_attribute("id")
        if id:
            ids.append(id)
            names.append(row.text)

    #Merge ids, names into a dictionary
    camera_dict = dict(zip(ids, names))
    with open('camera_dict.json', 'w') as f:
        json.dump(camera_dict, f)


def init(driver):
    #Save the screenhots to a folder with the format - 'Screenshots MM-DD-YYYY'
    folder_name = datetime.now().strftime("Screenshots %m-%d-%y")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    #Wrap login in a try catch block in case the 'favorite camera' bug appears
    try:
        login(driver)
    except:
        print('ERROR please manually setup favorite cameras.')
    input("Press Enter when camera issue fixed")
    
    time.sleep(5)
    driver.find_element("id", "menu-my_511").click()
    driver.implicitly_wait(2)
    time.sleep(1)
    driver.find_element('xpath', "//a[@id='menu-favorite_cameras']").click()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.511virginia.org")
    driver.implicitly_wait(15)
    init(driver)
    output_data(driver)
