from datetime import date
from datetime import time as dt_time

from django import forms

def is_booking_time_allowed(value: dt_time) -> bool:
    return value >= dt_time(hour=14, minute=0) or value <= dt_time(hour=2, minute=0)


class ReservationForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ваше имя",
                "autocomplete": "name",
            }
        ),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7 (___) ___-__-__",
                "autocomplete": "tel",
            }
        ),
    )
    reservation_date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    reservation_time = forms.TimeField(
        label="Время",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "step": 900,
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep min-date dynamic across long-running processes.
        self.fields["reservation_date"].widget.attrs["min"] = date.today().isoformat()

    def clean_phone(self) -> str:
        value = self.cleaned_data["phone"]
        stripped = "".join(ch for ch in value if ch.isdigit())
        if len(stripped) < 10:
            raise forms.ValidationError("Введите корректный номер телефона.")
        return value

    def clean_reservation_date(self):
        value = self.cleaned_data["reservation_date"]
        if value < date.today():
            raise forms.ValidationError("Дата брони не может быть в прошлом.")
        return value

    def clean_reservation_time(self):
        value = self.cleaned_data["reservation_time"]
        if not is_booking_time_allowed(value):
            raise forms.ValidationError("Бронирование доступно только с 14:00 до 02:00.")
        return value
