from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from rentals.models import Bike, Renter, Rental


class Command(BaseCommand):
    help = "Seed Djaunty demo data (bikes, renters, rentals) and optionally create an admin user."

    def add_arguments(self, parser):
        parser.add_argument(
            "--create-superuser",
            action="store_true",
            help="Create/update a superuser with username 'admin' and password 'admin1234'.",
        )

    def handle(self, *args, **options):
        if options["create_superuser"]:
            self._create_superuser()

        bikes = self._seed_bikes()
        renters = self._seed_renters()
        rentals = self._seed_rentals(bikes=bikes, renters=renters)

        self.stdout.write(self.style.SUCCESS("Seed complete."))
        self.stdout.write(f"Bikes: {Bike.objects.count()}")
        self.stdout.write(f"Renters: {Renter.objects.count()}")
        self.stdout.write(f"Rentals: {Rental.objects.count()}")

        self.stdout.write("\nSample queries:")
        self.stdout.write(f"- All bikes: {list(Bike.objects.all())}")
        self.stdout.write(
            f"- Electric bikes: {list(Bike.objects.filter(bike_type=Bike.ELECTRIC))}"
        )
        self.stdout.write(
            f"- Non-standard bikes: {list(Bike.objects.exclude(bike_type=Bike.STANDARD))}"
        )
        self.stdout.write(
            f"- Rentals for {renters[0]}: {list(renters[0].rental_set.all())}"
        )

    def _create_superuser(self) -> None:
        User = get_user_model()
        username = "admin"
        email = "admin@example.com"
        password = "admin1234"

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        if not created and email and not user.email:
            user.email = email

        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.WARNING(
                "Superuser ensured: username='admin' password='admin1234' (change after login)."
            )
        )

    def _seed_bikes(self) -> list[Bike]:
        desired = [
            (Bike.STANDARD, "blue"),
            (Bike.TANDEM, "red"),
            (Bike.ELECTRIC, "black"),
            (Bike.STANDARD, "green"),
            (Bike.ELECTRIC, "white"),
        ]

        bikes: list[Bike] = []
        for bike_type, color in desired:
            bike, _ = Bike.objects.get_or_create(bike_type=bike_type, color=color)
            bikes.append(bike)
        return bikes

    def _seed_renters(self) -> list[Renter]:
        desired = [
            ("Padma", "Lak", "123-456-7890", 12),
            ("Alex", "Rivera", "555-0101", 0),
            ("Sam", "Chen", "555-0199", 3),
        ]

        renters: list[Renter] = []
        for first_name, last_name, phone, vip_num in desired:
            renter, _ = Renter.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                defaults={"vip_num": vip_num},
            )
            if renter.vip_num != vip_num:
                renter.vip_num = vip_num
                renter.save(update_fields=["vip_num"])
            renters.append(renter)
        return renters

    def _seed_rentals(self, bikes: list[Bike], renters: list[Renter]) -> list[Rental]:
        desired_pairs = [
            (bikes[1], renters[0]),
            (bikes[2], renters[1]),
        ]

        rentals: list[Rental] = []
        for bike, renter in desired_pairs:
            rental = Rental(bike=bike, renter=renter)
            rental.calc_price()
            rental.save()
            rentals.append(rental)
        return rentals

