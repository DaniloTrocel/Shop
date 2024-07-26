class Cart:

    def __init__(self,request):
        self.request = request
        self.sesion = request.session

        cart = self.sesion.get("cart")
        montoTotal = self.sesion.get("cartMontoTotal")
        if not cart:
            cart = self.sesion["cart"] = {}
            montoTotal = self.sesion["cartMontoTotal"] = "0" 

        self.cart = cart
        self.montoTotal = float(montoTotal)

    def add(self, producto, cantidad):
        if str(producto.id) not in self.cart.keys():
            self.cart[producto.id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "cantidad": cantidad,
                "precio": str(producto.precio),
                "imagen": producto.imagen.url,
                "categoria": producto.categoria.nombre,
                "subtotal": str(producto.precio * cantidad)
            }
        else:
            #Actualizamos el carrito de compra
            for key, value in self.cart.items():
                if key == str(producto.id):
                    value["cantidad"] = str(int(value["cantidad"]) + cantidad)
                    value["subtotal"] = str(float(value["precio"]) * float(value["cantidad"]))
                    break    
        self.save()        

    def delete(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()  

    def clear(self):
        self.sesion["cart"] = {}
        self.sesion["cartMontoTotal"] = "0"

    def save(self):
        """ Guardar cambios en el carrito de compras """
        
        montoTotal = 0
        for key, value in self.cart.items():
            montoTotal += float(value["subtotal"])
        
        self.sesion["cartMontoTotal"] = montoTotal
        self.sesion["cart"] = self.cart
        self.sesion.modified = True