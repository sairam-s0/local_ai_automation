from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import time

# Open Chrome
driver = webdriver.Chrome()
driver.get("https://saranathan.codetantra.com/secure/course.jsp?eucId=67c968e7cb15964fb5f2b6b4#/contents/67c968e7cb15964fb5f2b6b5/67c968e7cb15964fb5f2b6b9/5b3a14dc64bac16d40c682ed")  # Replace with your quiz page

input("Log in manually, then press Enter...")

# Wait a bit for the question to render
time.sleep(3)

# Find the question area
question_element = driver.find_element(By.XPATH, "//div[contains(@class, 'ql-editor') and contains(@class, 'whitespace-normal')]")

# Take full-page screenshot
screenshot_path = "full_page.png"
driver.save_screenshot(screenshot_path)

# Get element position and size
location = question_element.location
size = question_element.size

# Crop to that region
image = Image.open(screenshot_path)
left = location['x']
top = location['y']
right = left + size['width']
bottom = top + size['height']
image = image.crop((left, top, right, bottom))
image.save("question.png")

print("✅ Cropped screenshot saved as question.png")

driver.quit()
