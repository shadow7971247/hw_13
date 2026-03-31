import allure
from allure_commons.types import AttachmentType


def add_screenshot(driver):
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=AttachmentType.PNG
    )


def add_page_source(driver):
    allure.attach(
        driver.page_source,
        name="page_source",
        attachment_type=AttachmentType.HTML
    )


def add_console_logs(driver):
    try:
        logs = driver.get_log("browser")
        if logs:
            allure.attach(
                "\n".join([str(log) for log in logs]),
                name="console_logs",
                attachment_type=AttachmentType.TEXT
            )
    except Exception:
        pass


def add_video(driver):
    try:
        video_url = "https://selenoid.autotests.cloud/video/" + driver.session_id + ".mp4"
        allure.attach(
            f'<video src="{video_url}" controls autoplay></video>',
            name="video",
            attachment_type=AttachmentType.HTML
        )
    except Exception:
        pass