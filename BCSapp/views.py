from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout

from .models import Transaction
from .transaction import send_transaction
from .forms import TxDescription, UserLoginForm


def tx_list(request):
    transactions = Transaction.objects.all().order_by('-id')
    paginator = Paginator(transactions, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        try:
            response = send_transaction()
            tx = Transaction(txid=response['result'])
            tx.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        except Exception as ex:  # Internal Server Error
            messages.add_message(request, messages.INFO, 'Произошла ошибка. '
                                                         'Пожалуйста, отправьте транзакцию еще раз.')
    return render(request, 'home.html', context={'page_obj': page_obj})


@user_passes_test(lambda u: u.is_superuser)
def add_description(request):
    TxFormset = modelformset_factory(Transaction, form=TxDescription, fields=('txid', 'description',),
                                     extra=0)
    if request.method == 'POST':
        form = TxFormset(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = TxFormset()
    return render(request, 'admin.html', context={'form': form})


def detail_description(request, txid):
    tx = Transaction.objects.filter(txid=txid).first()
    if (tx.description is None) or tx.description == '':
        return redirect(reverse_lazy('home'))
    return render(request, 'desc.html', context={'tx': tx})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')