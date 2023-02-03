from digikala_torture import gozaresh_dehi
from digikala_torture import selenium_way
from digikala_torture import api_way


api_or_selenium = input("HI! \nYou want use selenium or digikala api? (s/a)")

if api_or_selenium == "s":
    Firefox_or_chrome = input("Which browser do you have? Chrome or Firefox? (c/f)")

    selenium_way(Firefox_or_chrome)

else: #به این api خیلی علاقه دارم به همین خاطر به جای elif از else استفاده کردم.
    api_way()
gozaresh_dehi()