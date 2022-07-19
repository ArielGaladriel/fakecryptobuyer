from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, Bin
from .models import CryptoData, CustomUser
from django.contrib.auth.decorators import login_required
import requests
import json


def main_page(request):
    context = CryptoData.objects.all()[1:11]
    if request.user.is_authenticated:
        user_pocket = CustomUser.objects.get(id=request.user.id).pocket.values() #list of items from current user's pocket
        for crypto_item in user_pocket: #every item is a dict {name of item: {readable name: value, quantity: value, an amount of money spent for this item: value} }
            item_quantity = float(crypto_item['quantity']) #get quantity of item as a float number
            item_cost = float(CryptoData.objects.get(human_name = crypto_item['readable_name']).cost) #get actual price for the item
            crypto_item.update({"total_cost": str(round(item_quantity * item_cost, 2))}) #adding current total cost for every item because I didn't store this value in database
        return render(request, 'fakecryptobuyerApp/main.html', {"context": context, "user_pocket": user_pocket}) #now we can see how much user has spent for every item and current cost
    else:
        return render(request, 'fakecryptobuyerApp/main.html', {"context": context}) #if user is not autentificated we just see current exchange rates

def new_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #auto login user after registration
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'fakecryptobuyerApp/registration.html', {'form': form})

@login_required
def buy(request): #function for buying crypto (just updating how much user has spent and for what)
    context = CryptoData.objects.all()[1:11]
    if request.method == "POST":
        form = Bin(request.POST)
        if form.is_valid(): #below we're updating values of user's pocket
            name = request.POST['currencies'] #getting values from recieved POST
            quantity = request.POST['quantity']
            current_user = request.user #getting data such as id of authorised user
            user_data = CustomUser.objects.get(id=current_user.id)
            readable_name = CryptoData.objects.get(crypto_name=name).human_name #getting data about currency from database
            cost = CryptoData.objects.get(crypto_name=name).cost
            try: #this works if user wants to buy more crypto of the same type that they already have
                temp_quantity = quantity
                quantity = int(user_data.pocket[name]['quantity']) + int(quantity)
                spend = str(round(float(user_data.pocket[name]['spend']) + float(cost*int(temp_quantity)),2))
            except KeyError: #user didn't have this type of crypto in their pocket so there will be KeyError in this case
                quantity = int(quantity)
                spend = str(round(cost*quantity,2))
            user_data.pocket[name] = {'readable_name': readable_name, 'quantity': quantity, 'spend': spend} #rewritting data about selected type of currency from user's pocket
            user_data.save()
            messages.success(request, 'Your purchase has been successful')
            return redirect('buy')
    else:
        form = Bin()
    extra_content = currency_list() #this list is needed for dynamic (JS) calculator (cost x quantity) for pre-buying evaluation into template
    return render(request,'fakecryptobuyerApp/purchase.html', {'form': form, 'context': context, 'extra_content':extra_content})

def currency_list(): #result of this function is a dict {name of currency: cost of currency} for using as context in templates
    list_of_currencies = list(CryptoData.objects.values_list("crypto_name",flat=True))[:11]
    list_of_costs =[float(CryptoData.objects.get(crypto_name=i).cost) for i in list_of_currencies]
    return {x: y for x,y in zip(list_of_currencies,list_of_costs)}

def get_list(): #function for adding to database list of all cryptocurrencies
    model = CryptoData.objects.all()
    list_of_currencies = requests.get('https://api.coingecko.com/api/v3/coins/list').json() #recieving a json file
    for i in list_of_currencies:
        a = i["id"]
        b = i["name"]
        CryptoData.objects.create(crypto_name = a, cost = 0, human_name = b)

def get_cost(): #function for updating the cost of every cryptocurrency in database (~ 13k items)
    list_of_currencies = list(CryptoData.objects.values_list("crypto_name",flat=True))[:11] #I use free API that has only 50 requests per hour so only the first 10 currencies will be updated
    for i in list_of_currencies:
        cost_of_currency = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={i}&vs_currencies=usd').json()[i]['usd'] # "i" is a crypto_name for item in CryptoData model and id for get request
        model = CryptoData.objects.get(crypto_name=i) #taking a row from CryptoData by PK(crypto_name)
        model.cost = cost_of_currency #and updating the cost for actual one
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