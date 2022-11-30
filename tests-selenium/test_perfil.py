import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class testPerfil( unittest.TestCase ):
    
    # start driver as an attribute of the class (ir runs before EVERY test)
    def setUp(self):
        self.driver =  webdriver.Chrome(executable_path=r"C:\driverChrome\chromedriver.exe")

    # test a login with correct credentials
    def test_perfil(self):
        # go to the login page
        self.driver.get("http://localhost:5000/login")
        
        # Type email
        usuario = self.driver.find_element( By.ID, "email" )
        usuario.send_keys("chachy.drs@gmail.com")

        # Yype password
        password = self.driver.find_element( By.ID, "password" )
        password.send_keys("28126743")

        # Submit login form
        password.send_keys(Keys.ENTER)

        # Select profile picture (navbar)
        perfil = self.driver.find_element(By.ID, "perfilUsuario")
        perfil.send_keys(Keys.ENTER)

        dropdown = self.driver.find_element(By.ID, "dropdown-Profile")
        dropdown.send_keys(Keys.ENTER)        
        time.sleep(3)
        
        self.assertTrue( self.driver.current_url.split("/")[-1] == "chachy.drs@gmail.com" , "No se pudo visualizar el perfil del usuario" )
    

    # destructor (it runs after EVERY test)
    def tearDown(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    unittest.main()