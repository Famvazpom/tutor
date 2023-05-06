from .Cadenas import *
from gtts import gTTS
from django.utils.crypto import get_random_string


class math2speech:
    exponentes = None
    simbolos = None
    funciones = None
    lenguaje = None
    
    def __init__(self,exponentes=None,simbolos=None,funciones=None,lenguaje='es'):
        self.exponentes = {
            2: 'AL CUADRADO',
            3: 'AL CUBO',
            4: 'A LA CUARTA POTENCIA',
            5: 'A LA QUINTA POTENCIA',
            6: 'A LA SEXTA POTENCIA',
            7: 'A LA SÉPTIMA POTENCIA',
            8: 'A LA OCTAVA POTENCIA',
            9: 'A LA NOVENA POTENCIA',
            10: 'A LA DÉCIMA POTENCIA',
        } if not exponentes else exponentes
        
        self.simbolos = {
            '*':'por',
            '+':'mas',
            '/':'entre',
            '-':'menos',
            'tan': 'tangente de',
            'cos': 'coseno de',
            'sin': 'seno de',
            'atan': 'arcotangente de',
            'asin': 'arcoseno de',
            'acos': 'arcocoseno de',
            'sqrt': 'raiz cuadrada de',
            'cot': 'cotangente de',
            'csc': 'cosecante de',
            'sec': 'secante de',
            'exp': 'exponencial de',
            'ln': 'logaritmo natural de',
            'log': 'logaritmo de'
        } if not simbolos else simbolos
        self.funciones = ['atan','asin','acos','sqrt','sin','cos',
                          'tan','cot','csc','sec','exp','ln','log'] if not funciones else funciones
        self.lenguaje = 'es' if not lenguaje else lenguaje
        
    def procesaCadena(self,ltx,symbs):
        if not ltx or not symbs:
            return
        data = valida_ltx(ltx, symbs, funciones)
        cadena = data['cad']
        cadena_ajustada = ajusta_cadena(cadena,symbs) #procesa la cadena
        arbol = cad2tree(cadena_ajustada)
        expresion = tree2expr(arbol,0,symbs)
        return { 'arbol':arbol,'expresion':expresion}
    
   
    def simbolo_a_texto(self,valor):
        if not valor or valor == '0':
            return  ''
        if valor in self.simbolos.keys():
            return self.simbolos[valor]
        if '^' in valor and not '^(':
            valor_n = valor.replace('^','')
            valor_n = valor_n.replace('','')
            return self.exponentes.get(int(valor_n),f'A LA POTENCIA {valor_n}') if valor_n.isnumeric() else valor
        if '^(' in valor:
            valor_n = valor.replace('^(','')
            valor_n = valor_n.replace(')','')
            return self.exponentes.get(int(valor_n),f'A LA POTENCIA {valor_n}') if valor_n.isnumeric() else valor
        if ')=' in valor:
            valor = valor.replace(')','')
            return valor
        else:
            return valor
                
    '''
        Funcion obten_cadena
        Argumentos: 
            *index: Indice donde se comienza el recorrido del arbol.
            *tree: El arbol a recorrer
            *cadena: Cadena que se va armando

        Funcionamiento:
            Esta funcion se encarga de recorrer el arbol en cuestion, se obtienen las cadenas de texto de cada uno de los hijos
            y se ordenan de la siguiente manera dependiendo el caso:
                Cuando la cadena incluye tangente,seno, coseno, etc: Nodo actual, Cadena del hijo izquierdo, Cadena del hijo derecho
                En los demas casos: Cadena del hijo izquierdo, Nodo actual, Cadena del hijo derecho
    '''
    def obtenCadena(self,index=0,tree=None,cadena=''):
        if not index and index!=0:
            raise Exception('Se requiere el indice a empezar en el arbol')
        if not tree:
            raise Exception("Se requiere el arbol a recorrer")
        if index > len(tree):
            raise Exception("El indice debe ser menor a la longitud del arbol")
        nodo = tree[index]
        izq = ''
        der = ''
        if nodo.get('ind_h1',None):
            izq = self.obtenCadena(index=nodo['ind_h1'],tree=tree,cadena=cadena)
        centro = self.simbolo_a_texto(tree[index]['val'])
        if nodo.get('ind_h2',None):
            der = self.obtenCadena(index=nodo['ind_h2'],tree=tree,cadena=cadena)

        cadena = f'{izq} {centro} {der}' if not nodo['val'] in self.funciones else f'{centro} {izq} {der}'
        return cadena
    
    def generaAudio(self,cadena,filename='math2speech.mp3'):
        voz = gTTS(text=cadena,lang=self.lenguaje,slow=False)
        voz.save(filename)
        return
     
    
    def procesoCompleto(self,ltx=None,variables=None,filename='math2speech.mp3'):
        if not ltx:
            raise Exception('Es necesario la cadena latex')
        if not variables:
            raise Exception('Es necesario la lista de variables')
        datos = self.procesaCadena(ltx,variables)
        cadena = self.obtenCadena(0,datos['arbol'])
        cadena = cadena.replace(' .','')
    