from django.db import models


class Profesor(models.Model):#good
    documento = models.IntegerField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)
    materias = models.ManyToManyField('Materia', through='profesorxmateria')
    grupos = models.ManyToManyField('Grupo', through='grupoxprofesor')

    def getTeacherinSession(self):
        teacher = self.__class__. objects.get(nombres="John Alexander")
        return teacher



class Estudiante(models.Model):#good
    image = models.FileField(upload_to='media/profileImages')
    documento = models.IntegerField()
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    celular = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    correo = models.EmailField(max_length=256)
    acudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    tareas = models.ManyToManyField('Tarea', through='AsignarTarea')


class Grupo(models.Model):#good
    nombre = models.CharField(max_length=100)
    denominacion = models.CharField(max_length=100)
    materias = models.ManyToManyField('Materia', through='materiaxgrupo')


class Acudiente(models.Model):#good
    documento = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=256)


class Materia(models.Model):#good
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)

    def getContenidos(self, materia):
        contenidos=[]
        data = Contenidos.objects.filter(materia__nombre=materia)
        for i in data:
            contenidos.append(i.nombre)
        return contenidos


class Contenidos(models.Model):
    nombre = models.CharField(max_length=150)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)

    def getTemas(self, contenidos):
        temas=[]
        data = Contenidos.objects.filter(contenido__nombre=contenidos)
        for i in data:
            temas.append(i.nombre)
        return temas


class Tarea(models.Model):#good
    nombre = models.CharField(max_length=50)
    fecha_init = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)
    descripcion = models.CharField(max_length=256)
    file = models.FileField(upload_to='media/tareas', blank=True)


class AsignarTarea(models.Model):#good
    tarea = models.ForeignKey('Tarea', on_delete=models.CASCADE, related_name='ext')
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, related_name='ext')

    def asignTask(self, request):
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
        else:
            pass



class grupoxprofesor(models.Model):#good
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, related_name='gxp')
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, related_name='gxp')


class profesorxmateria(models.Model):#good
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, related_name='pxm')
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='pxm')

    def getMateriaToGrupo(self,idgrupo, denominacion, idp):
        materias = []
        materiasprofesor = self.__class__.objects.filter(profesor_id=idp, materia__grupo__denominacion=denominacion,
                                                           materia__grupo__nombre=idgrupo)
        for i in materiasprofesor:
            materias.append(i.materia.nombre)

        return materias


class materiaxgrupo(models.Model):
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name='mxg')
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, related_name='mxg')
