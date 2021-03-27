from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import datetime, time, random

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")

options.add_argument("--remote-debugging-port=9222")  # this

options.add_argument("--disable-dev-shm-using")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
driver = webdriver.Chrome(options=options)
driver.get('https://www.amazon.com')

time.sleep(random.randrange(3,10,1))

zip_locator = login_form = driver.find_element_by_id('nav-global-location-slot')
zip_locator.click()

cookie_file = open("cookies_1.txt","w")
cookies = driver.get_cookies()

for el in cookies:
    cookie_file.write('{}'.format(el)+'\n')

cookie_file.close()

try:
    csf_token = driver.find_element_by_name('anti-csrftoken-a2z')
    csf_token_file = open("csf_token_1.txt", "w")
    csf_token_file.write(csf_token.get_attribute('value'))
    csf_token_file.close()
except:
    pass

time.sleep(random.randrange(1,3,1))

pop_zip = driver.find_element_by_id('GLUXZipUpdateInput')
pop_zip.send_keys('10001')

pop_zip = driver.find_element_by_id('GLUXZipUpdate')
pop_zip.click()

time.sleep(random.randrange(1,2,1))

# reload again to avoid some checks
driver.get('https://www.amazon.com')

# print(driver.get_cookies())   #getting cookeis
#save cookies in a pkl file
cookie_file = open("cookies_2.txt","w")
cookies = driver.get_cookies()

for el in cookies:
    cookie_file.write('{}'.format(el)+'\n')

cookie_file.close()

# Get Header after switch
headers = driver.execute_script("var req = new XMLHttpRequest();req.open('GET', document.location, false);req.send(null);return req.getAllResponseHeaders()")

hh_file = open("headers.txt","w")
hh = headers.splitlines()

for hel in hh:
    hh_file.write('{}'.format(hel)+'\n')
hh_file.close()

try:
    csf_token = driver.find_element_by_name('anti-csrftoken-a2z')
    csf_token_file = open("csf_token_2.txt", "w")
    csf_token_file.write(csf_token.get_attribute('value'))
    csf_token_file.close()
except:
    pass

location_elem = driver.find_element_by_id('glow-ingress-block')
inner_html = location_elem.get_attribute('innerHTML')

#check whether is New York
print(inner_html)

if 'New York' in inner_html:
    print('Yes we switched to US :)')