from django.test import TestCase
from django.core.mail import EmailMessage

# Create your tests here.
from taskLearning.models import Tarea, Estudiante, Grupo, Acudiente, AsignarTarea


class TaskTest(TestCase):

    def setUp(self):
        tarea = Tarea(nombre="Ecuaciones",fecha_fin="2018-06-27",fecha_init="2018-06-23",descripcion="realizar el taller",activa=1)
        tarea.save()
        acudiente = Acudiente(documento="102030", nombres="fulano", apellidos="detal", telefono="321456987", correo="tasklearning4@gmail.com")
        acudiente.save()
        grupo = Grupo(nombre="decimo", denominacion="C")
        grupo.save()
        estudiante = Estudiante(image="", documento="908765", nombres="cristino", apellidos="perez", celular="65478952156", direccion="lejos", correo="tasklearning4@gmail.com", acudiente=acudiente, grupo=grupo)
        estudiante.save()

        estudiante1 = Estudiante(image="", documento="908765", nombres="fernando", apellidos="perez",
                            celular="65478952156", direccion="lejos", correo="tasklearning4@gmail.com",
                            acudiente=acudiente, grupo=grupo)

        estudiante1.save()

    def test_asignartarea(self):
        estudiante = Estudiante.objects.get(id=1)
        tarea = Tarea.objects.get(nombre="Ecuaciones")
        asig = AsignarTarea(estudiante=estudiante, tarea=tarea)
        asig.save()
        self.assertEqual(asig.estudiante.nombres,"cristino")

    def test_sendEmail(self):
        tarea = Tarea.objects.get(nombre="Ecuaciones")
        estudiante = Estudiante.objects.get(nombres="cristino")
        email = EmailMessage('Tarea ' + tarea.nombre + ' Asignada', 'Entra al sitio para ver mas detalles',
                             to=[estudiante.correo])
        email.send()
        self.assertTrue("Enviado")

    def test_tareavariosestudiantes(self):
        tarea = Tarea.objects.get(nombre="Ecuaciones")
        estudiantes = Estudiante.objects.filter(grupo__denominacion="decimo", grupo__nombre="C")
        for i in estudiantes:
            email = EmailMessage('Tarea ' + tarea.nombre + ' Asignada', 'Entra al sitio para ver mas detalles',
                                 to=[i.correo])
            email.send()
        self.assertTrue("Enviado")
