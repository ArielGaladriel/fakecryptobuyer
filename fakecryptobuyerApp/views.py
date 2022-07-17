from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, Bin
from .models import CryptoData, CustomUser
import requests
import json

def main_page(request):
    context = CryptoData.objects.all()[1:11]
    return render(request, 'fakecryptobuyerApp/main.html', {"context": context})

def new_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'fakecryptobuyerApp/registration.html', {'form':form})

def buy(request):
    context = CryptoData.objects.all()[1:11]
    if request.method == "POST":
        form = Bin(request.POST)
        if form.is_valid():
            name = request.POST['currencies']
            quantity = request.POST['quantity']
            readable_name = CryptoData.objects.get(crypto_name=name).human_name
            temp_pocket = {name: {'readable_name': readable_name, 'quantity': quantity}}
            current_user = request.user
            user_data = CustomUser.objects.get(id=current_user.id)
            try:
                user_data.pocket[name] = {'readable_name': readable_name, 'quantity': str(int(user_data.pocket[name]['quantity']) + int(quantity))}
            except KeyError:
                user_data.pocket[name] = {'readable_name': readable_name, 'quantity': str(quantity)}
            user_data.save()
            return redirect('main')
    else:
        form = Bin()
    return render(request,'fakecryptobuyerApp/purchase.html', {'form': form, 'context': context})


def get_list():
    model = CryptoData.objects.all()
    list_of_currencies = requests.get('https://api.coingecko.com/api/v3/coins/list').json()
    for i in list_of_currencies:
        a = i["id"]
        b = i["name"]
        CryptoData.objects.create(crypto_name = a, cost = 0, human_name = b)

def get_cost():
    list_of_currencies = list(CryptoData.objects.values_list("crypto_name",flat=True))[:11]
    for i in list_of_currencies:
        cost_of_currency = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={i}&vs_currencies=usd').json()[i]['usd']
        model = CryptoData.objects.get(crypto_name=i)
        model.cost = cost_of_currency
        model.save()


"""         
name = request.POST['currencies']
quantity = request.POST['quantity']
temp_pocket = {name: quantity}
current_user = request.user
user_data = CustomUser.objects.get(id=current_user.id)
            try:
                user_data.pocket[name] = str(int(user_data.pocket[name]) + int(quantity))
            except KeyError:
                user_data.pocket[name] = str(quantity)
            user_data.save()
            return redirect('main')
"""