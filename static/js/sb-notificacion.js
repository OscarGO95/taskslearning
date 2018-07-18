let vect = [];
let vectid = [];
let container = $('.container-fluid');
$(function () {
    setInterval(loadTarea, 1000);
});


function getcantidadtareas(){
    $.get("getsizetask/"+1, function (data) {
        $("#cant").text(data.size);
    });
}




/*metodo para cargar las tareas en la vista principal. realiza la peticion,
recorre el json generado por la peticion y valida si existe en pantalla la tarea en un vector
de control y asi asegurar que el objeto solo exista una sola vez para el usuario por cad segundo
*/
function loadTarea() {
    //getcantidadtareas();
    $.get("verifyTasks/"+1, function (data) {
        console.log(data);

        $.each(data.tasks, function (index, value) {

            let T = new Tarea(value.id, value.nombre, value.descripcion, value.fechainicio,value.fechafin,value.active);
            //console.log(value.nombre)
            if ((!vectid.includes(T.getid())) && T.getactivo()) {  //la tarea no esta incluida en el vector de control y tarea.estado= activa
                vectid.push(T.getid());//agregado a vector de control
                vect.push(T);//vector para mostrar informacion en pantalla
                container.append(createtask(T));//crea el div donde s generara la tarea
                $("#cant").text(vect.length);//cambia el contador de las tareas 
            }else{
                //refresca la pantalla y carga las tareas en caso de actualizacion de estado tarea
                if(!T.getactivo()){
                    container.html("");
                    vect=[];
                    vectid=[];
                }
            }
        });
    });
}


//metodo buscar una tarea en el controlador. devuelve un objeto de tipo tarea segun su id
function buscarTarea(id){
    $.post("searchTask",{"id":id}, function (value) {
        let T = new Tarea(value.id, value.nombre, value.descripcion, value.fechainicio,value.fechafin,value.active);
        return T;
    });
}


//clase tarea, usada para encapsular los datos que llegan de ajax y poder tener mayor manejo de estas
class Tarea {
    constructor(id, nombre, descripcion, fechainicio,fechafin,activo) {
        this.id=id;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.fechainicio = fechainicio;
        this.fechafin=fechafin;
        this.estado=activo;
    }

    getid() {
        return this.id;
    }

    getnombre() {
        return this.nombre;
    }

    getdescripcion() {
        return this.descripcion;
    }

    getfechainicio() {
        return this.fechainicio;
    }

    getfechafin(){
        return this.fechafin;
    }

    getactivo(){
        return this.estado;
    }
}

/* metodo encargado de una vez cargado el vector de tareas , se encarga de refresca la vista,
realizando un set al div seleccionado y concatenando cada una de las tareas para mostrarlas al usuario
 */
function createtask(Tarea) {
    let datafield="";
    datafield+='<div class="card mb-3">';
    datafield+='<div class="card-header">';
    datafield+='<i class="fa fa-table"></i>'+Tarea.getnombre()+'</div>';
    datafield+='<div class="card-body">';
    datafield+='<p><strong>Note:</strong> '+Tarea.getdescripcion()+'</p>';
    datafield+='</div>';
    datafield+='<div class="card-footer small text-muted">fecha de publicacion '+Tarea.getfechainicio()+ ' fecha de entrega : <b>'+Tarea.getfechafin()+'</b></div>';
    datafield+='</div>';
    return datafield;
}
