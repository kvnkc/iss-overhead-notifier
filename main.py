import requests
from datetime import datetime
import smtplib

MY_LAT = 39.176941
MY_LONG = -77.270157
MY_EMAIL = "from@example.com"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset and time_now <= sunrise:
        return True


if is_iss_overhead() and is_night():
    with smtplib.SMTP(host="smtp.mailtrap.io", port=2525) as connection:
        connection.starttls()
        connection.login(user='2a34c59a769644', password='18e850b3615af5')
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs='Kevin.Cheung.Kai@gmail.com',
                            msg='Subject: Hello\n\nLook up!'
                            )

# BONUS: run the code every 60 seconds.
