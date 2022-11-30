import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testLogin( unittest.TestCase ):
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login(self):
        self.driver.get("http://localhost:5000/login")
        usuario = self.driver.find_element( By.ID, "email" )
        usuario.send_keys("chachy.drs@gmail.com")

        password = self.driver.find_element( By.ID, "password" )
        password.send_keys("28126743")

        password.send_keys(Keys.ENTER)

        time.sleep(3)

        self.assertTrue( self.driver.current_url.split("/")[-1] != "login" , "Todavía seguimos en la dirección de login, por lo que no se inició sesión correctamente" )
    
    def tearDown(self) -> None:
        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()