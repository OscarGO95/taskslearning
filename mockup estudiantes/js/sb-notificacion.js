let vect = [];
let vectid = [];
let container = $('.container-fluid');
$(function () {
    setInterval(loadTarea, 500);
});


function loadTarea() {
    var fields = "";
    $.get("https://jsonplaceholder.typicode.com/posts", function (data) {
        $.each(data, function (index, value) {
            let T = new Tarea(value.userId, value.id, value.title, value.body);
            if ((!vectid.includes(T.getid())) && T.getid() <=4) {
                vectid.push(T.getid());
                vect.push(T);
                container.append(createtask(T));
            }
        });
    });
}




class Tarea {
    constructor(userid, id, title, body) {
        this.userid = userid;
        this.id = id;
        this.title = title;
        this.body = body;
    }

    getuserid() {
        return this.userid;
    }

    getid() {
        return this.id;
    }

    gettitle() {
        return this.title;
    }

    getbody() {
        return this.body;
    }
}

function createtask(Tarea) {
    let datafield="";
    datafield+='<div class="card mb-3">';
    datafield+='<div class="card-header">';
    datafield+='<i class="fa fa-table"></i>'+Tarea.getid()+'</div>';
    datafield+='<div class="card-body">';
    datafield+='<p><strong>Note:</strong> Internet Explorer 9 and earlier versions do not support Web Workers.</p>';
    datafield+='</div>';
    datafield+='<div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>';
    datafield+='</div>';
    return datafield;
}
