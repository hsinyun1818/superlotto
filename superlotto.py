from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
from collections import defaultdict, OrderedDict

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path='./chromedriver_mac', options=options)

sec1 = defaultdict(lambda: 0)
sec2 = defaultdict(lambda: 0)
number_set = defaultdict(lambda: 0)

driver.get("https://www.taiwanlottery.com.tw/lotto/superlotto638/history2.aspx")

for year in range(103, 110):
    driver.execute_script("document.querySelector('#SuperLotto638Control_history1_radYM').click();")
    print("year:", year)
    driver.execute_script("document.querySelector('#SuperLotto638Control_history1_dropYear').value=arguments[0]", year)
    for month in range(1, 13):
        print("month:", month)
        if year==109 and month>7:
            break
        driver.execute_script("document.querySelector('#SuperLotto638Control_history1_dropMonth').value=arguments[0]", month)
        driver.execute_script("document.querySelector('#SuperLotto638Control_history1_btnSubmit').click();")
        queries = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@id,"SuperLotto638Control_history1_dlQuery_DrawTerm_")]')))

        for i in range(0, len(queries)):
            history = []
            time = driver.find_element_by_xpath('//span[contains(@id,"SuperLotto638Control_history1_dlQuery_DrawTerm_'+str(i)+'")]').text
            numbers_ele = driver.find_elements_by_xpath('//span[contains(@id,"Control_history1_dlQuery_No") and contains(@id, "_'+str(i)+'")]')   #  1_0, 2_0
            numbers = [int(numbers_ele[j].text) for j in range(0,7)]
            print(time)
            print(numbers)
            for k in range(0, 6):
                sec1[numbers[k]]+=1
                for l in range(k+1, 6):
                        number_set[(numbers[k], numbers[l])] += 1
            print(dict(number_set))
            sec2[numbers[6]]+=1
        print(dict(sec1))
        print(dict(sec2))


print(json.dumps(dict(sec1), indent = 4))
print(json.dumps(dict(sec2), indent = 4))
json_dict = {str(k):v for k, v in number_set.items()}
print(json.dumps(OrderedDict(sorted(json_dict.items(), key=lambda item: item[1], reverse=True)), indent=4))
