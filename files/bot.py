import csv
from tkinter import Label
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

df_movie = pd.read_csv('data.csv')
# df_movie = df_movie[df_movie['type'] == 'Movie']
# df_movie['similar_movie'] = ['none'] * len(df_movie)


startFrom = 0
movieName = df_movie.iloc[startFrom]['title']


 

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(executable_path = path)
driver.get('https://www.netflix.com/il/login')
InputEmail = driver.find_element_by_name('userLoginId') 
InputEmail.send_keys('email@gmail.com')
InputPassword = driver.find_element_by_name('password') 
InputPassword.send_keys('password') 



driver.find_element_by_css_selector('.btn.login-button.btn-submit.btn-small').click()
driver.implicitly_wait(5)
options = driver.find_element_by_css_selector("a.profile-link")
options.click()
SearchElement = driver.find_element_by_class_name("searchTab")
SearchElement.click()
driver.find_element_by_id('searchInput').send_keys(movieName)
driver.implicitly_wait(5)
time.sleep(5)
thisCard = driver.find_element_by_css_selector("a.slider-refocus")
thisCard.click()
if thisCard.get_attribute('aria-label') == movieName:
    time.sleep(5)
    ele = driver.execute_script('return document.getElementsByClassName("more-like-this-item")')
    labels = [x.get_attribute('aria-label') for x in ele]
    df_movie.at[startFrom,'similar_movie'] = labels
else:
    df_movie.at[startFrom,'similar_movie'] = 'not found in israel'

for i in range(startFrom, len(df_movie)):
    movieName = df_movie.iloc[i + 1]['title']
    driver.find_element_by_class_name("previewModal-close").click()
    driver.find_element_by_class_name('icon-close').click()
    driver.find_element_by_id('searchInput').send_keys(movieName)
    driver.implicitly_wait(5)
    time.sleep(5)
    thisCard = driver.find_element_by_css_selector("a.slider-refocus")
    thisCard.click()
    time.sleep(5)
    if thisCard.get_attribute('aria-label') == movieName:
        ele = driver.execute_script('return document.getElementsByClassName("more-like-this-item")')
        labels = [x.get_attribute('aria-label') for x in ele]
        df_movie.at[i + 1,'similar_movie'] = labels
        df_movie.to_csv('netflix_movie.csv', index = False)
    else:
        df_movie.at[i + 1,'similar_movie'] = 'not found in israel'
        df_movie.to_csv('netflix_movie.csv', index = False)