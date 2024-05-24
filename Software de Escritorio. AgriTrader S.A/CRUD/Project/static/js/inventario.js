function listarInventario(){
	$.ajax({
		url: "/listarInventario/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_inventarios')){
				$('#tabla_inventarios').DataTable().clear();
				$('#tabla_inventarios').DataTable().destroy();
			}
			$('#tabla_inventarios tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['descrip_artprod'] + ' ' + response[i]["fields"]['cod_marca'] + ' ' + response[i]["fields"]['cod_modelo'] +'</td>';
				fila += '<td>' + response[i]["fields"]['cant_artprod'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nom_uni'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Inventario" aria-label="Editar Inventario"';
				fila += ' onclick = "abrir_modal_edicionInventario(\'/editarInventario/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Inventario" aria-label="Eliminar Inventario"';
				fila += ' onclick = "abrir_modal_eliminacionInventario(\'/eliminarInventario/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_inventarios tbody').append(fila);
			}
			$('#tabla_inventarios').DataTable({
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
					{ "data": "Articulo" },
					{ "data": "Cantidad" },
					{ "data": "Rif de la Unida" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarInventario(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionInventario').serialize(),
		url: $('#form_creacionInventario').attr('action'),
		type: $('#form_creacionInventario').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarInventario();
			cerrar_modal_creacionInventario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionInventario(error);
			activarBoton();
		}
	});
}
function editarInventario(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionInventario').serialize(),
		url: $('#form_edicionInventario').attr('action'),
		type: $('#form_edicionInventario').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarInventario();
			cerrar_modal_edicionInventario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionInventario(error);
			activarBoton();
		}
	});
}
function eliminarInventario(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionInventario').serialize(),
		url: $('#form_eliminacionInventario').attr('action'),
		type: $('#form_eliminacionInventario').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarInventario();
			cerrar_modal_eliminacionInventario();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Inventario tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionInventario();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionInventario(url){
	$('#creacionInventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionInventario(){
	$('#creacionInventario').modal('hide');
}
function abrir_modal_edicionInventario(url){
	$('#edicionInventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionInventario(){
	$('#edicionInventario').modal('hide');
}
function abrir_modal_eliminacionInventario(url){
	$('#eliminacionInventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionInventario(){
	$('#eliminacionInventario').modal('hide');
}
function mostrarErroresCreacionInventario(erroresInventario){
  $('.error-cod_artprod').addClass('d-none');
  $('.error-cant_artprod').addClass('d-none');
  $('.error-cod_uni').addClass('d-none');
  for(let item in erroresInventario.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresInventario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionInventario(erroresEdicionInventario){
  $('.error-cod_artprod').addClass('d-none');
  $('.error-cant_artprod').addClass('d-none');
  $('.error-cod_uni').addClass('d-none');
  for(let item in erroresEdicionInventario.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionInventario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarInventario();
});