# utilities/screenshot.py
import os
from datetime import datetime

def capture_screenshot(driver, test_name="screenshot"):
    # Create screenshots directory if it doesn't exist
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")

    # Capture screenshot
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    return screenshot_path

# Example usage
if __name__ == "__main__":
    from driver_setup import DriverSetup
    driver_setup = DriverSetup()
    driver = driver_setup.get_driver()
    driver.get("https://www.example.com")
    capture_screenshot(driver, "example_test")
    driver_setup.quit_driver()