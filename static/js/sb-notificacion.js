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

function loadTarea() {
    getcantidadtareas();
    var fields = "";
    $.get("verifyTasks/"+1, function (data) {
        console.log(data);

        $.each(data.tasks, function (index, value) {

            let T = new Tarea(value.id, value.nombre, value.descripcion, value.fechainicio,value.fechafin,value.active);
            //console.log(value.nombre)
            if ((!vectid.includes(T.getid())) && T.getactivo()) {
                vectid.push(T.getid());
                vect.push(T);
                container.append(createtask(T));
            }else{
                if(!T.getactivo()){
                    container.html("");
                    vect=[];
                    vectid=[];
                }
            }
        });

    });
}

function buscarTarea(id){
    $.post("searchTask",{"id":id}, function (value) {
        let T = new Tarea(value.id, value.nombre, value.descripcion, value.fechainicio,value.fechafin,value.active);
        return T;
    });
}

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
