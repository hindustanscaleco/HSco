from .models import DailyStock, GodownProduct


all_godown_products = GodownProduct.objects.all()
for product in all_godown_products:
    item = DailyStock()
    item.godown_products = product
    item.closing_stock = product.quantity
    item.save()

