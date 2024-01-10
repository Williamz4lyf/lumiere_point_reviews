import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np
import time
from pathlib import Path

# %%
options = webdriver.ChromeOptions()
chrome_driver_path = '/Users/nnankewilliams/chromedriver-mac-arm64/chromedriver'
chrome_service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)

url1 = f'https://www.google.com/travel/hotels/lumiere%20point%20hotel/entity/CgsI15GHguKf3N2dARAB/reviews?q=lumiere%20point%20hotel&g2lb=2502548%2C2503771%2C2503781%2C2504374%2C4258168%2C4284970%2C4308227%2C4814050%2C4874190%2C4893075%2C4924070%2C4965990%2C10208620%2C72277293%2C72298667%2C72302247%2C72313836%2C72317059%2C72406588%2C72412680%2C72414906%2C72421566%2C72430562%2C72440517%2C72442338%2C72442495%2C72456710%2C72458707%2C72464394%2C72464613%2C72468546%2C72468547%2C72470896&hl=en-NG&gl=ng&cs=1&ssta=1&ts=CAEaSQorEicyJTB4MTAzYjhmOGRjNDljMzZiOToweDlkYmI3MGZlMjA0MWM4ZDcaABIaEhQKBwjoDxABGAYSBwjoDxABGAcYATICEAAqBAoAGgA&rp=ENeRh4Lin9zdnQEQ15GHguKf3N2dATgCQABIAcABApoCAggA&ictx=1&utm_campaign=sharing&utm_medium=link&utm_source=htls&ved=0CAAQ5JsGahcKEwiAtNGlosmDAxUAAAAAHQAAAAAQAw'
driver.get(url1)

i = 1
while i <= 280:
    footer = driver.find_element(By.CSS_SELECTOR, 'div.XgdUTc')
    driver.execute_script("arguments[0].scrollIntoView();", footer)
    print('It has scrolled ' + str(i) + ' times')
    print('Now waiting 3 seconds before repeating')
    time.sleep(3)
    i += 1
else:
    print('The script has finished scrolling to the bottom of the page.')

with open(f'lumiere_google_reviews.html', 'w+') as file:
    file.write(driver.page_source)
time.sleep(2)
driver.quit()

#%%
with open(f'lumiere_google_reviews.html') as file:
    page = file.read()
    soup = BeautifulSoup(page, 'html.parser')
    soup_content = soup.find_all(class_='Svr5cf bKhjM')

print(soup_content)

#%%
len(soup_content)

#%%
r1 = soup_content[0]

rr = r1.find('div', class_='X4nL7d')

#%%
reviewer = []
review_date = []
general_rating = []
review = []
extra_info = []
specific_ratings = []

for i in soup_content:
    r_name = i.find('a', class_='DHIhE QB2Jof')
    if r_name:
        reviewer.append(r_name.text)
    else:
        reviewer.append(None)

    r_date = i.find('span', class_='iUtr1 CQYfx')
    if r_date:
        review_date.append(r_date.text)
    else:
        review_date.append(None)

    r_rating = i.find('div', class_='GDWaad')
    if r_rating:
        general_rating.append(r_rating.text)
    else:
        general_rating.append(None)

    r_review = i.find('div', class_='K7oBsc')
    if r_review:
        review.append(r_review.text)
    else:
        review.append(None)

    r_extra = i.find('div', class_='ThUm5b')
    if r_extra:
        extra_info.append(r_extra.text)
    else:
        extra_info.append(None)

    r_specifics = i.find('div', class_='X4nL7d')
    if r_specifics:
        specific_ratings.append(r_specifics.text)
    else:
        specific_ratings.append(None)


df = pd.DataFrame({
    'reviewer': reviewer, 'review_date': review_date,
    'general_rating': general_rating, 'review': review,
    'extra_info': extra_info, 'specific_ratings': specific_ratings
})

print(df.head())

#%%
df.to_csv('lumiere_reviews.csv', index=False)
