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


def screenshot_cameras(driver, path):
    #Helper function for naming screenshots
    def filename(cameraName, delta):
        now = datetime.now()
        if not delta:
          time = now.strftime(" %H:%M %m-%d-%y.png")
        else:
          time = now.strftime(" delta %H:%M %m-%d-%y.png")
        cameraName = cameraName.replace("/", "")
        cameraName = cameraName.replace("  ", " ")
        return cameraName + time
    
    #Get all the camera names from the table
    print('entering function')
    time.sleep(6)

    table = driver.find_element("id", "cameraList")
    rows = table.find_elements("css selector", "td.camera_selector")

    #Populate the list of camera ids
    ids = []
    for row in rows:
        id = row.get_attribute("id")
        if id:
            ids.append(id)

    #Iterate through the each ID and take a screenshot
    for id in ids:
        element = driver.find_element("id", id)
        element.click()
        time.sleep(1.5)
        stream = driver.find_element("id", "player_container")
        # Take a screenshot of the element
        screenshot = stream.screenshot_as_png
        # Save the screenshot to a file
        with open(path + filename(id, False), "wb") as file:
            file.write(screenshot)
        #Wait one second and take another screenshot so we can identify vehicle speed
        time.sleep(1)
        screenshot = stream.screenshot_as_png
        with open(path + filename(id, True), "wb") as file:
            file.write(screenshot)    

def init(driver):
    #Save the screenhots to a folder with the format - 'Screenshots MM-DD-YYYY'
    folder_name = datetime.now().strftime("Screenshots %m-%d-%y")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    #Wrap login in a try catch block in case the 'favorite camera' bug appears
    try:
        login(driver)
    except:
        #Wait for user input so that it waits until the user logs in
        print('ERROR')
    input("Press Enter when camera issue fixed")
    
    print('clocking')
    time.sleep(5)
    driver.find_element("id", "menu-my_511").click()
    driver.implicitly_wait(2)
    time.sleep(1)
    driver.find_element('xpath', "//a[@id='menu-favorite_cameras']").click()
    # driver.find_element('id', "menu-favorite_cameras").click()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.511virginia.org")
    driver.implicitly_wait(15)
    init(driver)
    folder_name = datetime.now().strftime("Screenshots %m-%d-%y")
    path = os.path.join(os.getcwd(), folder_name) + "/"
    screenshot_cameras(driver, path)