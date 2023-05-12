import requests
import json
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.contrib.auth.models import User
from .forms import SearchForm, ListForm, HistoryForm, DepositForm, DepositLoginForm, BalanceForm, StatementForm, \
    TransferForm, TransferSubmitForm, DepositRegisterForm, PaymentAccountChoiceForm, ConfirmForm, StatusForm

headers = {'Content-Type': 'application/json'}


class HomePageView(ListView):
    model = User
    template_name = 'home.html'


class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm
    success_url = reverse_lazy('result')

    def form_valid(self, form):
        data = {
            'departure_time': form.cleaned_data.get('dep_date'),
            'departure_place': form.cleaned_data.get('dep_place'),
            'destin_place': form.cleaned_data.get('dest_place')
        }
        self.request.session['search_data'] = data
        return super().form_valid(form)


# noinspection PyUnreachableCode
class FlightListView(ListView):
    template_name = 'flight_result.html'
    context_object_name = 'flight_list'
    model = ListForm
    success_url = reverse_lazy('pay')

    def get_data(self):
        data = self.request.session.get('search_data')
        flight_list = []
        print(data)
        response = requests.get('http://sc192jl.pythonanywhere.com/api/Airline/findflight', params=data)
        print(response)
        for item in response.json()['data']:
            flight_list.append(ListForm(item['flight_id'],
                                        item['departure_airport'],
                                        item['destin_airport'],
                                        item['departure_time'],
                                        item['arrival_time'],
                                        item['duration'],
                                        item['seat_price'],
                                        item['air_name'],
                                        item['flight_num'],
                                        item['aircraft_type'],
                                        item['spare_seats']))
        return flight_list

    def get_queryset(self):
        flight_list = self.get_data()
        return flight_list

    def post(self, request, *args, **kwargs):
        if request.POST.get('submit'):

            self.request.session['flight_selected'] = request.POST['submit']
            self.request.session['booking'] = 'true'
            return redirect('payment')
        return super().post(request, *args, **kwargs)


# book and pay
class BookingView(ListView):
    template_name = 'booking.html'
    success_url = reverse_lazy('home')
    context_object_name = 'confirm'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')

    def get_user_id(self):
        return self.request.session.get('uid')[self.request.session['payment']]

    def get_queryset(self):
        confirm = [ConfirmForm('Are you sure you want to book this flight?')]
        return confirm

    def post(self, request, *args, **kwargs):
        if request.POST.get('submit'):
            data = self.request.session['flight_selected'].split('|')

            flight_data = {
                "flight_id": int(data[0]),
                "payer_name": self.request.user.username,
                "payer_id": self.request.user.user_id
            }
            response1 = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/bookflight',
                                      data=json.dumps(flight_data), headers=headers)
            data1 = json.loads(response1.text)
            payment_data = {
                "payment_provider": self.request.session['payment'],
                "order_id": data1['order_id']
            }

            # 2
        return redirect('booking_status')


class BookingStatusView(ListView):
    template_name = 'status.html'
    context_object_name = 'status_list'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        elif 'uid' not in self.request.session.keys():
            return redirect('new')
        elif self.request.session['uid'] == 'None':
            return redirect('new')
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        status_list = [StatusForm(self.request.session['booking_status'])]
        return status_list



# history
class HistoryView(ListView):

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            return super().get(request, *args, **kwargs)

    template_name = 'history.html'
    context_object_name = 'order_list'
    success_url = reverse_lazy('order')

    def get_queryset(self):
        order_list = []
        send_data = {
            "payer_name": 'big boss',
            "payer_id": 1
        }
        response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/order',
                                 data=json.dumps(send_data), headers=headers)
        data = json.loads(response.text)
        for item in data['data']:
            order_list.append(HistoryForm(item['departure_airport'],
                                        item['destin_airport'],
                                        item['departure_time'],
                                        item['arrival_time'],
                                        item['duration'],
                                        item['seat_price'],
                                        item['air_name'],
                                        item['flight_num'],
                                        item['aircraft_type'],
                                        item['payment_provider'],
                                        item['order_id'],
                                        item['state']))
        return order_list

    def post(self, request, *args, **kwargs):
        if request.POST.get('submit'):
            order_id = request.POST['submit']
            order_data = {
                'order_id': int(order_id)
            }
            response = requests.post('http://sc192jl.pythonanywhere.com/api/Airline/cancelbooking',
                                     data=json.dumps(order_data), headers=headers)
            return redirect(reverse_lazy('order'))
        return redirect(reverse_lazy('order'))


class PaymentAccountChoose(FormView):
    form_class = PaymentAccountChoiceForm
    template_name = 'payment_account.html'
    success_url = reverse_lazy('payment_login')

    def form_valid(self, form):
        payment_name = form.cleaned_data.get('choice')
        self.request.session['payment_name'] = payment_name

        return super().form_valid(form)


# register
class PaymentRegister(FormView):
    template_name = 'payment_register.html'
    form_class = DepositRegisterForm
    success_url = reverse_lazy('home')

    def my_view(self):
        payment_name = self.request.session.get['payment_name']
        print(self.request.session.get['payment_name'])
        return render(self.request, 'payment_signup_deposit.html', {'payment_name': payment_name})

    def form_valid(self, form):
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password'),
            "name": form.cleaned_data.get('name')
        }
        payment_name = self.request.session.get('payment_name')
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/signup/', json=data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/signup/', json=data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/signup/', json=data)
        #response = requests.post('http://172.20.10.3:8080/Payment_nnr/signup/', json=data)
        print(response.json())

        return super().form_valid(form)


# login
class PaymentSigninView(FormView):
    template_name = 'payment_signup_deposit.html'
    form_class = DepositLoginForm
    success_url = reverse_lazy('payment_function')
    context_object_name = "payment_name"

    def my_view(self):
        payment_name = self.request.session.get['payment_name']
        print(self.request.session.get['payment_name'])
        return render(self.request, 'payment_signup_deposit.html', {'payment_name': payment_name})

    def form_valid(self, form):
        payment_name = self.request.session.get('payment_name')
        data = {
            "username": form.cleaned_data.get('username'),
            "password": form.cleaned_data.get('password')
        }
        uid = []
        print(payment_name)
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/signin/', json=data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/signin/', json=data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/signin/', json=data)
        else:
            return redirect('')
        uid.append(form.cleaned_data.get('username'))
        uid.append(response.json()['msg'])
        self.request.session['uid'] = uid
        print(uid)
        return super().form_valid(form)


class PaymentFunctionChoose(ListView):
    template_name = 'payment_function.html'
    model = User


class PaymentDepositView(ListView):
    template_name = 'deposit.html'
    context_object_name = 'deposit_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('uid')[1]

    def get_queryset(self):
        deposit_list = []
        if self.request.session.get('uid')[1] == "You have no account, please sign up.":
            print("@@@")
            return redirect('login_deposit.html')

        send_data = {
            "uid": self.get_user_id()
        }
        payment_name = self.request.session.get('payment_name')
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/deposit/', json=send_data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/deposit/', json=send_data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/deposit/', json=send_data)
        #response = requests.post('http://172.20.10.3:8080/' + name + '/deposit/', json=send_data)
        deposit_list.append(DepositForm(self.request.session.get('uid')[0], payment_name, response.json()['msg']))
        return deposit_list


class PaymentBalanceView(ListView):
    template_name = 'balance.html'
    context_object_name = 'balance_list'

    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('uid')[1]

    def get_queryset(self):
        if self.request.session.get('uid')[1] == "You have no account, please sign up.":
            print("###")
            return redirect('login_deposit.html')
        balance_list = []
        send_data = {
            "uid": self.get_user_id()
        }
        payment_name = self.request.session.get('payment_name')
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/balance/', json=send_data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/balance/', json=send_data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/balance/', json=send_data)
        #response = requests.post('http://172.20.10.3:8080/' + name + '/balance/', json=send_data)
        balance_list.append(BalanceForm(self.request.session.get('uid')[0], payment_name, response.json()['income'],
                                            response.json()['expense']))
        return balance_list


class PaymentStatementView(ListView):
    template_name = 'statement.html'
    context_object_name = 'statement_list'
    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_user_id(self):
        return self.request.session.get('uid')[1]

    def get_queryset(self):
        statement_list = []
        if self.request.session.get('uid')[1] == "You have no account, please sign up.":
            print("$$$")
            return redirect('login_deposit.html')
        send_data = {
            "uid": self.get_user_id()
        }
        payment_name = self.request.session.get('payment_name')
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/statement/', json=send_data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/statement/', json=send_data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/statement/', json=send_data)
        #response = requests.post('http://172.20.10.3:8080/' + name + '/statement/', json=send_data)
        for i in range(len(response.json()['msg'])):
            statement_list.append(
                StatementForm(self.request.session.get('uid')[0],
                              payment_name,
                              str(i+1),
                              response.json()['msg'][str(i)]['Time'],
                              response.json()['msg'][str(i)]['Money'],
                              response.json()['msg'][str(i)]['Recipient']))
        return statement_list


# transfer
class PaymentTransferSubmit(FormView):
    template_name = 'transfer_submit.html'
    form_class = TransferSubmitForm
    success_url = reverse_lazy('transfer')

    def form_valid(self, form):

        uid = self.request.session.get('uid')[1]
        print(uid)
        transfer_data = {
            "uid": uid,
            "password": form.cleaned_data.get('password'),
            "u2": form.cleaned_data.get('goal_username'),
            "u3": form.cleaned_data.get('goal_username'),
            "money": int(form.cleaned_data.get('money'))
        }
        self.request.session['transfer_data'] = transfer_data
        return super().form_valid(form)


class PaymentTransferView(ListView):
    template_name = 'transfer_result.html'
    context_object_name = 'transfer_list'
    # success_url = reverse_lazy('deposit')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        transfer_list = []
        send_data = self.request.session.get('transfer_data')
        payment_name = self.request.session.get('payment_name')
        if payment_name == "Payment_WS":
            response = requests.post('https://ccty.pythonanywhere.com/' + payment_name + '/transfer/', json=send_data)
        elif payment_name == "Payment_nnr":
            response = requests.post('https://sc192yz.pythonanywhere.com/' + payment_name + '/transfer/', json=send_data)
        elif payment_name == "Payment_weha":
            response = requests.post('https://sc19yx2.pythonanywhere.com/' + payment_name + '/transfer/', json=send_data)
        #response = requests.post('http://172.20.10.3:8080/Payment_nnr/transfer/', json=send_data)
        transfer_list.append(TransferForm(response.json()['msg']))
        return transfer_list

