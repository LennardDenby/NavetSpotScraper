import secret
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium import webdriver


def login(driver: uc.Chrome):
    
    
    driver.get("https://ifinavet.no/login/")
    
    userInp = driver.find_element(By.ID, "LoginName")
    passInp = driver.find_element(By.ID, "Password")
    logginButton = driver.find_element(By.ID, "login-submit")

    userInp.send_keys(secret.username)
    passInp.send_keys(secret.password)
        
    logginButton.click()
    
    while True:
        pass
    #driver.quit()
    
def main():
    options = webdriver.ChromeOptions()
    #options.add_argument("--proxy-server=84.247.50.78:8443")
    #options.add_argument("--user-data-dir=C:\\Users\\Lennard\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    #options.add_argument("--profile-directory=Profile 4")
    #options.add_argument("--disable-blink-features=AutomationControlled") 
    #options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    #options.add_experimental_option("useAutomationExtension", False) 
    
    driver = webdriver.Chrome(
        options = options
    )
    login(driver)

if __name__ == '__main__':
    main()