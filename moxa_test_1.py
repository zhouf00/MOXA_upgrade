import os
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://192.168.127.253")

driver.find_element_by_id("Username").clear()
driver.find_element_by_id("Username").send_keys("admin")
driver.find_element_by_id("Password").clear()
driver.find_element_by_id("Password").send_keys("moxa")
driver.find_element_by_name("Submit").click()
#driver.switch_to.frame("contents")
driver.switch_to.frame(1)
driver.find_element_by_id("folder59").click()
driver.find_element_by_id("item62").click()
print("%s"%("="*50))
driver.switch_to.parent_frame()
#driver.switch_to.frame("main")
driver.switch_to.frame(2)
driver.find_element_by_name("filename").send_keys("D:\临时\moxa升级\附件三AWK1137C_1.2.4_Build_18053019.rom")
driver.find_element_by_name("Submit").click()


#driver.quit()