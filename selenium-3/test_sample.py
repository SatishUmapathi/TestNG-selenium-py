import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import warnings

username = os.getenv("LT_USERNAME")  # Replace with your username
access_key = os.getenv("LT_ACCESS_KEY")  # Replace with your access key


def suppress_resource_warnings():
    warnings.filterwarnings("ignore", category=ResourceWarning)


# Parameterized fixture for browser setup
@pytest.fixture(params=[
    ("chrome", "Windows 10"),
    ("firefox", "Windows 10"),
    ("edge", "Windows 10"),
    ("chrome", "macOS Sierra"),
    ("firefox", "macOS Sierra"),
    ("edge", "macOS Sierra")
])
def driver_setup(request):
    suppress_resource_warnings()

    browser,platfrom = request.param
    capabilities = {
        "browserName": browser,
        "browserVersion": "latest",
        "LT:Options": {
            "username": username,
            "accessKey": access_key,
            "platformName": platfrom,
            "build": "Selenium 3 Example",
            "name": f"Selenium 3 Sample Test on {browser.capitalize()}"
        }
    }



    # Start the WebDriver instance on the specified browser
    driver = webdriver.Remote(
        command_executor=f"http://{username}:{access_key}@hub.lambdatest.com/wd/hub",
        desired_capabilities=capabilities
    )
    yield driver
    driver.quit()


@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_demo_site(driver_setup):
    driver = driver_setup
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    # Open the sample to-do app
    print("Loading URL")
    driver.get("https://lambdatest.github.io/sample-todo-app/")

    # Click on the first and second list items
    driver.find_element(By.NAME, "li1").click()
    driver.find_element(By.NAME, "li2").click()
    print("Clicked on the second element")

    # Add a new item to the list
    driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
    driver.find_element(By.ID, "addbutton").click()
    print("Added LambdaTest checkbox")

    # Verify if the heading is displayed
    heading = driver.find_element(By.CSS_SELECTOR, ".container h2")
    assert heading.is_displayed(), "Heading is not displayed"
    print(heading.text)

    # Mark the test as passed or failed in LambdaTest platform
    if heading.is_displayed():
        driver.execute_script("lambda-status=passed")
        print(f"Tests ran successfully on {driver.capabilities['browserName']}!")
    else:
        driver.execute_script("lambda-status=failed")
        print(f"Test failed on {driver.capabilities['browserName']}!")
