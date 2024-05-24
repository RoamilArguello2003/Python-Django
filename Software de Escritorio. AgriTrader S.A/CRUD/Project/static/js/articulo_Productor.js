function listarArticulo_Productor(){
	$.ajax({
		url: "/listarArticulo_Productor/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_articulos_productor')){
				$('#tabla_articulos_productor').DataTable().clear();
				$('#tabla_articulos_productor').DataTable().destroy();
			}
			$('#tabla_articulos_productor tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['descrip_artprod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['marca_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['modelo_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['año_artprod'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Articulo" aria-label="Editar Articulo"';
				fila += ' onclick = "abrir_modal_edicionArticulo_Productor(\'/editarArticulo_Productor/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Articulo" aria-label="Eliminar Articulo"';
				fila += ' onclick = "abrir_modal_eliminacionArticulo_Productor(\'/eliminarArticulo_Productor/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_articulos_productor tbody').append(fila);
			}
			$('#tabla_articulos_productor').DataTable({
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
					{ "data": "Descripción" },
					{ "data": "Marca" },
					{ "data": "Modelo" },
					{ "data": "Año" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarArticulo_Productor(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionArticulo_Productor').serialize(),
		url: $('#form_creacionArticulo_Productor').attr('action'),
		type: $('#form_creacionArticulo_Productor').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarArticulo_Productor();
			cerrar_modal_creacionArticulo_Productor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionArticulo_Productor(error);
			activarBoton();
		}
	});
}
function editarArticulo_Productor(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionArticulo_Productor').serialize(),
		url: $('#form_edicionArticulo_Productor').attr('action'),
		type: $('#form_edicionArticulo_Productor').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarArticulo_Productor();
			cerrar_modal_edicionArticulo_Productor();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionArticulo_Productor(error);
			activarBoton();
		}
	});
}
function eliminarArticulo_Productor(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionArticulo_Productor').serialize(),
		url: $('#form_eliminacionArticulo_Productor').attr('action'),
		type: $('#form_eliminacionArticulo_Productor').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarArticulo_Productor();
			cerrar_modal_eliminacionArticulo_Productor();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Articulo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionArticulo_Productor();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionArticulo_Productor(url){
	$('#creacionArticulo_Productor').load(url, function(){
		$('#creacionInventario').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionArticulo_Productor(){
	$('#creacionArticulo_Productor').modal('hide');
	if (!$('#edicion').is(':visible')) {;
		$('#creacionInventario').modal('show');
	}
}
function abrir_modal_edicionArticulo_Productor(url){
	$('#edicionArticulo_Productor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionArticulo_Productor(){
	$('#edicionArticulo_Productor').modal('hide');
}
function abrir_modal_eliminacionArticulo_Productor(url){
	$('#eliminacionArticulo_Productor').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionArticulo_Productor(){
	$('#eliminacionArticulo_Productor').modal('hide');
}
function mostrarErroresCreacionArticulo_Productor(erroresArticulo_Productor){
  $('.error-descrip_artprod').addClass('d-none');
  $('.error-cod_marca').addClass('d-none');
  $('.error-cod_modelo').addClass('d-none');
  $('.error-año_artprod').addClass('d-none');
  for(let item in erroresArticulo_Productor.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresArticulo_Productor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionArticulo_Productor(erroresEdicionArticulo_Productor){
  $('.error-descrip_artprod').addClass('d-none');
  $('.error-cod_marca').addClass('d-none');
  $('.error-cod_modelo').addClass('d-none');
  $('.error-año_artprod').addClass('d-none');
  for(let item in erroresEdicionArticulo_Productor.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionArticulo_Productor.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarArticulo_Productor();
});