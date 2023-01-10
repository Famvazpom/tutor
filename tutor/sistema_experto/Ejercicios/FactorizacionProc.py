# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 11:19:23 2014

@author: fernando
"""

from tutor.sistema_experto.LatexProc.Cadenas import factores
from sympy import expand, symbols, latex
from tutor.sistema_experto.EjerciciosClases.Ejercicios import *
#from EjProdNotFact import fact_dif_cub_proc, fact_bin_conj_proc, mix_fact_proc
#from EjProdNotFact import selecc_fact, fact_bin_cuad_proc, fact_prod_bins_proc, fact_prod_monomio_poly_proc
from tutor.sistema_experto.Ejercicios.exp_systm_fact_tree import polinomio, explica_fact
from tutor.sistema_experto.Assess.FactorAssess import factorEsSolucion, factorPasoCorrecto

class procedureFactor(procedureExcercise):    
    def __init__(self, d_ext):        
        
        d = {}
        d['preg'] = d_ext['preg']
        d['symbs'] = d_ext['symbs']
        if type(d_ext['e']) in [str]:
            d['e'] = eval(d_ext['e'])
        else:
            d['e'] = d_ext['e']
        
        if type(d_ext['ef']) in [str]:
            d['ef'] = eval(d_ext['ef'])
        else:
            d['ef'] = d_ext['ef']
        
        self.ltx_ans = latex(d['ef'])
        self.ltx_math_prob = latex(d['e'])
        ltx_math_prob = latex(d['e']) #expresión latex del problema a resolver
        #la lista de funciones está vacía pues no es necesaria en un polinomio
        
        self.e = d['e']
        self.ef = d['ef']
        
        super(procedureFactor,self).__init__(d['symbs'],[],d['preg'],d['e'],d['ef'],ltx_math_prob)
        
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()
        
        #print d
        
        d['answers'] = []
        
        #intenta resolver el problema de factorización        
        d['options'] = [None]
        d['exType'] = 4
        d['ltxMathProb'] = self.ltx_math_prob
        sol_of = self.ef.as_ordered_factors()
        if sol_of[0] == -1:
            sol_of[1] = -sol_of[1]
            sol_of = sol_of[1:]
        sol_of = [latex(f) for f in sol_of]                    
        d['dataToAssess'] = {"clase":"Factorizacion", 'symbs':self.symbs, 'ans':self.ltx_ans, 'sol_ofs':sol_of}        
        
        solvd = self.procedimiento(d)
        
        if solvd['solvd']['calif'] != 1:
            d['not_solvd'] = True
        else:
            d['procedure'] = [solvd['procedure']]
                 
        return d
    
    def procedimiento(self,data):
        
        #verifica que el problema se pueda resolver
        ltx = latex(self.e)            
        #pasa el polinomio a factorizar
        poly = polinomio(pol_ltx = ltx, symbs = data['dataToAssess']['symbs'])
        pol = poly.getPoly()        
        
        #explicación de la factorización
        exp_f = explica_fact(ltx)    
        sol = exp_f.factoriza(pol,data['dataToAssess']['symbs'],None)        
        e = exp_f.latex_explicacion()        
        resp = {}
        resp['procedure'] = e['exp']
        #resp['solvd'] = latex(sol) 
        resp['solvd'] = factorEsSolucion(data['dataToAssess'], latex(sol))
        #resp['solvd'] = factorEsSolucion(data['dataToAssess'], latex(sol))        
        return resp
    
    #indica si la cadena guarda un resultado que es equivalente
    #al problema original
    # la función regresa:
    #  -1 Si la cadena no es válida (error de sintaxis)
    #   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
    #   1 Si el paso es correcto
    def esSolucion(self, ltx):
        if len(ltx.replace(' ','')) == 0:
            return -1        
        #verifica primero que la cadena sea válida
        d = super(procedureFactor,self).validaLtx(ltx)
        
        if not d['valida']:
            return -1
            
        #utilizar la función de la clase
        cad = d['cad']       
        
        e = super(procedureFactor,self).cad2exp(cad)

        if e == False:
            return 0            
        else:
            digs = ['0','1','2','3','4','5','6','7','8','9']
            #factores de la solución
            sol_of = self.answer.as_ordered_factors()
            #e_of = e.as_ordered_factors()
            e_st_factor = factores(ajusta_cadena(cad,self.symbs))
            
            e_of = [super(procedureFactor,self).cad2exp(f) for f in e_st_factor]
            
            #detecta si algún factor es una constante
            #y si ec_of y ec_of tienen diferente tamaño
            
            dif = 1
            for f in e_of:
                if f in sol_of:
                    sol_of.remove(f)
                elif -f in sol_of:
                    sol_of.remove(-f)
                    dif = -dif
                #busca dividir el factor entre otro
                else:
                    found = False
                    f_ot = f.as_ordered_terms()                    
                    for ff in sol_of:
                        ff_ot = ff.as_ordered_terms()
                        if len(f_ot) == len(ff_ot):                                                
                            d = factor(f)/factor(ff)
                            ad = abs(d)
                            is_num = True
                            st_d = str(ad)                          
                            for s in st_d:
                                if not s in digs:
                                    is_num = False
                                    break
                            if is_num:
                                sol_of.remove(ff)
                                dif = dif*d
                                found = True
                                break                            
                    if not found:
                        dif = dif*f
            
            pr = 1
            for f in sol_of:
                pr = pr*f
             
            if (dif == 1 or dif == -1) and dif == pr:
                return 1
            elif dif == pr and (str(dif) in e_st_factor or str(-dif) in e_st_factor):
                return 1
            else:
                return 0

    #indica si la cadena guarda un resultado que es equivalente
    #al problema original
    # la función regresa:
    #  -1 Si la cadena no es válida (error de sintaxis)
    #  -2 Si no se presenta un cambio con respecto al paso anterior
    #   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
    #   1 Si el paso es correcto
    def pasoCorrecto(self,ltx):
        if len(ltx.replace(' ','')) == 0:
            return -1

        d = super(procedureFactor,self).validaLtx(ltx)

        #la cadena no es válida (error de sintaxis)
        if not d['valida']:
            return -1
        
        #el paso es diferente al anterior
        if self.last_step == ltx:
            return -2
        
        #utilizar la función de la clase
        cad = d['cad']
        e = super(procedureFactor,self).cad2exp(cad)

        if e == False:
            return 0
        else:
            #extiende la cadena  la compara con el resultado
            ext_e = expand(e)
            if ext_e == self.math_prob:
                self.last_step = ltx
                return 1
            else:
                return 0


'''
#la subclase guarda el objeto de sympy que permite comparar después la respuesta
#la clase procedureFactor agrega métodos que 
#permiten verificar que
# 1.- el texto de entrada es válido (debe implementarse en las subclases)
# 2.- una vez que la cadena de texto es validada se compara con el resultado
# guardado en el objeto
        
class procedureFactor(procedureExcercise):    
    def __init__(self, tipo='mon_poly', nlits=2, deg=2, nterms=3, d_ext = {}):
        if tipo == 'mon_poly':
            d = fact_prod_monomio_poly_proc('t','n',nlits,nterms,deg)             
        elif tipo == 'prod_bins_simp':
            d = fact_prod_bins_proc('t','n',nlits,True)
        elif tipo == 'prod_bins':
            d = fact_prod_bins_proc('t','n',nlits,False)
        elif tipo == 'bin_cuad':
            d = fact_bin_cuad_proc('t','n',nlits,5)
        elif tipo == 'bin_conj':
            d = fact_bin_conj_proc('t','n',nlits,deg,5,0,0,4)
        elif tipo == 'dif_cub':
            d = fact_dif_cub_proc('t','n',nlits,deg,0,0,2)
        elif tipo == 'mix':
            d = mix_fact_proc('t','n')
        elif tipo == 'dict':
            d = d_ext
        elif tipo == 'ext': #el ejercicio se genera con 
            a,b,c = symbols('a,b,c')
            x,y,z = symbols('x,y,z')
            
            d = {}
            d['preg'] = d_ext['preg']
            d['symbs'] = d_ext['symbs']
            d['e'] = eval(d_ext['e'])
            d['ef'] = eval(d_ext['ef'])
        
        self.ltx_ans = latex(d['ef'])
        self.ltx_math_prob = latex(d['e'])
        
        ltx_math_prob = latex(d['e']) #expresión latex del problema a resolver
        #la lista de funciones está vacía pues no es necesaria en un polinomio
        super(procedureFactor,self).__init__(d['symbs'],[],d['preg'],d['e'],d['ef'],ltx_math_prob)
        
    def getData(self):
        d = {}
        d['question'] = self.getQuestion()
        d['answers'] = []
        
        #intenta resolver el problema de factorización
        
        
        d['procedure'] = []
        d['options'] = [None]
        d['exType'] = 4
        d['ltxMathProb'] = self.ltx_math_prob
        d['dataToAssess'] = {"clase":"Factorizacion", 'symbs':self.symbs, 'ans':self.ltx_ans}
        solvd = self.procedimiento(d)
        if solvd['solvd'] != 1:
            d['not_solvd'] = True
        else:
            d['procedure'] = [solvd['procedure']] 
        return d
    
    def procedimiento(self,data):
        #explicación de la factorización
        poly = polinomio(pol_ltx = data['ltxMathProb'], symbs = data['dataToAssess']['symbs'])
        pol = poly.getPoly()        
        exp_f = explica_fact()    
        sol = exp_f.factoriza(pol,data['dataToAssess']['symbs'],None)
        e = exp_f.latex_explicacion()
        resp = {}
        resp['procedure'] = e['exp']
        resp['solvd'] = factorEsSolucion(data['dataToAssess'], latex(sol))
        return resp 
        
        
    
    #indica si la cadena guarda un resultado que es equivalente
    #al problema original
    # la función regresa:
    #  -1 Si la cadena no es válida (error de sintaxis)
    #   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
    #   1 Si el paso es correcto
    def esSolucion(self, ltx):
        if len(ltx.replace(' ','')) == 0:
            return -1
                
        #verifica primero que la cadena sea válida
        d = super(procedureFactor,self).validaLtx(ltx)
        
        if not d['valida']:
            return -1
            
        #utilizar la función de la clase
        cad = d['cad']       
        
        e = super(procedureFactor,self).cad2exp(cad)

        if e == False:
            return 0            
        else:
            digs = ['0','1','2','3','4','5','6','7','8','9']
            #factores de la solución
            sol_of = self.answer.as_ordered_factors()
            #e_of = e.as_ordered_factors()
            e_st_factor = factores(ajusta_cadena(cad,self.symbs))
            
            e_of = [super(procedureFactor,self).cad2exp(f) for f in e_st_factor]
            
            #detecta si algún factor es una constante
            #y si ec_of y ec_of tienen diferente tamaño
            
            dif = 1
            for f in e_of:
                if f in sol_of:
                    sol_of.remove(f)
                elif -f in sol_of:
                    sol_of.remove(-f)
                    dif = -dif
                #busca dividir el factor entre otro
                else:
                    found = False
                    f_ot = f.as_ordered_terms()                    
                    for ff in sol_of:
                        ff_ot = ff.as_ordered_terms()
                        if len(f_ot) == len(ff_ot):                                                
                            d = factor(f)/factor(ff)
                            ad = abs(d)
                            is_num = True
                            st_d = str(ad)                          
                            for s in st_d:
                                if not s in digs:
                                    is_num = False
                                    break
                            if is_num:
                                sol_of.remove(ff)
                                dif = dif*d
                                found = True
                                break                            
                    if not found:
                        dif = dif*f
            
            pr = 1
            for f in sol_of:
                pr = pr*f
             
            if (dif == 1 or dif == -1) and dif == pr:
                return 1
            elif dif == pr and (str(dif) in e_st_factor or str(-dif) in e_st_factor):
                return 1
            else:
                return 0

    #indica si la cadena guarda un resultado que es equivalente
    #al problema original
    # la función regresa:
    #  -1 Si la cadena no es válida (error de sintaxis)
    #  -2 Si no se presenta un cambio con respecto al paso anterior
    #   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
    #   1 Si el paso es correcto
    def pasoCorrecto(self,ltx):
        if len(ltx.replace(' ','')) == 0:
            return -1

        d = super(procedureFactor,self).validaLtx(ltx)

        #la cadena no es válida (error de sintaxis)
        if not d['valida']:
            return -1
        
        #el paso es diferente al anterior
        if self.last_step == ltx:
            return -2
        
        #utilizar la función de la clase
        cad = d['cad']
        e = super(procedureFactor,self).cad2exp(cad)

        if e == False:
            return 0
        else:
            #extiende la cadena  la compara con el resultado
            ext_e = expand(e)
            if ext_e == self.math_prob:
                self.last_step = ltx
                return 1
            else:
                return 0
'''            
#cuándo un polinomio es diferente o igual a otro?
## verificar que el código latex sea diferente
        
#procedureFactor(tipo="mon_poly")', 'procedureFactor(tipo="prod_bins_simp")', 'procedureFactor(tipo="prod_bins")', 'procedureFactor(tipo="prod_bins")', 'procedureFactor(tipo="bin_cuad")', 'procedureFactor(tipo="bin_cuad")', 'procedureFactor(tipo="bin_conj")', 'procedureFactor(tipo="dif_cub")', 'procedureFactor(tipo="dif_cub")
        
if __name__ == '__main__':    
    pass
    
    '''
    ltx = 'x^2+2x+1'
    print factorPasoCorrecto(d['dataToAssess'], ltx)
    ltx = '(x+1)^2'
    print factorEsSolucion(d['dataToAssess'], ltx)
    '''