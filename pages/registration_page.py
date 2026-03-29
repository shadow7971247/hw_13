from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> "RegistrationPage":
        wrapper = self.driver.find_element(By.CSS_SELECTOR, ".practice-form-wrapper")
        assert "Student Registration Form" in wrapper.text
        return self

    def fill_first_name(self, value: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#firstName").send_keys(value)
        return self

    def fill_last_name(self, value: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(value)
        return self

    def fill_email(self, value: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#userEmail").send_keys(value)
        return self

    def select_gender(self, gender: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#genterWrapper").find_element(
            By.XPATH, f".//*[text()='{gender}']"
        ).click()
        return self

    def fill_mobile(self, value: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#userNumber").send_keys(value)
        return self

    def fill_subjects(self, subjects: list) -> "RegistrationPage":
        subject_input = self.driver.find_element(By.CSS_SELECTOR, "#subjectsInput")
        for subject in subjects:
            subject_input.send_keys(subject)
            subject_input.send_keys(Keys.ENTER)
        return self

    def select_hobbies(self, hobbies: list) -> "RegistrationPage":
        wrapper = self.driver.find_element(By.CSS_SELECTOR, "#hobbiesWrapper")
        for hobby in hobbies:
            element = wrapper.find_element(By.XPATH, f".//*[text()='{hobby}']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            clickable = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//*[@id='hobbiesWrapper']//*[text()='{hobby}']"))
            )
            self.driver.execute_script("arguments[0].click();", clickable)
        return self

    def upload_picture(self, file_name: str) -> "RegistrationPage":
        file_path = Path(__file__).parent.parent / "resources" / file_name
        file_input = self.driver.find_element(By.CSS_SELECTOR, "#uploadPicture")
        file_input.send_keys(str(file_path.resolve()))
        return self

    def fill_address(self, value: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#currentAddress").send_keys(value)
        self.driver.execute_script("window.scrollTo(200, document.body.scrollHeight);")
        return self

    def select_state(self, state: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#state").click()
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@id='stateCity-wrapper']//*[text()='{state}']"))
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def select_city(self, city: str) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#city").click()
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@id='stateCity-wrapper']//*[text()='{city}']"))
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def submit(self) -> "RegistrationPage":
        self.driver.find_element(By.CSS_SELECTOR, "#submit").click()
        return self

    def should_have_success_modal(self) -> "RegistrationPage":
        title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#example-modal-sizes-title-lg"))
        )
        assert "Thanks for submitting the form" in title.text
        return self