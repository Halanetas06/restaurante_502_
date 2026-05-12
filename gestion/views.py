from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
from django import forms 
from decimal import Decimal

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=[
                ('Disponible', 'Disponible'),
                ('Ocupada', 'Ocupada'),
                ('Reservada', 'Reservada'),
                ('Mantenimiento', 'Mantenimiento'),
            ])
        }

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input-style'})

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input-style'})

def vista_login(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    
    return render(request, 'gestion/login.html', {'form': form})

def vista_registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Error en el registro. Verifica los datos.")
    else:
        form = UserCreationForm()
    
    return render(request, 'gestion/registro.html', {'form': form})

def vista_logout(request):
    logout(request)
    return redirect('login')

def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(), 
        'total_facturas': Factura.objects.count(), 
    }
    return render(request, 'gestion/inicio.html', context)

def lista_clientes(request):

    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})

def lista_empleados(request):

    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})

def lista_mesas(request):

    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})

def lista_platos(request):

    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})

def lista_ordenes(request):

    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})

def lista_facturas(request):

    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})

#Empleado

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'gestion/form_empleado.html', {'form': form, 'titulo': 'Agregar Empleado'})

def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id) 
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'gestion/form_empleado.html', {'form': form, 'titulo': 'Editar Empleado'})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, "Empleado eliminado.")
        return redirect('lista_empleados')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': empleado, 
        'tipo': 'empleado',
        'url_cancelar': 'lista_empleados'
    })

# Cliente

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente registrado exitosamente.")
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'gestion/form_cliente.html', {'form': form, 'titulo': 'Registrar Cliente'})

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del cliente actualizados.")
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/form_cliente.html', {'form': form, 'titulo': 'Editar Cliente'})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect('lista_clientes')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': cliente, 
        'tipo': 'cliente',
        'url_cancelar': 'lista_clientes'
    })

# Mesas

def lista_mesas(request):
    mesas = Mesa.objects.all().order_by('numero_mesa')
    return render(request, 'gestion/mesas.html', {'mesas': mesas})

def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesa creada exitosamente.")
            return redirect('lista_mesas')
    else:
        form = MesaForm()
    return render(request, 'gestion/form_mesa.html', {'form': form, 'titulo': 'Agregar Mesa'})

def editar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mesa #{mesa.numero_mesa} actualizada.") 
            return redirect('lista_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'gestion/form_mesa.html', {'form': form, 'titulo': 'Editar Mesa'})

def eliminar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        num = mesa.numero_mesa
        mesa.delete()
        messages.success(request, f"Mesa #{num} eliminada.")
        return redirect('lista_mesas')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': mesa, 
        'tipo': 'mesa', 
        'url_cancelar': 'lista_mesas'
    })

# Platos

def lista_platos(request):
    platos = Plato.objects.all().order_by('categoria', 'nombre_plato')
    return render(request, 'gestion/platos.html', {'platos': platos})

def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Plato añadido al menú correctamente.")
            return redirect('lista_platos')
    else:
        form = PlatoForm()
    return render(request, 'gestion/form_plato.html', {'form': form, 'titulo': 'Nuevo Plato'})

def editar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, f"Plato '{plato.nombre_plato}' actualizado.")
            return redirect('lista_platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'gestion/form_plato.html', {'form': form, 'titulo': 'Editar Plato'})

def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        nombre = plato.nombre_plato
        plato.delete()
        messages.success(request, f"El plato '{nombre}' ha sido eliminado.")
        return redirect('lista_platos')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': plato, 
        'tipo': 'plato', 
        'url_cancelar': 'lista_platos'
    })

# Ordenes

def lista_ordenes(request):
    ordenes = Orden.objects.all().order_by('-id')
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save()
            messages.success(request, f"Orden #{orden.id} creada exitosamente.")
            return redirect('lista_ordenes')
    else:
        form = OrdenForm()
    return render(request, 'gestion/form_orden.html', {'form': form, 'titulo': 'Nueva Orden'})

def editar_orden(request, id):
    orden = get_object_or_404(Orden, id=id)
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, f"Orden #{orden.id} actualizada.")
            return redirect('lista_ordenes')
    else:
        form = OrdenForm(instance=orden)
    return render(request, 'gestion/form_orden.html', {'form': form, 'titulo': 'Editar Orden'})

def eliminar_orden(request, id):
    orden = get_object_or_404(Orden, id=id)
    if request.method == 'POST':
        id_temp = orden.id
        orden.delete()
        messages.success(request, f"Orden #{id_temp} eliminada correctamente.")
        return redirect('lista_ordenes')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': orden, 
        'tipo': 'orden', 
        'url_cancelar': 'lista_ordenes'
    })

# Facturas

def lista_facturas(request):
    facturas = Factura.objects.all().order_by('-id')
    return render(request, 'gestion/facturas.html', {'facturas': facturas})

def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            
            orden_vinculada = factura.orden
            factura.subtotal = orden_vinculada.total
            factura.impuesto = factura.subtotal * Decimal('0.19')
            factura.total_factura = factura.subtotal + factura.impuesto
            
            factura.save()
            
            orden_vinculada.estado_orden = 'Facturada'
            orden_vinculada.save()
            
            messages.success(request, f"Factura #{factura.id} generada con éxito.")
            return redirect('lista_facturas')
    else:
        form = FacturaForm()
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-input-style'})
            
    return render(request, 'gestion/form_factura.html', {
        'form': form, 
        'titulo': 'Nueva Factura'
    })

def editar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, f"Factura #{factura.id} actualizada.")
            return redirect('lista_facturas')
    else:
        form = FacturaForm(instance=factura)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-input-style'})
            
    return render(request, 'gestion/form_factura.html', {'form': form, 'titulo': 'Editar Factura'})

def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, "Factura eliminada correctamente.")
        return redirect('lista_facturas')
    
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': factura, 
        'tipo': 'factura',
        'url_cancelar': 'lista_facturas'
    })