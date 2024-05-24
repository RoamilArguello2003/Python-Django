function listarProductor(){
	$.ajax({
		url: "/listarProductor/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_productores')){
				$('#tabla_productores').DataTable().clear();
				$('#tabla_productores').DataTable().destroy();
			}
			$('#tabla_productores tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_cedula_prod'] + response[i]["fields"]['cedula_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apell_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['direccion_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_telef_prod'] + response[i]["fields"]['telef_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_movil_prod'] + response[i]["fields"]['movil_prod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['correo_prod'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Productor" aria-label="Editar Productor"';
				fila += ' onclick = "abrir_modal_edicionProductor(\'/editarProductor/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Productor" aria-label="Eliminar Productor"';
				fila += ' onclick = "abrir_modal_eliminacionProductor(\'/eliminarProductor/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_productores tbody').append(fila);
			}
			$('#tabla_productores').DataTable({
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
					{ "data": "Cedula" },
					{ "data": "Nombre" },
					{ "data": "Apellido" },
					{ "data": "Dirreción" },
					{ "data": "Telefono de casa" },
					{ "data": "Telefono movil" },
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
function registrarProductor(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionProductor').serialize(),
		url: $('#form_creacionProductor').attr('action'),
		type: $('#form_creacionProductor').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarProductor();
			cerrar_modal_creacionProductor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionProductor(error);
			activarBoton();
		}
	});
}
function editarProductor(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionProductor').serialize(),
		url: $('#form_edicionProductor').attr('action'),
		type: $('#form_edicionProductor').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarProductor();
			cerrar_modal_edicionProductor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionProductor(error);
			activarBoton();
		}
	});
}
function eliminarProductor(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionProductor').serialize(),
		url: $('#form_eliminacionProductor').attr('action'),
		type: $('#form_eliminacionProductor').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarProductor();
			cerrar_modal_eliminacionProductor();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Productor tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionProductor();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionProductor(url){
	$('#creacionProductor').load(url, function(){
		$('#creacionUnidad_Productiva').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionProductor(){
	$('#creacionProductor').modal('hide');
	$('#creacionUnidad_Productiva').modal('show');
}
function abrir_modal_edicionProductor(url){
	$('#edicionProductor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionProductor(){
	$('#edicionProductor').modal('hide');
}
function abrir_modal_eliminacionProductor(url){
	$('#eliminacionProductor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionProductor(){
	$('#eliminacionProductor').modal('hide');
}
function mostrarErroresCreacionProductor(erroresProductor){
  $('.error-cedula_prod').addClass('d-none');
  $('.error-nom_prod').addClass('d-none');
  $('.error-apell_prod').addClass('d-none');
  $('.error-direccion_prod').addClass('d-none');
  $('.error-telef_prod').addClass('d-none');
  $('.error-movil_prod').addClass('d-none');
  $('.error-correo_prod').addClass('d-none');
  for(let item in erroresProductor.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresProductor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionProductor(erroresEdicionProductor){
  $('.error-cedula_prod').addClass('d-none');
  $('.error-nom_prod').addClass('d-none');
  $('.error-apell_prod').addClass('d-none');
  $('.error-direccion_prod').addClass('d-none');
  $('.error-telef_prod').addClass('d-none');
  $('.error-movil_prod').addClass('d-none');
  $('.error-correo_prod').addClass('d-none');
  for(let item in erroresEdicionProductor.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionProductor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarProductor();
});