import json
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import IntegrityError
from django.forms.widgets import HiddenInput
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import forms
from .forms import FormularioLogin, FormularioUsuario, FormularioUsuarioEdicion, ProductorForm, CultivoForm, DetalleForm, ResponsableForm, Unidad_ProductivaForm, CensoForm, Marca_ArticuloForm, Modelo_ArticuloForm, Articulo_ProductorForm, InventarioForm, Articulo_EmpresaForm, Necesidad_ProductorForm, UploadFileForm
from .models import Usuario, Productor, Cultivo, Detalle, Responsable, Unidad_Productiva, Censo, Marca_Articulo, Modelo_Articulo, Articulo_Productor, Inventario, Articulo_Empresa, Necesidad_Productor
from django.contrib.admin.views.decorators import staff_member_required
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import date
from django.core.management import call_command
from django.conf import settings
import datetime
from django.contrib import messages


# Create your views here.

#------------------------------ INICIO ------------------------------#


class Home(TemplateView):
    template_name = 'Inicio/index.html'

#------------------------------ LOGIN y LOGAUT ------------------------------#


class Login(FormView):
    template_name = 'Inicio/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)
    
    def form_invalid(self, form):
        # Add error message to form
        messages.error(self.request, 'Usuario o contraseña incorrecta')
        return super().form_invalid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


#------------------------------ USUARIO ------------------------------#


class ListarUsuario(View):
    model = Usuario

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Usuario')


class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuario/registrarUsuario.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email = form.cleaned_data.get('email'),
                    username = form.cleaned_data.get('username'),
                    nombre = form.cleaned_data.get('nombre'),
                    apellido = form.cleaned_data.get('apellido')
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                mensaje = f'El Usuario se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Usuario no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')


class EditarUsuario(UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEdicion
    template_name = 'Usuario/editarUsuario.html'
    context_object_name = 'usuario'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Usuario se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Usuario no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')


class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = 'Usuario/eliminarUsuario.html'
    success_url = reverse_lazy('inicio_Usuario')
    context_object_name = 'usuario'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            usuario = self.get_object()
            form.delete()
            mensaje = f'El Usuario se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Usuario')
            
class CambiarContraseña(UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Inicio/cambiarContraseña.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['imagen'].widget = forms.HiddenInput()
        form.fields['usuario_administrador'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Contraseña se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Contraseña no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('login')

class CambiarContraseñaModal(UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuario/cambiarContraseña.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['imagen'].widget = forms.HiddenInput()
        form.fields['usuario_administrador'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Contraseña se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Contraseña no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')

class CambiarPerfil(UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEdicion
    template_name = 'Inicio/cambiarPerfil.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['usuario_administrador'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            mensaje = 'El perfil se ha actualizado correctamente'
            error = 'No hay error'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                messages.success(request, mensaje)
                return redirect('home')
        else:
            mensaje = 'El perfil no se ha podido actualizar'
            error = form.errors
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
            else:
                messages.error(request, mensaje)
                return redirect('home')

#------------------------------ Productor ------------------------------#


class ListarProductor(View):
    model = Productor

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Productor')

class EditarProductor(UpdateView):
    model = Productor
    form_class = ProductorForm
    template_name = 'Productor/editarProductor.html'
    context_object_name = 'productor'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo_cedula_prod'].widget = forms.HiddenInput()
        form.fields['cedula_prod'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Productor se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Productor no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Productor')

class RegistrarProductor(CreateView):
    model = Productor
    form_class = ProductorForm
    template_name = 'Productor/registrarProductor.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Productor se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Productor no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Productor')

class EliminarProductor(DeleteView):
    model = Productor
    template_name = 'Productor/eliminarProductor.html'
    success_url = reverse_lazy('inicio_Productor')
    context_object_name = 'productor'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            productor = self.get_object()
            form.delete()
            mensaje = f'El Productor se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Productor')


#------------------------------ Cultivo ------------------------------#


class ListarCultivo(View):
    model = Cultivo

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Cultivo')

class EditarCultivo(UpdateView):
    model = Cultivo
    form_class = CultivoForm
    template_name = 'Cultivo/editarCultivo.html'
    context_object_name = 'cultivo'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Cultivo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Cultivo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Cultivo')

class RegistrarCultivo(CreateView):
    model = Cultivo
    form_class = CultivoForm
    template_name = 'Cultivo/registrarCultivo.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Cultivo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Cultivo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Cultivo')

class EliminarCultivo(DeleteView):
    model = Cultivo
    template_name = 'Cultivo/eliminarCultivo.html'
    success_url = reverse_lazy('inicio_Cultivo')
    context_object_name = 'cultivo'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cultivo = self.get_object()
            form.delete()
            mensaje = f'El Cultivo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Cultivo')


#------------------------------ Detalle ------------------------------#


class ListarDetalle(View):
    model = Detalle

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Detalle')

class EditarDetalle(UpdateView):
    model = Detalle
    form_class = DetalleForm
    template_name = 'Detalle/editarDetalle.html'
    context_object_name = 'detalle'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Detalle se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Detalle no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Detalle')

class RegistrarDetalle(CreateView):
    model = Detalle
    form_class = DetalleForm
    template_name = 'Detalle/registrarDetalle.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Detalle se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Detalle no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Detalle')

class EliminarDetalle(DeleteView):
    model = Detalle
    template_name = 'Detalle/eliminarDetalle.html'
    success_url = reverse_lazy('inicio_Detalle')
    context_object_name = 'detalle'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            detalle = self.get_object()
            form.delete()
            mensaje = f'El Detalle se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Detalle')


#------------------------------ Responsable ------------------------------#


class ListarResponsable(View):
    model = Responsable

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Responsable')

class EditarResponsable(UpdateView):
    model = Responsable
    form_class = ResponsableForm
    template_name = 'Responsable/editarResponsable.html'
    context_object_name = 'responsable'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cedula_res'].widget = forms.HiddenInput()
        form.fields['tipo_cedula_res'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Responsable se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Responsable no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Responsable')

class RegistrarResponsable(CreateView):
    model = Responsable
    form_class = ResponsableForm
    template_name = 'Responsable/registrarResponsable.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Responsable se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Responsable no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Responsable')

class EliminarResponsable(DeleteView):
    model = Responsable
    template_name = 'Responsable/eliminarResponsable.html'
    success_url = reverse_lazy('inicio_Responsable')
    context_object_name = 'responsable'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            Responsable = self.get_object()
            form.delete()
            mensaje = f'El Responsable se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Responsable')


#------------------------------ Unidad_Productiva ------------------------------#


class ListarUnidad_Productiva(View):
    model = Unidad_Productiva

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Unidad_Productiva')

class EditarUnidad_Productiva(UpdateView):
    model = Unidad_Productiva
    form_class = Unidad_ProductivaForm
    template_name = 'Unidad_Productiva/editarUnidad_Productiva.html'
    context_object_name = 'unidad_productiva'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Unidad se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Unidad no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Unidad_Productiva')

class RegistrarUnidad_Productiva(CreateView):
    model = Unidad_Productiva
    form_class = Unidad_ProductivaForm
    template_name = 'Unidad_Productiva/registrarUnidad_Productiva.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'La Unidad se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Unidad no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Unidad_Productiva')

class EliminarUnidad_Productiva(DeleteView):
    model = Unidad_Productiva
    template_name = 'Unidad_Productiva/eliminarUnidad_Productiva.html'
    success_url = reverse_lazy('inicio_Unidad_Productiva')
    context_object_name = 'unidad_productiva'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            unidad_productiva = self.get_object()
            form.delete()
            mensaje = f'La Unidad se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Unidad_Productiva')


#------------------------------ Censo ------------------------------#


class ListarCenso(View):
    model = Censo

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Censo')

class EditarCenso(UpdateView):
    model = Censo
    form_class = CensoForm
    template_name = 'Censo/editarCenso.html'
    context_object_name = 'censo'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Censo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Censo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Censo')

class RegistrarCenso(CreateView):
    model = Censo
    form_class = CensoForm
    template_name = 'Censo/registrarCenso.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Censo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Censo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Censo')

class EliminarCenso(DeleteView):
    model = Censo
    template_name = 'Censo/eliminarCenso.html'
    success_url = reverse_lazy('inicio_Censo')
    context_object_name = 'censo'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            censo = self.get_object()
            form.delete()
            mensaje = f'El Censo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Censo')

            
#------------------------------ Marca_Articulo ------------------------------#


class ListarMarca_Articulo(View):
    model = Marca_Articulo

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Marca_Articulo')

class EditarMarca_Articulo(UpdateView):
    model = Marca_Articulo
    form_class = Marca_ArticuloForm
    template_name = 'Marca_Articulo/editarMarca_Articulo.html'
    context_object_name = 'marca_articulo'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Marca se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Marca no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Marca_Articulo')

class RegistrarMarca_Articulo(CreateView):
    model = Marca_Articulo
    form_class = Marca_ArticuloForm
    template_name = 'Marca_Articulo/registrarMarca_Articulo.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'La Marca se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Marca no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Marca_Articulo')

class EliminarMarca_Articulo(DeleteView):
    model = Marca_Articulo
    template_name = 'Marca_Articulo/eliminarMarca_Articulo.html'
    success_url = reverse_lazy('inicio_Marca_Articulo')
    context_object_name = 'marca_articulo'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            marca_articulo = self.get_object()
            form.delete()
            mensaje = f'La Marca se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Marca_Articulo')


#------------------------------ Modelo_Articulo ------------------------------#


class ListarModelo_Articulo(View):
    model = Modelo_Articulo

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Modelo_Articulo')

class EditarModelo_Articulo(UpdateView):
    model = Modelo_Articulo
    form_class = Modelo_ArticuloForm
    template_name = 'Modelo_Articulo/editarModelo_Articulo.html'
    context_object_name = 'modelo_articulo'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Modelo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Modelo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Modelo_Articulo')

class RegistrarModelo_Articulo(CreateView):
    model = Modelo_Articulo
    form_class = Modelo_ArticuloForm
    template_name = 'Modelo_Articulo/registrarModelo_Articulo.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Modelo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Modelo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Modelo_Articulo')

class EliminarModelo_Articulo(DeleteView):
    model = Modelo_Articulo
    template_name = 'Modelo_Articulo/eliminarModelo_Articulo.html'
    success_url = reverse_lazy('inicio_Modelo_Articulo')
    context_object_name = 'modelo_articulo'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            modelo_articulo = self.get_object()
            form.delete()
            mensaje = f'El Modelo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Modelo_Articulo')


#------------------------------ Articulo_Productor ------------------------------#


class ListarArticulo_Productor(View):
    model = Articulo_Productor

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Articulo_Productor')

class EditarArticulo_Productor(UpdateView):
    model = Articulo_Productor
    form_class = Articulo_ProductorForm
    template_name = 'Articulo_Productor/editarArticulo_Productor.html'
    context_object_name = 'articulo_productor'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Articulo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Articulo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Articulo_Productor')

class RegistrarArticulo_Productor(CreateView):
    model = Articulo_Productor
    form_class = Articulo_ProductorForm
    template_name = 'Articulo_Productor/registrarArticulo_Productor.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Articulo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Articulo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Articulo_Productor')

class EliminarArticulo_Productor(DeleteView):
    model = Articulo_Productor
    template_name = 'Articulo_Productor/eliminarArticulo_Productor.html'
    success_url = reverse_lazy('inicio_Articulo_Productor')
    context_object_name = 'articulo_productor'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            articulo_productor = self.get_object()
            form.delete()
            mensaje = f'El Articulo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Articulo_Productor')


#------------------------------ Inventario ------------------------------#


class ListarInventario(View):
    model = Inventario

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Inventario')

class EditarInventario(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'Inventario/editarInventario.html'
    context_object_name = 'inventario'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Inventario se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Inventario no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Inventario')

class RegistrarInventario(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'Inventario/registrarInventario.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Inventario se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Inventario no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Inventario')

class EliminarInventario(DeleteView):
    model = Inventario
    template_name = 'Inventario/eliminarInventario.html'
    success_url = reverse_lazy('inicio_Inventario')
    context_object_name = 'inventario'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            inventario = self.get_object()
            form.delete()
            mensaje = f'El Inventario se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Inventario')


#------------------------------ Articulo_Empresa ------------------------------#


class ListarArticulo_Empresa(View):
    model = Articulo_Empresa

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Articulo_Empresa')

class EditarArticulo_Empresa(UpdateView):
    model = Articulo_Empresa
    form_class = Articulo_EmpresaForm
    template_name = 'Articulo_Empresa/editarArticulo_Empresa.html'
    context_object_name = 'articulo_empresa'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Articulo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Articulo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Articulo_Empresa')

class RegistrarArticulo_Empresa(CreateView):
    model = Articulo_Empresa
    form_class = Articulo_EmpresaForm
    template_name = 'Articulo_Empresa/registrarArticulo_Empresa.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Articulo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Articulo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Articulo_Empresa')

class EliminarArticulo_Empresa(DeleteView):
    model = Articulo_Empresa
    template_name = 'Articulo_Empresa/eliminarArticulo_Empresa.html'
    success_url = reverse_lazy('inicio_Articulo_Empresa')
    context_object_name = 'articulo_empresa'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            articulo_empresa = self.get_object()
            form.delete()
            mensaje = f'El Articulo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Articulo_Empresa')


#------------------------------ Necesidad_Productor ------------------------------#


class ListarNecesidad_Productor(View):
    model = Necesidad_Productor

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Necesidad_Productor')

class EditarNecesidad_Productor(UpdateView):
    model = Necesidad_Productor
    form_class = Necesidad_ProductorForm
    template_name = 'Necesidad_Productor/editarNecesidad_Productor.html'
    context_object_name = 'necesidad_productor'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Necesidad se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Necesidad no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Necesidad_Productor')

class RegistrarNecesidad_Productor(CreateView):
    model = Necesidad_Productor
    form_class = Necesidad_ProductorForm
    template_name = 'Necesidad_Productor/registrarNecesidad_Productor.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'La Necesidad se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Necesidad no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Necesidad_Productor')

class EliminarNecesidad_Productor(DeleteView):
    model = Necesidad_Productor
    template_name = 'Necesidad_Productor/eliminarNecesidad_Productor.html'
    success_url = reverse_lazy('inicio_Necesidad_Productor')
    context_object_name = 'necesidad_productor'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            necesidad_productor = self.get_object()
            form.delete()
            mensaje = f'La Necesidad se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Necesidad_Productor')


#--------------------------------------Generar reportes--------------------------------------------#

@staff_member_required

def reporte_productores(request):
    # Obtener los datos de los productores desde la base de datos
    productores = Productor.objects.all().values_list('nom_prod', 'apell_prod', 'direccion_prod', 'tipo_movil_prod', 'movil_prod')

    # Concatenar tipo de móvil y móvil en una sola columna
    productores = [(nombre, apellido, direccion, f"{tipo} {movil}") for nombre, apellido, direccion, tipo, movil in productores]

    # Crear un objeto HttpResponse con el tipo MIME adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productores.pdf"'

    # Crear el documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Agregar encabezado con el nombre de la empresa y la fecha actual
    fecha = date.today().strftime('%d/%m/%Y')
    styles = getSampleStyleSheet()
    elements.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
    elements.append(Paragraph(fecha, styles['Normal']))
    elements.append(Paragraph('Reporte de Productores', styles['Title']))

    # Crear la tabla con los datos de los productores
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'), # Ajustar la casilla de dirección al contenido
        ('ROWHEIGHTS', (0, 1), (-1, -1), 0.3*inch), # Ajustar la altura de la fila correspondiente a la dirección
        ('COLWIDTH', (0, 0), (2, -1), 100), # Ancho de columna para Nombre, Apellido, y Dirección
        ('COLWIDTH', (3, 0), (3, -1), 100), # Ancho de columna para Móvil
    ])
    tabla_productores = Table([['Nombre', 'Apellido', 'Dirección', 'Móvil']] + list(productores), colWidths=[100, 100, 200, 100])
    tabla_productores.setStyle(style)
    elements.append(tabla_productores)

    # Agregar el número de página al pie de cada página
    def footer(canvas, doc):
        canvas.saveState()
        # Mover el origen del lienzo al pie de la página
        canvas.translate(inch, inch)
        # Dibujar el número de página
        pagina = "Página {}".format(doc.page)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(0, 0, pagina)
        canvas.restoreState()

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    # Obtener el contenido del buffer y agregarlo a la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
# def reporte_productores(request):
#     # Obtener los datos de los productores desde la base de datos
#     productores = Productor.objects.all().values_list('nom_prod', 'apell_prod', 'direccion_prod', 'tipo_movil_prod', 'movil_prod')

#     # Concatenar tipo de móvil y móvil en una sola columna
#     productores = [(nombre, apellido, direccion, f"{tipo} {movil}") for nombre, apellido, direccion, tipo, movil in productores]

#     # Crear un objeto HttpResponse con el tipo MIME adecuado
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="reporte_productores.pdf"'

#     # Crear el documento PDF
#     doc = SimpleDocTemplate(response, pagesize=landscape(letter))
#     elements = []
    
#     # Agregar encabezado con el nombre de la empresa y la fecha actual
#     fecha = date.today().strftime('%d/%m/%Y')
#     styles = getSampleStyleSheet()
#     elements.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
#     elements.append(Paragraph(fecha, styles['Normal']))
#     elements.append(Paragraph('Reporte de Productores', styles['Title']))

#     # Crear la tabla con los datos de los productores
#     style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 14),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('VALIGN', (0, 1), (-1, -1), 'TOP'), # Ajustar la casilla de dirección al contenido
#         ('ROWHEIGHTS', (0, 1), (-1, -1), 0.3*inch), # Ajustar la altura de la fila correspondiente a la dirección
#         ('COLWIDTH', (0, 0), (2, -1), 100), # Ancho de columna para Nombre, Apellido, y Dirección
#         ('COLWIDTH', (3, 0), (3, -1), 100), # Ancho de columna para Móvil
#     ])
#     tabla_productores = Table([['Nombre', 'Apellido', 'Dirección', 'Móvil']] + list(productores), colWidths=[100, 100, 200, 100])
#     tabla_productores.setStyle(style)
#     elements.append(tabla_productores)

#     # Finalmente, construir el documento PDF
#     doc.build(elements)
#     return response

def reporte_unidades_productivas(request):
    # Obtener todas las unidades productivas y sus respectivos productores
    unidades_productivas = Unidad_Productiva.objects.all().select_related('cod_prod')

    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()

    # Crear el documento PDF con reportlab
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Agregar encabezado con el nombre de la empresa y la fecha actual
    fecha = date.today().strftime('%d/%m/%Y')
    styles = getSampleStyleSheet()
    elements.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
    elements.append(Paragraph(fecha, styles['Normal']))
    elements.append(Paragraph('Reporte de Unidades Productivas', styles['Title']))

    # Crear la tabla con los datos de las unidades productivas
    data = []
    data.append(['Codigo', 'Rif', 'Unidad Productiva', 'Productor'])
    for up in unidades_productivas:
        data.append([up.cod_uni, up.rif_uni, up.nom_uni, f'{up.cod_prod.nom_prod} {up.cod_prod.apell_prod}'])
    table = Table(data, colWidths=[70, 80, 180, 180], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)

    # Agregar el número de página al pie de cada página
    def footer(canvas, doc):
        canvas.saveState()
        # Mover el origen del lienzo al pie de la página
        canvas.translate(inch, inch)
        # Dibujar el número de página
        pagina = "Página {}".format(doc.page)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(0, 0, pagina)
        canvas.restoreState()

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    # Obtener los bytes del buffer y generar la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte_unidades_productivas.pdf'

    # Obtener el contenido del buffer y agregarlo a la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def reporteunidadesconinventario(request):
    # Obtener todas las unidades productivas con su respectivo inventario
    unidades_productivas = Unidad_Productiva.objects.all().prefetch_related('inventario_set__cod_artprod__cod_marca', 'inventario_set__cod_artprod__cod_modelo')

    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()

    # Crear el documento con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_unidades_productivas_inventario.pdf"'
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Agregar encabezado con el nombre de la empresa y la fecha actual
    fecha = date.today().strftime('%d/%m/%Y')
    styles = getSampleStyleSheet()
    elements.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
    elements.append(Paragraph(fecha, styles['Normal']))
    elements.append(Paragraph('Reporte de Unidades Productivas con su inventario', styles['Title']))

    # Crear la tabla que contendrá los datos
    data = []
    headings = ['Nombre de la unidad', 'Rif de la unidad', 'Artículo', 'Descripción', 'Marca', 'Modelo', 'Cantidad']
    data.append(headings)

    for up in unidades_productivas:
        for inv in up.inventario_set.all():
            data.append([
                up.nom_uni,
                up.rif_uni,
                inv.cod_artprod.cod_artprod,
                inv.cod_artprod.descrip_artprod,
                inv.cod_artprod.cod_marca.marca_art,
                inv.cod_artprod.cod_modelo.modelo_art,
                inv.cant_artprod,
            ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
    
    elements.append(table)

    # Agregar el número de página al pie de cada página
    def footer(canvas, doc):
        canvas.saveState()
        # Mover el origen del lienzo al pie de la página
        canvas.translate(inch, inch)
        # Dibujar el número de página
        pagina = "Página {}".format(doc.page)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(0, 0, pagina)
        canvas.restoreState()

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    
    # Obtener el contenido del buffer y agregarlo a la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# def generar_reporteunidadespormuni(request):
#     municipios = set(Unidad_Productiva.objects.values_list('municipio_uni', flat=True))

#     if request.method == 'POST':
#         municipio = request.POST.get('municipio')
#         unidades_productivas = Unidad_Productiva.objects.filter(municipio_uni=municipio).select_related('cod_prod')

#         # Generar el reporte en PDF usando ReportLab
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="reporteunidadespormunicipio.pdf"'

#         p = canvas.Canvas(response)

#         # Encabezado del reporte
#         p.drawString(100, 800, f"Unidades Productivas en el municipio: {municipio}")

#         # Listar las unidades productivas
#         y = 750
#         for unidad in unidades_productivas:
#             p.drawString(100, y, f"{str(unidad)} - {str(unidad.cod_prod.nom_prod)} {str(unidad.cod_prod.apell_prod)}")
#             y -= 20

#         p.showPage()
#         p.save()
#         return response

#     return render(request, 'Reportes/generar_reporte.html', {'municipios': municipios})

def generar_reporteunidadespormuni(request):
    municipios = set(Unidad_Productiva.objects.values_list('municipio_uni', flat=True))

    if request.method == 'POST':
        municipio = request.POST.get('municipio')
        unidades_productivas = Unidad_Productiva.objects.filter(municipio_uni=municipio).select_related('cod_prod')

        # Encabezado del reporte
        titulo = f"Unidades Productivas en el municipio: {municipio}"

        # Crear la tabla de datos
        data = [['Nombre unidad', 'Rif unidad', 'Nombre Productor', 'Parroquia']]
        for unidad in unidades_productivas:
            data.append([str(unidad.nom_uni), str(unidad.tipo_rif+unidad.rif_uni), str(unidad.cod_prod.nom_prod +" "+ unidad.cod_prod.apell_prod), str(unidad.parroquia_uni)])

        # Aplicar estilos a la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        # Crear el objeto de tabla y aplicar los estilos
        tabla = Table(data)
        tabla.setStyle(style)

        # Crear un buffer de bytes para el PDF
        buffer = BytesIO()

        # Crear el documento PDF y agregar la tabla
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporteunidadespormunicipio.pdf"'
        p = SimpleDocTemplate(buffer, pagesize=letter)
        elementos = []
        # Agregar encabezado con el nombre de la empresa y la fecha actual
        fecha = date.today().strftime('%d/%m/%Y')
        styles = getSampleStyleSheet()
        elementos.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
        elementos.append(Paragraph(fecha, styles['Normal']))
        elementos.append(Paragraph(titulo))
        elementos.append(tabla)

        # Agregar el número de página al pie de cada página
        def footer(canvas, doc):
            canvas.saveState()
            # Mover el origen del lienzo al pie de la página
            canvas.translate(inch, inch)
            # Dibujar el número de página
            pagina = "Página {}".format(doc.page)
            canvas.setFont('Helvetica', 9)
            canvas.drawString(0, 0, pagina)
            canvas.restoreState()

        p.build(elementos, onFirstPage=footer, onLaterPages=footer)
        
        # Obtener el contenido del buffer y agregarlo a la respuesta HTTP
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    return render(request, 'Reportes/generar_reporte.html', {'municipios': municipios})


def reporte_necesidades_productor(request):
    # Obtener todas las necesidades del productor ordenadas por fecha
    necesidades = Necesidad_Productor.objects.all().order_by('fecha_nec')

    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()

    # Crear un objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_necesidades.pdf"'
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = []

    # Agregar encabezado con el nombre de la empresa y la fecha actual
    fecha = date.today().strftime('%d/%m/%Y')
    styles = getSampleStyleSheet()
    elements.append(Paragraph('AGRITRADER S.A.', styles['Heading2']))
    elements.append(Paragraph(fecha, styles['Normal']))
    elements.append(Paragraph('Reporte de Necesidades del Productor', styles['Title']))

    # Crear una lista con los datos de las necesidades del productor
    data = [['Fecha', 'Unidad Productiva', 'Descripción del Artículo', 'Marca', 'Modelo', 'Cantidad']]
    for necesidad in necesidades:
        data.append([necesidad.fecha_nec, necesidad.nom_uni, necesidad.descrip_art, necesidad.marca_art, necesidad.modelo_art, necesidad.canti_art])

    # Crear la tabla con los datos
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Agregar el número de página al pie de cada página
    def footer(canvas, doc):
        canvas.saveState()
        # Mover el origen del lienzo al pie de la página
        canvas.translate(inch, inch)
        # Dibujar el número de página
        pagina = "Página {}".format(doc.page)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(0, 0, pagina)
        canvas.restoreState()

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    
    # Obtener el contenido del buffer y agregarlo a la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def export_db(request):
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="backup-{timestamp}.json"'
    call_command('dumpdata', stdout=response)
    return response


def import_db(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = f"{settings.MEDIA_ROOT}/{file.name}"
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            call_command('loaddata', file_path)
            return render(request, 'Inicio/importar_database.html', {'form': form, 'success_message': 'Los datos se importaron correctamente.'})
    else:
        form = UploadFileForm()
    return render(request, 'Inicio/importar_database.html', {'form': form})