from django.db import models
import time
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, RegexValidator

# Create your models here.
#------------------------------ Usuario ------------------------------#

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombre, apellido, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username = username,
            nombre = nombre,
            apellido = apellido,
            email = self.normalize_email(email)
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, nombre, apellido, email, password):
        usuario = self.create_user(
            email,
            username = username,
            nombre = nombre,
            apellido = apellido,
            password = password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    cod_usuario = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    username = models.CharField(
        'Nombre de usuario', unique=True, max_length=100)
    nombre = models.CharField(
        'Nombre', max_length=16, validators=[MinLengthValidator(2)], blank=False, null=False)
    apellido = models.CharField(
        'Apellido', max_length=16, validators=[MinLengthValidator(2)], blank=False, null=False)
    email = models.EmailField(
        'Correo electrónico', unique=True, max_length=100, blank=False, null=False)
    imagen = models.ImageField(
        'Foto de perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank=True, null=True)
    usuario_administrador = models.BooleanField(
        default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.username = (self.username).upper()
        self.nombre = (self.nombre).upper()
        self.apellido = (self.apellido).upper()
        self.email = (self.email).upper()
        return super(Usuario, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.usuario_administrador


#------------------------------ Productor ------------------------------#


class Productor(models.Model):
    cod_prod = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_cedula_prod = models.CharField(
        max_length=2, blank=False, null=False)
    cedula_prod = models.CharField(
        'Cedula', unique=True, max_length=8, validators=[MinLengthValidator(7)], blank=False, null=False)
    nom_prod = models.CharField(
        'Nombre', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    apell_prod = models.CharField(
        'Apellido', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    direccion_prod = models.TextField(
        'Dirección', blank=False, null=False)
    tipo_telef_prod = models.CharField(
        max_length=5, blank=True, null=True)
    telef_prod = models.CharField(
        'Telefono local', max_length=7, validators=[MinLengthValidator(7)], blank=True, null=True)
    tipo_movil_prod = models.CharField(
        max_length=5, blank=False, null=False)
    movil_prod = models.CharField(
        'Telefono movil', max_length=7, validators=[MinLengthValidator(7)], blank=False, null=False)
    correo_prod = models.EmailField(
        'Correo electrónico', unique=True, max_length=100, blank=False, null=False)


    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'
        ordering = ['cedula_prod']

    def __str__(self):
        return f'{self.tipo_cedula_prod}{self.cedula_prod} {self.nom_prod} {self.apell_prod}'

    def save(self, *args, **kwargs):
        self.nom_prod = (self.nom_prod).upper()
        self.apell_prod = (self.apell_prod).upper()
        self.direccion_prod = (self.direccion_prod).upper()
        self.correo_prod = (self.correo_prod).upper()
        return super(Productor, self).save(*args, **kwargs)


#------------------------------ Cultivo ------------------------------#


class Cultivo(models.Model):
    cod_cult = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    nom_cult = models.CharField(
        'Cultivo', unique=True, max_length=30, blank=False, null=False)
   
    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'
        ordering = ['nom_cult']

    def __str__(self):
        return str(self.nom_cult)

    def save(self, *args, **kwargs):
        self.nom_cult = (self.nom_cult).upper()
        return super(Cultivo, self).save(*args, **kwargs)

#------------------------------ Detalle ------------------------------#


class Detalle(models.Model):
    cod_det = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    cod_cult = models.ForeignKey(
        Cultivo, verbose_name='Cultivo', on_delete=models.PROTECT, blank=False, null=False)
    areahectarea_pro = models.TextField(
        'Area del Cultivo', blank=False, null=False)
    nom_cult = models.CharField(
        'Cultivo', max_length=30, blank=True, null=True)
   
    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        ordering = ['cod_det']

    def __str__(self):
        return f'{self.cod_cult} Area: {self.areahectarea_pro} Ha'
    
    def save(self, *args, **kwargs):
        self.nom_cult = self.cod_cult.nom_cult
        super().save(*args, **kwargs)


#------------------------------ Responsable ------------------------------#


class Responsable(models.Model):
    cod_res = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_cedula_res = models.CharField(
        max_length=2, blank=False, null=False)
    cedula_res = models.CharField(
        'Cedula', unique=True, max_length=8, validators=[MinLengthValidator(7)], blank=False, null=False)
    nom_res = models.CharField(
        'Nombre', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    apell_res = models.CharField(
        'Apellido', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    direccion_res = models.TextField(
        'Dirección', blank=False, null=False)
    tipo_telef_res = models.CharField(
        max_length=5, blank=True, null=True)
    telef_res = models.CharField(
        'Telefono local', max_length=7, validators=[MinLengthValidator(7)], blank=True, null=True)
    tipo_movil_res = models.CharField(
        max_length=5, blank=False, null=False)
    movil_res = models.CharField(
        'Telefono movil', max_length=7, validators=[MinLengthValidator(7)], blank=False, null=False)
    correo_res = models.EmailField(
        'Correo electrónico', unique=True, max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Responsable'
        verbose_name_plural = 'Responsables'
        ordering = ['cedula_res']

    def __str__(self):
        return f'{self.tipo_cedula_res}{self.cedula_res} {self.nom_res} {self.apell_res}'

    def save(self, *args, **kwargs):
        self.nom_res = (self.nom_res).upper()
        self.apell_res = (self.apell_res).upper()
        self.direccion_res = (self.direccion_res).upper()
        self.correo_res = (self.correo_res).upper()
        return super(Responsable, self).save(*args, **kwargs)


#------------------------------ Unidad_Productiva ------------------------------#


class Unidad_Productiva(models.Model):
    cod_uni = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_rif = models.CharField(
        max_length=2, blank=False, null=False)
    rif_uni = models.CharField(
        'Rif de la unidad productiva', max_length=9, validators=[MinLengthValidator(9)], blank=False, null=False)
    cod_prod = models.ForeignKey(
        Productor, verbose_name='Productor', on_delete=models.PROTECT, blank=False, null=False)
    nom_prod = models.TextField(
        'Nombre', blank=True, null=True)
    apell_prod = models.TextField(
        'Apellido', blank=True, null=True)
    cod_res = models.ForeignKey(
        Responsable, verbose_name='Responsable', on_delete=models.PROTECT, blank=False, null=False)
    nom_res = models.TextField(
        'Nombre', blank=True, null=True)
    apell_res = models.TextField(
        'Apellido', blank=True, null=True)
    nom_uni = models.CharField(
        'Nombre de la unidad', max_length=30, validators=[MinLengthValidator(2)], blank=False, null=False)
    estado_uni = models.CharField(
        'Estado', max_length=30, blank=True, null=True)
    municipio_uni = models.CharField(
        'Municipio', max_length=30, blank=True, null=True)
    parroquia_uni = models.CharField(
        'Parroquia', max_length=30, blank=True, null=True)


    class Meta:
        verbose_name = 'Unidad Productiva'
        verbose_name_plural = 'Unidades Productivas'
        ordering = ['rif_uni']

    def __str__(self):
        return f'{self.tipo_rif}{self.rif_uni} {self.nom_uni} Productor: {self.nom_prod} {self.apell_prod}'

    def save(self, *args, **kwargs):
        self.nom_prod = self.cod_prod.nom_prod
        self.apell_prod = self.cod_prod.apell_prod
        self.nom_res = self.cod_res.nom_res
        self.apell_res = self.cod_res.apell_res
        super().save(*args, **kwargs)


#------------------------------ Censo ------------------------------#


class Censo(models.Model):
    cod_cen = models.AutoField(
        'codigo', primary_key=True, blank=False, null=False)
    fecha_cen = models.DateField(
        'Fecha del censo', auto_now=True, blank=False, null=False)
    cod_uni = models.ForeignKey(
        Unidad_Productiva, verbose_name='Rif de la unidad', blank=False, null=False, on_delete=models.PROTECT)
    nom_uni = models.TextField(
        'Nombre de la unidad', blank=True, null=True)
    tipo_det = models.CharField(
        'Opcion de detalles', max_length=2, blank=False, null=False)
    cod_det = models.ForeignKey(
        Detalle, verbose_name='Producción de cultivo', blank=True, null=True, on_delete=models.PROTECT)
    nom_cult = models.TextField(
        'Cultivo', blank=True, null=True)
    areahectarea_pro = models.TextField(
        'Area del Cultivo', blank=True, null=True)
    ganado_leche = models.CharField(
        'Producción de leche', max_length=2, blank=False, null=False)
    ganado_carne = models.CharField(
        'Producción de carne', max_length=2, blank=False, null=False)


    class Meta:
        verbose_name = 'Censo'
        verbose_name_plural = 'Censos'
        ordering = ['fecha_cen']

    def __str__(self):
        return f'{self.fecha_cen} {self.cod_uni}'
    
    def save(self, *args, **kwargs):
        self.nom_uni = self.cod_uni.nom_uni
        if self.tipo_det == 'NO':  # Si el valor de tipo_det es 'No'
            self.nom_cult = 'NO TIENE'
            self.areahectarea_pro = ''  # Establecer el valor de nom_cult en 'No Tiene'
        elif self.tipo_det== 'SI':  # Si tipo_det es SI
            self.nom_cult = self.cod_det.cod_cult.nom_cult
            self.areahectarea_pro = self.cod_det.areahectarea_pro
        super().save(*args, **kwargs)


#------------------------------ Marca_Articulo ------------------------------#


class Marca_Articulo(models.Model):
    cod_marca = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    marca_art = models.CharField(
        'Marca', unique=True, max_length=30, blank=False, null=False)

    class Meta:
        verbose_name = 'Marca del articulo'
        verbose_name_plural = 'Marca de los articulos'
        ordering = ['marca_art']

    def __str__(self):
        return str(self.marca_art)

    def save(self, *args, **kwargs):
        self.marca_art = (self.marca_art).upper()
        return super(Marca_Articulo, self).save(*args, **kwargs)


#------------------------------ Modelo_Articulo ------------------------------#


class Modelo_Articulo(models.Model):
    cod_modelo = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    modelo_art = models.CharField(
        'Modelo', unique=True, max_length=20, blank=False, null=False)

    class Meta:
        verbose_name = 'Modelo del articulo'
        verbose_name_plural = 'Modelo de los articulos'
        ordering = ['modelo_art']

    def __str__(self):
        return str(self.modelo_art)

    def save(self, *args, **kwargs):
        self.modelo_art = (self.modelo_art).upper()
        return super(Modelo_Articulo, self).save(*args, **kwargs)


#------------------------------ Articulo_Productor ------------------------------#


class Articulo_Productor(models.Model):
    cod_artprod = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    descrip_artprod = models.TextField(
        'Descripción', blank=False, null=False)
    cod_marca = models.ForeignKey(
        Marca_Articulo, verbose_name='Marca', blank=False, null=False, on_delete=models.PROTECT)
    marca_art = models.TextField(
        'Marca', blank=True, null=True)
    cod_modelo = models.ForeignKey(
        Modelo_Articulo, verbose_name='Modelo', blank=False, null=False, on_delete=models.PROTECT)
    modelo_art = models.TextField(
        'Modelo', blank=True, null=True)
    año_artprod = models.CharField(
        'Año', max_length=4, blank=False, null=False, choices=[(str(year), str(year)) for year in range(time.localtime().tm_year, 1899, -1)])

    def edadmaqui(self):
        current_year = datetime.datetime.now().year
        return current_year - int(self.año_artprod)

    class Meta:
        verbose_name = 'Articulos del Productor'
        verbose_name_plural = 'Articulos de los Productor'
        ordering = ['cod_artprod']

    def __str__(self):
        return f'{self.descrip_artprod} {self.marca_art} {self.modelo_art} Año: {self.año_artprod}'

    def save(self, *args, **kwargs):
        self.descrip_artprod = (self.descrip_artprod).upper()
        self.marca_art = self.cod_marca.marca_art
        self.modelo_art = self.cod_modelo.modelo_art
        return super(Articulo_Productor, self).save(*args, **kwargs)


#------------------------------ Inventario ------------------------------#


class Inventario(models.Model):
    cod_inv = models.AutoField(
        'Codigo del inventario', primary_key=True, blank=False, null=False)
    cod_artprod = models.ForeignKey(
        Articulo_Productor, verbose_name='Codigo del Articulo', on_delete=models.PROTECT, blank=False, null=False)
    descrip_artprod = models.TextField(
        'Descripción', blank=True, null=True)
    cod_marca = models.TextField(
        'Marca', blank=True, null=True)
    cod_modelo = models.TextField(
        'Modelo', blank=True, null=True)
    cant_artprod = models.IntegerField(
        'Cantidad', validators=[MaxValueValidator(100000), MinValueValidator(1)], blank=False, null=False)
    cod_uni = models.ForeignKey(
        Unidad_Productiva, verbose_name='Rif de la Unidad', on_delete=models.PROTECT, blank=False, null=False)
    nom_uni = models.CharField(
        'Nombre de la Unidad', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['cod_artprod']

    def __str__(self):
        return f'{self.cod_artprod} {self.cod_uni}'

    def save(self, *args, **kwargs):
        self.nom_uni = self.cod_uni.nom_uni
        self.descrip_artprod = self.cod_artprod.descrip_artprod
        self.cod_marca = self.cod_artprod.marca_art
        self.cod_modelo = self.cod_artprod.modelo_art
        super().save(*args, **kwargs)


#------------------------------ Articulo_Empresa ------------------------------#


class Articulo_Empresa(models.Model):
    cod_art = models.AutoField(
        'Codigo de la Maquinaria de la empresa', primary_key=True, blank=False, null=False)
    descrip_art = models.TextField(
        'Descripción', blank=False, null=False)
    marca_art = models.CharField(
        'Marca', max_length=20, blank=False, null=False)
    modelo_art = models.CharField(
        'Modelo', max_length=20, blank=False, null=False)
    precio = models.IntegerField(
        'Precio', validators=[MaxValueValidator(100000), MinValueValidator(1)], blank=False, null=False)
    stock = models.IntegerField(
        'Stock', validators=[MaxValueValidator(100000), MinValueValidator(1)], blank=False, null=False)
    fecha_duracion = models.DateField(
        'Tiempo de desuso', blank=False, null=False)

    class Meta:
        verbose_name = 'Articulo de la Empresa'
        verbose_name_plural = 'Articulos de la Empresa'
        ordering = ['stock']

    def __str__(self):
        return f'{self.descrip_art} {self.marca_art} {self.modelo_art} Precio: {self.precio}'

    def save(self, *args, **kwargs):
        self.descrip_art = (self.descrip_art).upper()
        self.marca_art = (self.marca_art).upper()
        self.modelo_art = (self.modelo_art).upper()
        return super(Articulo_Empresa, self).save(*args, **kwargs)


#------------------------------ Necesidad_Productor ------------------------------#


class Necesidad_Productor(models.Model):
    cod_nec = models.AutoField(
        'Codigo de la necesidad', primary_key=True, blank=False, null=False)
    fecha_nec = models.DateField(
        'Fecha de la necesidad', blank=False, null=False)
    cod_uni = models.ForeignKey(
        Unidad_Productiva, verbose_name='Codigo de la Unidad', on_delete=models.PROTECT, blank=False, null=False)
    nom_uni = models.CharField(
        'Nombre de la Unidad', max_length=30, blank=True, null=True)
    cod_art = models.ForeignKey(
        Articulo_Empresa, verbose_name='Articulo de la Empresa', on_delete=models.PROTECT, blank=False, null=False)
    descrip_art = models.TextField(
        'Descripción', blank=True, null=True)
    marca_art = models.TextField(
        'Marca', max_length=20, blank=True, null=True)
    modelo_art = models.TextField(
        'Modelo', max_length=20, blank=True, null=True)
    canti_art = models.IntegerField(
        'Cantidad del articulo', validators=[MaxValueValidator(100000), MinValueValidator(1)], blank=False, null=False)

    class Meta:
        verbose_name = 'Necesidad del productor'
        verbose_name_plural = 'Necesidades del productor'
        ordering = ['fecha_nec']

    def __str__(self):
        return f'{self.fecha_nec} {self.cod_uni}'

    def save(self, *args, **kwargs):
        self.nom_uni = self.cod_uni.nom_uni
        self.descrip_art = self.cod_art.descrip_art
        self.marca_art = self.cod_art.marca_art
        self.modelo_art = self.cod_art.modelo_art
        super().save(*args, **kwargs)