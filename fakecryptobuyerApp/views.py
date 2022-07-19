from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, Bin
from .models import CryptoData, CustomUser
import requests
import json

def main_page(request):
    context = CryptoData.objects.all()[1:11]
    if request.user.is_authenticated:
        user_pocket = CustomUser.objects.get(id=request.user.id).pocket.values()
        for crypto_item in user_pocket:
            item_quantity = float(crypto_item['quantity'])
            item_cost = float(CryptoData.objects.get(human_name = crypto_item['readable_name']).cost)
            crypto_item.update({"total_cost": str(round(item_quantity * item_cost, 2))})
        return render(request, 'fakecryptobuyerApp/main.html', {"context": context, "user_pocket": user_pocket})
    else:
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
            current_user = request.user
            user_data = CustomUser.objects.get(id=current_user.id)
            cost = CryptoData.objects.get(crypto_name=name).cost
            try:
                temp_quantity = quantity
                quantity = int(user_data.pocket[name]['quantity']) + int(quantity)
                spend = str(round(float(user_data.pocket[name]['spend']) + float(cost*int(temp_quantity)),2))
            except KeyError:
                quantity = int(quantity)
                spend = str(round(cost*quantity,2))
            user_data.pocket[name] = {'readable_name': readable_name, 'quantity': quantity, 'spend': spend}
            user_data.save()
            return redirect('main')
    else:
        form = Bin()
    extra_content = currency_list()
    return render(request,'fakecryptobuyerApp/purchase.html', {'form': form, 'context': context, 'extra_content':extra_content})

def currency_list():
    list_of_currencies = list(CryptoData.objects.values_list("crypto_name",flat=True))[:11]
    list_of_costs =[float(CryptoData.objects.get(crypto_name=i).cost) for i in list_of_currencies]
    return {x: y for x,y in zip(list_of_currencies,list_of_costs)}

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