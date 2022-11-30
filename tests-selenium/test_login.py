import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testLogin( unittest.TestCase ):
    
    # start driver as an attribute of the class (ir runs before EVERY test)
    def setUp(self):
        self.driver = webdriver.Firefox()

    # test a login with correct credentials
    def test_login_correct(self):
        # go to the login page
        self.driver.get("http://localhost:5000/login")
        
        # type email
        usuario = self.driver.find_element( By.ID, "email" )
        usuario.send_keys("chachy.drs@gmail.com")

        # type password
        password = self.driver.find_element( By.ID, "password" )
        password.send_keys("28126743")

        # submit login form
        password.send_keys(Keys.ENTER)

        #wait to load lol
        time.sleep(3)

        # if I'm still in login, i haven't logged in (duh...)
        self.assertTrue( self.driver.current_url.split("/")[-1] != "login" , "Todavía seguimos en la dirección de login, por lo que no se inició sesión correctamente" )
    

    # test a login witch incorrect credentials
    def test_login_incorrect(self):
        # go to the login page
        self.driver.get("http://localhost:5000/login")
        
        # type email
        usuario = self.driver.find_element( By.ID, "email" )
        usuario.send_keys("chachy.drs@gmail.com")

        # type password
        password = self.driver.find_element( By.ID, "password" )
        password.send_keys("not the correct password")

        # submit login form
        password.send_keys(Keys.ENTER)

        #wait to load lol
        time.sleep(3)

        # if I'm still in login, i haven't logged in (duh...)
        self.assertTrue( self.driver.current_url.split("/")[-1] == "login" , "Logramos entrar a la aplicación con una clave incorrecta" )

    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()