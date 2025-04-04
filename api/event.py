from opperai import Opper
import os

# Your API key will be loaded from the environment variable OPPER_API_KEY if not provided
OPPER_API_KEY = os.getenv("OPPER_API_KEY")
opper = Opper(api_key=OPPER_API_KEY)

result, _ = opper.call(name="onboarding", input="What is the capital of Sweden?")
print(result)
