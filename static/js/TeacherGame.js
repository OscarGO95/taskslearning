var estudiantesSelect = [];

$(function(){

    $('#selectgrado').change(function() {
            var select=$(this).val();
            var datagroup=select.split("-");
            let html="";
        let container = $("#containerCards");
            $.post('../getStudents',{"nombre":datagroup[0], "denominacion":datagroup[1]},function (response) {
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
            $('#modalseleccion').modal({
                show: true
            });
        });
    });

    $('#getStudents').click('on',function () {
        estudiantesSelect = [];
        let data = $("input[name=check]");
        let cont=0;
        for( let i = 0; i<data.length; i++){
            if (data[i].checked){
                estudiantesSelect.push(data[i].id);
                cont++;
            }
        }
        $("#cuantos").text(cont+" estudiantes seleccionados");
    });

    $('#asignarGame').click('on', function () {
        let parse= estudiantesSelect.join(",");
        $.post("../asignarjuego",{'estudiantes': parse}, function (response) {
            alert("El juego es visible ahora para los estudiantes seleccionados");
        });
    });
});