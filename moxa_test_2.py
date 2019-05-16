# 检查参数是否正常
import time
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://192.168.127.253")

driver.find_element_by_id("Username").clear()
driver.find_element_by_id("Username").send_keys("admin")
driver.find_element_by_id("Password").clear()
driver.find_element_by_id("Password").send_keys("moxa")
driver.find_element_by_name("Submit").click()

driver.switch_to.frame(1)
driver.find_element_by_id("folder7").click()
driver.find_element_by_xpath("//*[@id='folder10']/tbody/tr/td[1]/a[1]/img").click()
driver.find_element_by_id("item13").click()

driver.switch_to.parent_frame()
driver.switch_to.frame(2)
driver.find_element_by_xpath("//*[@id='turboRoaming_enable']").click()
table1 = driver.find_element_by_xpath("//*[@id='turboRoamingSettings']")
table1_rows = table1.find_element_by_tag_name("tr")
print(table1_rows)
table = driver.find_element_by_xpath("//*[@id='iw_turboRoaming_channels']")
t_rows = table.find_elements_by_tag_name("tr")
print(len(t_rows))