from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ReservationForm
from .menu_data import (
    BEERS,
    SALADS,
    SANDWICHES,
    SANDWICH_SNACKS,
    SAUCES,
    SHOT_SETS,
    SNACK_BASKET,
    SNACK_HIGHLIGHT,
    SNACKS,
    SOFT_DRINKS,
    SPECIAL_SNACKS,
    TEA_OPTIONS,
    TINCTURE_BERRY,
    TINCTURE_CLASSIC,
    TINCTURE_CREAM,
    TINCTURE_VEGETABLE,
)
from .telegram import send_reservation_to_telegram


@require_http_methods(["GET", "POST"])
def home(request: HttpRequest) -> HttpResponse:
    feedback = None
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            sent, error_text = send_reservation_to_telegram(**form.cleaned_data)
            if sent:
                feedback = {
                    "type": "success",
                    "text": (
                        "Заявка отправлена в Telegram. Менеджер свяжется с вами для "
                        "подтверждения."
                    ),
                }
                form = ReservationForm()
            else:
                feedback = {"type": "error", "text": error_text}
        else:
            feedback = {"type": "error", "text": "Проверьте форму: есть ошибки в данных."}
    else:
        form = ReservationForm()

    context = {
        "form": form,
        "feedback": feedback,
        "sandwiches": SANDWICHES,
        "salads": SALADS,
        "snacks": SNACKS,
        "snack_highlight": SNACK_HIGHLIGHT,
        "special_snacks": SPECIAL_SNACKS,
        "sandwich_snacks": SANDWICH_SNACKS,
        "sauces": SAUCES,
        "snack_basket": SNACK_BASKET,
        "tea_options": TEA_OPTIONS,
        "soft_drinks": SOFT_DRINKS,
        "beers": BEERS,
        "tincture_berry": TINCTURE_BERRY,
        "tincture_classic": TINCTURE_CLASSIC,
        "tincture_cream": TINCTURE_CREAM,
        "tincture_vegetable": TINCTURE_VEGETABLE,
        "shot_sets": SHOT_SETS,
    }
    return render(request, "website/home.html", context)
