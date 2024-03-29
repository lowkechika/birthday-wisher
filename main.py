import pandas
import csv
import datetime as dt
from random import choice
import smtplib

# There's probably a simpler way to do this but I'm too lazy to look into it atm

# DATA ENTRY SECTION and updating dict - YOU CAN MODIFY FOR MORE THAN ONE TIME USE
name = input("Enter receiver's first name: ").title()
receiver_email = input("Enter receiver's email: ").lower()
y_birth = int(input("Enter receiver's year of birth: "))
m_birth = int(input("Enter receiver's month of birth: "))
d_birth = int(input("Enter receiver's date of birth: "))

field_name_ids = ['name', 'email', 'year', 'month', 'day']
latest_data = {"name": name, "email": receiver_email, "year": y_birth, "month": m_birth, "day": d_birth}

try:
    pandas.read_csv("birthdays.csv")

except FileNotFoundError:
    new_data = [{"name": name, "email": receiver_email, "year": y_birth, "month": m_birth, "day": d_birth}]
    new_data_file = pandas.DataFrame(new_data)
    new_data_file.to_csv("birthdays.csv", index=False)

else:
    with open("birthdays.csv", 'a', newline="") as data_file:
        contents = csv.DictWriter(data_file, fieldnames=field_name_ids)
        contents.writerow(latest_data)

# DATETIME MODULE
now = dt.datetime.now()
day = now.day
month = now.month

PLACEHOLDER = "[NAME]"

data = pandas.read_csv("birthdays.csv")
working_data = data.to_dict(orient="records")
for receiver in working_data:
    receiver_month = receiver['month']
    receiver_day = receiver['day']
    if receiver_day == day and receiver_month == month:
        receiver_name = receiver['name']
        receiver_email = receiver['email']

        file_names = ['letter_1.txt', 'letter_2.txt', 'letter_3.txt']
        random_file = choice(file_names)

        with open(f"letter_templates\{random_file}") as first_letter_file:
            letter = first_letter_file.read()

        # REPLACING PLACEHOLDER
        new_letter = letter.replace(PLACEHOLDER, f"{receiver_name}")

        # FINALLY SENDING THE EMAILS
        PASSWORD = "your_special_password" # use your own
        EMAIL = "testemails334e@gmail.com" # use your own
        with smtplib.SMTP("smtp.gmail.com") as connection: # best to check further if you're using other providers i.e. yahoo
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=receiver_email,
                msg=f"Subject: Happy Birthday!\n\n{new_letter}"
            )

# My code might not be 100% perfect. Let me know if there's more to be improved
