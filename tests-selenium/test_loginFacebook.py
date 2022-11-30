import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testLoginFabook(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\driverChrome\chromedriver.exe")

    def test_loginFacebook_correcto(self):
        self.driver.get("http://localhost:5000/login")              # Open Chrome and go to http://localhost:5000/login

        # Click Facebook Button
        facebook = self.driver.find_element(By.ID, "facebookButton")
        facebook.send_keys(Keys.ENTER)

        # Type Email 
        email = self.driver.find_element(By.ID, "email")
        email.send_keys("Chachy.drs@gmail.com")

        # Type Password 
        password = self.driver.find_element(By.ID, "pass")
        password.send_keys("atiEquipo3Daniela")

        # Send 
        password.send_keys(Keys.ENTER)
        time.sleep(30)
        self.assertTrue( self.driver.current_url.split("/")[-1] != "login" , "No se inició sesión correctamente" )

# Destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()





