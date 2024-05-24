function listarModelo_Articulo(){
	$.ajax({
		url: "/listarModelo_Articulo/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_modelos_articulos')){
				$('#tabla_modelos_articulos').DataTable().clear();
				$('#tabla_modelos_articulos').DataTable().destroy();
			}
			$('#tabla_modelos_articulos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['modelo_art'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Modelo" aria-label="Editar Modelo"';
				fila += ' onclick = "abrir_modal_edicionModelo_Articulo(\'/editarModelo_Articulo/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Modelo" aria-label="Eliminar Modelo"';
				fila += ' onclick = "abrir_modal_eliminacionModelo_Articulo(\'/eliminarModelo_Articulo/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_modelos_articulos tbody').append(fila);
			}
			$('#tabla_modelos_articulos').DataTable({
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
					{ "data": "Modelo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarModelo_Articulo(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionModelo_Articulo').serialize(),
		url: $('#form_creacionModelo_Articulo').attr('action'),
		type: $('#form_creacionModelo_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarModelo_Articulo();
			cerrar_modal_creacionModelo_Articulo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionModelo_Articulo(error);
			activarBoton();
		}
	});
}
function editarModelo_Articulo(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionModelo_Articulo').serialize(),
		url: $('#form_edicionModelo_Articulo').attr('action'),
		type: $('#form_edicionModelo_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarModelo_Articulo();
			cerrar_modal_edicionModelo_Articulo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionModelo_Articulo(error);
			activarBoton();
		}
	});
}
function eliminarModelo_Articulo(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionModelo_Articulo').serialize(),
		url: $('#form_eliminacionModelo_Articulo').attr('action'),
		type: $('#form_eliminacionModelo_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarModelo_Articulo();
			cerrar_modal_eliminacionModelo_Articulo();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Modelo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionModelo_Articulo();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionModelo_Articulo(url){
	$('#creacionModelo_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionModelo_Articulo(){
	$('#creacionModelo_Articulo').modal('hide');
}
function abrir_modal_edicionModelo_Articulo(url){
	$('#edicionModelo_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionModelo_Articulo(){
	$('#edicionModelo_Articulo').modal('hide');
}
function abrir_modal_eliminacionModelo_Articulo(url){
	$('#eliminacionModelo_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionModelo_Articulo(){
	$('#eliminacionModelo_Articulo').modal('hide');
}
function mostrarErroresCreacionModelo_Articulo(erroresModelo_Articulo){
  $('.error-modelo_art').addClass('d-none');
  for(let item in erroresModelo_Articulo.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresModelo_Articulo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionModelo_Articulo(erroresEdicionModelo_Articulo){
  $('.error-modelo_art').addClass('d-none');
  for(let item in erroresEdicionModelo_Articulo.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionModelo_Articulo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarModelo_Articulo();
});