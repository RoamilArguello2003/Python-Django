function listarMarca_Articulo(){
	$.ajax({
		url: "/listarMarca_Articulo/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_marcas_articulos')){
				$('#tabla_marcas_articulos').DataTable().clear();
				$('#tabla_marcas_articulos').DataTable().destroy();
			}
			$('#tabla_marcas_articulos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['marca_art'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Marca" aria-label="Editar Marca"';
				fila += ' onclick = "abrir_modal_edicionMarca_Articulo(\'/editarMarca_Articulo/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Marca" aria-label="Eliminar Marca"';
				fila += ' onclick = "abrir_modal_eliminacionMarca_Articulo(\'/eliminarMarca_Articulo/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_marcas_articulos tbody').append(fila);
			}
			$('#tabla_marcas_articulos').DataTable({
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
					{ "data": "Marca" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarMarca_Articulo(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionMarca_Articulo').serialize(),
		url: $('#form_creacionMarca_Articulo').attr('action'),
		type: $('#form_creacionMarca_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarMarca_Articulo();
			cerrar_modal_creacionMarca_Articulo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionMarca_Articulo(error);
			activarBoton();
		}
	});
}
function editarMarca_Articulo(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionMarca_Articulo').serialize(),
		url: $('#form_edicionMarca_Articulo').attr('action'),
		type: $('#form_edicionMarca_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarMarca_Articulo();
			cerrar_modal_edicionMarca_Articulo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionMarca_Articulo(error);
			activarBoton();
		}
	});
}
function eliminarMarca_Articulo(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionMarca_Articulo').serialize(),
		url: $('#form_eliminacionMarca_Articulo').attr('action'),
		type: $('#form_eliminacionMarca_Articulo').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarMarca_Articulo();
			cerrar_modal_eliminacionMarca_Articulo();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Esta Marca tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionMarca_Articulo();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionMarca_Articulo(url){
	$('#creacionMarca_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionMarca_Articulo(){
	$('#creacionMarca_Articulo').modal('hide');
}
function abrir_modal_edicionMarca_Articulo(url){
	$('#edicionMarca_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionMarca_Articulo(){
	$('#edicionMarca_Articulo').modal('hide');
}
function abrir_modal_eliminacionMarca_Articulo(url){
	$('#eliminacionMarca_Articulo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionMarca_Articulo(){
	$('#eliminacionMarca_Articulo').modal('hide');
}
function mostrarErroresCreacionMarca_Articulo(erroresMarca_Articulo){
  $('.error-marca_art').addClass('d-none');
  for(let item in erroresMarca_Articulo.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresMarca_Articulo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionMarca_Articulo(erroresEdicionMarca_Articulo){
  $('.error-marca_art').addClass('d-none');
  for(let item in erroresEdicionMarca_Articulo.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionMarca_Articulo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarMarca_Articulo();
});