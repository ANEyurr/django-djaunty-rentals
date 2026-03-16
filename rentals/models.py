from django.db import models
import datetime


BASE_PRICE = 20.0
TANDEM_SURCHARGE = 5.0
ELECTRIC_SURCHARGE = 10.0


class Bike(models.Model):
    STANDARD = "ST"
    TANDEM = "TA"
    ELECTRIC = "EL"

    BIKE_TYPE_CHOICES = [
        (STANDARD, "Standard"),
        (TANDEM, "Tandem"),
        (ELECTRIC, "Electric"),
    ]

    bike_type = models.CharField(
        max_length=2, choices=BIKE_TYPE_CHOICES, default=STANDARD
    )
    color = models.CharField(max_length=10, default="")

    def __str__(self) -> str:
        return f"{self.bike_type} - {self.color}"


class Renter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    vip_num = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - #{self.phone}"


class Rental(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    price = models.FloatField(default=0.0)

    def calc_price(self) -> None:
        curr_price = BASE_PRICE

        if self.bike.bike_type == Bike.TANDEM:
            curr_price += TANDEM_SURCHARGE
        if self.bike.bike_type == Bike.ELECTRIC:
            curr_price += ELECTRIC_SURCHARGE
        if self.renter.vip_num > 0:
            curr_price *= 0.8

        self.price = curr_price
