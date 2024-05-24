# Generated by Django 4.1.3 on 2024-05-24 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen1', models.ImageField(blank=True, null=True, upload_to='images_landing/')),
                ('imagen2', models.ImageField(blank=True, null=True, upload_to='images_landing/')),
                ('imagen3', models.ImageField(blank=True, null=True, upload_to='images_landing/')),
                ('imagen4', models.ImageField(blank=True, null=True, upload_to='images_landing/')),
                ('imagen5', models.ImageField(blank=True, null=True, upload_to='images_landing/')),
                ('texto1', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona_residencia', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(choices=[('V-', 'V-'), ('E-', 'E-'), ('J-', 'J-')], default='V-', max_length=2)),
                ('cedula', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=11, null=True)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino')], max_length=2)),
                ('f_nacimiento', models.DateField()),
                ('embarazada', models.BooleanField()),
                ('c_residencia', models.FileField(blank=True, null=True, upload_to='constancias_residencias/')),
                ('direccion', models.TextField()),
                ('patologia', models.TextField(blank=True, null=True)),
                ('rol', models.CharField(choices=[('AD', 'Administrador'), ('AL', 'Almacenista'), ('AT', 'Atención al Cliente'), ('JC', 'Jefe de Comunidad'), ('PA', 'Paciente')], default='PA', max_length=2)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidades.zona')),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
                'permissions': [('cambiar_password', 'cambiar contraseña a usuarios'), ('respaldar_db', 'Respaldar Base de datos'), ('recuperar_db', 'Recuperar Base de datos'), ('cambiar_estado_usuarios', 'cambiar estado de usuarios'), ('cambiar_estado_jornada', 'cambiar estatus de jornadas'), ('cambiar_estado_solicitudes', 'cambiar status de solicitudes'), ('entregar_solicitud_medicamentos', 'Entregar solicitud de medicamentos'), ('entregar_jornada_medicamentos', 'Entregar jornada de medicamentos'), ('ver_inicio', 'Ver inicio'), ('ver_mis_solicitudes_de_medicamentos', 'Ver mis solicitudes de medicamentos'), ('ver_mis_jornada_medicamentos', 'Ver mis jornadas de medicamentos'), ('registrar_mi_solicitud_de_medicamentos', 'Registrar mi solicitud de medicamentos'), ('registrar_mi_jornada_medicamentos', 'Registrar mi jornada de medicamentos')],
            },
        ),
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(choices=[('V-', 'V-'), ('E-', 'E-'), ('J-', 'J-')], default='V-', max_length=2)),
                ('cedula', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('patologia', models.TextField(blank=True, null=True)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino')], default='MA', max_length=2)),
                ('jefe_comunidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comunidad', to='entidades.perfil')),
            ],
            options={
                'verbose_name': 'Comunidad',
                'verbose_name_plural': 'Comunidades',
            },
        ),
        migrations.CreateModel(
            name='Beneficiado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nacionalidad', models.CharField(choices=[('V-', 'V-'), ('E-', 'E-'), ('J-', 'J-')], default='V-', max_length=2)),
                ('cedula', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=11, null=True)),
                ('genero', models.CharField(choices=[('MA', 'Masculino'), ('FE', 'Femenino')], max_length=2)),
                ('f_nacimiento', models.DateField()),
                ('embarazada', models.BooleanField()),
                ('c_residencia', models.FileField(blank=True, null=True, upload_to='constancias_residencias/')),
                ('direccion', models.TextField()),
                ('patologia', models.TextField(blank=True, null=True)),
                ('parentesco', models.CharField(blank=True, choices=[('EO', 'Esposo'), ('EA', 'Esposa'), ('HO', 'Hijo'), ('HA', 'Hija')], max_length=2, null=True)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beneficiados', to='entidades.perfil')),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidades.zona')),
            ],
            options={
                'verbose_name': 'Beneficiado',
                'verbose_name_plural': 'Beneficiados',
            },
        ),
    ]
