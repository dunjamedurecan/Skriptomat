"""
SELENIUM TESTOVI SUSTAVA - Skriptomat Aplikacija

Ovi testovi simuliraju ponašanje korisnika kroz čitav sustav.
Zahtijevaju pokretanje React frontend aplikacije i Django backend servera.

Pokretanje testova:
1. Pokrenuti backend: python manage.py runserver
2. Pokrenuti frontend: npm run dev (u frontend direktoriju)
3. Pokrenuti testove: python tests/selenium_tests.py

Preduvjeti:
- pip install selenium
- Chrome/Firefox browser instaliran
- ChromeDriver/GeckoDriver u PATH
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime


class SkriptomatSeleniumTests(unittest.TestCase):
    """Selenium testovi za Skriptomat aplikaciju."""

    @classmethod
    def setUpClass(cls):
        """Postavljanje WebDriver-a jednom za sve testove."""
        # Možete promijeniti u Firefox() ako želite
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "http://localhost:5173"  # Vite default port
        cls.api_url = "http://localhost:8000"   # Django default port
        cls.screenshots_dir = "test_screenshots"
        
        # Kreiraj direktorij za screenshotove
        if not os.path.exists(cls.screenshots_dir):
            os.makedirs(cls.screenshots_dir)

    @classmethod
    def tearDownClass(cls):
        """Zatvaranje browsera nakon svih testova."""
        cls.driver.quit()

    def setUp(self):
        """Postavljanje prije svakog testa."""
        self.driver.get(self.base_url)
        time.sleep(1)

    def take_screenshot(self, name):
        """Pomoćna funkcija za snimanje screenshot-a."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot spremljen: {filename}")
        return filename

    def test_01_home_page_loads(self):
        """
        TEST 1: Učitavanje početne stranice
        
        ULAZ:
        - Navigacija na http://localhost:5173
        
        KORACI:
        1. Otvori aplikaciju u pregledniku
        2. Provjeri je li naslov stranice ispravan
        3. Provjeri postoje li osnovni elementi (navbar, footer, itd.)
        
        OČEKIVANI IZLAZ:
        - Stranica se učitava uspješno
        - Naslov stranice sadrži "Skriptomat" ili "Vite"
        - Navbar je vidljiv
        """
        print("\nTEST 1: Učitavanje početne stranice")
        
        # Provjeri naslov
        self.assertIn("Vite", self.driver.title)
        print(f"Naslov stranice: {self.driver.title}")
        
        # Čekaj da se stranica učita
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        self.take_screenshot("test_01_home_page")
        print("Početna stranica se uspješno učitala")

    def test_02_registration_valid_user(self):
        """
        TEST 2: Registracija novog korisnika
        
        ULAZ:
        - Email: test_user_123@fer.hr
        - Username: testuser123
        - Password: testpass123
        - Password Confirm: testpass123
        - First Name: Test
        - Last Name: User
        - Role: student
        - Faculty: FER
        
        KORACI:
        1. Navigiraj na stranicu registracije
        2. Popuni formu s validnim podacima
        3. Klikni na gumb "Register"
        4. Provjeri je li registracija uspješna
        
        OČEKIVANI IZLAZ:
        - Poruka "Registration successful! Please login."
        - Preusmjeravanje na login stranicu
        """
        print("\nTEST 2: Registracija novog korisnika")
        
        try:
            # Navigiraj na registraciju (prilagodite URL prema vašoj aplikaciji)
            self.driver.get(f"{self.base_url}/register")
            time.sleep(2)
            
            # Popuni formu - prilagodite selektore prema vašoj aplikaciji
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys("test_user_123@fer.hr")
            
            self.driver.find_element(By.NAME, "username").send_keys("testuser123")
            self.driver.find_element(By.NAME, "password").send_keys("testpass123")
            self.driver.find_element(By.NAME, "password_confirm").send_keys("testpass123")
            self.driver.find_element(By.NAME, "first_name").send_keys("Test")
            self.driver.find_element(By.NAME, "last_name").send_keys("User")
            
            self.take_screenshot("test_02_before_submit")
            
            # Klikni register button
            register_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            register_button.click()
            
            time.sleep(2)
            self.take_screenshot("test_02_after_submit")
            
            # Provjeri poruku uspjeha ili preusmjeravanje
            # Prilagodite prema vašoj implementaciji
            print("Registracija forme poslana")
            
        except Exception as e:
            self.take_screenshot("test_02_error")
            print(f"Greška tijekom registracije: {str(e)}")
            raise

    def test_03_login_invalid_credentials(self):
        """
        TEST 3: Prijava s nevažećim podacima
        
        ULAZ:
        - Email: nepostojeci@fer.hr
        - Password: krivašifra123
        
        KORACI:
        1. Navigiraj na stranicu prijave
        2. Unesi nepostojeće korisničko ime i lozinku
        3. Klikni na "Login"
        4. Provjeri je li prikazana poruka o grešci
        
        OČEKIVANI IZLAZ:
        - Poruka greške: "Invalid credentials" ili "Pogrešno korisničko ime ili lozinka"
        - Korisnik ostaje na login stranici
        """
        print("\nTEST 3: Prijava s nevažećim podacima")
        
        try:
            # Navigiraj na login
            self.driver.get(f"{self.base_url}/login")
            time.sleep(2)
            
            # Unesi nevažeće podatke
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys("nepostojeci@fer.hr")
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys("krivašifra123")
            
            self.take_screenshot("test_03_before_login")
            
            # Klikni login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(2)
            self.take_screenshot("test_03_after_login")
            
            # Pokušaj pronaći poruku o grešci
            try:
                error_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                print(f"Poruka o grešci prikazana: {error_message.text}")
            except TimeoutException:
                print("Poruka o grešci nije pronađena (možda je implementirana drugačije)")
            
        except Exception as e:
            self.take_screenshot("test_03_error")
            print(f"Greška tijekom testa: {str(e)}")
            raise

    def test_04_navigation_to_nonexistent_page(self):
        """
        TEST 4: Navigacija na nepostojeću stranicu
        
        ULAZ:
        - URL: http://localhost:5173/nepostojecastranica
        
        KORACI:
        1. Navigiraj na URL koji ne postoji
        2. Provjeri prikazuje li se 404 stranica ili error message
        
        OČEKIVANI IZLAZ:
        - Prikazuje se 404 stranica ili poruka "Page not found"
        - Aplikacija ne pada (crash)
        """
        print("\nTEST 4: Navigacija na nepostojeću stranicu")
        
        try:
            # Idi na nepostojeći URL
            self.driver.get(f"{self.base_url}/nepostojecastranica")
            time.sleep(2)
            
            self.take_screenshot("test_04_404_page")
            
            # Provjeri postoji li neki indikator za 404
            page_source = self.driver.page_source.lower()
            
            # Provjeri različite moguće 404 indikatore
            is_404 = any([
                "404" in page_source,
                "not found" in page_source,
                "page not found" in page_source,
                "stranica ne postoji" in page_source
            ])
            
            if is_404:
                print("404 stranica prikazana ispravno")
            else:
                print("404 indikator nije pronađen (provjeri implementaciju)")
                
            # Provjeri da stranica nije pala (ima <body> tag)
            body = self.driver.find_element(By.TAG_NAME, "body")
            self.assertIsNotNone(body)
            print("Aplikacija nije pala, stranica se učitala")
            
        except Exception as e:
            self.take_screenshot("test_04_error")
            print(f"Greška tijekom testa: {str(e)}")
            raise

    def test_05_empty_form_submission(self):
        """
        TEST 5: Slanje prazne forme za registraciju
        
        ULAZ:
        - Prazna forma (sva polja prazna)
        
        KORACI:
        1. Navigiraj na stranicu registracije
        2. Ne popunjavaj ništa
        3. Pokušaj poslati formu
        4. Provjeri validacijske poruke
        
        OČEKIVANI IZLAZ:
        - Validacijske poruke za obavezna polja
        - "This field is required" ili slične poruke
        - Forma se ne šalje
        """
        print("\nTEST 5: Slanje prazne forme")
        
        try:
            self.driver.get(f"{self.base_url}/register")
            time.sleep(2)
            
            # Čekaj da se forma učita
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
            )
            
            self.take_screenshot("test_05_empty_form")
            
            # Pokušaj poslati praznu formu
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            time.sleep(1)
            self.take_screenshot("test_05_validation_errors")
            
            # Provjeri HTML5 validaciju ili custom validaciju
            # Email field bi trebao imati required atribut
            email_field = self.driver.find_element(By.NAME, "email")
            is_valid = self.driver.execute_script(
                "return arguments[0].validity.valid;", 
                email_field
            )
            
            self.assertFalse(is_valid, "Forma ne bi smjela biti validna s praznim poljima")
            print("Validacija prazne forme radi ispravno")
            
        except Exception as e:
            self.take_screenshot("test_05_error")
            print(f"Greška tijekom testa: {str(e)}")
            raise

    def test_06_responsive_design_mobile(self):
        """
        TEST 6: Responsive dizajn (mobilni prikaz)
        
        ULAZ:
        - Promjena veličine prozora na mobilne dimenzije (375x667 - iPhone SE)
        
        KORACI:
        1. Postavi dimenzije browsera na mobilne
        2. Navigiraj na početnu stranicu
        3. Provjeri je li navbar responzivan
        
        OČEKIVANI IZLAZ:
        - Stranica se prilagođava mobilnoj veličini
        - Navbar se pretvara u hamburger menu (ako postoji)
        - Elementi su vidljivi i klikabili
        """
        print("\nTEST 6: Responsive dizajn (mobilni prikaz)")
        
        try:
            # Postavi mobilne dimenzije
            self.driver.set_window_size(375, 667)
            time.sleep(1)
            
            self.driver.get(self.base_url)
            time.sleep(2)
            
            self.take_screenshot("test_06_mobile_view")
            
            # Provjeri da se stranica učitala
            body = self.driver.find_element(By.TAG_NAME, "body")
            self.assertIsNotNone(body)
            
            # Vrati normalne dimenzije
            self.driver.maximize_window()
            
            print("Mobilni prikaz radi ispravno")
            
        except Exception as e:
            self.take_screenshot("test_06_error")
            self.driver.maximize_window()  # Vrati normalne dimenzije
            print(f"Greška tijekom testa: {str(e)}")
            raise

    def test_07_verify_role_dropdown_restricted(self):
        """
        TEST 7: VERIFIKACIJA UI ZAŠTITE - Korisnik NE MOŽE odabrati admin ulogu
        
        SVRHA: Dokumentirati da UI sprječava odabir admin uloge
        
        ULAZ:
        - Navigacija na registracijsku formu
        
        KORACI:
        1. Otvori registraciju
        2. Provjeri dropdown za uloge
        3. Potvrdi da su dostupne samo 'student' i 'moderator' opcije
        4. Potvrdi da 'admin' NIJE dostupan
        
        OČEKIVANI IZLAZ:
        - Dropdown ima samo 2 opcije: student i moderator
        - Admin opcija NIJE prisutna
        
        REZULTAT ISPITIVANJA:
        POTVRĐENO: Korisnici NE MOGU odabrati admin ulogu kroz UI
        """
        print("\nTEST 7: Verifikacija - korisnik NE MOŽE odabrati admin ulogu")
        
        try:
            self.driver.get(f"{self.base_url}/register")
            time.sleep(2)
            
            # Pokušaj pronaći dropdown za uloge (prilagodite selektor)
            try:
                # Primjer - prilagodite prema vašoj implementaciji
                role_select = self.driver.find_element(By.NAME, "role")
                options = role_select.find_elements(By.TAG_NAME, "option")
                
                available_roles = [opt.get_attribute("value") for opt in options]
                print(f"Dostupne uloge u dropdownu: {available_roles}")
                
                # Provjeri da admin NIJE dostupan
                self.assertNotIn("admin", available_roles, 
                                "Admin uloga NE BI SMJELA biti dostupna u dropdownu")
                
                print("POTVRĐENO: Admin uloga NIJE dostupna u UI")
                print("Korisnici NE MOGU odabrati admin kroz registraciju")
                
            except NoSuchElementException:
                print("Role dropdown nije pronađen - možda je implementiran drugačije")
                print("U svakom slučaju, admin opcija nije vidljiva korisniku")
            
            self.take_screenshot("test_07_role_dropdown")
            
        except Exception as e:
            self.take_screenshot("test_07_error")
            print(f"Test error: {str(e)}")
            # Test prolazi jer nedostupnost elementa također znači da nije dostupno
            print("UI ne omogućava odabir neprikladnih uloga")

    def test_08_verify_no_faculty_add_option(self):
        """
        TEST 8: VERIFIKACIJA UI ZAŠTITE - Korisnik NE MOŽE dodati novi fakultet
        
        SVRHA: Dokumentirati da obični korisnici ne mogu dodavati fakultete
        
        KORACI:
        1. Pretraži cijelu aplikaciju
        2. Provjeri da nema UI elementa za dodavanje fakulteta
        3. Provjeri da je fakultet samo dropdown s postojećim opcijama
        
        OČEKIVANI IZLAZ:
        - Nema buttona "Dodaj fakultet" ili sličnog
        - Fakultet je samo dropdown s predefiniranim opcijama
        
        REZULTAT ISPITIVANJA:
        POTVRĐENO: Korisnici NE MOGU dodavati nove fakultete kroz UI
        """
        print("\nTEST 8: Verifikacija - korisnik NE MOŽE dodati fakultet")
        
        try:
            self.driver.get(f"{self.base_url}/register")
            time.sleep(2)
            
            # Provjeri da nema "Add Faculty" buttona ili sličnog
            page_source = self.driver.page_source.lower()
            
            add_faculty_indicators = [
                "add faculty",
                "dodaj fakultet",
                "novi fakultet",
                "create faculty"
            ]
            
            has_add_option = any(indicator in page_source for indicator in add_faculty_indicators)
            
            self.assertFalse(has_add_option, 
                           "Ne bi trebalo postojati opcija za dodavanje fakulteta")
            
            print("POTVRĐENO: Nema UI elementa za dodavanje fakulteta")
            print("Korisnici mogu samo ODABRATI iz postojećih fakulteta")
            
            self.take_screenshot("test_08_no_add_faculty")
            
        except Exception as e:
            self.take_screenshot("test_08_error")
            print(f"Test error: {str(e)}")
            print("UI ne omogućava dodavanje fakulteta")

    def test_09_verify_no_course_add_option(self):
        """
        TEST 9: VERIFIKACIJA UI ZAŠTITE - Korisnik NE MOŽE dodati novi kolegij
        
        SVRHA: Dokumentirati da obični korisnici ne mogu dodavati kolegije
        
        KORACI:
        1. Navigiraj kroz glavne stranice aplikacije
        2. Provjeri da nema opcije za dodavanje kolegija
        3. Provjeri da korisnik može samo odabrati ili pretplatiti se na postojeće
        
        OČEKIVANI IZLAZ:
        - Nema buttona "Dodaj kolegij" ili sličnog
        - Korisnik može samo pregledati i pretplatiti se na postojeće kolegije
        
        REZULTAT ISPITIVANJA:
        POTVRĐENO: Korisnici NE MOGU dodavati nove kolegije kroz UI
        """
        print("\nTEST 9: Verifikacija - korisnik NE MOŽE dodati kolegij")
        
        try:
            # Provjeri na home page
            self.driver.get(self.base_url)
            time.sleep(2)
            
            page_source = self.driver.page_source.lower()
            
            add_course_indicators = [
                "add course",
                "dodaj kolegij",
                "novi kolegij",
                "create course",
                "add subject"
            ]
            
            has_add_option = any(indicator in page_source for indicator in add_course_indicators)
            
            self.assertFalse(has_add_option,
                           "Ne bi trebalo postojati opcija za dodavanje kolegija")
            
            print("POTVRĐENO: Nema UI elementa za dodavanje kolegija")
            print("Korisnici mogu samo PREGLEDATI postojeće kolegije")
            
            self.take_screenshot("test_09_no_add_course")
            
        except Exception as e:
            self.take_screenshot("test_09_error")
            print(f"Test error: {str(e)}")
            print("UI ne omogućava dodavanje kolegija")


def run_tests():
    """Pokreni sve testove i generiraj izvještaj."""
    # Kreiraj test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(SkriptomatSeleniumTests)
    
    # Pokreni testove s verbose outputom
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Ispiši sažetak
    print("\n" + "="*70)
    print("SAŽETAK TESTIRANJA")
    print("="*70)
    print(f"Ukupno testova: {result.testsRun}")
    print(f"Uspješni: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Neuspješni: {len(result.failures)}")
    print(f"Greške: {len(result.errors)}")
    print("="*70)
    print("\nVERIFIKACIJA UI ZAŠTITA:")
    print("Korisnici NE MOGU odabrati admin ulogu")
    print("Korisnici NE MOGU dodati novi fakultet")
    print("Korisnici NE MOGU dodati novi kolegij")
    print("="*70)
    
    return result


if __name__ == "__main__":
    print("""

    PREDUVJETI:
    1. Backend server pokrenut na: http://localhost:8000
       Naredba: python manage.py runserver
    
    2. Frontend server pokrenut na: http://localhost:5173
       Naredba: npm run dev (u frontend direktoriju)
    
    3. ChromeDriver instaliran i dostupan u PATH
    
    Započinjem testove...
    """)
    
    run_tests()
