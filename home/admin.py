from django.contrib import admin
from .models import Product_Table, Product_Category, color, size, Embroidery, Order, Order_Products
# Register your models here.


admin.site.register(Product_Category)


class order_table_inline_products(admin.TabularInline):
    model = Order_Products


class show_Orders_Admin(admin.ModelAdmin):
    inlines = [order_table_inline_products]
    search_fields = ('Order_id', 'Full_Name', 'Total_Price')
    list_display = ['Order_id', 'Full_Name', 'Total_Price']
admin.site.register(Order, show_Orders_Admin)


class product_table_inline_color(admin.TabularInline):
    model = color

class product_table_inline_size(admin.TabularInline):
    model = size

class product_table_inline_Embroidery(admin.TabularInline):
    model = Embroidery


class show_product_Admin(admin.ModelAdmin):
    inlines = [product_table_inline_color, product_table_inline_size, product_table_inline_Embroidery]
    search_fields = ('Product_Name', 'Product_Category', 'availability')
    list_display = ['Product_Name', 'Product_Category', 'availability']
admin.site.register(Product_Table, show_product_Admin)