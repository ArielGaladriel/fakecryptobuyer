About:
This is my first Django project which I made by myself from scratch. 
It is a web-site where you are able to buy crypto currency (not actually buying, I didn't add a payment system).
You can go through registration process, choose a currency from the list, insert quantity and then "buy" it. 
Before the purchase the script will show you how much you are going to spend.
Non-authenticated users have access only to the main page where they can look up exchange rates. 
Authenticated users have access to their portfolio. 
That portfolio shows the following information about every coin bought: quantity, current total cost and how much was spent.

In this project i've learned:
1. How to make custom user (by overrading UserAdmin, AbstractBaseUser and BaseUserManager classes). I made login by email instead of username. 
2. How to get data from another web-service via API. I wrote a function which can get exchange rates of all cryptocurrencies from anoter resource. 
3. How to implement scripts into Django templates. I wrote a script (on JavaScript) which dynamicly counts a total cost of an item. 

Getting Started:
Run get_list() and get_cost() from fakecryptobuyerApp.views to pre-load data about exchange rates into database 
