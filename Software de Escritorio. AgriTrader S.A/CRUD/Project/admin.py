from django.contrib import admin
from .models import Usuario, Productor, Cultivo, Detalle, Responsable, Unidad_Productiva, Censo, Marca_Articulo, Modelo_Articulo, Articulo_Productor, Inventario, Articulo_Empresa, Necesidad_Productor

# Register your models here.

@admin.register(Usuario)
class Usuario(admin.ModelAdmin):
	list_display = ('cod_usuario', 'username', 'nombre', 'apellido', 'email', 'imagen', 'usuario_administrador')

@admin.register(Productor)
class Productor(admin.ModelAdmin):
	list_display = ('cod_prod', 'tipo_cedula_prod', 'cedula_prod', 'nom_prod', 'apell_prod', 'direccion_prod', 'tipo_telef_prod', 'telef_prod', 'tipo_movil_prod', 'movil_prod', 'correo_prod')

@admin.register(Cultivo)
class Cultivo(admin.ModelAdmin):
	list_display = ('cod_cult', 'nom_cult')

@admin.register(Detalle)
class Detalle(admin.ModelAdmin):
	list_display = ('cod_det', 'cod_cult', 'areahectarea_pro')

@admin.register(Responsable)
class Responsable(admin.ModelAdmin):
	list_display = ('cod_res', 'tipo_cedula_res', 'cedula_res', 'nom_res', 'apell_res', 'direccion_res', 'tipo_telef_res', 'telef_res', 'tipo_movil_res', 'movil_res', 'correo_res')

@admin.register(Unidad_Productiva)
class Unidad_Productiva(admin.ModelAdmin):
	list_display = ('cod_uni', 'tipo_rif', 'rif_uni', 'cod_prod', 'cod_res', 'nom_uni', 'estado_uni', 'municipio_uni', 'parroquia_uni')

@admin.register(Censo)
class Censo(admin.ModelAdmin):
	list_display = ('cod_cen', 'fecha_cen', 'cod_uni', 'cod_det', 'ganado_leche', 'ganado_carne')

@admin.register(Marca_Articulo)
class Marca_Articulo(admin.ModelAdmin):
	list_display = ('cod_marca', 'marca_art')

@admin.register(Modelo_Articulo)
class Modelo_Articulo(admin.ModelAdmin):
	list_display = ('cod_modelo', 'modelo_art')

@admin.register(Articulo_Productor)
class Articulo_Productor(admin.ModelAdmin):
	list_display = ('cod_artprod', 'descrip_artprod', 'cod_marca', 'cod_modelo', 'año_artprod')

@admin.register(Inventario)
class Inventario(admin.ModelAdmin):
	list_display = ('cod_inv', 'cod_artprod', 'cant_artprod', 'cod_uni')

@admin.register(Articulo_Empresa)
class Articulo_Empresa(admin.ModelAdmin):
	list_display = ('cod_art', 'descrip_art', 'marca_art', 'modelo_art', 'precio', 'stock', 'fecha_duracion')

@admin.register(Necesidad_Productor)
class Necesidad_Productor(admin.ModelAdmin):
	list_display = ('cod_nec', 'fecha_nec', 'cod_uni', 'cod_art', 'canti_art')