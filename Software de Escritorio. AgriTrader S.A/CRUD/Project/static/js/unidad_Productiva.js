function listarUnidad_Productiva(){
	$.ajax({
		url: "/listarUnidad_Productiva/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_unidades_productivas')){
				$('#tabla_unidades_productivas').DataTable().clear();
				$('#tabla_unidades_productivas').DataTable().destroy();
			}
			$('#tabla_unidades_productivas tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_rif'] + response[i]["fields"]['rif_uni'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_prod'] + ' ' + response[i]["fields"]['apell_prod'] +'</td>';
				fila += '<td>' + response[i]["fields"]['nom_res'] + ' ' + response[i]["fields"]['apell_res'] +'</td>';
				fila += '<td>' + response[i]["fields"]['nom_uni'] + '</td>';
				fila += '<td>' + response[i]["fields"]['estado_uni'] + ' - ' + response[i]["fields"]['municipio_uni'] + ' - ' + response[i]["fields"]['parroquia_uni'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Unidad" aria-label="Editar Unidad"';
				fila += ' onclick = "abrir_modal_edicionUnidad_Productiva(\'/editarUnidad_Productiva/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Unidad" aria-label="Eliminar Unidad"';
				fila += ' onclick = "abrir_modal_eliminacionUnidad_Productiva(\'/eliminarUnidad_Productiva/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_unidades_productivas tbody').append(fila);
			}
			$('#tabla_unidades_productivas').DataTable({
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
					{ "data": "Rif" },
					{ "data": "Productor" },
					{ "data": "Responsable" },
					{ "data": "Nombre de la unidad" },
					{ "data": "Dirección" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarUnidad_Productiva(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionUnidad_Productiva').serialize(),
		url: $('#form_creacionUnidad_Productiva').attr('action'),
		type: $('#form_creacionUnidad_Productiva').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarUnidad_Productiva();
			cerrar_modal_creacionUnidad_Productiva();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionUnidad_Productiva(error);
			activarBoton();
		}
	});
}
function editarUnidad_Productiva(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionUnidad_Productiva').serialize(),
		url: $('#form_edicionUnidad_Productiva').attr('action'),
		type: $('#form_edicionUnidad_Productiva').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarUnidad_Productiva();
			cerrar_modal_edicionUnidad_Productiva();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionUnidad_Productiva(error);
			activarBoton();
		}
	});
}
function eliminarUnidad_Productiva(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionUnidad_Productiva').serialize(),
		url: $('#form_eliminacionUnidad_Productiva').attr('action'),
		type: $('#form_eliminacionUnidad_Productiva').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarUnidad_Productiva();
			cerrar_modal_eliminacionUnidad_Productiva();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Esta Unidad tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionUnidad_Productiva();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionUnidad_Productiva(url){
	$('#creacionUnidad_Productiva').load(url, function(){
		$('#creacionCenso').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionUnidad_Productiva(){
	$('#creacionUnidad_Productiva').modal('hide');
	$('#creacionCenso').modal('show');
}
function abrir_modal_edicionUnidad_Productiva(url){
	$('#edicionUnidad_Productiva').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionUnidad_Productiva(){
	$('#edicionUnidad_Productiva').modal('hide');
}
function abrir_modal_eliminacionUnidad_Productiva(url){
	$('#eliminacionUnidad_Productiva').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionUnidad_Productiva(){
	$('#eliminacionUnidad_Productiva').modal('hide');
}
function mostrarErroresCreacionUnidad_Productiva(erroresUnidad_Productiva){
  $('.error-rif_uni').addClass('d-none');
  $('.error-cod_prod').addClass('d-none');
  $('.error-cod_res').addClass('d-none');
  $('.error-nom_uni').addClass('d-none');
  $('.error-estado_uni').addClass('d-none');
  $('.error-municipio_uni').addClass('d-none');
  $('.error-parroquia_uni').addClass('d-none');
  for(let item in erroresUnidad_Productiva.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresUnidad_Productiva.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionUnidad_Productiva(erroresEdicionUnidad_Productiva){
  $('.error-rif_uni').addClass('d-none');
  $('.error-cod_prod').addClass('d-none');
  $('.error-cod_res').addClass('d-none');
  $('.error-nom_uni').addClass('d-none');
  $('.error-estado_uni').addClass('d-none');
  $('.error-municipio_uni').addClass('d-none');
  $('.error-parroquia_uni').addClass('d-none');
  for(let item in erroresEdicionUnidad_Productiva.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionUnidad_Productiva.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarUnidad_Productiva();
});