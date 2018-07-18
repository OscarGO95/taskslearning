from django.db import models
from datetime import datetime, timedelta
from django.core.mail import EmailMessage

class Profesor(models.Model):#good
    '''
    Modelo de Profesor
    '''
    documento = models.IntegerField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)
    materias = models.ManyToManyField('Materia', through='profesorxmateria')
    grupos = models.ManyToManyField('Grupo', through='grupoxprofesor')

    def getTeacherinSession(self):
        '''
        Simula la búsqueda de un profesor que tenga una sesión iniciada
        :return: profesor con la sesión iniciada
        '''
        teacher = self.__class__. objects.get(nombres="John Alexander")
        return teacher

    def getTeacherID(self, id):
        '''
        :param id: id de un profesor a buscar en la Base de Datos

        se obtiene la información del profesor por medio del id y se guarda en la variable teacher

        :return teacher: Queryset con toda la información del profesor
        '''
        teacher = self.__class__.objects.get(id=id)
        print(teacher)
        return teacher


class Estudiante(models.Model):#good
    '''
    Modelo de Estudiante
    '''
    image = models.ImageField(upload_to='media/profileImages')
    documento = models.IntegerField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    celular = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    correo = models.EmailField(max_length=256)
    acudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    tareas = models.ManyToManyField('Tarea', through='AsignarTarea')
    isvisibleGame = models.BooleanField(default=False)


    def getStudentID(self, id):
        '''
        Se recibe un parámetro con el id del estudiante
        y se retorna el objeto con toda la información del estudiante
        :param id:  id del estudiante
        :return: Objeto Estudiante con toda la información
        '''
        return self.__class__.objects.get(id=id)


    def getStudent(self, grupo, denominacion):
        '''
        se buscan los estudiantes que pertenecen a un grupo con su denominación EJ: Grupo: Septimo Denominación: B
        :param grupo:  Grupo (Séptimo, Octavo, Décimo)
        :param denominación: denominación del grupo literales que determinan el número de grupos iguales que existen (A,B,C)
        :return: los estudiantes que pertenecen a grupo específico
        '''
        response = []
        data = self.__class__.objects.filter(grupo__denominacion=denominacion, grupo__nombre=grupo)
        for i in data:
            tmp = {}
            tmp["id"] = i.id
            tmp["documento"] = i.documento
            tmp["nombre"] = i.nombres
            tmp["apellido"] = i.apellidos
            tmp["imagen"] = i.image.url
            response.append(tmp)
        return response

    def setVisibleGame(self, estudiantes):
        '''
        :param estudiantes: Lista de id de estudiantes los cuales podrán visualizar el juego (Snake)

        Se obtienen los estudiantes de la base de datos
        se verifica que sus ids esten contenidos en la lista de estudiantes obtenida por parametro
        de contenerse se modifica la visibilidad del juego por Verdadera y en caso contrario el la
        visibilidad se modifica por Falsa se guarda el registro en la base de datos

        :return: None
        '''
        tmp = estudiantes.split(",")
        all = self.__class__.objects.all()
        for i in all:
            if str(i.id) in tmp:
                i.isvisibleGame = True
            else:
                i.isvisibleGame = False
            i.save()


class Grupo(models.Model):#good
    '''
    Modelo de Grupos
    contiene las materias que ve cada uno de los grupos y su respectiva denominación
    '''
    nombre = models.CharField(max_length=100)
    denominacion = models.CharField(max_length=100)
    materias = models.ManyToManyField('Materia', through='materiaxgrupo')


class Acudiente(models.Model):#good
    '''
    Modelo de Acudiente
    '''
    documento = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=256)


class Materia(models.Model):#good
    '''
    Modelo Materia
    '''
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)

    def getContenidos(self, materia):
        '''
        Obtiene los contenidos de una materia buscada por el nombre en específico
        :param materia: nombre de la materia
        :return: lista de temas de la materia seleccionada
        '''
        contenidos = []
        data = Contenidos.objects.filter(materia__nombre=materia)
        for i in data:
            contenidos.append(i.nombre)
        return contenidos


class Contenidos(models.Model):
    '''
    Modelos de Contenidos
    '''
    nombre = models.CharField(max_length=150)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)

    def getTemas(self, contenidos):
        '''
        Obtiene los temas específicos de un contenido
        :param contenidos:
        :return: Lista de temas
        '''
        temas = []
        data = Contenidos.objects.filter(contenido__nombre=contenidos)
        for i in data:
            temas.append(i.nombre)
        return temas

class Tarea(models.Model):#good
    '''
    Modelo de Tarea
    '''
    nombre = models.CharField(max_length=50)
    fecha_init = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)
    descripcion = models.CharField(max_length=256)
    file = models.FileField(upload_to='media/tareas', blank=True)
    activa = models.BooleanField(default=True)

class AsignarTarea(models.Model):#good
    '''
    Modelo usado para asignar una tarea a un estudiante
    '''
    tarea = models.ForeignKey('Tarea', on_delete=models.CASCADE, related_name='ext')
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, related_name='ext')

    def asignTask(self, request):
        '''
        Se crea una tarea con sus respectivos valores
        se Revisa si tiene un archivos adjunto si es así se guarda en la tarea
        sino el campo es None y se guarda la tarea en base de datos
        después se verifica para quien se va a publicar la tarea 1 para todos y se les asigna la tarea
        y si no es 1 se procede a verificar los ids contenidos en la petición y a los estudiantes que tengan ese código
        se les asigna la tarea
        cuando se les asigna la tarea se le envía un correo electrónico a los estudiantes con esta tarea asignada
        :param request: petición con todos los campos requeridos para realizar la asignación de tareas
        :return: None
        '''
        tarea = Tarea()
        tarea.nombre = request.POST['titulo_tarea']
        tarea.fecha_fin = request.POST['fecha_fin']
        tarea.fecha_init = request.POST['fecha_creacion']
        tarea.descripcion = request.POST["descripcion_tarea"]
        if request.FILES:
            tarea.file = request.FILES['fileUpload']
        else:
            tarea.file = None
        tarea.save()
        quienes = request.POST['selectpublicado']
        if quienes == "1":
            estudiantes = Estudiante.objects.all()
            for i in estudiantes:
                obj = AsignarTarea(estudiante=i, tarea=tarea)
                obj.save()
                email = EmailMessage('Tarea '+tarea.nombre+' Asignada', 'Entra al sitio para ver mas detalles', to=[i.correo])
                email.send()
        else:
            estudiantes = request.POST['estudiantes'].split("-")
            for i in estudiantes:
                tmp = Estudiante.objects.get(id=i)
                obj = AsignarTarea(estudiante=tmp, tarea=tarea)
                obj.save()
                email = EmailMessage('Tarea ' + tarea.nombre + ' Asignada', 'Entra al sitio para ver mas detalles',
                                     to=[i.correo])
                email.send()

    def getSizeTask(self, idx):
        '''
        obtiene el número de tarea de un estudiante en los siguientes 2 días
        :param idx: id del estudiante a verificar su número de tareas asignadas
        :return: número con el total de tareas asignadas en los próximos 2 días
        '''
        fechahoy = datetime.now().date()
        dias = timedelta(days=2)
        data = self.__class__.objects.filter(estudiante__id=idx, tarea__activa=1, tarea__fecha_fin__range=[str(fechahoy), str(fechahoy+dias)])
        return len(data)

    def getTasksActive(self, idx):
        '''
        Se buscan todas las tareas activas que tenga un estudiante para los siguientes 2 días
        :param idx: id del estudiante a buscar
        :return: Lista de tareas para el estudiante en cuestion
        '''
        tasks = []
        # tarea__activa=1
        fechahoy = datetime.now().date()
        dias = timedelta(days=2)
        data = self.__class__.objects.filter(estudiante__id=idx, tarea__fecha_fin__range=[str(fechahoy), str(fechahoy+dias)]).order_by('estudiante__tareas__fecha_fin')[:2]
        for i in data:
            tmp = {}
            tmp["id"] = i.tarea.id
            tmp["nombre"] = i.tarea.nombre
            tmp["descripcion"] = i.tarea.descripcion
            tmp["fechainicio"] = i.tarea.fecha_init
            tmp["fechafin"] = i.tarea.fecha_fin
            tmp["active"] = i.tarea.activa
            tasks.append(tmp)
        return tasks

    def getTask(self, id):
        '''
        busca una tarea específica
        :param id: id de la tareas a buscar
        :return: un objeto con los valores de la tarea
        '''
        data = self.__class__.objects.get(tarea__id=id)
        tmp = {}
        tmp["id"] = data.tarea.id
        tmp["nombre"] = data.tarea.nombre
        tmp["descripcion"] = data.tarea.descripcion
        tmp["fechainicio"] = data.tarea.fecha_init
        tmp["fechafin"] = data.tarea.fecha_fin
        tmp["active"] = data.tarea.activa
        return tmp

class grupoxprofesor(models.Model):#good
    '''
    Modelo Intermedios entre grupo y profesor
    se usa para saber que profesor le dicta clases a un grupo en especifico
    '''
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, related_name='gxp')
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, related_name='gxp')

class profesorxmateria(models.Model):#good
    '''
    Modelo intermedio para saber que materia dicta un profesor en específico
    '''
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, related_name='pxm')
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='pxm')

    def getMateriaToGrupo(self, idgrupo, denominacion, idp):
        '''
        Buscar las materias que un profesor le da a un grupo con su demnominacion
        :param idgrupo: Nombre del Grupo
        :param denominacion: Denominación del Grupo
        :param idp: Identificador del profesir
        :return: Lista de materias
        '''
        materias = []
        materiasprofesor = self.__class__.objects.filter(profesor_id=idp, materia__grupo__denominacion=denominacion, materia__grupo__nombre=idgrupo)
        for i in materiasprofesor:
            materias.append(i.materia.nombre)

        return materias

class materiaxgrupo(models.Model):
    '''
    Modelo intermedia entre materia y grupo
    se usa para saber que materia se le dicta a un grupo en específico
    '''
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='mxg')
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, related_name='mxg')
