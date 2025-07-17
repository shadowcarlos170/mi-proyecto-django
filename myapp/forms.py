from django import forms
from .models import Producto,Proveedor,Cliente,Compra,Empleado,Venta,Compra,DetalleCompra,DetalleVenta
from django.forms import inlineformset_factory


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'descripcion', 'precio', 'stock', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'required': True}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'id': 'marca', 'required': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'id': 'descripcion', 'required': True}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'id': 'precio', 'step': '0.01', 'required': True}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'stock', 'min': 0, 'required': True}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'imagen'}),
        }



class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['empresa', 'contacto', 'telefono', 'direccion']
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),

            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona de contacto'}),

            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),

            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'cargo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'}),
        }



class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'empleado']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
        }

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

DetalleCompraFormSet = inlineformset_factory(
    Compra,
    DetalleCompra,
    form=DetalleCompraForm,
    extra=1,
    can_delete=True
)




class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'empleado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

DetalleVentaFormSet = inlineformset_factory(
    Venta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True
)











