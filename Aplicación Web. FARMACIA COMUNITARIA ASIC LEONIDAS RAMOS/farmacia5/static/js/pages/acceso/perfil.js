let form_edit_info = document.getElementById('form_edit_info');
let form_nuevo_bene = document.getElementById('form_nuevo_bene');
let form_edit_bene = document.getElementById('form_edit_bene');
let display_embarazada = document.getElementById('display_embarazada');

let getData = async () => {
    // PROVIDERS LIST
    /*await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_beneficiados',
        {
            'action': 'search_beneficiados',
        },
        [
            {"data": "cedula"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "genero"},
            {"data": "f_nacimiento"},
            {"data": "embarazada"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar Beneficiado"><i class="fa fa-edit"></i></a>';
                    return buttons
                }
            },{
                targets: [-2],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if(data == 'True'){
                        return 'SI';
                    } else if(row['genero'] == 'Masculino'){
                        return 'NO APLICA';
                    } else {
                        return 'NO';
                    }
                }
            }
        ],
        '/mi-perfil/'
    );*/
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_beneficiados',
        {
            'action': 'search_beneficiados',
        },
        [
            {"data": "cedula"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "genero"},
            {"data": "f_nacimiento"},
            {"data": "embarazada"},
            {"data": "c_residencia"}, // Agrega la columna para la constancia de residencia
            {"data": "id"},
        ],
        [
            {
                targets: [-2], // La columna de la constancia de residencia es la penúltima (-2)
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data) {
                        return '<a href="' + data + '" target="_blank" class="btn btn-sm btn-info">Visualizar</a>';
                    } else {
                        return 'Vacio';
                    }
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = `
                        <a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar Beneficiado">
                            <i class="fa fa-edit"></i>
                        </a>
                        <button class="btn btn-icon btn-danger btn-eliminar-bene" data-bene-id="${row.id}" data-bs-toggle="tooltip" data-bs-placement="top" title="Eliminar Beneficiado">
                            <i class="fa fa-trash"></i>
                        </button>`;
                    return buttons;
                }
            },{
                targets: [-3], // Ajusta los índices de destino para los botones de edición si es necesario
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if(data == true){
                        return 'SI';
                    } else if(row['genero'] == 'Masculino'){
                        return 'NO APLICA';
                    } else {
                        return 'NO';
                    }
                }
            }
        ],
        '/mi-perfil/'
    );
}

$( async function () {
    await getData();

    form_edit_info.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_edit_info);

        await SendDataJsonForm(type_actions['perfil_edit'][action_edit.value], parameters, async () => {
            await getData();
            $('#smallmodal').modal('hide');
            $("#form_edit_info")[0].reset();
            window.location.reload();
        });
    });

    form_nuevo_bene.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_nuevo_bene);

        await SendDataJsonForm(type_actions['benefi'][action_bene.value], parameters, async () => {
            await getData();
            $('#modal_nuevo_bene').modal('hide');
            $("#form_nuevo_bene")[0].reset();
        });
    });

    // REGISTER USUARIO
    $('#btn_edit_info').on('click', function () {
        $('input[name="action_edit"]').val('editar_info');
        $('#smallmodal').modal('show');
    });

    $('#btn_nuevo_bene').on('click', function () {
        $('input[name="action"]').val('nuevo_bene');
        $('#modal_nuevo_bene').modal('show');
    });

    $('#listado_beneficiados tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_edit_bene')[0].reset();
        $('#modal_edit_bene').modal('show');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('editar_bene');
        $('input[name="id"]').val(data.cedula);
        $('input[name="telefono_bene"]').val(data.telefono);
        $('select[name="parentesco"]').val(data.parentesco);
        $('select[name="zona_bene"]').val(data.zona.id);
        $('textarea[name="direccion_bene"]').val(data.direccion);
        $('textarea[name="patologia_bene"]').val(data.patologia);


        if(data.genero == 'Femenino'){
            display_embarazada.style.display = 'block';
            if(data.embarazada == true){
                $('input[name="embarazada_bene"]').prop('checked', true)
            }else{
                $('input[name="embarazada_bene"]').prop('checked', false)
            }
        }else{
            display_embarazada.style.display = 'none';
        }

    });
    $('#listado_beneficiados tbody').on('click', 'button.btn-eliminar-bene', function () {
        let beneficiarioId = $(this).data('bene-id');
        $('#confirmacionModal').modal('show');

        $('#confirmarEliminacionBtn').on('click', function() {
            $.ajax({
                type: 'POST',
                url: '/mi-perfil/',
                data: {
                    action: 'eliminar_bene',
                    id: beneficiarioId,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function (response) {
                    if (response.response && response.response.type_response === 'success') {
                        $('#alertaExito').fadeIn().delay(3000).fadeOut();
                        getData();
                    } else {
                        $('#alertaError').fadeIn().delay(3000).fadeOut();
                    }
                },
                error: function (xhr, errmsg, err) {
                        $('#alertaError').fadeIn().delay(3000).fadeOut();
                }
            });
            $('#confirmacionModal').modal('hide'); // Cerrar el modal después de hacer clic en "Eliminar"
        });
    });

    // Cerrar el modal cuando se hace clic en el botón "Cancelar"
    $('#confirmacionModal button.btn-secondary').on('click', function() {
        $('#confirmacionModal').modal('hide');
        // Reiniciar la variable de seguimiento del error cuando se cierra el modal
        errorShown = false;
    });


    form_edit_bene.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_edit_bene);

        await SendDataJsonForm(type_actions['benefi'][action.value], parameters, async () => {
            await getData();
            $('#modal_edit_bene').modal('hide');
            $("#form_edit_bene")[0].reset();
        });
    });

    $('#id_genero').change(function () {
        if ($(this).val() == "MA") {
            // Deshabilitar checkboxes
            $('.deshabilitar').prop('disabled', true);
            $('#inline-radio2').prop('checked', true)
        } else {
            // Habilitar checkboxes
            $('.deshabilitar').prop('disabled', false);
        }
    }).trigger('change'); // Trigger para establecer el estado inicial
});