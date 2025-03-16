# config/credentials.py
import os

class Credentials:
    # Valid credentials
    VALID_EMAIL = os.getenv("COGNISAAS_EMAIL", "kemalzor@btcmod.com")
    VALID_PASSWORD = os.getenv("COGNISAAS_PASSWORD", "India@123")

    # Invalid credentials for negative testing
    INVALID_EMAIL = "wrong@example.com"
    INVALID_PASSWORD = "wrongpass"


    # SuperCrm prod = rupesh.rao@gmail.com
