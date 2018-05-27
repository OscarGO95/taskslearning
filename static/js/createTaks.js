var id=$('#idprofesor').val();
$(function(){
    cargarMateriasxPgrupo();
});

function cargarMateriasxPgrupo(){
    $('#selectgrado').change(function() {
        var select=$(this).val();
        var datagroup=select.split("-");

        $.post('getasignatura',{"idgrupo":datagroup[0],"denominacion":datagroup[1],"idprofesor":id},function (data) {

            let options = data.materias;
            selecttmp = $('#selectAsignaturaOptions');
            selecttmp.html("");
            let html ='';
            html+='<option selected="selected" disabled="disabled" value="">Seleccione una asignatura</option>';
            options.forEach(function (element) {
                html+='<option value='+element+'>'+element+'</option>';
            });
            selecttmp.html(html);
        });
    });

    $('#selectAsignaturaOptions').change(function () {
        let select=$(this).val();
        $.post('getTemas',{"materia":select}, function (data) {
            let options = data.contenidos;
            let selecttmp = $('#selectContenidos');
            selecttmp.html("")
            let html = "";
            html+="<option selected='selected' disabled='disabled' value=''>Seleccione un Contenido</option>";
            options.forEach(function (element) {
                html+="<option value='"+element+"'>"+element+"</option>";
            });
            selecttmp.html(html)
        });
    });

    $('#selectContenidos').change(function () {
        let select = $(this).val();
        $.post('getContenidos',{"contenido":select},function (data) {
            let options = data.temas;
            let selecttmp = $('#selectTemas');
            selecttmp.html("");
            let html ="";
            html+="<option selected='selected' disabled='disabled' value=''>Seleccione un Tema</option>";
            options.forEach(function (element) {
                html+="<option value='"+element+"'>"+element+"</option>"
            });
            selecttmp.html(html);
        });
    });

    $('#selectpublicados').change(function () {
        let select=$(this).val();
        if (select ==2){
            $('#modalseleccion').modal({
                show: true
            });
        }
    });

    $('#saveForm').click('on',function () {
        let formGUI = $('#save_tarea').get(0);
        let form = new FormData(formGUI);
        console.log(form);
        $.ajax({
            url: 'uploadTask',
            type: 'POST',
            data: form,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                alert('Tarea Asignada con Exito');
            }
        });
    });
}

