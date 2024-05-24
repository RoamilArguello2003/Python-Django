function listarArticulo_Empresa(){
	$.ajax({
		url: "/listarArticulo_Empresa/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_articulos_empresa')){
				$('#tabla_articulos_empresa').DataTable().clear();
				$('#tabla_articulos_empresa').DataTable().destroy();
			}
			$('#tabla_articulos_empresa tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['descrip_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['marca_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['modelo_art'] + '</td>';
				fila += '<td>' + response[i]["fields"]['precio'] + '</td>';
				fila += '<td>' + response[i]["fields"]['stock'] + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_duracion'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Articulo" aria-label="Editar Articulo"';
				fila += ' onclick = "abrir_modal_edicionArticulo_Empresa(\'/editarArticulo_Empresa/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Articulo" aria-label="Eliminar Articulo"';
				fila += ' onclick = "abrir_modal_eliminacionArticulo_Empresa(\'/eliminarArticulo_Empresa/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_articulos_empresa tbody').append(fila);
			}
			$('#tabla_articulos_empresa').DataTable({
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
					{ "data": "Precio" },
					{ "data": "Stock" },
					{ "data": "Fecha de desuso" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarArticulo_Empresa(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionArticulo_Empresa').serialize(),
		url: $('#form_creacionArticulo_Empresa').attr('action'),
		type: $('#form_creacionArticulo_Empresa').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarArticulo_Empresa();
			cerrar_modal_creacionArticulo_Empresa();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionArticulo_Empresa(error);
			activarBoton();
		}
	});
}
function editarArticulo_Empresa(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionArticulo_Empresa').serialize(),
		url: $('#form_edicionArticulo_Empresa').attr('action'),
		type: $('#form_edicionArticulo_Empresa').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarArticulo_Empresa();
			cerrar_modal_edicionArticulo_Empresa();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionArticulo_Empresa(error);
			activarBoton();
		}
	});
}
function eliminarArticulo_Empresa(pk){
  activarBoton();
  $.ajax({
    data: $('#form_eliminacionArticulo_Empresa').serialize(),
    url: $('#form_eliminacionArticulo_Empresa').attr('action'),
    type: $('#form_eliminacionArticulo_Empresa').attr('method'),
    success: function(response){
      notificacionSuccessEliminacion(response.mensaje);
      listarArticulo_Empresa();
      cerrar_modal_eliminacionArticulo_Empresa();
    },
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Articulo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionArticulo_Empresa();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionArticulo_Empresa(url){
	$('#creacionArticulo_Empresa').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionArticulo_Empresa(){
	$('#creacionArticulo_Empresa').modal('hide');
}
function abrir_modal_edicionArticulo_Empresa(url){
	$('#edicionArticulo_Empresa').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionArticulo_Empresa(){
	$('#edicionArticulo_Empresa').modal('hide');
}
function abrir_modal_eliminacionArticulo_Empresa(url){
	$('#eliminacionArticulo_Empresa').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionArticulo_Empresa(){
	$('#eliminacionArticulo_Empresa').modal('hide');
}
function mostrarErroresCreacionArticulo_Empresa(erroresArticulo_Empresa){
  $('.error-descrip_art').addClass('d-none');
  $('.error-marca_art').addClass('d-none');
  $('.error-modelo_art').addClass('d-none');
  $('.error-precio').addClass('d-none');
  $('.error-stock').addClass('d-none');
  $('.error-fecha_duracion').addClass('d-none');
  for(let item in erroresArticulo_Empresa.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresArticulo_Empresa.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionArticulo_Empresa(erroresEdicionArticulo_Empresa){
	$('.error-descrip_art').addClass('d-none');
  $('.error-marca_art').addClass('d-none');
  $('.error-modelo_art').addClass('d-none');
  $('.error-precio').addClass('d-none');
  $('.error-stock').addClass('d-none');
  $('.error-fecha_duracion').addClass('d-none');
  for(let item in erroresEdicionArticulo_Empresa.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionArticulo_Empresa.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarArticulo_Empresa();
});