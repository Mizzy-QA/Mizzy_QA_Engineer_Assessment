import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
from datetime import datetime


# Load configuration files created
def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


# log in to Twitter(Use config, to change is required)
def login_to_twitter(driver, username, password):
    print("Navigating to Twitter login page...")
    driver.get('https://twitter.com/login')
    time.sleep(5)

    try:
        #Username Log in
        print("Entering username...")
        username_field = driver.find_element(By.NAME, 'text')
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(2)

        #Password Log in
        print("Entering password...")
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Return True if login is successful
        print("Logged in successfully.")
        return True

        # Return False if login fails
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False


# Function to go to a specific Twitter profile(as set up in config)
def go_to_profile(driver, profile_url, locale):
    print(f"Navigating to profile: {profile_url} with locale: {locale}")
    full_url = f"{profile_url}?locale={locale}"
    driver.get(full_url)
    time.sleep(5)
    print("Profile loaded.")


# Take a screenshot of tweets
def take_screenshots(driver, screenshot_path, num_screenshots):
    try:
        print(f"Preparing to take {num_screenshots} screenshots...")

        # Ensure screenshot directory exists
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
            print(f"Created screenshot directory: {screenshot_path}")
        else:
            # Archive existing files if not empty already
            if any(os.scandir(screenshot_path)):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = f"{screenshot_path}/archive_{timestamp}"
                os.makedirs(archive_path)
                print(f"Archiving existing files to: {archive_path}")

                for item in os.listdir(screenshot_path):
                    item_path = os.path.join(screenshot_path, item)
                    if os.path.isfile(item_path):
                        shutil.move(item_path, archive_path)

        # Scroll and take screenshots of tweets
        screenshots_taken = 0
        tweets_set = set()
        while screenshots_taken < num_screenshots:
            print("Scrolling to load more tweets...")
            tweets = driver.find_elements(By.CSS_SELECTOR, 'article')

            # Remove duplicates tweets(add issue with it duplicating)
            new_tweets = [tweet for tweet in tweets if tweet not in tweets_set]
            tweets_set.update(new_tweets)

            for tweet in new_tweets[:num_screenshots - screenshots_taken]:
                tweet.screenshot(f'{screenshot_path}/tweet_{screenshots_taken + 1}.png')
                screenshots_taken += 1
                print(f"Screenshot {screenshots_taken} taken.")
                if screenshots_taken >= num_screenshots:
                    break

            # Scroll down to load more tweets
            if screenshots_taken < num_screenshots:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

        print("Finished taking screenshots.")

    except Exception as e:
        print(f"An error occurred while taking screenshots: {e}")


# main function
def main(config_file):
    print(f"Starting script with config file: {config_file}")
    config = load_config(config_file)

    username = config['TWITTER']['username']
    password = config['TWITTER']['password']
    profile_url = config['TWITTER']['profile_url']
    locale = config['TWITTER']['locale']
    screenshot_path = config['TWITTER']['screenshot_path']
    num_screenshots = int(config['TWITTER']['num_screenshots'])

    # Selenium Setup
    chrome_options = Options()
    # Run headless for no GUI capturing full element
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    logged_in = login_to_twitter(driver, username, password)

    # Continue with the rest of the script regardless of login outcome
    go_to_profile(driver, profile_url, locale)
    take_screenshots(driver, screenshot_path, num_screenshots)

    driver.quit()
    print("Driver closed.")

#Add or remove config that runs
if __name__ == '__main__':
    main('config_en.ini')
    main('config_ar.ini')
    main('config_NASA.ini')
