from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
    titulo = models.CharField(max_length=50)
    cuerpo = models.TextField()
    fecha_creacion = models.DateField()
    imagen = models.ImageField(upload_to='blogs', null=True, blank=True)
    publico = models.BooleanField()
    visitas = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + " " + str(self.fecha_creacion) + " " + str(self.visitas) + " " + ("Publico" if self.publico else "No publico") + " " + self.user.username