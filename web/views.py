from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto, Cliente, Pedido, PedidoDetalle

from .carrito import Cart

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from paypal.standard.forms import PayPalPaymentsForm

from .forms import ClienteForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.core.mail import send_mail

from django.conf import settings

# Create your views here.
""" VISTAS PARA EL  CATALOGO DE PRODUCTOS """
def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias
    }
    return render(request, 'index.html',context)

""" VISTAS PARA FILTRAR PRODUCTOS POR CATEGORIA"""
def productoPorCategoria(request,categoria_id):
    objCatalogo = Categoria.objects.get(pk=categoria_id)
    listaProducto = objCatalogo.producto_set.all()

    listaCategoria = Categoria.objects.all()

    context = {
        'categoria': listaCategoria,
        'productos': listaProducto
    }

    return render(request, 'index.html', context)

""" VISTAS PARA BUSCAR PRODUCTOS POR NOMBRE"""
def productosPorNombre(request):
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__icontains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias': listaCategorias,
        'productos': listaProductos
    }

    return render(request, 'index.html', context)

""" VISTAS PARA VER DETALLES DE UN PRODUCTO"""
def productoDetalle(request, producto_id):
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto, pk=producto_id)

    context = {
        'producto': objProducto
    }
    return render(request, 'producto.html', context)

""" VISTAS PARA EL CARRITO DE COMPRAS """

def carrito(request):
    
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1    

    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add = (objProducto, cantidad)

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(Producto, pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')

""" VISTAS PARA CLIENTES Y USUARIOS """
def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        if nuevoUsuario is not None:
            login(request, nuevoUsuario)
            return redirect('/cuenta')


    return render(request, 'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next', None)
    context = {
        'paginaDestino': paginaDestino
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['paginaDestino']

        usuarioAuth = authenticate(username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)

            return redirect('/cuenta')
        else:
            context = {
                'mensajeError': 'Usuario o contraseña incorrectos'
            }

    return render(request, 'login.html', context)

def logoutUsuario(request):
    logout(request)
    return redirect('/login')

def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'cedula': clienteEditar.cedula,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento
        }
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'formCliente': frmCliente
    }

    return render(request, 'cuenta.html', context)

def actualizarCliente(request):
    mensaje = ""

    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            #Actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellido']
            actUsuario.email = dataCliente['email']
            actUsuario.save()

            #Registrar cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.cedula = dataCliente['cedula']
            nuevoCliente.direccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()

            mensaje = 'Datos actualizados correctamente' 

    context ={
        'mensaje': mensaje,
        'formCliente': frmCliente
    }

    return render(request, 'cuenta.html', context)

""" VISTAS PARA EL PROCESO DE COMPRA """


@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'cedula': clienteEditar.cedula,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento
        }
    except:
        dataCliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
        }

    frmCliente = ClienteForm(dataCliente)

    context = {
        'formCliente': frmCliente
    }

    return render(request, 'pedido.html', context)

@login_required(login_url='/login')
def confirmarPedido(request):
    context ={}

    if request.method == 'POST':
        
        #actualizar usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellidos']
        actUsuario.save()
        #registramos o actualizamos cliente
        try:
            clientePedido = Cliente.objects.get(usuario=request.user)
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion = request.POST['direccion']
            clientePedido.save()
        except:
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion = request.POST['direccion']
            clientePedido.save()    
        #registramos nuevo pedido
        nroPedido = ''
        montoTotal = float(request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()

        #registramos el detalle del pedido
        carritoPedido = request.session.get('cart')
        for key,value in carritoPedido.items():
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            detallePedido = PedidoDetalle()
            detallePedido.pedido = nuevoPedido
            detallePedido.producto = productoPedido
            detallePedido.cantidad = int(value['cantidad'])
            detallePedido.subtotal = float(value['subtotal'])
            detallePedido.save()

        #registrar variable de sesion para el pedido
        request.session['pedido_id'] = nuevoPedido.id    

        #actualizar pedido
        nroPedido = 'PED' + nuevoPedido.fecha_registro.strftime('%Y') + str(nuevoPedido.id)
        nuevoPedido.nro_pedido = nroPedido
        nuevoPedido.monto_total = montoTotal
        nuevoPedido.save()

        #creacion del boton de paypal
        paypal_dict = {
        "business": settings.PAYPAL_USER_EMAIL,
        "amount": montoTotal,
        "item_name": "PEDIDO CODIGO: " + nroPedido,
        "invoice": nroPedido,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('/gracias')),
        "cancel_return": request.build_absolute_uri(reverse('/'))
    }    
        #create the instance
        formPaypal = PayPalPaymentsForm(initial=paypal_dict)

        context = {
            'pedido': nuevoPedido,
            'formPaypal': formPaypal
        }
        
        #limpiar carrito de compras
        carrito = Cart(request)
        carrito.clear()

    return render(request, 'pedido.html',context)

@login_required(login_url='/login')
def gracias(request):
    paypalId = request.GET.get('PayerID', None)
    context ={}
    if paypalId is not None:
        pedidoId = request.session.get('pedidoId')
        pedido = pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()

        send_mail(
            'GRACIAS POR TU COMPRA',
            'Tu nro de pedido es' + pedido.nro_pedido,
            settings.ADMIN_USER_EMAIL,
            [request.user.email],
            fail_silently=False
        )

        context = {
            'pedido': pedido
        }
    else:
        return redirect('/')

    return render(request, 'gracias.html', context)
    