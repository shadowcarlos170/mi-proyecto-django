from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static



urlpatterns = [
    path('', views.login_view, name='login'),         # login en la raíz
    path('home/', views.home, name='home'),           # home luego del login
    path('logout/', views.logout_view, name='logout'), # cerrar sesión
    path('productos/', views.productos, name='productos'),
   
    
    
  
    path('modificarProducto/<int:id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminarProducto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('crearProducto/', views.crear_producto, name='crear_producto'),
    
    
    
    
    


    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores_crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores_editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores_eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes_crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes_editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes_eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),


    path('empleados/', views.empleados, name='empleados'),
    path('empleados_crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados_editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados_eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),


    path('compras/', views.compras, name='compras'),
    path('compras/nueva/', views.crear_compra, name='crear_compra'),
    path('comprasdet/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('compras_editar/<int:compra_id>/', views.editar_compra, name='editar_compra'),
    path('compras_eliminar/<int:compra_id>/', views.eliminar_compra, name='eliminar_compra'),


    path('ventas/', views.ventas, name='ventas'),
    path('ventas_nueva/', views.crear_venta, name='crear_venta'),
    path('ventas_Detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),

    path('ventas_editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('ventas_eliminar/<int:venta_id>/',views.eliminar_venta, name='eliminar_venta'),

    path('productos/imprimir/', views.productos_print_view, name='productos_print'),
    path('productos/descargar_pdf/', views.descargar_pdf_productos, name='descargar_pdf_productos'),

    path('proveedores/imprimir/', views.proveedores_print_view, name='proveedores_print'),
    path('proveedores/descargar_pdf/', views.descargar_pdf_proveedores, name='descargar_pdf_proveedores'),


    path('clientes/imprimir/', views.clientes_print_view, name='clientes_print'),
    path('clientes/descargar_pdf/', views.descargar_pdf_clientes, name='descargar_pdf_clientes'),


    path('empleados/imprimir/', views.empleados_print_view, name='empleados_print'),
    path('empleados/descargar_pdf/', views.descargar_pdf_empleados, name='descargar_pdf_empleados'),

    path('ventas/imprimir/', views.ventas_print_view, name='ventas_print'),
    path('ventas/descargar_pdf/', views.descargar_pdf_ventas, name='descargar_pdf_ventas'),
    path('ventas/<int:venta_id>/imprimir/', views.imprimir_factura, name='imprimir_factura'),


    path('compras/imprimir/', views.compras_print_view, name='compras_print'),
    path('compras/descargar_pdf/', views.descargar_pdf_compras, name='descargar_pdf_compras'),


    

    path('compras/<int:compra_id>/factura/', views.imprimir_factura_compra, name='imprimir_factura_compra'),

    path('api/productos-por-marca/', views.grafico_productos_marca, name='grafico_productos_marca'),


    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

