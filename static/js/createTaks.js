var id=$('#idprofesor').val();
var estudiantesTarea = [];
$(function(){
    let fecha = new Date();
    let mes = (fecha.getMonth()+1).toString();
    let dia = (fecha.getDate()).toString();
    if(mes.length <2){
        mes = "0"+mes;
    }
    if(dia.length <2){
        dia = "0"+dia;
    }
    let creacion = $("#inputfechainicio").val(fecha.getFullYear()+"-"+mes+"-"+dia);
    console.log(creacion.val());
    let selectPublicar = $("#selectpublicados").val(1);
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
        let html="";
        let container = $("#containerCards");

        $.post('getStudents',{"nombre":datagroup[0], "denominacion":datagroup[1]},function (response) {
            console.log(response);
            if(response.estudiantes.length>0){
                response.estudiantes.forEach(function (element) {
                html+="<div class='card'>";
                html+="<img class='card-img-top' src='"+element.imagen+"' alt='Card image cap'>";
                html+="<div class='card-body'>";
                html+="<h5 class='card-title'>"+element.nombre+" "+element.apellido+"</h5>";
                html+="<input name='check' id='"+element.id+"' type='checkbox' style='alignment: center'>";
                html+="</div>";
                html+="</div>";
                });
            }else{
                html="<h5>No hay Estudiantes Inscritos</h5>";
            }
            container.html(html);

        });
    });

    $('#selectAsignaturaOptions').change(function () {
        let select=$(this).val();
        $.post('getTemas',{"materia":select}, function (data) {
            let options = data.contenidos;
            let selecttmp = $('#selectContenidos');
            selecttmp.html("")
            let html = "";
            html+="<option selected='selected' disabled='disabled' value=''>Seleccione un Tema</option>";
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

    $('#getStudents').click('on',function () {
        let data = $("input[name=check]");
        for( let i = 0; i<data.length; i++){
            if (data[i].checked){
                estudiantesTarea.push(data[i].id);
            }
        }

    });

    $('#saveformTarea').click('on',function () {
        let formGUI = $('#save_tarea').get(0);
        let form = new FormData(formGUI);
        form.append("estudiantes", estudiantesTarea);
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

