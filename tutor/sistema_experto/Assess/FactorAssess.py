# -*- coding: utf-8 -*-
'''
Created on 12/06/2017

@author: fgomez
'''

from tutor.sistema_experto.LatexProc.Cadenas import valida_ltx, str2expr, ajusta_cadena, factores
#from cadenas import valida_ltx, str2expr, ajusta_cadena, factores
from sympy import factor, expand
from sympy.core import numbers

def factorEsSolucion(data, ltx):
    num_tps = [int, numbers.One, numbers.Integer, numbers.NegativeOne, numbers.Rational, numbers.Half]
    if len(ltx.replace(' ','')) == 0:
        return -1
    
    your_ans = "Tu respuesta fue:$$"+ltx+"$$"
    resp_corr = "La respuesta correcta es: $$"+data['ans']+'$$'
            
    #verifica primero que la cadena sea válida
    d = valida_ltx(ltx, data['symbs'], [])
    if not d['valida']:
        return {'calif':-1,'msg':your_ans+resp_corr}
        
    #utilizar la función de la clase
    cad = d['cad']       
    
    e = str2expr(cad,data['symbs'])    
    if e == False:
        return {'calif':-1,'msg':your_ans+resp_corr}    
    else:
        
        digs = ['0','1','2','3','4','5','6','7','8','9']
        #factores de la solución
        sol_of = []
        for f in data['sol_ofs']:
            fe = ltxToE(f, data['symbs'])
            sol_of.append(fe)
            
        #e_of = e.as_ordered_factors()                
        e_st_factor = factores(ajusta_cadena(cad,data['symbs']))        
        e_of = [str2expr(f,data['symbs']) for f in e_st_factor]
        
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
                
                if not type(f) in num_tps:
                    f_ot = f.as_ordered_terms() #términos ordenados del factor
                else:
                    f_ot = [f]                    
                
                for ff in sol_of:
                    if not type(ff) in num_tps:
                        ff_ot = ff.as_ordered_terms()
                    else:
                        ff_ot = [ff]
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
            return {'calif':1,'msg':your_ans}
        elif dif == pr and (str(dif) in e_st_factor or str(-dif) in e_st_factor):
            return {'calif':1,'msg':your_ans}
        else:
            return {'calif':0,'msg':your_ans+resp_corr}


#indica si la cadena guarda un resultado que es equivalente
#al problema original
# la función regresa:
#  -1 Si la cadena no es válida (error de sintaxis)
#   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
#   1 Si el paso es correcto

#indica si la cadena guarda un resultado que es equivalente
#al problema original
# la función regresa:
#  -1 Si la cadena no es válida (error de sintaxis)
#  -2 Si no se presenta un cambio con respecto al paso anterior
#   0 Si el paso es incorrecto, aunque la cadena sea válida y diferente al aspo anterior     
#   1 Si el paso es correcto
def factorPasoCorrecto(data,ltx):
    if len(ltx.replace(' ','')) == 0:
        return -1

    #verifica primero que la cadena sea válida
    d = valida_ltx(ltx, data['symbs'], [])    
    if not d['valida']:
        return -1

    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return -1
    
    #utilizar la función de la clase
    cad = d['cad']
    e = str2expr(cad,data['symbs'])

    if e == False:
        return 0
    else:
        #extiende la solución 
        sol = ltxToE(data['ans'],data['symbs'])        
        exp_sol = expand(sol)
        #extiende la cadena  la compara con el resultado
        exp_e = expand(e)
        if exp_e == exp_sol:
            return 1
        else:
            return 0
        
def ltxToE(ltx,symbs):
    ltx_nspxc = ltx.replace(' ','')
    d = valida_ltx(ltx_nspxc,symbs,['sqrt'])
    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return None
    cad = d['cad']
    e = str2expr(cad,symbs)
    return e

if __name__ == '__main__':
    #data = {'ans':'- 2 c^{3} \\left(7 c^{3} - 9\\right)', 'clase':'Factorizacion', 'sol_ofs': ['-2', 'c^{3}', '7 c^{3} - 9'],'symbs': ['c']}
    #ltx='2 c^{3} \\left(-7 c^{3} + 9\\right)'
    #ltx = '-2c^{3} \\left(7 c^{3} - 9\\right)'
    d={'ans': '- 32 x^{2} y^{2} z^{2} \\left(2 x^{2} z + x y^{2} z + 1\\right)', 'clase': 'Factorizacion', 'sol_ofs': ['-32', 'x^{2}', 'y^{2}', 'z^{2}', '2 x^{2} z + x y^{2} z + 1'], 'symbs': ['x', 'y', 'z']} 
    ltx=d['ans']
        
    #print factorEsSolucion(d, ltx)