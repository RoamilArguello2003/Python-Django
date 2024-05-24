function listarUsuario(){
	$.ajax({
		url: "/listarUsuario/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_usuarios')){
				$('#tabla_usuarios').DataTable().clear();
				$('#tabla_usuarios').DataTable().destroy();
			}
			$('#tabla_usuarios tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['username'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apellido'] + '</td>';
				fila += '<td>' + response[i]["fields"]['email'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Cambiar Contraseña" aria-label="Cambiar Contraseña"';
				fila += ' onclick = "abrir_modal_cambioContraseña(\'/cambiarContraseña/' + response[i]["pk"] + '/\');"><i class="fa fa-lock fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Editar Usuario" aria-label="Editar Usuario"';
				fila += ' onclick = "abrir_modal_edicionUsuario(\'/editarUsuario/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Usuario" aria-label="Eliminar Usuario"';
				fila += ' onclick = "abrir_modal_eliminacionUsuario(\'/eliminarUsuario/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_usuarios tbody').append(fila);
			}
			$('#tabla_usuarios').DataTable({
				language: {
					decimal: "",
					emptyTable: "No hay información",
					info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
					infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
					infoFiltered: "(Filtrado de _MAX_ total entradas)",
					infoPostFix: "",
					thousands: ",",
					lengthMenu: "Mostrar _MENU_ Entradas",
					loadingRecords: "Cargando...",
					processing: "Procesando...",
					search: "Buscar:",
					zeroRecords: "Sin resultados encontrados",
					paginate: {
						first: "Primero",
						last: "Ultimo",
						next: "Siguiente",
						previous: "Anterior",
					},
				},
				"columns": [
					{ "data": "#" },
					{ "data": "Usuario" },
					{ "data": "Nombre" },
					{ "data": "Apellido" },
					{ "data": "Correo electronico" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarUsuario(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionUsuario').serialize(),
		url: $('#form_creacionUsuario').attr('action'),
		type: $('#form_creacionUsuario').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarUsuario();
			cerrar_modal_creacionUsuario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionUsuario(error);
			activarBoton();
		}
	});
}
function editarUsuario(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionUsuario').serialize(),
		url: $('#form_edicionUsuario').attr('action'),
		type: $('#form_edicionUsuario').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarUsuario();
			cerrar_modal_edicionUsuario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionUsuario(error);
			activarBoton();
		}
	});
}
function eliminarUsuario(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionUsuario').serialize(),
		url: $('#form_eliminacionUsuario').attr('action'),
		type: $('#form_eliminacionUsuario').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarUsuario();
			cerrar_modal_eliminacionUsuario();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Usuario tiene relación en otra tabla.');
		  }
			cerrar_modal_eliminacionUsuario();
		  activarBoton();
		}
  });
}
function cambiarContraseña(){
	activarBoton();
	$.ajax({
		data: $('#form_cambiarContraseña').serialize(),
		url: $('#form_cambiarContraseña').attr('action'),
		type: $('#form_cambiarContraseña').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarUsuario();
			cerrar_modal_cambioContraseña();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionUsuario(error);
			activarBoton();
		}
	});
}
function cambiarPerfil() {
    activarBoton();
    $.ajax({
        url: $('#form_cambiarPerfil').attr('action'),
        type: $('#form_cambiarPerfil').attr('method'),
        processData: false, // Evitar procesamiento de datos
        contentType: false, // Evitar configuración automática del tipo de contenido
        success: function(response) {
            notificacionSuccessEdicion(response.mensaje);
            listarUsuario();
            cerrar_modal_edicionUsuario();
            window.location.href = '/';
        },
        error: function(error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicionUsuario(error);
            activarBoton();
        }
    });
}
function abrir_modal_creacionUsuario(url){
	$('#creacionUsuario').load(url, function(){
		$('#creacionUnidad_Productiva').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionUsuario(){
	$('#creacionUsuario').modal('hide');
	$('#creacionUnidad_Productiva').modal('show');
}
function abrir_modal_edicionUsuario(url){
	$('#edicionUsuario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionUsuario(){
	$('#edicionUsuario').modal('hide');
}
function abrir_modal_eliminacionUsuario(url){
	$('#eliminacionUsuario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionUsuario(){
	$('#eliminacionUsuario').modal('hide');
}
function abrir_modal_cambioContraseña(url){
	$('#cambioContraseña').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_cambioContraseña(){
	$('#cambioContraseña').modal('hide');
}
function mostrarErroresCreacionUsuario(erroresUsuario){
  $('.error-email').addClass('d-none');
  $('.error-username').addClass('d-none');
  $('.error-nombre').addClass('d-none');
  $('.error-apellido').addClass('d-none');
  $('.error-password1').addClass('d-none');
  $('.error-password2').addClass('d-none');
  $('.error-usuario_administrador').addClass('d-none');
  $('.error-imagen').addClass('d-none');
  for(let item in erroresUsuario.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresUsuario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionUsuario(erroresEdicionUsuario){
  $('.error-email').addClass('d-none');
  $('.error-username').addClass('d-none');
  $('.error-nombre').addClass('d-none');
  $('.error-apellido').addClass('d-none');
  $('.error-password1').addClass('d-none');
  $('.error-password2').addClass('d-none');
  $('.error-usuario_administrador').addClass('d-none');
  $('.error-imagen').addClass('d-none');
  for(let item in erroresEdicionUsuario.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionUsuario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarUsuario();
});