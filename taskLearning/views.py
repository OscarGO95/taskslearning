
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from taskLearning.models import *

class Views:

    def loadTaksGUI(request):
        obj = Profesor()
        teacher = obj.getTeacherinSession()
        return render(request, "createTask.html", {"profesor": teacher})

    @csrf_exempt
    def getAsignatura(request):
        if request.method == "POST":
            obj = profesorxmateria()
            materias = obj.getMateriaToGrupo(request.POST['idgrupo'],request.POST['denominacion'],request.POST['idprofesor'])
            return JsonResponse({"materias":materias}, safe=False)

    @csrf_exempt
    def getTemas(request):
        if request.method == "POST":
            materia = request.POST['materia']
            obj = Materia()
            data = obj.getContenidos(materia)
        return JsonResponse({"contenidos": data}, safe=False)

    @csrf_exempt
    def getContenidos(request):
        obj = Contenidos()
        data = obj.getTemas(request.POST['contenido'])
        return JsonResponse({"temas": data}, safe=False)


    @csrf_exempt
    def getStudents(request):
        obj = Estudiante()
        data = obj.getStudent(request.POST['nombre'], request.POST['denominacion'])
        return JsonResponse({"estudiantes": data}, safe=False)

    @csrf_exempt
    def uploadTak(request):
        obj = AsignarTarea()
        obj.asignTask(request)
        return JsonResponse({}, safe=False)

    @csrf_exempt
    def verifyTasks(request, id):
        obj = AsignarTarea()
        tasks = obj.getTasksActive(id)
        return JsonResponse({"tasks": tasks}, safe=False)

    @csrf_exempt
    def getTask(request):
        obj = AsignarTarea()
        data = obj.getTask(request.POST['id'])
        return JsonResponse({"task": data}, safe=False)

    def getNumberTask(self,id):
        obj = AsignarTarea()
        data = obj.getSizeTask(id)
        return JsonResponse({"size": data}, safe=False)

    def loadDash(request):
        '''
        Renderiza el dashboard Inicial para el estudiante
        :return: render de la vista
        '''
        return render(request, "dashboard.html")

    def loadGame(request,id):
        '''
        Carga la vista con el juego del Snake para el estudiante con el id que llega por parametro
        :param id: id del estudainte
        :return: render de la vista con el objeto estudiante especifico
        '''
        obj = Estudiante()
        data = obj.getStudentID(id)
        return render(request, "game.html", {"estudiante":data})

    def dashboardTeacher(request, id):
        '''
        :param id: se recibe el id del profesor que esta en ese momento con la sesion iniciada

        se obtiene toda la info del profesor desde el modelo correspondiente

        :return: el render de la vista con el objeto con toda la info del profesor con la sesion iniciada y la vista que debe ser
        cargada
        '''
        obj = Profesor()
        response = obj.getTeacherID(id)
        return render(request, "dashboardTeacher.html", {"profesor": response})

    @csrf_exempt
    def asignGame(request):
        '''
        Se recibe por metodo post la lista de ids de los estudiantes los cuales podran visualizar el juego
        y se envia a los modelos correspondiente que se encarga de realizar las operaciones respectivas

        :return: Json vacio de confirmacion que es necesario para verificar la correcta actualizacion en la BD
        '''
        obj = Estudiante()
        obj.setVisibleGame(request.POST['estudiantes'])
        return JsonResponse({}, safe=False)

    def rutainutil(request):
        '''
        :return: renderiza la vista la cual esta contenida el juego Snake
        '''
        return render(request, "indexSnake.html")
