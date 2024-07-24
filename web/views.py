from django.shortcuts import render, get_object_or_404

from .models import Categoria, Producto

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