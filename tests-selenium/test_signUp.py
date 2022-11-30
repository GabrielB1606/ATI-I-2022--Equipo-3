import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testSignUp( unittest.TestCase ):
    
    # start driver as an attribute of the class (ir runs before EVERY test)
    def setUp(self):
        self.driver = webdriver.Firefox()

    # test a sign up process
    def test_register_correct(self):
        # go to the sign up page
        self.driver.get("http://localhost:5000/sign_in")

        # type email
        self.driver.find_element( By.ID, "email" ).send_keys( "johnDoe@gmail.com" )

        # type password
        self.driver.find_element( By.ID, "password" ).send_keys("12345678")
        # confirm password
        self.driver.find_element( By.ID, "confirm" ).send_keys("12345678")

        # type
        self.driver.find_element( By.ID, "name" ).send_keys("John Doe")

        # type bio
        self.driver.find_element( By.ID, "biography" ).send_keys("Soy John Doe")
        
        # set birthday date
        date = '2000-05-01'
        self.driver.execute_script(f"document.getElementById('birthday').value = '{date}'")
        
        # type languages
        self.driver.find_element( By.ID, "languages" ).send_keys("C++ y Python")

        # type book        
        self.driver.find_element( By.ID, "book" ).send_keys("Como matar a un ruiseñor")

        # type color
        self.driver.find_element( By.ID, "color" ).send_keys("Azul")
        
        # submit register form
        self.driver.find_element( By.ID, "color" ).send_keys(Keys.ENTER)

        #wait to load lol
        time.sleep(3)

        # if I'm still in login, i haven't logged in (duh...)
        self.assertTrue( self.driver.current_url.split("/")[-1] != "sign_in" , "Todavía seguimos en la dirección de registro, por lo que no se inició sesión correctamente" )

    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()