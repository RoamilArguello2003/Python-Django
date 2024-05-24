function listarCenso(){
	$.ajax({
		url: "/listarCenso/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_censos')){
				$('#tabla_censos').DataTable().clear();
				$('#tabla_censos').DataTable().destroy();
			}
			$('#tabla_censos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_cen'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_uni'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_cult'] + ' ' + response[i]["fields"]['areahectarea_pro'] + '</td>';
				fila += '<td>' + response[i]["fields"]['ganado_leche'] + '</td>';
				fila += '<td>' + response[i]["fields"]['ganado_carne'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Censo" aria-label="Editar Censo"';
				fila += ' onclick = "abrir_modal_edicionCenso(\'/editarCenso/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Censo" aria-label="Eliminar Censo"';
				fila += ' onclick = "abrir_modal_eliminacionCenso(\'/eliminarCenso/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_censos tbody').append(fila);
			}
			$('#tabla_censos').DataTable({
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
					{ "data": "Fecha" },
					{ "data": "Unidad productiva" },
					{ "data": "Cultivo" },
					{ "data": "Producción de leche" },
					{ "data": "Producción de carne" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarCenso(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionCenso').serialize(),
		url: $('#form_creacionCenso').attr('action'),
		type: $('#form_creacionCenso').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarCenso();
			cerrar_modal_creacionCenso();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionCenso(error);
			activarBoton();
		}
	});
}
function editarCenso(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionCenso').serialize(),
		url: $('#form_edicionCenso').attr('action'),
		type: $('#form_edicionCenso').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarCenso();
			cerrar_modal_edicionCenso();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionCenso(error);
			activarBoton();
		}
	});
}
function eliminarCenso(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionCenso').serialize(),
		url: $('#form_eliminacionCenso').attr('action'),
		type: $('#form_eliminacionCenso').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarCenso();
			cerrar_modal_eliminacionCenso();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Censo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionCenso();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionCenso(url){
	$('#creacionCenso').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionCenso(){
	$('#creacionCenso').modal('hide');
}
function abrir_modal_edicionCenso(url){
	$('#edicionCenso').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionCenso(){
	$('#edicionCenso').modal('hide');
}
function abrir_modal_eliminacionCenso(url){
	$('#eliminacionCenso').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionCenso(){
	$('#eliminacionCenso').modal('hide');
}
function mostrarErroresCreacionCenso(erroresCenso){
  $('.error-cod_uni').addClass('d-none');
  $('.error-tipo_det').addClass('d-none');
  $('.error-ganado_leche').addClass('d-none');
  $('.error-ganado_carne').addClass('d-none');
  for(let item in erroresCenso.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresCenso.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionCenso(erroresEdicionCenso){
  $('.error-cod_uni').addClass('d-none');
  $('.error-tipo_det').addClass('d-none');
  $('.error-ganado_leche').addClass('d-none');
  $('.error-ganado_carne').addClass('d-none');
  for(let item in erroresEdicionCenso.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionCenso.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarCenso();
});