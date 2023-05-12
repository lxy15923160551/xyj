from django import forms


class SearchForm(forms.Form):
    dep_date = forms.CharField(label='Take-off Time', error_messages={'required': 'Cannot be empty!'})
    dep_place = forms.CharField(label='Take-off Place', error_messages={'required': 'Cannot be empty!'})
    dest_place = forms.CharField(label='Land Place', error_messages={'required': 'Cannot be empty!'})


class ListForm(forms.Form):
    flight_id = forms.IntegerField
    dep_airport = forms.CharField
    dest_airport = forms.CharField
    departure_time = forms.CharField
    arrival_time = forms.CharField
    duration = forms.CharField
    seat_price = forms.CharField
    airline_name = forms.CharField
    flight_num = forms.CharField
    aircraft_type = forms.CharField
    spare_seats = forms.CharField

    def __init__(self, flight_id, dep_airport, dest_airport, departure_time, arrival_time, duration, seat_price,
                 airline_name, flight_num, aircraft_type, spare_seats):
        self.flight_id = flight_id
        self.dep_airport = dep_airport
        self.dest_airport = dest_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.seat_price = seat_price
        self.airline_name = airline_name
        self.flight_num = flight_num
        self.aircraft_type = aircraft_type
        self.spare_seats = spare_seats


class ConfirmForm(forms.Form):
    text = forms.CharField

    def __init__(self, text):
        self.text = text


class StatementForm(forms.Form):
    payment = forms.CharField
    number = forms.CharField
    time = forms.CharField
    money = forms.CharField
    recipient = forms.CharField

    def __init__(self, payment, number, time, money, recipient):
        self.payment = payment
        self.number = number
        self.time = time
        self.money = money
        self.recipient = recipient

class HistoryForm(forms.Form):
    dep_airport = forms.CharField
    dest_airport = forms.CharField
    departure_time = forms.CharField
    arrival_time = forms.CharField
    duration = forms.CharField
    seat_price = forms.CharField
    airline_name = forms.CharField
    flight_num = forms.CharField
    aircraft_type = forms.CharField
    payment_provider = forms.CharField
    order_id = forms.CharField
    state = forms.CharField

    def __init__(self, dep_airport, dest_airport, departure_time, arrival_time, duration, seat_price, airline_name,
                 flight_num, aircraft_type, payment_provider, order_id, state):
        self.dep_airport = dep_airport
        self.dest_airport = dest_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.seat_price = seat_price
        self.airline_name = airline_name
        self.flight_num = flight_num
        self.aircraft_type = aircraft_type
        self.payment_provider = payment_provider
        self.order_id = order_id
        self.state = state


# payment
class PaymentAccountChoiceForm(forms.Form):
    CHOICES = [
        ('Payment_WS', 'Payment_WS'),
        ('Payment_nnr', 'Payment_nnr'),
        ('Payment_weha', 'Payment_weha'),
        ('choice4', 'Choice 4'),
    ]
    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class DepositLoginForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})


class DepositRegisterForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})
    name = forms.CharField(label='name', error_messages={'required': 'Cannot be empty!'})


class BalanceLoginForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})


class DepositForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    deposit = forms.CharField

    def __init__(self, username, paymentname, deposit):
        self.paymentname = paymentname
        self.deposit = deposit
        self.username = username


class BalanceForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    income = forms.CharField
    expense = forms.CharField

    def __init__(self, username, paymentname, income, expense):
        self.paymentname = paymentname
        self.username = username
        self.income = income
        self.expense = expense


class StatementForm(forms.Form):
    paymentname = forms.CharField
    username = forms.CharField
    number = forms.CharField
    time = forms.CharField
    money = forms.CharField
    recipient = forms.CharField

    def __init__(self, paymentname, username, number, time, money, recipient):
        self.paymentname = paymentname
        self.username = username
        self.number = number
        self.time = time
        self.money = money
        self.recipient = recipient


class TransferSubmitForm(forms.Form):
    username = forms.CharField(label='username', error_messages={'required': 'Cannot be empty!'})
    password = forms.CharField(label='password', error_messages={'required': 'Cannot be empty!'})
    goal_username = forms.CharField(label='goal_username', error_messages={'required': 'Cannot be empty!'})
    money = forms.CharField(label='money', error_messages={'required': 'Cannot be empty!'})


class TransferForm(forms.Form):
    status = forms.CharField

    def __init__(self, status):
        self.status = status


class StatusForm(forms.Form):
    status = forms.CharField

    def __init__(self, status):
        self.status = status
