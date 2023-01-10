# -*- coding: utf-8 -*-
'''
Created on 13/06/2017

@author: fgome
'''

from tutor.sistema_experto.LatexProc.Cadenas import valida_ltx, str2expr, ajusta_cadena, factores, ltx_terminos2, ajusta_cad_latex, factores3
#from cadenas import valida_ltx, str2expr, ajusta_cadena, factores
from sympy import factor, expand, Rational

def prodNotPasoCorrecto(data,ltx):
    
    if len(ltx.replace(' ','')) == 0:
        return -1
        
    #verifica primero que la cadena sea válida
    d = valida_ltx(ltx, data['symbs'], [])
    if not d['valida']:
        return -1
        #utilizar la función de la clase
    
    cad = d['cad']
    e = str2expr(cad, data['symbs'])

    if e == False:
        return 0
    else:
        #extiende la cadena  la compara con el resultado
        ext_e = expand(e)
        sol = ltxToE(data['ans'],data['symbs'])
        if sol.equals(ext_e):
            return 1
        else:
            return 0
    
def prodNotEsSolucion(data,ltx): 
    
    your_ans = "Tu respuesta fue:$$"+ltx+"$$"
    resp_corr = "La respuesta correcta es: $$"+data['ans']+'$$'
       
    if len(ltx.replace(' ','')) == 0:
        return {'calif':-1,'msg':your_ans+resp_corr}
        
    #verifica primero que la cadena sea válida
    d = valida_ltx(ltx, data['symbs'], [])
    if not d['valida']:
        return {'calif':-1,'msg':your_ans+resp_corr}
        #utilizar la función de la clase
    
    cad = d['cad']
    e = str2expr(cad, data['symbs'])

    if e == False:
        return {'calif':0,'msg':your_ans+resp_corr}
    
    sol = ltxToE(data['ans'],data['symbs'])
    sol_ot = sol.as_ordered_terms()
    
    #extrae los términos de la cadena látex
    trms = ltx_terminos2(ltx,data['symbs'])
    #recupera los factores de cada término y los compara con la solución
    
    for t in trms:
        f = False
        for tt in sol_ot:
            tt_of = tt.as_ordered_factors()
            if factores_iguales(t,tt_of,data['symbs']) == 1:
                sol_ot.remove(tt)
                f = True
                break
        if not f:
            return {'calif':0,'msg':your_ans+resp_corr}
    if len(sol_ot) == 0:
        return {'calif':1,'msg':your_ans}
    else:
        return {'calif':0,'msg':your_ans+resp_corr}                
                
        
def factores_iguales(cad,sol_of,symbs):
    ltx_ajst = ajusta_cad_latex(cad,symbs)
    resp_of = []
    facts = factores3(ltx_ajst,True)
    
    #extrae los fcatores del término
    for f in facts:
        fe = str2expr(f['c'],symbs)
        #if fe != 1:
        if not f['in_num']:
            if type(fe) == type(1):
                resp_of.append(Rational(1,fe))
            else:
                resp_of.append(fe**(-1))
        else:
            resp_of.append(str2expr(f['c'], symbs))
    
    #detecta si algún factor es una constante
    #y si sol_of y res_of tienen diferente tamaño
    digs = ['0','1','2','3','4','5','6','7','8','9']    
    dif = 1
    for f in resp_of:
        if f in sol_of:
            sol_of.remove(f)
        elif -f in sol_of:
            sol_of.remove(-f)
            dif = -dif
        #busca dividir el factor entre otro
        else:
            found = False
            if type(f) != type(1):
                f_ot = f.as_ordered_terms()                    
            else:
                f_ot = [f]
            for ff in sol_of:
                if type(ff) != type(1):
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


if __name__ == "__main__":
    ltx='8876+0876'
    data={u'ans': u'1296 z^{4} + 3456 z^{3} + 3456 z^{2} + 1536 z + 256', u'clase': u'ProdNot', u'symbs': [u'z']}
    
    
    prodNotEsSolucion(data, ltx)
    
    
    
    