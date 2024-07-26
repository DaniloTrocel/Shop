from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto

from .carrito import Cart

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