# -*- coding: utf-8 -*-
'''
Created on 26/05/2017

@author: fgome
'''

from EjerciciosClases.Ejercicios import procedureExcercise
from LatexProc.Cadenas import valida_ltx, ajusta_cad_latex, str2expr
from sympy import symbols, latex

class aritm_sucesion_exercise(procedureExcercise):
    def __init__(self, data):        
        funcs =  [] if not 'funcs' in data.keys() else data['funcs']
        math_prob = "" if not 'math_prob' in data.keys() else data['math_prob']
        ltx_math_prob = latex(math_prob) if not 'ltx_math_prob' in data.keys() else data['ltx_math_prob']
        self.tipo = 3 if not 'tipo' in data.keys() else data["tipo"] #debe se tipo 3 (sin paso a paso) o 4 (con revisión del paso a paso)
        self.procedure = [] if not "procedure" in data.keys() else data["procedure"] #proceso de solución
        self.right_steps = [] if not "steps" in data.keys() else data["steps"] #pasos para la solución del problema
        #guarda los datos del polinomio para poder regeneralo
        self.t1 = 0 if not 't1' in data.keys() else data['t1']
        self.d = 1 if not 'd' in data.keys() else data['d']
                                        
        super(aritm_sucesion_exercise,self).__init__(data['symbs'],funcs,data['preg'],math_prob,data['sol'],ltx_math_prob)
        
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()
        d['answers'] = []
        d['options'] = []
        d['procedure'] = self.procedure
        d['exType'] = self.tipo

        if self.d < 0:
            ans = "t_n = " + str(self.t1) + "-" + str(abs(self.d)) + "(n-1)"
        else:
            ans = "t_n = " + str(self.t1) + "+" + str(abs(self.d)) + "(n-1)"

        #ans = ans.replace('$','')
        d['dataToAssess'] = {"clase":"aritm_suc", "t1":self.t1, "d":self.d, 'ans': ans}
        return d
    
class geom_sucesion_exercise(procedureExcercise):
    def __init__(self, data):        
        funcs =  [] if not 'funcs' in data.keys() else data['funcs']
        math_prob = "" if not 'math_prob' in data.keys() else data['math_prob']
        ltx_math_prob = latex(math_prob) if not 'ltx_math_prob' in data.keys() else data['ltx_math_prob']
        self.tipo = 3 if not 'tipo' in data.keys() else data["tipo"] #debe se tipo 3 (sin paso a paso) o 4 (con revisión del paso a paso)
        self.procedure = [] if not "procedure" in data.keys() else data["procedure"] #proceso de solución
        self.right_steps = [] if not "steps" in data.keys() else data["steps"] #pasos para la solución del problema
        
        #guarda los datos del polinomio para poder regeneralo
        self.t1 = 1 if not 't1' in data.keys() else data['t1']
        self.f = 1 if not 'f' in data.keys() else data['f']
                                        
        super(geom_sucesion_exercise,self).__init__(data['symbs'],funcs,data['preg'],math_prob,data['sol'],ltx_math_prob)
        
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()
        d['answers'] = []
        d['options'] = []
        d['procedure'] = self.procedure
        d['exType'] = self.tipo
        ans = latex(self.getAnswer())
        ans = ans.replace('$','')
        d['dataToAssess'] = {"clase":"geom_suc", "t1":self.t1, "f":self.f, 'ans':ans}
        return d


def sucesion_aritm_formula_correcta(data,cad):
    
    #verifica que la cadena no esté vacía
    ltx_nsp = cad.replace(' ','')
    if len(ltx_nsp) == 0:
        return {"calif":-1, "msg":"Sin respuesta"}
    #verifica si el estudiante ingresó una igualdad
    ltx = ltx_nsp
    if ltx.find("=") >= 0:
        [li,ld] = ltx.split("=")
        ltx = ld        
    #analiza solamente el lado derecho
    d = valida_ltx(ltx,['n'],[])
    if not d['valida']:
        return {"calif":-1, "msg":"La solución está mal escrita"}
    else:
        ltx_ajst = ajusta_cad_latex(d['cad'],['n'])
        res = str2expr(ltx_ajst,['n'])        
        n = symbols("n")
        e = data["t1"]+(n-1)*data["d"]
        if e.equals(res):
            return {"calif":1, "msg":"Correcto"}
        else:
            return {"calif":0, "msg":"Incorrecto"}
        
def sucesion_geom_formula_correcta(data,cad):
    tu_resp = 'Tu respuesta fue:$$'+cad+'$$'
    correc = 'La respuesta correcta es: $$'+data['ans']+'$$'  
    
    
    #verifica que la cadena no esté vacía
    ltx_nsp = cad.replace(' ','')
    if len(ltx_nsp) == 0:
        msg = tu_resp+correc
        return {"calif":-1, "msg":msg}
    #verifica si el estudiante ingresó una igualdad
    ltx = ltx_nsp
    if ltx.find("=") >= 0:
        [li,ld] = ltx.split("=")
        ltx = ld        
    #analiza solamente el lado derecho
    d = valida_ltx(ltx,['n'],[])
    if not d['valida']:
        return {"calif":-1, "msg":"La respuesta está mal escrita"}
    else:
        ltx_ajst = ajusta_cad_latex(d['cad'],['n'])
        res = str2expr(ltx_ajst,['n'])        
        n = symbols("n")
        e = data["t1"]*data["f"]**(n-1)
        
        if e.equals(res):
            msg = tu_resp
            return {"calif":1, "msg":msg}
        else:
            msg = tu_resp+correc
            return {"calif":0, "msg":msg}
    
if __name__ == "__main__":
    d = {"t1":8, "f":2}
    ltx = "4\\times 2^{n}"
    print(sucesion_geom_formula_correcta(d,ltx))
         
    
    