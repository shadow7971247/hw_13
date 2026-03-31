import allure
from pages.registration_page import RegistrationPage
from models.user import User, Gender, Hobby


@allure.title("Successful fill form")
def test_successful(setup_browser):
    driver = setup_browser

    user = User(
        first_name="Jane",
        last_name="Doe",
        email="JaneD@example.com",
        gender=Gender.OTHER,
        mobile="1231231230",
        subjects=["Physics"],
        hobbies=[Hobby.SPORTS],
        picture="test.jpg",
        address="Ulitsa Pushkina 1",
        state="NCR",
        city="Delhi"
    )

    page = RegistrationPage(driver)

    with allure.step("Open registration form"):
        page.open()

    with allure.step("Fill first name"):
        page.fill_first_name(user.first_name)

    with allure.step("Fill last name"):
        page.fill_last_name(user.last_name)

    with allure.step("Fill email"):
        page.fill_email(user.email)

    with allure.step("Select gender"):
        page.select_gender(user.gender)

    with allure.step("Fill mobile number"):
        page.fill_mobile(user.mobile)

    with allure.step("Fill subjects"):
        page.fill_subjects(user.subjects)

    with allure.step("Select hobbies"):
        page.select_hobbies(user.hobbies)

    with allure.step("Upload picture"):
        page.upload_picture(user.picture)

    with allure.step("Fill current address"):
        page.fill_address(user.address)

    with allure.step("Select state"):
        page.select_state(user.state)

    with allure.step("Select city"):
        page.select_city(user.city)

    with allure.step("Submit form"):
        page.submit()

    with allure.step("Verify success modal"):
        page.should_have_success_modal()