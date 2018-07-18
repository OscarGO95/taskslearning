var error = [];
var fechaactual= new Date();
$(function () {
    SendFormTarea();
    let creacion = $("#inputfechainicio").val();
});

//este metodo es encargado de las validaciones de cada uno de los campos del formulario de crear tareas
//recorre todos los campos de un formulario ,extrae todos los campos que sean del tipo  indicado,
// los guarda en una coleccion y recorre cada uno de los valores de esos campos y valida si este es 
//un campo vacio , acumula el error en una variable global : sout , se guarda en la lista de errores
//y se muestra en un modal al final del proceso

function validatefieldsInput(form, type) {
    $.each(form.find(":input[type=" + type + "]"), function (index) {//selecciona todos los campos de tipo input en el formulario 
        var input = $(this);
        var sout = "";
        if (input.val().length == 0) {//el valor del campo esta vacio?
        	if(type=="text"){
        		switch (input.attr('name')) {//extrae el atributo name de los campos y los compara con switch case
                	case 'titulo_tarea':
                    	sout = "El campo titulo esta vacio";
                    	break;
            	}
        	}
        	if(type=="date"){
        		switch (input.attr('name')) {
                	case 'fecha_creacion':
                    	sout = "El campo fecha inicio de la tarea  esta vacio";
                    	break;

                    case 'fecha_fin':
                    	sout = "El campo fecha limite de la tarea  esta vacio";
                    	break;
            	}
        	}

            error.push(sout);//lista final de errores para desplegar en el modal
        }
    });
}


//funciona igual que el anterior solo que este requiere validaciones adicionales
function validatefieldsInput(form, type) {
    $.each(form.find(":input[type=" + type + "]"), function (index) {
        var input = $(this);
        var sout = "";
        if (input.val().length == 0) {
        	if(type=="text"){
        		switch (input.attr('name')) {
                	case 'titulo_tarea':
                    	sout = "El campo titulo esta vacio";
                    	break;
            	}
        	}
        	if(type=="date"){
        		switch (input.attr('name')) {
                	case 'fecha_creacion':
                    	sout = "El campo fecha inicio de la tarea  esta vacio";
                    	break;

                    case 'fecha_fin':
                    	sout = "El campo fecha limite de la tarea  esta vacio";
                    	break;
            	}
        	}

            error.push(sout);
        }
    });
}


function validatefieldsTextarea(form) {
    $.each(form.find("textarea"), function (index) {
        var input = $(this);
        var sout = "";
        if (input.val().length == 0) {
        	switch (input.attr('name')) {
                case 'descripcion_tarea':
                    sout = "El campo de la descripcion de la tarea esta vacio";
                    error.push(sout);
                    break;
            }
        }
    });
}

function validatefieldsSelect(form) {
    $.each(form.find("select option:selected"), function (index) {
        var input = $(this);
        var sout = "";
        if (input.val().length == 0) {

        	switch (input.text()) {
                case 'Seleccione un grado':
                    sout = "No ha seleccionado un grado";
                    break;

                case 'Seleccione una asignatura':
                    sout = "No ha seleccionado una asignatura";
                    break;

                case 'Seleccione un Contenido':
                    sout = "No ha seleccionado una Contenido";
                    break;

                case 'Seleccione un Tema':
                    sout = "No ha seleccionado un Temas para la tarea";
                    break;

                case 'Seleccione publicacion':
                    sout = "No ha seleccionado Para quienes es la tarea";
                    break;
            }
            error.push(sout);
        } 
    });
}




//metodo para levantar el modal de error al usuario sino cumple con las validaciones
function SendFormTarea() {


    $('#saveformTarea').on('click', function (event) {
        //evitar envio del formulario
        event.preventDefault();
        //extraccion de datos
        var save_tarea = $('#save_tarea');
        let creacion = $("#inputfechainicio").val();
        let final = $("#inputfechafin").val();
        let s = creacion.split("-");
        let fechacreacion = new Date(s[0],s[1]-1,s[2]);
        let s1 = final.split("-");
        let fechafinal = new Date(s1[0],s1[1]-1,s1[2]);
        let vectoractual=fechaactual.toLocaleDateString().split('/');
        let actualsolofecha=new Date(vectoractual[2],vectoractual[1]-1,vectoractual[0]);
        console.log(actualsolofecha);

        //validacion de campos y agregar al vector de errores si es requerido
        if(fechacreacion.getTime() >= fechafinal.getTime()){
            error.push("la fecha de finalización debe ser mayor o igual a la fecha de entrega");
        }

        if(fechacreacion.getTime() < actualsolofecha.getTime()){
            error.push("la fecha de creación debe ser mayor a la fecha actual");
        }

        //validacion de cada uno de los campos del formulario segun tipo 
        validatefieldsInput(save_tarea,"text");
        validatefieldsInput(save_tarea,"date");
        validatefieldsTextarea(save_tarea);
        validatefieldsSelect(save_tarea);
        var element = "";
        if (error.length > 0) {
            var data = $('#data-form-error');

            $.each(error, function (index, val) {
                element += val + "*" + "<br>";
            });
            //levanta el modal escondido en el html y despliega los errores
            data.html(element);
            error = [];
            $('#myModal').modal({
                show: true
            });
        }
        else {
            //location.reload();
        }
    });
}