from django.shortcuts import render, redirect
from .models import Product_Table, Product_Category, size, Embroidery, Order, Order_Products, color
import json
import uuid
from django.contrib import messages
# Create your views here.


def index(request):
    all_products = Product_Table.objects.filter(availability='Available')
    all_categories = Product_Category.objects.all()
    home = True
    context = {'all_products':all_products, 'all_categories':all_categories, 'home':home}
    return render(request, 'index.html', context)



def category_products(request, pk):
    get_cat = Product_Category.objects.get(id=pk) # specific category product getting from database
    all_products = Product_Table.objects.filter(availability='Available', Product_Category=get_cat)
    all_categories = Product_Category.objects.all()
    context = {'all_products':all_products, 'all_categories':all_categories, 'get_cat':get_cat}
    return render(request, 'index.html', context)



# product details page function
def product_details(request, pk):
    get_products = Product_Table.objects.get(id = pk) # specific product getting from database


    first_filter_sizes = size.objects.filter(Product=get_products).order_by('price').first()
    last_filter_sizes = size.objects.filter(Product=get_products).order_by('price').last()

    last_filter_Embroidery = Embroidery.objects.filter(Product=get_products).order_by('Additional_Price').last()


    first_price = first_filter_sizes.price
    last_price = last_filter_sizes.price + last_filter_Embroidery.Additional_Price
    context = {'get_products':get_products, 'first_price':first_price, 'last_price':last_price}
    return render(request, 'product_details.html', context)


# cart page
def cart(request):
    return render(request, 'cart.html')


# checkout page
def checkout(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        address_input = request.POST.get('address_input')

        cartItems = request.POST.get('cartItems')
        all_item = json.loads(cartItems)# json to python format

        print('all_item')
        print(all_item)

        var_order = Order(Order_id = str(uuid.uuid1()), Full_Name=full_name, Address=address_input, Total_Price=0)
        var_order.save()

        totalPrice = 0
        for prd in all_item:

            print(prd)
            print(prd[4])
            get_prd = Product_Table.objects.get(id=prd[4])
            get_clr = color.objects.get(id=prd[9])
            get_size = size.objects.get(id=prd[10])

            print(prd[11])
            if int(prd[11]) == 0:
                get_embroidery = None
            else:
                get_embroidery = Embroidery.objects.get(id=prd[11])

            subTotalPrice = int(prd[0]) * int(prd[2])
            totalPrice = totalPrice + subTotalPrice
            var_order_product = Order_Products(Order_id=var_order, Product=get_prd, Color=get_clr, Size=get_size, Embroidery=get_embroidery, Quantity=prd[0], Single_Price=prd[2], Subtotal_Price=subTotalPrice)
            var_order_product.save()

            messages = ["Successfully Ordered and saved to database!"]

        var_order.Total_Price = totalPrice
        var_order.save()

        all_products = Product_Table.objects.filter(availability='Available')
        all_categories = Product_Category.objects.all()
        home = True
        cart_clear = True
        context = {'all_products': all_products, 'all_categories': all_categories, 'home': home, 'cart_clear':cart_clear, 'messages':messages}
        return render(request, 'index.html', context)

    return render(request, 'checkout.html')