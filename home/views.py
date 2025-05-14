from django.shortcuts import render, redirect
from . import models
# Create your views here.
def dash(request):
    pizza = models.Pizza.objects.all()
    order = models.Order.objects.all().order_by('-order_date')
    context = {
        'pizzas': pizza,
        'orders': order,
    }
    return render(request, 'dash.html',context)

def order(request, order_id):
    print(order_id)
    try:
        order = models.Order.objects.get(order_id=order_id)
    except Exception as e:
        print(e)
        return redirect('/')
    print(order)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)

def order_pizza(request, pizza_id):
    pizza = models.Pizza.objects.get(id=pizza_id)
    models.Order.objects.create(pizza=pizza, user=request.user, amount=pizza.price)
    return redirect('/')