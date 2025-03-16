# config/base_config.py
class BaseConfig:
    # Default timeout for WebDriverWait (in seconds)
    DEFAULT_TIMEOUT = 10

    # Default browser settings
    BROWSER = "chrome"
    HEADLESS = False