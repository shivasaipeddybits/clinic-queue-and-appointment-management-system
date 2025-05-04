from dotenv import load_dotenv
import os
import requests
load_dotenv()

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox1c8fc794354f4626a8ced3957cdcf223.mailgun.org/messages",
		auth=("api", os.getenv('API_KEY')),
		data={"from": "Mailgun Sandbox <postmaster@sandbox1c8fc794354f4626a8ced3957cdcf223.mailgun.org>",
			  "to": "Sushant <sushant1.devne@gmail.com>",
			  "subject": "Hello Sushant",
			  "text": "Congratulations Sushant, you just sent an email with Mailgun! You are truly awesome!"})

send_simple_message()