import os
import threading
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import string


# util function
def read_names_from_file(filename):
    file_obj = open(filename, "r")
    return file_obj.read().split(", ")


def generate_full_name():
    male_first_names = read_names_from_file("data/male_names.txt")
    female_first_names = read_names_from_file("data/female_names.txt")
    last_names = read_names_from_file("data/last_names.txt")

    # TODO: change this
    gender = random.choice(["male", "female"])
    if gender == "male":
        first_name = random.choice(male_first_names)
    else:
        first_name = random.choice(female_first_names)

    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"

    return full_name


# this can be used for phone number and student id
def generate_random_digits():
    return "".join(random.sample("0123456789", 10))


def generate_email(full_name: str, modifier=""):
    split_name = full_name.split(" ")
    separator = random.choice([".", "_", "-"])
    domain = random.choice(["nru.edu", "unrschool.edu", "myunr.com", "fuckyou.edu"])

    email = (
        f"{split_name[0].lower()}{separator}{split_name[1].lower()}{modifier}@{domain}"
    )
    return email


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(20))
    return password


def fill_form():
    driver = webdriver.Firefox()

    target = os.getenv("TARGET")
    if not target:
        print("NO TARGET DEFINED. STOPPING")
        return

    driver.get(target)

    # there are some random links on the form which are targeted by tabbing through
    # so we have to skip through those first
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.TAB)

    # full name
    full_name = generate_full_name()
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(full_name)

    # student id
    student_id = generate_random_digits()
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(student_id)

    # email
    current_email = generate_email(full_name)
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(current_email)

    # pass
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(generate_password())

    # old email (why would they need this)
    old_email = generate_email(
        full_name, random.choice(["imtrollingyou", "123", "0", "old", "OLD"])
    )
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(old_email)

    # old shit
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(generate_password())  #
    # Generate random month (1-12), formatted as a 2-digit stri

    month = f"{random.randint(1, 12):02d}"
    date = f"{random.randint(1, 30):02d}"
    year = f"{random.randint(1900, 2010):04d}"

    # birthdate
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(month)

    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(date)

    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(year)

    # Phone Number
    phone_number = generate_random_digits()
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(phone_number)

    # done
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.ENTER)

    sleep(2)
    driver.close()


for _ in range(10):
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=fill_form)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
