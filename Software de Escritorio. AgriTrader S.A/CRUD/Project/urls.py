from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import Home, Login, logoutUsuario, ListarUsuario, RegistrarUsuario, EditarUsuario, EliminarUsuario, CambiarContraseña, CambiarContraseñaModal, CambiarPerfil, ListarProductor, EditarProductor, RegistrarProductor, EliminarProductor, ListarCultivo, EditarCultivo, RegistrarCultivo, EliminarCultivo, ListarDetalle, EditarDetalle, RegistrarDetalle, EliminarDetalle, ListarResponsable, EditarResponsable, RegistrarResponsable, EliminarResponsable, ListarUnidad_Productiva, EditarUnidad_Productiva, RegistrarUnidad_Productiva, EliminarUnidad_Productiva, ListarCenso, EditarCenso, RegistrarCenso, EliminarCenso, ListarMarca_Articulo, EditarMarca_Articulo, RegistrarMarca_Articulo, EliminarMarca_Articulo, ListarModelo_Articulo, EditarModelo_Articulo, RegistrarModelo_Articulo, EliminarModelo_Articulo, ListarArticulo_Productor, EditarArticulo_Productor, RegistrarArticulo_Productor, EliminarArticulo_Productor, ListarInventario, EditarInventario, RegistrarInventario, EliminarInventario, ListarArticulo_Empresa, EditarArticulo_Empresa, RegistrarArticulo_Empresa, EliminarArticulo_Empresa, ListarNecesidad_Productor, EditarNecesidad_Productor, RegistrarNecesidad_Productor, EliminarNecesidad_Productor, reporte_productores, reporte_unidades_productivas, reporteunidadesconinventario, generar_reporteunidadespormuni, reporte_necesidades_productor
from . import views


urlpatterns = [

    #------------------------------ Inicio ------------------------------#

    path('', login_required(Home.as_view()), name="home"),
    path('accounts/login/', Login.as_view(), name="login"),
    path('logout/', login_required(logoutUsuario), name='logout'),

    #------------------------------ Usuario ------------------------------#

    path('registrarUsuario/', login_required(RegistrarUsuario.as_view()), name="registrar_Usuario"),
    path('inicioUsuario/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Usuario/listarUsuario.html'
                                    )
                                ), name="inicio_Usuario"),
    path('listarUsuario/', login_required(ListarUsuario.as_view()), name="listar_Usuario"),
    path('editarUsuario/<int:pk>/', login_required(EditarUsuario.as_view()), name="editar_Usuario"),
    path('eliminarUsuario/<int:pk>/', login_required(EliminarUsuario.as_view()), name="eliminar_Usuario"),
    path('cambiarMiContraseña/<int:pk>/', login_required(CambiarContraseña.as_view()), name="cambiar_Mi_Contraseña"),
    path('cambiarContraseña/<int:pk>/', login_required(CambiarContraseñaModal.as_view()), name="cambiar_Contraseña"),
    path('cambiarPerfil/<int:pk>/', login_required(CambiarPerfil.as_view()), name="cambiar_Perfil"),
    
    #------------------------------ Productor ------------------------------#

    path('registrarProductor/', login_required(RegistrarProductor.as_view()), name="registrar_Productor"),
    path('inicioProductor/', login_required(
    							TemplateView.as_view(
    								template_name = 'Productor/listarProductor.html'
    								)
    							), name="inicio_Productor"),
    path('listarProductor/', login_required(ListarProductor.as_view()), name="listar_Productor"),
    path('editarProductor/<int:pk>/', login_required(EditarProductor.as_view()), name="editar_Productor"),
    path('eliminarProductor/<int:pk>/', login_required(EliminarProductor.as_view()), name="eliminar_Productor"),

    #------------------------------ Cultivo ------------------------------#

    path('registrarCultivo/', login_required(RegistrarCultivo.as_view()), name="registrar_Cultivo"),
    path('inicioCultivo/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Cultivo/listarCultivo.html'
                                    )
                                ), name="inicio_Cultivo"),
    path('listarCultivo/', login_required(ListarCultivo.as_view()), name="listar_Cultivo"),
    path('editarCultivo/<int:pk>/', login_required(EditarCultivo.as_view()), name="editar_Cultivo"),
    path('eliminarCultivo/<int:pk>/', login_required(EliminarCultivo.as_view()), name="eliminar_Cultivo"),

    #------------------------------ Detalle ------------------------------#

    path('registrarDetalle/', login_required(RegistrarDetalle.as_view()), name="registrar_Detalle"),
    path('inicioDetalle/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Detalle/listarDetalle.html'
                                    )
                                ), name="inicio_Detalle"),
    path('listarDetalle/', login_required(ListarDetalle.as_view()), name="listar_Detalle"),
    path('editarDetalle/<int:pk>/', login_required(EditarDetalle.as_view()), name="editar_Detalle"),
    path('eliminarDetalle/<int:pk>/', login_required(EliminarDetalle.as_view()), name="eliminar_Detalle"),

    #------------------------------ Responsable ------------------------------#

    path('registrarResponsable/', login_required(RegistrarResponsable.as_view()), name="registrar_Responsable"),
    path('inicioResponsable/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Responsable/listarResponsable.html'
                                    )
                                ), name="inicio_Responsable"),
    path('listarResponsable/', login_required(ListarResponsable.as_view()), name="listar_Responsable"),
    path('editarResponsable/<int:pk>/', login_required(EditarResponsable.as_view()), name="editar_Responsable"),
    path('eliminarResponsable/<int:pk>/', login_required(EliminarResponsable.as_view()), name="eliminar_Responsable"),

    #------------------------------ Unidad_Productiva ------------------------------#

    path('registrarUnidad_Productiva/', login_required(RegistrarUnidad_Productiva.as_view()), name="registrar_Unidad_Productiva"),
    path('inicioUnidad_Productiva/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Unidad_Productiva/listarUnidad_Productiva.html'
                                    )
                                ), name="inicio_Unidad_Productiva"),
    path('listarUnidad_Productiva/', login_required(ListarUnidad_Productiva.as_view()),  name="listar_Unidad_Productiva"),
    path('editarUnidad_Productiva/<int:pk>/', login_required(EditarUnidad_Productiva.as_view()), name="editar_Unidad_Productiva"),
    path('eliminarUnidad_Productiva/<int:pk>/', login_required(EliminarUnidad_Productiva.as_view()), name="eliminar_Unidad_Productiva"),

    #------------------------------ Censo ------------------------------#

    path('registrarCenso/', login_required(RegistrarCenso.as_view()), name="registrar_Censo"),
    path('inicioCenso/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Censo/listarCenso.html'
                                    )
                                ), name="inicio_Censo"),
    path('listarCenso/', login_required(ListarCenso.as_view()), name="listar_Censo"),
    path('editarCenso/<int:pk>/', login_required(EditarCenso.as_view()), name="editar_Censo"),
    path('eliminarCenso/<int:pk>/', login_required(EliminarCenso.as_view()), name="eliminar_Censo"),

    #------------------------------ Marca_Articulo ------------------------------#

    path('registrarMarca_Articulo/',login_required(RegistrarMarca_Articulo.as_view()), name="registrar_Marca_Articulo"),
    path('inicioMarca_Articulo/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Marca_Articulo/listarMarca_Articulo.html'
                                    )
                                ), name="inicio_Marca_Articulo"),
    path('listarMarca_Articulo/', login_required(ListarMarca_Articulo.as_view()), name="listar_Marca_Articulo"),
    path('editarMarca_Articulo/<int:pk>/', login_required(EditarMarca_Articulo.as_view()), name="editar_Marca_Articulo"),
    path('eliminarMarca_Articulo/<int:pk>/', login_required(EliminarMarca_Articulo.as_view()), name="eliminar_Marca_Articulo"),

    #------------------------------ Modelo_Articulo ------------------------------#

    path('registrarModelo_Articulo/',login_required(RegistrarModelo_Articulo.as_view()), name="registrar_Modelo_Articulo"),
    path('inicioModelo_Articulo/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Modelo_Articulo/listarModelo_Articulo.html'
                                    )
                                ), name="inicio_Modelo_Articulo"),
    path('listarModelo_Articulo/', login_required(ListarModelo_Articulo.as_view()), name="listar_Modelo_Articulo"),
    path('editarModelo_Articulo/<int:pk>/', login_required(EditarModelo_Articulo.as_view()), name="editar_Modelo_Articulo"),
    path('eliminarModelo_Articulo/<int:pk>/', login_required(EliminarModelo_Articulo.as_view()), name="eliminar_Modelo_Articulo"),

    #------------------------------ Articulo_Productor ------------------------------#

    path('registrarArticulo_Productor/',login_required(RegistrarArticulo_Productor.as_view()), name="registrar_Articulo_Productor"),
    path('inicioArticulo_Productor/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Articulo_Productor/listarArticulo_Productor.html'
                                    )
                                ), name="inicio_Articulo_Productor"),
    path('listarArticulo_Productor/', login_required(ListarArticulo_Productor.as_view()), name="listar_Articulo_Productor"),
    path('editarArticulo_Productor/<int:pk>/', login_required(EditarArticulo_Productor.as_view()), name="editar_Articulo_Productor"),
    path('eliminarArticulo_Productor/<int:pk>/', login_required(EliminarArticulo_Productor.as_view()), name="eliminar_Articulo_Productor"),

    #------------------------------ Inventario ------------------------------#

    path('registrarInventario/',login_required(RegistrarInventario.as_view()), name="registrar_Inventario"),
    path('inicioInventario/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Inventario/listarInventario.html'
                                    )
                                ), name="inicio_Inventario"),
    path('listarInventario/', login_required(ListarInventario.as_view()), name="listar_Inventario"),
    path('editarInventario/<int:pk>/', login_required(EditarInventario.as_view()), name="editar_Inventario"),
    path('eliminarInventario/<int:pk>/', login_required(EliminarInventario.as_view()), name="eliminar_Inventario"),

    #------------------------------ Articulo_Empresa ------------------------------#

    path('registrarArticulo_Empresa/',login_required(RegistrarArticulo_Empresa.as_view()), name="registrar_Articulo_Empresa"),
    path('inicioArticulo_Empresa/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Articulo_Empresa/listarArticulo_Empresa.html'
                                    )
                                ), name="inicio_Articulo_Empresa"),
    path('listarArticulo_Empresa/', login_required(ListarArticulo_Empresa.as_view()), name="listar_Articulo_Empresa"),
    path('editarArticulo_Empresa/<int:pk>/', login_required(EditarArticulo_Empresa.as_view()), name="editar_Articulo_Empresa"),
    path('eliminarArticulo_Empresa/<int:pk>/', login_required(EliminarArticulo_Empresa.as_view()), name="eliminar_Articulo_Empresa"),

    #------------------------------ Necesidad_Productor ------------------------------#

    path('registrarNecesidad_Productor/',login_required(RegistrarNecesidad_Productor.as_view()), name="registrar_Necesidad_Productor"),
    path('inicioNecesidad_Productor/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Necesidad_Productor/listarNecesidad_Productor.html'
                                    )
                                ), name="inicio_Necesidad_Productor"),
    path('listarNecesidad_Productor/', login_required(ListarNecesidad_Productor.as_view()), name="listar_Necesidad_Productor"),
    path('editarNecesidad_Productor/<int:pk>/', login_required(EditarNecesidad_Productor.as_view()), name="editar_Necesidad_Productor"),
    path('eliminarNecesidad_Productor/<int:pk>/', login_required(EliminarNecesidad_Productor.as_view()), name="eliminar_Necesidad_Productor"),

    #------------------------------Generar reportes------------------------------#
    path('reporteProductores/', login_required(reporte_productores), name="reporteproductores"),
    path('unidadproductor/', login_required(reporte_unidades_productivas), name="reporteunidadprod"),
    path('unidadinventario/', login_required(reporteunidadesconinventario), name="reporteunidadinven"),
    path('unidadmunicipio/', login_required(generar_reporteunidadespormuni), name="reporteunidadmuni"),
    path('reporte-necesidades/', reporte_necesidades_productor, name='reporte_necesidades'),
    
    path('export-db/', views.export_db, name='export_db'),
    path('import-db/', views.import_db, name='import_db'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)