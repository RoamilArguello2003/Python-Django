from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Productor, Cultivo, Detalle, Responsable, Unidad_Productiva, Censo, Marca_Articulo, Modelo_Articulo, Articulo_Productor, Inventario, Articulo_Empresa, Necesidad_Productor

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class FormularioLogin(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(FormularioLogin, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
		self.fields['password'].widget.attrs['class'] = 'form-control'
		self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class FormularioUsuario(forms.ModelForm):
	usuario_administrador = forms.BooleanField(required=False)

	imagen = forms.ImageField(required=False)

	password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Ingrese su contraseña',
			'id': 'password1',
			'required': 'required',
			}
		)
	)


	password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Ingrese nuevamente su contraseña',
			'id': 'password2',
			'required': 'required',
			}
		)
	)

	class Meta:
		model = Usuario
		fields = ('email', 'username', 'nombre', 'apellido', 'usuario_administrador')
		widgets = {
			'email': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico',
				}
			),
			'nombre': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre',

				}
			),
			'apellido': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido',
				}
			),
			'username': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de usuario',
				}
			)
		}

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		return password2

	def save(self, commit = True):
		usuario = super().save(commit = False)
		usuario.set_password(self.cleaned_data['password1'])
		if commit:
			usuario.save()
		return usuario

class FormularioUsuarioEdicion(forms.ModelForm):
	usuario_administrador = forms.BooleanField(required=False)
	imagen = forms.ImageField(required=False)

	class Meta:
		model = Usuario
		fields = ('email', 'username', 'nombre', 'apellido', 'imagen', 'usuario_administrador')
		widgets = {
			'email': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico',
				}
			),
			'nombre': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre',

				}
			),
			'apellido': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido',
				}
			),
			'username': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de usuario',
				}
			)
		}

	def save(self, commit=True):
		usuario = super().save(commit=False)
		if self.cleaned_data['imagen']:
			usuario.imagen = self.cleaned_data['imagen']
		if commit:
			usuario.save()
		return usuario

class ProductorForm(forms.ModelForm):
	class Meta:
		model = Productor
		fields = ['tipo_cedula_prod','cedula_prod','nom_prod', 'apell_prod', 'direccion_prod', 'tipo_telef_prod', 'telef_prod', 'tipo_movil_prod', 'movil_prod', 'correo_prod']
		label = {
			'tipo_cedula_prod': '',
			'cedula_prod': 'Cedula',
			'nom_prod': 'Nombre',
			'apell_prod': 'Apellido',
			'direccion_prod': 'Dirección',
			'tipo_telef_prod': '',
			'telef_prod': 'Telefono de casa',
			'tipo_telef_prod': '',
			'Movil_prod': 'Telefono movil',
			'correo_prod': 'Correo electrónico'
		}
		widgets = {
			'tipo_cedula_prod': forms.Select(
				choices=[('','Selecciona una opción'), ('V-', 'V-'), ('E-', 'E-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'cedula_prod': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Cedula'
				}
			),
			'nom_prod': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre'
				}
			),
			'apell_prod': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido'
				}
			),
			'direccion_prod': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Dirección',
					'rows': '1'
				}
			),
			'tipo_telef_prod': forms.Select(
				choices=[('','Selecciona una opción'), ('0255-', '0255-'), ('0256-', '0256-'), ('0257-', '0257-')],
				attrs = {
					'class': 'form-control',
				}
			),
			'telef_prod': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono de casa'
				}
			),
			'tipo_movil_prod': forms.Select(
				choices=[('','Selecciona una opción'), ('0212-', '0212-'), ('0412-', '0412-'), ('0414-', '0414-'), ('0416-', '0416-'), ('0424-', '0424-'), ('0426-', '0426-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'movil_prod': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono de movil'
				}
			),
			'correo_prod': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico'
				}
			),
		}


class CultivoForm(forms.ModelForm):
	class Meta:
		model = Cultivo
		fields = ('nom_cult',)
		label = {
			'nom_cult': 'Cultivo'
		}
		widgets ={
			'nom_cult': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre del cultivo'
				}
			)
		}


class DetalleForm(forms.ModelForm):
	class Meta:
		model = Detalle
		fields = ('cod_cult', 'areahectarea_pro')
		label = {
			'cod_cult':'Codigo del Cultivo',
			'areahectarea_pro': 'Area del Cultivo'
		}
		widgets ={
			'cod_cult': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
			'areahectarea_pro': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Area del Cultivo'
				}
			)
		}


class ResponsableForm(forms.ModelForm):
	class Meta:
		model = Responsable
		fields = ('tipo_cedula_res', 'cedula_res', 'nom_res', 'apell_res', 'direccion_res', 'tipo_telef_res', 'telef_res', 'tipo_movil_res', 'movil_res', 'correo_res')
		label = {
			'tipo_cedula_res': '',
			'cedula_res': 'Cedula',
			'nom_res': 'Nombre',
			'apell_res': 'Apellido',
			'direccion_res': 'Dirección',
			'tipo_telef_res': '',
			'telef_res': 'Telefono de casa',
			'tipo_telef_res': '',
			'Movil_res': 'Telefono movil',
			'correo_res': 'Correo electrónico'
		}
		widgets = {
			'tipo_cedula_res': forms.Select(
				choices=[('','Selecciona una opción'), ('V-', 'V-'), ('E-', 'E-')],
				attrs = {
					'class': 'form-control',
				}
			),
			'cedula_res': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Cedula'
				}
			),
			'nom_res': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre'
				}
			),
			'apell_res': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido'
				}
			),
			'direccion_res': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Dirección',
					'rows': '1'
				}
			),
			'tipo_telef_res': forms.Select(
				choices=[('','Selecciona una opción'), ('0255-', '0255-'), ('0256-', '0256-'), ('0257-', '0257-')],
				attrs = {
					'class': 'form-control',
				}
			),
			'telef_res': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono de casa'
				}
			),
			'tipo_movil_res': forms.Select(
				choices=[('','Selecciona una opción'), ('0212-', '0212-'), ('0412-', '0412-'), ('0414-', '0414-'), ('0416-', '0416-'), ('0424-', '0424-'), ('0426-', '0426-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'movil_res': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono de movil'
				}
			),
			'correo_res': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico'
				}
			),
		}


class Unidad_ProductivaForm(forms.ModelForm):
	class Meta:
		model = Unidad_Productiva
		fields = ('tipo_rif', 'rif_uni', 'cod_prod', 'cod_res', 'nom_uni', 'estado_uni', 'municipio_uni', 'parroquia_uni')
		label = {
			'tipo_rif':'',
			'rif_uni':'Rif de la unidad',
			'cod_prod': 'Codigo del Productor',
			'cod_res': 'Cedula del Responsable',
			'nom_uni': 'Nombre de la Unidad',
			'estado_uni': 'Estado de la Unidad',
			'municipio_uni': 'Municipi de la Unidad',
			'parroquia_uni': 'Parroquia de la Unidad'
		}
		widgets ={
			'tipo_rif': forms.Select(
				choices=[('','Selecciona una opción'),('J-', 'J-'), ('G-', 'G-'), ('V-', 'V-')],
				attrs = {
					'class': 'form-control'
					}
				),
			'rif_uni': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Rif de la Unidad',
				}
			),
			'cod_prod': forms.Select(
				attrs = {
					'class':'form-control'
					}
				),
			'cod_res': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'nom_uni': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de la Unidad'
				}
			),
			'estado_uni': forms.Select(
				choices=[('','Selecciona una opción'), ('PORTUGUESA', 'PORTUGUESA')],
				attrs = {
					'class': 'form-control',
					'placeholder': 'Estado'
				}
			),
			'municipio_uni': forms.Select(
				choices=[('','Selecciona una opción'), ('GUANARE', 'GUANARE'), ('JOSÉ VICENTE DE UNDA', 'JOSÉ VICENTE DE UNDA'), ('SAN GENARO DE BOCONOÍTO', 'SAN GENARO DE BOCONOÍTO'), ('SUCRE', 'SUCRE')],
				attrs = {
					'class': 'form-control',
					'placeholder': 'Municipio'
				}
			),
			'parroquia_uni': forms.Select(
				choices=[('','Selecciona una opción'), ('ANTOLÍN TOVAR ANQUINO', 'ANTOLÍN TOVAR ANQUINO'), ('BOCONOÍTO', 'BOCONOÍTO'), ('BISCUCUY', 'BISCUCUY'), ('CONCEPCIÓN', 'CONCEPCIÓN'), ('CORDOVA', 'CORDOVA'), ('CHABASQUÉN', 'CHABASQUÉN'), ('GUANARE', 'GUANARE'), ('SAN JUAN DE GUANAGUANARE', 'SAN JUAN DE GUANAGUANARE'), ('SAN JOSÉ DE LA MONTAÑA', 'SAN JOSÉ DE LA MONTAÑA'), ('SAN JOSE DE SAGUAZ', 'SAN JOSE DE SAGUAZ'), ('SAN RAFAEL PALO ALZAO', 'SAN RAFAEL PALO ALZAO'), ('PEÑA BLANCA', 'PEÑA BLANCA'), ('VILLA ROSA', 'VILLA ROSA'), ('VIRGEN DE COROMOTO', 'VIRGEN DE COROMOTO'), ('UVENCIO A VELAZQUEZ', 'UVENCIO A VELAZQUEZ')],
				attrs = {
					'class': 'form-control',
					'placeholder': 'Parroquia'
				}
			),
		}

		
class CensoForm(forms.ModelForm):
	class Meta:
		model = Censo
		fields = ('cod_uni', 'tipo_det', 'cod_det', 'ganado_leche', 'ganado_carne')
		label = {
			'cod_uni': 'Codigo de la Unidad',
			'tipo_det':'',
			'cod_det': 'Producción de cultivo',
			'ganado_leche':'Producción de leche',
			'ganado_carne': 'Producción de carne'
		}
		widgets = {
			'cod_uni': forms.Select(
				attrs = {
					'class':'form-control'
					}
				),
			'tipo_det': forms.RadioSelect(
				choices=[('SI', 'SI'), ('NO', 'NO')],
				attrs = {
					'id': 'id_tipo_det'
					}
				),
			'cod_det': forms.Select(
				attrs = {
					'class': 'form-control',
					'id': 'id_cod_det'
					}
				),
			'ganado_leche': forms.RadioSelect(
				choices=[('SI', 'SI'), ('NO', 'NO')]
				),
			'ganado_carne': forms.RadioSelect(
				choices=[('SI', 'SI'), ('NO', 'NO')],
				),
			}


class Marca_ArticuloForm(forms.ModelForm):
	class Meta:
		model = Marca_Articulo
		fields = ('marca_art',)
		label = {
			'marca_art': 'Marca'
		}
		widgets ={
			'marca_art': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Marca'
				}
			)
		}


class Modelo_ArticuloForm(forms.ModelForm):
	class Meta:
		model = Modelo_Articulo
		fields = ('modelo_art',)
		label = {
			'modelo_art': 'Modelo'
		}
		widgets ={
			'modelo_art': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Modelo'
				}
			)
		}


class Articulo_ProductorForm(forms.ModelForm):
	class Meta:
		model = Articulo_Productor
		fields = ('descrip_artprod', 'cod_marca', 'cod_modelo', 'año_artprod')
		label = {
			'descrip_artprod': 'Descripción',
			'cod_marca': 'Marca',
			'cod_modelo': 'Modelo',
			'año_artprod': 'Año'
		}
		widgets ={
			'descrip_artprod': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripcion del Articulo',
					'rows': '1'
				}
			),
			'cod_marca': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
			'cod_modelo': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
			'año_artprod': forms.Select(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Año del Articulo'
				}
			),
		}

class InventarioForm(forms.ModelForm):
	class Meta:
		model = Inventario
		fields = ('cod_artprod', 'cant_artprod', 'cod_uni')
		label = {
			'cod_artprod': 'Articulo',
			'cant_artprod': 'Cantidad',
			'cod_uni': 'Rif de la unidad'
			}
		widgets ={
			'cod_artprod': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
			'cant_artprod': forms.NumberInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad'
				}
			),
			'cod_uni': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
		}

class Articulo_EmpresaForm(forms.ModelForm):
	class Meta:
		model = Articulo_Empresa
		fields = ('descrip_art', 'marca_art', 'modelo_art', 'precio', 'stock', 'fecha_duracion')
		label = {
			'descrip_art': 'Descripción',
			'marca_art': 'Marca',
			'modelo_art': 'Modelo',
			'precio': 'Precio',
			'stock': 'Cantidad',
			'fecha_duracion': 'Tiempo de desuso'
		}
		widgets ={
			'descrip_art': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripcion del Articulo',
					'rows': '1'
				}
			),
			'marca_art': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Marca'
				}
			),
			'modelo_art': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Modelo'
				}
			),
			'precio': forms.NumberInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Precio'
				}
			),
			'stock': forms.NumberInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Stock'
				}
			),
			'fecha_duracion': forms.DateInput(
				attrs = {
					'type': 'date',	
					'class': 'form-control'
				},
				format='%Y-%m-%d'
			)
		}


class Necesidad_ProductorForm(forms.ModelForm):
	class Meta:
		model = Necesidad_Productor
		fields = ('fecha_nec', 'cod_uni', 'cod_art', 'canti_art')
		label = {
			'fecha_nec': 'Fecha',
			'cod_uni': 'Rif de la Unidad',
			'cod_art': 'Codigo del Articulo',
			'canti_art': 'Cantidad del Articulo'
		}
		widgets ={
			'fecha_nec': forms.DateInput(
				attrs = {
					'type': 'date',	
					'class': 'form-control'
				},
				format='%Y-%m-%d'
			),
			'cod_uni': forms.Select(
				attrs = {
					'class': 'form-control',
				}
			),
			'cod_art': forms.Select(
				attrs = {
					'class': 'form-control'
				}
			),
			'canti_art': forms.NumberInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Articulo'
				}
			)
		}