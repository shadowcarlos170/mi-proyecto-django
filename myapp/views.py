from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm,ProveedorForm,ClienteForm,EmpleadoForm,CompraForm,DetalleCompraForm
from .models import Producto,Proveedor,Cliente,Empleado,Compra,DetalleCompra,DetalleVenta
from django.http import JsonResponse
from .forms import  DetalleCompraFormSet
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaFormSet

from django.db.models import Count, Sum

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


#productos vistas--------------------------------------------------------

def productos(request):
    productos = Producto.objects.all()  # ordena por nombre, puedes cambiarlo
    return render(request, 'productos/Productos.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')  # nombre de la url que muestra productos
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})


def modificar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/crear_producto.html', {'form': form})
#----------------------------------------------------
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})
#---------------------------------------------------


def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')  # Ajusta al nombre correcto de tu URL
    else:
        form = ProveedorForm()
    
    return render(request, 'proveedores/crear_proveedor.html', {'form': form})

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')  # o el nombre de tu url para lista de proveedores
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/crear_proveedor.html', {'form': form})


def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores')
    return render(request, 'proveedores/confirmar_eliminacion.html', {'proveedor': proveedor})






def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedores.html', {'proveedores': proveedores})










def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/crear_cliente.html', {'form': form})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        cliente.delete()
    return redirect('clientes')





def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/empleados.html', {'empleados': empleados})

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado correctamente.')
            return redirect('empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/crear_empleado.html', {'form': form})

def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/crear_empleado.html', {'form': form})

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('empleados')
    # Opcional: si quieres página de confirmación, renderiza aquí alguna plantilla
    return redirect('empleados')


def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.total = 0  # inicializamos total
            compra.save()
            formset = DetalleCompraFormSet(request.POST, instance=compra)
            if formset.is_valid():
                detalles = formset.save(commit=False)
                total = 0
                for detalle in detalles:
                    detalle.compra = compra
                    detalle.save()
                    # Actualiza stock sumando
                    detalle.producto.stock += detalle.cantidad
                    detalle.producto.save()
                    total += detalle.cantidad * detalle.precio_unitario
                compra.total = total
                compra.save()
                formset.save_m2m()
                return redirect('compras')
        else:
            formset = DetalleCompraFormSet(request.POST)  # para mostrar errores
    else:
        form = CompraForm()
        formset = DetalleCompraFormSet()

    return render(request, 'compras/crear_compra.html', {
        'form': form,
        'formset': formset
    })


def compras(request):
    compras = Compra.objects.all().order_by('-fecha')

    compras_con_totales = []
    for compra in compras:
        total = sum([
            detalle.cantidad * detalle.precio_unitario
            for detalle in compra.detallecompra_set.all()
        ])
        compras_con_totales.append({
            'compra': compra,
            'total': total
        })

    return render(request, 'compras/compras.html', {
        'compras_con_totales': compras_con_totales
    })


def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = compra.detallecompra_set.all()

    # Calculamos subtotal para cada detalle
    total = 0
    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        total+=detalle.subtotal

    context = {
        'compra': compra,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'compras/detalle_compra.html', context)


from django.db import transaction
from django.forms import modelformset_factory
from .models import Compra, DetalleCompra
from .forms import CompraForm, DetalleCompraForm, DetalleCompraFormSet

def editar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    
    DetalleCompraFormSet = modelformset_factory(
        DetalleCompra,
        form=DetalleCompraForm,
        extra=0,
        can_delete=True
    )
    
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        formset = DetalleCompraFormSet(
            request.POST,
            queryset=DetalleCompra.objects.filter(compra=compra),
            prefix='detalles'
        )
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar compra principal
                    compra = form.save(commit=False)
                    
                    # Procesar detalles
                    detalles = formset.save(commit=False)
                    
                    # Manejar eliminación de detalles
                    for obj in formset.deleted_objects:
                        # Restaurar stock si se elimina un detalle
                        obj.producto.stock -= obj.cantidad
                        obj.producto.save()
                        obj.delete()
                    
                    # Actualizar o crear nuevos detalles
                    for detalle in detalles:
                        detalle.compra = compra
                        detalle.save()
                    
                    # Calcular total
                    compra.total = sum(
                        detalle.cantidad * detalle.precio_unitario 
                        for detalle in compra.detallecompra_set.all()
                    )
                    compra.save()
                    
                    messages.success(request, f'Compra #{compra_id} actualizada correctamente!')
                    return redirect('detalle_compra', compra_id=compra.id)
                    
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
    else:
        form = CompraForm(instance=compra)
        formset = DetalleCompraFormSet(
            queryset=DetalleCompra.objects.filter(compra=compra),
            prefix='detalles'
        )
    
    return render(request, 'compras/editar_compra.html', {
        'form': form,
        'formset': formset,
        'compra': compra
    })

def eliminar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Restaurar stock de productos
                detalles = compra.detallecompra_set.all()
                for detalle in detalles:
                    producto = detalle.producto
                    producto.stock -= detalle.cantidad  # Disminuimos el stock (compra inversa)
                    producto.save()
                
                compra.delete()
                messages.success(request, f'Compra #{compra_id} eliminada!')
                return redirect('compras')
                
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
            return redirect('detalle_compra', compra_id=compra_id)
    
    return redirect('detalle_compra', compra_id=compra_id)




#vistas para ventas

def ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    ventas_con_totales = []

    for venta in ventas:
        total = sum([
            detalle.cantidad * detalle.precio_unitario
            for detalle in venta.detalleventa_set.all()
        ])
        ventas_con_totales.append({
            'venta': venta,
            'total': total
        })

    return render(request, 'ventas/ventas.html', {
        'ventas_con_totales': ventas_con_totales
    })


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.total = 0  # inicializamos total
            venta.save()
            formset = DetalleVentaFormSet(request.POST, instance=venta)
            if formset.is_valid():
                detalles = formset.save(commit=False)
                total = 0
                for detalle in detalles:
                    detalle.venta = venta
                    detalle.save()
                    # Actualizar stock
                    detalle.producto.stock -= detalle.cantidad
                    detalle.producto.save()
                    total += detalle.cantidad * detalle.precio_unitario
                venta.total = total
                venta.save()
                formset.save_m2m()
                return redirect('ventas')
        else:
            formset = DetalleVentaFormSet(request.POST)  # para mostrar errores
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'ventas/crear_venta.html', {
        'form': form,
        'formset': formset
    })


def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalleventa_set.all()

    total = 0
    for detalle in detalles:
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        total += detalle.subtotal
        
    context = {
        'venta': venta,
        'detalles': detalles,
        'total': total,  # total de la venta para mostrar en la plantilla
    }
    return render(request, 'ventas/detalle_venta.html', context)




from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm

def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    DetalleVentaFormSet = modelformset_factory(
        DetalleVenta,
        form=DetalleVentaForm,
        extra=0,
        can_delete=True
    )
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = DetalleVentaFormSet(
            request.POST,
            queryset=DetalleVenta.objects.filter(venta=venta),
            prefix='detalles'
        )
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar venta principal
                    venta = form.save(commit=False)
                    
                    # Procesar detalles
                    detalles = formset.save(commit=False)
                    
                    # Manejar eliminación de detalles
                    for obj in formset.deleted_objects:
                        # Restaurar stock si se elimina un detalle
                        obj.producto.stock += obj.cantidad
                        obj.producto.save()
                        obj.delete()
                    
                    # Actualizar o crear nuevos detalles
                    for detalle in detalles:
                        detalle.venta = venta
                        detalle.save()
                    
                    # Calcular total
                    venta.total = sum(
                        detalle.cantidad * detalle.precio_unitario 
                        for detalle in venta.detalleventa_set.all()
                    )
                    venta.save()
                    
                    messages.success(request, f'Venta #{venta_id} actualizada correctamente!')
                    return redirect('detalle_venta', venta_id=venta.id)
                    
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleVentaFormSet(
            queryset=DetalleVenta.objects.filter(venta=venta),
            prefix='detalles'
        )
    
    return render(request, 'ventas/editar_venta.html', {
        'form': form,
        'formset': formset,
        'venta': venta
    })


from django.db import transaction
from django.contrib import messages

def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():  # Asegura que todas las operaciones sean exitosas o ninguna
                # 1. Restaurar el stock de los productos
                detalles = venta.detalleventa_set.all()
                for detalle in detalles:
                    producto = detalle.producto
                    producto.stock += detalle.cantidad  # Devolvemos el stock
                    producto.save()
                
                # 2. Eliminar la venta (esto borrará en cascada los detalles por el on_delete=CASCADE)
                venta.delete()
                
                messages.success(request, f'Venta #{venta_id} eliminada correctamente.')
                return redirect('ventas')
                
        except Exception as e:
            messages.error(request, f'Error al eliminar la venta: {str(e)}')
            return redirect('detalle_venta', venta_id=venta_id)
    
    # Si no es POST, redirige al detalle
    return redirect('detalle_venta', venta_id=venta_id)








def home(request):
    productos_por_marca = Producto.objects.values('marca').annotate(total=Count('id'))
    total_stock = Producto.objects.aggregate(stock_total=Sum('stock'))['stock_total'] or 0

    labels = [item['marca'] for item in productos_por_marca]
    data = [item['total'] for item in productos_por_marca]

    return render(request, 'home.html', {
        'labels': labels,
        'data': data,
        'total_stock': total_stock,
    })

def grafico_productos_marca(request):
    datos = Producto.objects.values('marca').annotate(cantidad=Count('id')).order_by('-cantidad')
    labels = [item['marca'] for item in datos]
    data = [item['cantidad'] for item in datos]
    return JsonResponse({'labels': labels, 'data': data})




 #reporte  productos


from xhtml2pdf import pisa
from django.http import HttpResponse
from django.utils.timezone import now


def productos_print_view(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos_print.html', {'productos': productos})


def descargar_pdf_productos(request):
    productos = Producto.objects.all()
    template_path = 'productos/productos_pdf.html'
    context = {
        'productos': productos,
        'now': now(),  # Pasamos la hora actual al template
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response






#reporete de provedores 

def proveedores_print_view(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedores_print.html', {'proveedores': proveedores})

def descargar_pdf_proveedores(request):
    proveedores = Proveedor.objects.all()
    template_path = 'proveedores/proveedores_pdf.html'
    context = {
        'proveedores': proveedores,
        'now': now(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proveedores.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response


#reporte de clientes
def clientes_print_view(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes_print.html', {'clientes': clientes})

def descargar_pdf_clientes(request):
    clientes = Cliente.objects.all()
    template_path = 'clientes/clientes_pdf.html'
    context = {
        'clientes': clientes,
        'now': now(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response
#reporte empleados


def empleados_print_view(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/empleados_print.html', {'empleados': empleados})

def descargar_pdf_empleados(request):
    empleados = Empleado.objects.all()
    template_path = 'empleados/empleados_pdf.html'
    context = {
        'empleados': empleados,
        'now': now(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="empleados.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response
# ventas y compras reportes 
# views.py


from .models import Venta, DetalleVenta

def ventas_print_view(request):
    ventas = Venta.objects.all()
    ventas_con_totales = []

    for venta in ventas:
        detalles = DetalleVenta.objects.filter(venta=venta)
        total = sum(d.cantidad * d.precio_unitario for d in detalles)
        ventas_con_totales.append({
            'venta': venta,
            'total': total
        })

    return render(request, 'ventas/ventas_print.html', {
        'ventas_con_totales': ventas_con_totales
    })


def descargar_pdf_ventas(request):
    ventas = Venta.objects.all()
    ventas_con_totales = []

    for venta in ventas:
        detalles = DetalleVenta.objects.filter(venta=venta)
        total = sum(d.cantidad * d.precio_unitario for d in detalles)
        ventas_con_totales.append({
            'venta': venta,
            'total': total
        })

    template_path = 'ventas/ventas_pdf.html'
    context = {
        'ventas_con_totales': ventas_con_totales,
        'now': now()
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response

# COMPRAS
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.timezone import now


def compras_print_view(request):
    compras = Compra.objects.all()
    compras_con_totales = []

    for compra in compras:
        detalles = DetalleCompra.objects.filter(compra=compra)
        total = sum(d.cantidad * d.precio_unitario for d in detalles)
        compras_con_totales.append({
            'compra': compra,
            'total': total
        })

    return render(request, 'compras/compras_print.html', {
        'compras_con_totales': compras_con_totales
    })


def descargar_pdf_compras(request):
    compras = Compra.objects.all()
    compras_con_totales = []

    for compra in compras:
        detalles = DetalleCompra.objects.filter(compra=compra)
        total = sum(d.cantidad * d.precio_unitario for d in detalles)
        compras_con_totales.append({
            'compra': compra,
            'total': total
        })

    template_path = 'compras/compras_pdf.html'
    context = {
        'compras_con_totales': compras_con_totales,
        'now': now()
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_compras.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err)
    return response







from .models import Venta, DetalleVenta


def imprimir_factura(request, venta_id):
    venta = Venta.objects.get(id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    # Calculamos el subtotal manualmente por cada detalle
    for d in detalles:
        d.subtotal = d.cantidad * d.precio_unitario

    total = sum(d.subtotal for d in detalles)

    template_path = 'ventas/factura_pdf.html'
    context = {
        'venta': venta,
        'detalles': detalles,
        'total': total,
        'now': now()
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_venta_{venta.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar la factura PDF')
    return response





from .models import Compra, DetalleCompra

def imprimir_factura_compra(request, compra_id):
    compra = Compra.objects.get(id=compra_id)
    detalles = DetalleCompra.objects.filter(compra=compra)

    # Calculamos subtotal manualmente
    for d in detalles:
        d.subtotal = d.cantidad * d.precio_unitario

    total = sum(d.subtotal for d in detalles)

    template_path = 'compras/factura_pdf.html'  # Asegúrate que coincida con tu template
    context = {
        'compra': compra,
        'detalles': detalles,
        'total': total,
        'now': now(),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_compra_{compra.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar la factura PDF')
    return response
