function listarDetalle(){
	$.ajax({
		url: "/listarDetalle/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_detalles')){
				$('#tabla_detalles').DataTable().clear();
				$('#tabla_detalles').DataTable().destroy();
			}
			$('#tabla_detalles tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_cult'] + '</td>';
				fila += '<td>' + response[i]["fields"]['areahectarea_pro'] + ' HA ' + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Detalle" aria-label="Editar Detalle"';
				fila += ' onclick = "abrir_modal_edicionDetalle(\'/editarDetalle/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Detalle" aria-label="Eliminar Detalle"';
				fila += ' onclick = "abrir_modal_eliminacionDetalle(\'/eliminarDetalle/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_detalles tbody').append(fila);
			}
			$('#tabla_detalles').DataTable({
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
					{ "data": "Area del cultivo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarDetalle(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionDetalle').serialize(),
		url: $('#form_creacionDetalle').attr('action'),
		type: $('#form_creacionDetalle').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarDetalle();
			cerrar_modal_creacionDetalle();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionDetalle(error);
			activarBoton();
		}
	});
}
function editarDetalle(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionDetalle').serialize(),
		url: $('#form_edicionDetalle').attr('action'),
		type: $('#form_edicionDetalle').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarDetalle();
			cerrar_modal_edicionDetalle();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionDetalle(error);
			activarBoton();
		}
	});
}
function eliminarDetalle(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionDetalle').serialize(),
		url: $('#form_eliminacionDetalle').attr('action'),
		type: $('#form_eliminacionDetalle').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarDetalle();
			cerrar_modal_eliminacionDetalle();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Detalle tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionDetalle();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionDetalle(url){
	$('#creacionDetalle').load(url, function(){
		$('#creacionCenso').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionDetalle(){
	$('#creacionDetalle').modal('hide');
	$('#creacionCenso').modal('show');
}
function abrir_modal_edicionDetalle(url){
	$('#edicionDetalle').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionDetalle(){
	$('#edicionDetalle').modal('hide');
}
function abrir_modal_eliminacionDetalle(url){
	$('#eliminacionDetalle').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionDetalle(){
	$('#eliminacionDetalle').modal('hide');
}
function mostrarErroresCreacionDetalle(erroresDetalle){
  $('.error-cod_cult').addClass('d-none');
  $('.error-areahectarea_pro').addClass('d-none');
  for(let item in erroresDetalle.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresDetalle.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionDetalle(erroresEdicionDetalle){
  $('.error-cod_cult').addClass('d-none');
  $('.error-areahectarea_pro').addClass('d-none');
  for(let item in erroresEdicionDetalle.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionDetalle.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarDetalle();
});