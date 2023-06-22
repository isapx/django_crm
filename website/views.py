from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    #revisamos si hay usuario logueado
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #autenticamos
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Has iniciado sesion")
            return redirect('home')
        else:
            messages.error(request,"Hay un error al iniciar sesion")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "Has cerrado sesion")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #autenticacion e inicio de sesion
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,"Has sido registrado con exito!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})

    return render(request,'register.html',{'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        #buscar registro
        customer_record = Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.error(request,"Debes iniciar sesion para ver esta pagina!")
        return redirect('home')
    

def delete_record(request, pk): #pk significa Primary Key
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"El registro ha sido eliminado con exito")
        return redirect('home')
    else:
        messages.error(request,"Debes iniciar sesion para ver esta pagina!")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"El registro ha sido añadido con exito")
                return redirect('home')
        return render(request,'add_record.html',{"form":form})
    else:
        messages.error(request,"Debes iniciar sesion para ver esta pagina!")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"El registro ha sido modificado con exito")
            return redirect('home')
        return render(request,'update_record.html',{"form": form, "current_record": current_record})
    else:
        messages.error(request,"Debes iniciar sesion para ver esta pagina!")
        return redirect('home')