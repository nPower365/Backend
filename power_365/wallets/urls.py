from django.urls import path


from power_365.wallets.api.views import (
    currencies,
    currency,
    transactions,
    transaction_detail,
)

app_name = "wallets"

urlpatterns = [
    path("currencies/", view=currencies, name="currencies"),
    path("currencies/<pk>", view=currency, name="currency"),
    path("balances/", view=currencies, name="currencies"),
    path("transactions/", view=transactions, name="transactions"),
    path("transactions/<pk>", view=transaction_detail, name="transaction"),
]
