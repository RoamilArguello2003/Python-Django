function listarNecesidad_Productor(){
	$.ajax({
		url: "/listarNecesidad_Productor/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_necesidades_productor')){
				$('#tabla_necesidades_productor').DataTable().clear();
				$('#tabla_necesidades_productor').DataTable().destroy();
			}
			$('#tabla_necesidades_productor tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_nec'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_uni'] + '</td>';
				fila += '<td>' + response[i]["fields"]['descrip_art'] + ' ' + response[i]["fields"]['marca_art'] + ' ' + response[i]["fields"]['modelo_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['canti_art'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Necesidad" aria-label="Editar Necesidad"';
				fila += ' onclick = "abrir_modal_edicionNecesidad_Productor(\'/editarNecesidad_Productor/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Necesidad" aria-label="Eliminar Necesidad"';
				fila += ' onclick = "abrir_modal_eliminacionNecesidad_Productor(\'/eliminarNecesidad_Productor/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_necesidades_productor tbody').append(fila);
			}
			$('#tabla_necesidades_productor').DataTable({
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
					{ "data": "Unidad" },
					{ "data": "Articulo" },
					{ "data": "Cantidad" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarNecesidad_Productor(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionNecesidad_Productor').serialize(),
		url: $('#form_creacionNecesidad_Productor').attr('action'),
		type: $('#form_creacionNecesidad_Productor').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarNecesidad_Productor();
			cerrar_modal_creacionNecesidad_Productor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionNecesidad_Productor(error);
			activarBoton();
		}
	});
}
function editarNecesidad_Productor(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionNecesidad_Productor').serialize(),
		url: $('#form_edicionNecesidad_Productor').attr('action'),
		type: $('#form_edicionNecesidad_Productor').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarNecesidad_Productor();
			cerrar_modal_edicionNecesidad_Productor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionNecesidad_Productor(error);
			activarBoton();
		}
	});
}
function eliminarNecesidad_Productor(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionNecesidad_Productor').serialize(),
		url: $('#form_eliminacionNecesidad_Productor').attr('action'),
		type: $('#form_eliminacionNecesidad_Productor').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarNecesidad_Productor();
			cerrar_modal_eliminacionNecesidad_Productor();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Esta Necesidad tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionNecesidad_Productor();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionNecesidad_Productor(url){
	$('#creacionNecesidad_Productor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionNecesidad_Productor(){
	$('#creacionNecesidad_Productor').modal('hide');
}
function abrir_modal_edicionNecesidad_Productor(url){
	$('#edicionNecesidad_Productor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionNecesidad_Productor(){
	$('#edicionNecesidad_Productor').modal('hide');
}
function abrir_modal_eliminacionNecesidad_Productor(url){
	$('#eliminacionNecesidad_Productor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionNecesidad_Productor(){
	$('#eliminacionNecesidad_Productor').modal('hide');
}
function mostrarErroresCreacionNecesidad_Productor(erroresNecesidad_Productor){
  $('.error-fecha_nec').addClass('d-none');
  $('.error-cod_uni').addClass('d-none');
  $('.error-cod_art').addClass('d-none');
  $('.error-canti_art').addClass('d-none');
  for(let item in erroresNecesidad_Productor.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresNecesidad_Productor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionNecesidad_Productor(erroresEdicionNecesidad_Productor){
  $('.error-fecha_nec').addClass('d-none');
  $('.error-cod_uni').addClass('d-none');
  $('.error-cod_art').addClass('d-none');
  $('.error-canti_art').addClass('d-none');
  for(let item in erroresEdicionNecesidad_Productor.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionNecesidad_Productor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarNecesidad_Productor();
});