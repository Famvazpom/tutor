# End points del tutor virtual unicaribe

## End points referentes a los modelos de la base de datos:

#### Nota importante:
Es necesario iniciar sesion en el tutor virtual para poder realizar consultas a cualquiera de estos endpoints.

### tutor/api/materias/ 

En este endpoint podras consultar todas las materias ingresadas en el tutor virtual



### tutor/api/materias/id/

En este endpoint podras consultar una materia especifica, esta retorna sus datos base, los temas que esten relacionados a ella y la primera explicacion de cada tema.

Con este endpoint se puede realizar la mayoria de las operaciones

Para entender eso puedes usar el siguiente diagrama

* Materia 
    * id - Id de la materia
    * nombre - Nombre de la materia
    * corto - Nombre corto de la materia
    * temas [ - Lista de temas de esta materia
        * id - Id del tema
        * nombre - Nombre del tema
        * explicacion - Primera parte de la explicacion del tema
        [
            * anterior - Enlace a la parte anterior
            * siguiente - Enlace a la parte siguiente
            * titulo - Titulo de esta seccion
            * descripcion - Texto a mostrar
            * voz - Archivo de voz
        ]
* ]

Ejemplo de un objeto:
```
{
        "id": 1,
        "temas": [
            {
                "id": 1,
                "explicacion": {
                    "id": 4,
                    "anterior": "/tutor/api/explicaciones/1/",
                    "siguiente": null,
                    "titulo": "FACTORIZACION DE BINOMIOS CON TERMINO COMUN 2",
                    "descripcion": "Observa que del producto se obtuvieron tres términos y además:\r\n\r\n+ Uno de los tres términos es el cuadrado del término común de ambos binomios.\r\n+ Otro de los tres términos es el producto de los términos que no son comunes en los binomios.\r\n+ El término restante es la suma de los términos no comunes multiplicados por el término común en los binomios.\r\n\r\nEstas observaciones son la clave para realizar la factorización, la cual es el proceso inverso del desarrollo del producto notable:\r\n\r\n\\begin{equation}\r\nx^2+(a+b)x+ab =  (x+a)(x+b)\r\n\\end{equation}",
                    "voz": "/media/voz/None_FACTORIZACION_DE_BINOMIOS_CON_TERMINO_COMUN_2.mp3"
                },
                "nombre": "FACTORIZACION"
            },
            {
                "id": 2,
                "explicacion": {
                    "id": 3,
                    "anterior": "/tutor/api/explicaciones/2/",
                    "siguiente": null,
                    "titulo": "Monomio común Parte 2",
                    "descripcion": "Observa que para factorizar el producto de un monomio por un polinomio seguimos los siguientes pasos:\r\n\r\n+ Identificamos el máximo común divisor de los términos del polinomio.\r\n+ Dividimos el polinomio entre el máximo común divisor con lo que obtenemos un factor. El segundo factor es el máximo común divisor.",
                    "voz": "/media/voz/None_Monomio_com%C3%BAn_Parte_2.mp3"
                },
                "nombre": "FACTORIZACION DE MONOMIOS"
            }
        ],
        "nombre": "PROPEDEUTICO DE MATEMATICAS",
        "corto": "PROPEDEUTI",
        "codigo": "MT-4716"
    }
```

### tutor/api/temas

En este endpoint podras consultar todos los temas ingresados en el tutor virtual



### tutor/api/temas/id/

En este endpoint podras consultar un tema especifico, retorna su información base y la primera parte de la explicacion del tema.

Ejemplo de un objeto
```
  {
        "id": 1,
        "explicacion": {
            "id": 4,
            "tema": {
                "id": 1,
                "materia": {
                    "id": 1,
                    "nombre": "PROPEDEUTICO DE MATEMATICAS",
                    "corto": "PROPEDEUTI",
                    "codigo": "MT-4716"
                },
                "nombre": "FACTORIZACION"
            },
            "anterior": "/tutor/api/explicaciones/1/",
            "siguiente": null,
            "titulo": "FACTORIZACION DE BINOMIOS CON TERMINO COMUN 2",
            "descripcion": "Observa que del producto se obtuvieron tres términos y además:\r\n\r\n+ Uno de los tres términos es el cuadrado del término común de ambos binomios.\r\n+ Otro de los tres términos es el producto de los términos que no son comunes en los binomios.\r\n+ El término restante es la suma de los términos no comunes multiplicados por el término común en los binomios.\r\n\r\nEstas observaciones son la clave para realizar la factorización, la cual es el proceso inverso del desarrollo del producto notable:\r\n\r\n\\begin{equation}\r\nx^2+(a+b)x+ab =  (x+a)(x+b)\r\n\\end{equation}",
            "voz": "/media/voz/None_FACTORIZACION_DE_BINOMIOS_CON_TERMINO_COMUN_2.mp3"
        },
        "nombre": "FACTORIZACION"
    },
```

### tutor/api/explicaciones

En este endpoint podras consultar todas las explicaciones ingresados en el tutor virtual

### tutor/api/explicaciones/

En este endpoint podras consultar una explicacion en especifico, entrega sus datos base, un enlace a la parte anterior y un enlace a la parte siguiente.

Debes enviar el id del tema por query para obtener una explicación.

Ejemplo:
```
    tutor/api/explicaciones/?tema=1
```


Ejemplo de un objeto
```
    {
       "id": 51,
        "anterior": null,
        "siguiente": "/tutor/api/explicaciones-data/52/",
        "titulo": "FACTORIZACION 4 b^{2} + 28 b + 49",
        "descripcion": "$4 b^{2} + 28 b + 49$",
        "voz_texto": "En este ejemplo, vamos a factorizar el polinomio: $4 b^{2} + 28 b + 49$",
        "voz": "/media/voz/51_FACTORIZACION_4_b%5E%7B2%7D_%2B_28_b_%2B_49.mp3",
        "dificultad": 2,
        "detalles": null
    }
```

Los siguientes datos deben aparecer en la plataforma:
* Descripcion : Es lo que aparecera en la "pizarra"
* Voz: El archivo de voz que se esta utilizando
* Detalles: Estos detalles deben aparecer como un ? el cual con un hover se muestren.
* Siguiente: Enlace a la siguiente parte de la explicacion
* Anterior: Enlace a la parte anterior de la explicacion

Datos extra: 
* voz_texto: Transcripcion de la voz a texto
* Id: Id de la explicacion
* dificutlad: Nivel de dificultad de la explicacion.


### tutor/api/estudiante

En este endpoint podras recibir toda la informacion relevante del estudiante que inicio sesion.

```
    [
        {
            "id": 1,
            "nombre": "NOE VAZQUEZ POMPA",
            "materias": [
                {
                    "id": 1,
                    "temas": [
                        {
                            "tema": {
                                "id": 1,
                                "nombre": "FACTORIZACION",
                                "clave": null
                            },
                            "nivel": 2,
                            "maestria": 0.0
                        },
                        {
                            "tema": {
                                "id": 3,
                                "nombre": "FACTORIZACION DE BINOMIOS CUADRADOS",
                                "clave": "fact_bin2"
                            },
                            "nivel": 3,
                            "maestria": 0.6826417596961675
                        }
                    ],
                    "nombre": "PROPEDEUTICO DE MATEMATICAS",
                    "corto": "PROPEDEUTI",
                    "codigo": "MT-4716"
                }
            ],
            "programa_educativo": {
                "nombre": "IDEIO",
                "codigo": "ADSSAEQW"
            }
        }
    ]
```

### tutor/api/ejercicio

En este endpoint podras recibir un ejercicio para el estudiante.

### tutor/api/ejercicio/

Params: 
* id: Id del ejercicio 
* tema: Id del tema del ejercicio

Si envias el ID del ejercicio te entregara el ejercicio en cuestion por ejemplo:
```
    {
        "id": 12,
        "ejercicio": {
            "id": 86,
            "tema": {
                "id": 3,
                "nombre": "FACTORIZACION DE BINOMIOS CUADRADOS",
                "clave": "fact_bin2"
            },
            "enunciado": "Factoriza la siguiente expresión: $$y^{2} - 8 y + 16$$",
            "respuesta": "5",
            "opciones": "['$$\\\\left(y + 4\\\\right)^{2}$$', '$$\\\\left(y + 2\\\\right)^{2}$$', '$$\\\\left(y + 8\\\\right)^{2}$$', '$$\\\\left(y - 8\\\\right)^{2}$$', '$$\\\\left(y - 2\\\\right)^{2}$$', '$$\\\\left(y - 4\\\\right)^{2}$$']",
            "dificultad": 1
        },
        "correcto": true,
        "fecha_inicio": "2023-03-07T17:26:13.634703Z",
        "fecha_fin": "2023-03-07T17:46:18.074467Z",
        "intentos": 1,
        "primera_respuesta": true,
        "estudiante": 1
    }
```

En caso de no enviar el ID, es necesario enviar el id del tema del ejercicio para poder generar un ejercicio:


#### POST

Para realizar un POST a este endpoint es necesario dos cosas:
* id: Id del ejercicio
* aswer: Id de la respuesta entregada

Te retornara el objeto actualizado, el parametro "correcto" determina si la respuesta fue correcta o no.


### refresh-token/

En este end point puedes refrescar el token en caso de que expire.

#### POST

Para realizar un POST a este endpoint es necesario una cosa en el body:
* token: token a refrescar

### verify-token/

En este end point puedes verificar el token en caso de que expire.

#### POST

Para realizar un POST a este endpoint es necesario una cosa en el body:
* token: token a verificar