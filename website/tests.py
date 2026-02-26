from datetime import date, time, timedelta

from django.test import SimpleTestCase

from .forms import ReservationForm


class ReservationFormTests(SimpleTestCase):
    def test_form_allows_evening_time(self):
        form = ReservationForm(
            data={
                "name": "Петр",
                "phone": "+79998887766",
                "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
                "reservation_time": "21:00",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_allows_after_midnight_time(self):
        form = ReservationForm(
            data={
                "name": "Петр",
                "phone": "+79998887766",
                "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
                "reservation_time": "01:30",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_rejects_daytime_time(self):
        form = ReservationForm(
            data={
                "name": "Петр",
                "phone": "+79998887766",
                "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
                "reservation_time": time(hour=10, minute=0).strftime("%H:%M"),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("reservation_time", form.errors)

    def test_form_rejects_invalid_phone(self):
        form = ReservationForm(
            data={
                "name": "Петр",
                "phone": "12345",
                "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
                "reservation_time": "19:00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_form_rejects_past_date(self):
        form = ReservationForm(
            data={
                "name": "Петр",
                "phone": "+79998887766",
                "reservation_date": (date.today() - timedelta(days=1)).isoformat(),
                "reservation_time": "19:00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("reservation_date", form.errors)
