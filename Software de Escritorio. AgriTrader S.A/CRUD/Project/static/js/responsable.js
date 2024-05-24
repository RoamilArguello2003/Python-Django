function listarResponsable(){
	$.ajax({
		url: "/listarResponsable/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_responsables')){
				$('#tabla_responsables').DataTable().clear();
				$('#tabla_responsables').DataTable().destroy();
			}
			$('#tabla_responsables tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_cedula_res'] + response[i]["fields"]['cedula_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apell_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['direccion_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_telef_res'] + response[i]["fields"]['telef_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_movil_res'] + response[i]["fields"]['movil_res'] + '</td>';
				fila += '<td>' + response[i]["fields"]['correo_res'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Responsable" aria-label="Editar Responsable"';
				fila += ' onclick = "abrir_modal_edicionResponsable(\'/editarResponsable/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Responsable" aria-label="Eliminar Responsable"';
				fila += ' onclick = "abrir_modal_eliminacionResponsable(\'/eliminarResponsable/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_responsables tbody').append(fila);
			}
			$('#tabla_responsables').DataTable({
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
					{ "data": "Correo electrónico" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarResponsable(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionResponsable').serialize(),
		url: $('#form_creacionResponsable').attr('action'),
		type: $('#form_creacionResponsable').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarResponsable();
			cerrar_modal_creacionResponsable();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionResponsable(error);
			activarBoton();
		}
	});
}
function editarResponsable(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionResponsable').serialize(),
		url: $('#form_edicionResponsable').attr('action'),
		type: $('#form_edicionResponsable').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarResponsable();
			cerrar_modal_edicionResponsable();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionResponsable(error);
			activarBoton();
		}
	});
}
function eliminarResponsable(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionResponsable').serialize(),
		url: $('#form_eliminacionResponsable').attr('action'),
		type: $('#form_eliminacionResponsable').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarResponsable();
			cerrar_modal_eliminacionResponsable();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Responsable tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionResponsable();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionResponsable(url){
	$('#creacionResponsable').load(url, function(){
		$('#creacionUnidad_Productiva').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionResponsable(){
	$('#creacionResponsable').modal('hide');
	$('#creacionUnidad_Productiva').modal('show');
}
function abrir_modal_edicionResponsable(url){
	$('#edicionResponsable').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionResponsable(){
	$('#edicionResponsable').modal('hide');
}
function abrir_modal_eliminacionResponsable(url){
	$('#eliminacionResponsable').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionResponsable(){
	$('#eliminacionResponsable').modal('hide');
}
function mostrarErroresCreacionResponsable(erroresResponsable){
  $('.error-cedula_res').addClass('d-none');
  $('.error-nom_res').addClass('d-none');
  $('.error-apell_res').addClass('d-none');
  $('.error-direccion_res').addClass('d-none');
  $('.error-telef_res').addClass('d-none');
  $('.error-movil_res').addClass('d-none');
  $('.error-correo_res').addClass('d-none');
  for(let item in erroresResponsable.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresResponsable.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionResponsable(erroresEdicionResponsable){
  $('.error-cedula_res').addClass('d-none');
  $('.error-nom_res').addClass('d-none');
  $('.error-apell_res').addClass('d-none');
  $('.error-direccion_res').addClass('d-none');
  $('.error-telef_res').addClass('d-none');
  $('.error-movil_res').addClass('d-none');
  $('.error-correo_res').addClass('d-none');
  for(let item in erroresEdicionResponsable.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionResponsable.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarResponsable();
});