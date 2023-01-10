# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 15:56:34 2014

@author: fernando
"""

from sympy import symbols, simplify, latex, I
from sympy.core import numbers
from tutor.sistema_experto.LatexProc.Cadenas import ajusta_cadena, valida_ltx, str2expr, ltx_terminos3
        
#se supone que la cadena ya fue validada
# la cadena puede tener la siguientes estructuras
#  a+bi
#  (a+bi)
#  (a)+bi        
# bi
# a        
def extrae_real_imag(ltx):
    #extrae los dos términos de la cadena
    ltx_n = ltx.replace('(','')
    ltx_n = ltx_n.replace(')','')
    ltx_n = ltx_n.replace(' ','')
    ltx_n = ltx_n.replace('*','')
    ltx_n = ltx_n.replace('/','')
    
    trms = []
    buf = ''
    n_1 = len(ltx_n)-1 
    for i,s in enumerate(ltx_n):
        if (i > 0 and s in ['+','-']) or i == n_1:            
            if i == n_1:
                buf += s
            trms.append(buf)
            if s == '-':
                buf = '-'
            else:
                buf = ''
        else:
            buf += s
    d = {'val':True,'re':0,'im':0}
    ntrms = len(trms)    
    if ntrms <= 2:        
        if ntrms == 0:
            d['im'] = 0
            d['re'] = 0
        elif ntrms == 1:
            t = trms[0]
            if t.find('i')>=0:                
                if t == 'i':
                    i_coef = 1
                elif t == '-i':
                    i_coef = -1
                else:
                    i_coef = int(t.replace('i',''))
                d['im'] = i_coef
                d['re'] = 0
            else:
                d['re'] = int(t)
                d['im'] = 0
        else:
            t0 = trms[0]
            t1 = trms[1]
            if t0.find('i') >= 0 and t1.find('i') >= 0:
                d['val'] = False
            elif t0.find('i') >= 0 or t1.find('i') >= 0:
                if t0.find('i') >= 0:
                    if t0.count('i') > 1:
                        d['val'] = False
                    else:                        
                        if t0 == 'i':
                            i_coef = 1
                        elif t0 == '-i':
                            i_coef = -1
                        else:
                            i_coef = int(t0.replace('i',''))
                        d['im'] = i_coef
                        d['re'] = int(t1)
                else:
                    if t1.count('i') > 1:
                        d['val'] = False
                    else:
                        if t1 == 'i':
                            i_coef = 1
                        elif t1 == '-i':
                            i_coef = -1
                        else:
                            i_coef = int(t1.replace('i',''))                        
                        d['im'] = i_coef
                        d['re'] = int(t0)
            else:
                d['val'] = False            
    else:
        d['val'] = False
        
    return d
    
def complx_oper_pasoCorrecto(data,ltx):
    num_tps = [int, numbers.One, numbers.Integer, numbers.NegativeOne, numbers.Rational, numbers.Half]
    #verifica que la cadena no esté vacía
    i = symbols('i')
    
    s_real = ltxToE(data['real'],['i'])
    s_im = ltxToE(data['im'],['i'])
    
    sol = s_real+s_im*I
    
    #cadena vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:        
        return -1
    
    #reconstruye la solución del usuario
    e = ltxToE(ltx, ['i'])        
    if not e:
        return -1
    
    if not type(e) in num_tps:
        ae = e.atoms()
        if i in ae:
            e = e.xreplace({i:I})        
    if sol.equals(e):
        return 1
    else:
        return 0
    
            
def complx_oper_esSolucion(data,ltx):
    #verifica que la cadena no esté vacía
    i = symbols('i')
        
    s_real = ltxToE(data['real'],['i'])
    s_im = ltxToE(data['im'],['i'])
    
    sol = s_real+s_im*i
    your_ans = "Tu respuesta fue: $$" + ltx + "$$"
    if s_im > 0:
        ltx_sol = data['real']+'+'+data['im']+'i'
    else:
        ltx_sol = data['real']+'-'+latex(abs(s_im))+'i'
    resp_corr = "La respuesta correcta es: $$" + ltx_sol+'$$' 
    
    #cadena vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        res = {'calif':-1, 'msg':your_ans+resp_corr}
        return res
    
    #reconstruye la solución del usuario
    e = ltxToE(ltx, ['i'])
    if not e:
        res = {'calif':-1, 'msg':your_ans+resp_corr}
        return res
        
    if not sol.equals(e):
        res = {'calif':0, 'msg':your_ans+resp_corr}
        return res       
    
    #extrae la parte real y la imaginaria de la solución del usuario
    #borra los paréntesis
    ltx_npar = ltx_nspxc.replace("(",'')
    ltx_npar = ltx_npar.replace(")",'')
    trms = ltx_terminos3(ltx_npar,['i'])
    ntrms = 0
    if abs(s_im) > 0:
        ntrms = 1
    if abs(s_real) > 0:
        ntrms += 1
               
    if len(trms) != ntrms:
        res = {'calif':0, 'msg':your_ans+resp_corr}
        return res
            
    return {'calif':1, 'msg':your_ans}
    

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
    d = {'im':'0','real':'0','symbs':['i']}
    #ltx = '\\frac{(2+i)(1-i)}{2(1-i)}'
    ltx = '0+0i'
    #print complx_oper_esSolucion(d,ltx)
    #print complx_oper_pasoCorrecto(d, ltx)