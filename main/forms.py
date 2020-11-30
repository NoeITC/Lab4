
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Localizacion, Categoria, Cliente, Colaborador

#lo usaremos para generar nuestro formulario de registro
class UserForm(UserCreationForm):
    # django.contrib.auth.User attributese
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=150)
    # Profile attributes
    documento_identidad = forms.CharField(max_length=8)
    fecha_nacimiento = forms.DateField()
    estado = forms.CharField(max_length=3)
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario'),
    ]
    genero = forms.ChoiceField(choices=GENERO_CHOICES)

    #Agregamos los datos de los modelos Cliente y Colaborador

    #Atributos de Cliente
    is_cliente = forms.BooleanField(required=False)
    preferencias = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False)

    #Atributos de Colaborador
    is_colaborador = forms.BooleanField(required=False)
    reputacion = forms.FloatField(required=False)
    cobertura_entrega = forms.ModelChoiceField(queryset=Localizacion.objects.all(), required=False)


    # Nos permite indicarle que modelo de datos esta asociado a este formulario (en este caso User) y tambien personalizarlo. Por ejemplo el atributo field permite definir el orden en el que los usuarios veran los campos a llenar del formulario:
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','documento_identidad','fecha_nacimiento','estado','genero','is_colaborador','reputacion','cobertura_entrega',]
