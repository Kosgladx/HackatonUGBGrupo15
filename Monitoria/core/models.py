from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Grupo(models.Model):

    numero = models.IntegerField(unique=True)

    monitores = models.ManyToManyField(
        'Usuario',
        blank=True,
        related_name='grupos_monitorados'
    )

    def __str__(self):
        return f"Grupo {self.numero}"


class Usuario(AbstractUser):

    TIPOS = [
        ('monitor', 'Monitor'),
        ('integrante', 'Integrante')
    ]

    PERIODOS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    telefone_validator = RegexValidator(
        regex=r'^\d{2}\s\d{9}$',
        message='Formato correto: 24 999660787'
    )

    nome = models.CharField(max_length=100)

    matricula = models.CharField(
        max_length=20,
        unique=True
    )

    periodo = models.CharField(
        max_length=2,
        choices=PERIODOS
    )

    email = models.EmailField(
        unique=True
    )

    telefone = models.CharField(
        max_length=20,
        validators=[telefone_validator]
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome