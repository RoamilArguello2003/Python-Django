function listarCultivo(){
	$.ajax({
		url: "/listarCultivo/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_cultivos')){
				$('#tabla_cultivos').DataTable().clear();
				$('#tabla_cultivos').DataTable().destroy();
			}
			$('#tabla_cultivos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_cult'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Cultivo" aria-label="Editar Cultivo"';
				fila += ' onclick = "abrir_modal_edicionCultivo(\'/editarCultivo/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Cultivo" aria-label="Eliminar Cultivo"';
				fila += ' onclick = "abrir_modal_eliminacionCultivo(\'/eliminarCultivo/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_cultivos tbody').append(fila);
			}
			$('#tabla_cultivos').DataTable({
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
					{ "data": "Cultivo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarCultivo(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionCultivo').serialize(),
		url: $('#form_creacionCultivo').attr('action'),
		type: $('#form_creacionCultivo').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarCultivo();
			cerrar_modal_creacionCultivo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionCultivo(error);
			activarBoton();
		}
	});
}
function editarCultivo(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionCultivo').serialize(),
		url: $('#form_edicionCultivo').attr('action'),
		type: $('#form_edicionCultivo').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarCultivo();
			cerrar_modal_edicionCultivo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionCultivo(error);
			activarBoton();
		}
	});
}
function eliminarCultivo(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionCultivo').serialize(),
		url: $('#form_eliminacionCultivo').attr('action'),
		type: $('#form_eliminacionCultivo').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarCultivo();
			cerrar_modal_eliminacionCultivo();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Cultivo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionCultivo();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionCultivo(url){
	$('#creacionCultivo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionCultivo(){
	$('#creacionCultivo').modal('hide');
}
function abrir_modal_edicionCultivo(url){
	$('#edicionCultivo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionCultivo(){
	$('#edicionCultivo').modal('hide');
}
function abrir_modal_eliminacionCultivo(url){
	$('#eliminacionCultivo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionCultivo(){
	$('#eliminacionCultivo').modal('hide');
}
function mostrarErroresCreacionCultivo(erroresCultivo){
  $('.error-nom_cult').addClass('d-none');
  for(let item in erroresCultivo.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresCultivo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionCultivo(erroresEdicionCultivo){
  $('.error-nom_cult').addClass('d-none');
  for(let item in erroresEdicionCultivo.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionCultivo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarCultivo();
});