from django.urls import path
from .views import HomePageView, SearchView, FlightListView, HistoryView, PaymentDepositView, \
    PaymentSigninView, PaymentBalanceView,  PaymentStatementView, PaymentTransferView, PaymentTransferSubmit,\
    PaymentRegister, PaymentAccountChoose, PaymentFunctionChoose

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('searchflight/', SearchView.as_view(), name='search'),
    path('searchresults/', FlightListView.as_view(), name='result'),
    # payment

    path('history/', HistoryView.as_view(), name='history'),
    path('deposit/', PaymentDepositView.as_view(), name='deposit'),
    path('balance/', PaymentBalanceView.as_view(), name='balance'),
    path('statement/', PaymentStatementView.as_view(), name='statement'),
    path('transfer/', PaymentTransferView.as_view(), name='transfer'),
    path('paymenttransfersubmit/', PaymentTransferSubmit.as_view(), name='submit_transfer'),
    path('paymentregister/', PaymentRegister.as_view(), name='payment_register'),
    path('paymentlogin/', PaymentSigninView.as_view(), name='payment_login'),
    path('choosepayment/', PaymentAccountChoose.as_view(), name='payment_account'),
    path('choosepaymentfunction/', PaymentFunctionChoose.as_view(), name='payment_function'),
]
