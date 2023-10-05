import secret
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium import webdriver

def loginStatus(driver: uc.Chrome):
    user = driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[6]/a')
    
    if user.text == "Logg inn":
        print("No user logged inn")
        return False
    else:
        print(f"Logged in as {user.text}")
        return True
        
def logout(driver: uc.Chrome):
    clickHref(driver, "Logg ut")
    print("Logged out user")

def login(driver: uc.Chrome):
    clickHref(driver, "Logg inn")
    
    userInp = driver.find_element(By.ID, "LoginName")
    passInp = driver.find_element(By.ID, "Password")
    logginButton = driver.find_element(By.ID, "login-submit")

    userInp.send_keys(secret.username)
    passInp.send_keys(secret.password)
        
    logginButton.click()
    
    print(f"Logging in as {secret.username}")
    

def clickHref(driver: uc.Chrome, href: str):
    hrefLink = driver.find_element(By.LINK_TEXT, href)
    hrefLink.click()
    
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\Lennard\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    options.add_argument("--profile-directory=Profile 4")
    
    driver = uc.Chrome(
        options = options
    )
    
    driver.get("https://ifinavet.no/login/")
    
    if not loginStatus(driver):
        login(driver)
    
    clickHref("Arrangementer")
    while True:
        pass

if __name__ == '__main__':
    main()