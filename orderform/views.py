from django.shortcuts import render
from .forms import pizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

# Create your views here.  
def home(request):
    return render(request, 'home.html')

def order(request):
    multiple_form= MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = pizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza=filled_form.save()
            created_pizza_pk =created_pizza.id
            note = 'Thanks for ordering! Your %s %s and %s size pizza  will be served in a short time' %(
                filled_form.cleaned_data['topping1'], filled_form.cleaned_data['topping2'], filled_form.cleaned_data['size'])
            filled_form = pizzaForm()
        else:
            created_pizza_pk= None
            note = "pizza order has failed, try again"
        context = {'pizzaform': filled_form,'created_pizza_pk':created_pizza_pk, 'note':note, 'multiple_form':multiple_form}
        return render(request, 'order.html', context)
            
             
    else:
        form =pizzaForm()
        context = {'pizzaform': form, 'multiple_form': multiple_form}
        return render(request, 'order.html', context)

def pizzas(request):
    number_of_pizzas=2
    filled_multiple_pizza_form= MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas= filled_multiple_pizza_form.cleaned_data['number']


    PizzaFormSet=formset_factory(pizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method =='POST':
        filled_formset= PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered'
        else:
            note = 'Order is not created, Please try again later'
        context ={ 'note': note,'formset':formset}
        return render(request,'pizzas.html',context)

    else:
        
        context = { 'formset': formset}
        return render(request, 'pizzas.html',context)


def edit_order(request, pk):
    pizza =Pizza.objects.get(pk=pk)
    form =pizzaForm(instance=pizza)
    if request.method=='POST':
        filled_form = pizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form=filled_form
            note ='Order has been updated'
            context={'form':form, 'pizza':pizza, 'note': note}
            return render(request, 'edit_order.html',context)
    context = {'form': form, 'pizza': pizza}
    return render(request, 'edit_order.html', context)
