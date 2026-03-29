import allure
from pages.registration_page import RegistrationPage
from models.user import User


@allure.title("Successful fill form")
def test_successful(driver):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="JaneD@example.com",
        gender="Other",
        mobile="1231231230",
        subjects=["Physics"],
        hobbies=["Sports"],
        picture="test.jpg",
        address="Ulitsa Pushkina 1",
        state="NCR",
        city="Delhi"
    )

    page = RegistrationPage(driver)

    with allure.step("Open registration form"):
        page.open()

    with allure.step("Fill form"):
        page.fill_first_name(user.first_name)
        page.fill_last_name(user.last_name)
        page.fill_email(user.email)
        page.select_gender(user.gender)
        page.fill_mobile(user.mobile)
        page.fill_subjects(user.subjects)
        page.select_hobbies(user.hobbies)
        page.upload_picture(user.picture)
        page.fill_address(user.address)
        page.select_state(user.state)
        page.select_city(user.city)
        page.submit()

    with allure.step("Check success modal"):
        page.should_have_success_modal()