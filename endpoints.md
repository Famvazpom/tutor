# End points del tutor virtual unicaribe

## End points referentes a los modelos de la base de datos:

#### Nota importante:
Es necesario iniciar sesion en el tutor virtual para poder realizar consultas a cualquiera de estos endpoints.

### tutor/api/materias/ 

En este endpoint podras consultar todas las materias ingresadas en el tutor virtual



### tutor/api/materias/id/

En este endpoint podras consultar una materia especifica y modificarla en caso de ser necesario

Ejemplo de un objeto:
```
    {
        "id": 1,
        "nombre": "PROPEDEUTICO DE MATEMATICAS",
        "codigo": "MT-4716"
    }
```

### tutor/api/temas

En este endpoint podras consultar todos los temas ingresados en el tutor virtual



### tutor/api/temas/id/

En este endpoint podras consultar un tema especifico y modificarlo en caso de ser necesario.

Ejemplo de un objeto
```
 {
        "id": 1,
        "materia": {
            "id": 1,
            "nombre": "PROPEDEUTICO DE MATEMATICAS",
            "codigo": "MT-4716"
        },
        "nombre": "FACTORIZACION"
    }
```

### tutor/api/explicaciones

En este endpoint podras consultar todas las explicaciones ingresados en el tutor virtual

### tutor/api/explicaciones/id/

En este endpoint podras consultar una explicacion en especifico y modificarla en caso de ser necesario.

Ejemplo de un objeto
```
{
        "id": 1,
        "tema": {
            "id": 1,
            "materia": {
                "id": 1,
                "nombre": "PROPEDEUTICO DE MATEMATICAS",
                "codigo": "MT-4716"
            },
            "nombre": "FACTORIZACION"
        },
        "titulo": "PRUEBA",
        "descripcion": "Recordemos del tema de productos notables que el producto de binomios con un término común genera el siguiente resultado:\r\n\\begin{equation}\r\n(x+a)(x+b) = x^2+(a+b)x+ab\r\n\\end{equation}\r\n\r\nObserva que del producto se obtuvieron tres términos y además:\r\n\r\n+ Uno de los tres términos es el cuadrado del término común de ambos binomios.\r\n+ Otro de los tres términos es el producto de los términos que no son comunes en los binomios.\r\n+ El término restante es la suma de los términos no comunes multiplicados por el término común en los binomios.\r\n\r\nEstas observaciones son la clave para realizar la factorización, la cual es el proceso inverso del desarrollo del producto notable:\r\n\r\n\\begin{equation}\r\nx^2+(a+b)x+ab =  (x+a)(x+b)\r\n\\end{equation}",
        "voz": "http://localhost:8000/media/voz/1_PRUEBA.mp3",
        "anterior": null,
        "siguiente": null
    }
```

### tutor/api/ejercicios

En este endpoint podras consultar todos los ejercicios generados en el tutor virtual

### tutor/api/ejercicios/id/

En este endpoint podras consultar un ejercicio especifico y modificarlo en caso de ser necesario.

Ejemplo de un objeto
```
     {
        "id": 1,
        "tema": {
            "id": 1,
            "materia": {
                "id": 1,
                "nombre": "PROPEDEUTICO DE MATEMATICAS",
                "codigo": "MT-4716"
            },
            "nombre": "FACTORIZACION"
        },
        "enunciado": "Factoriza la siguiente expresión: $$x^{4} y^{2} z^{2} - 6 x^{3} y z - 6 x^{2} y^{3} z^{3} + 9 x^{2} + 18 x y^{2} z^{2} + 9 y^{4} z^{4}$$",
        "respuesta": "\\left(x^{2} y z - 3 x - 3 y^{2} z^{2}\\right)^{2}",
        "alumno": 1
    },
```

### tutor/api/ejercicios/id_tema/generar

En este endpoint podras generar un ejercicio aleatorio del tema seleccionado y asignarlo al usuario que realiza la petición.
