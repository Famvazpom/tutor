#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 13:26:05 2021

@author: fgomez
"""

from LatexProc.Cadenas import ltxToE
from sympy import simplify, sympify, latex, log

def expresionVector_esSolucion(data, ltx):
    answer = data['answer']
    ltx_cmps = ltx.split(',')
    resp_cmps = answer.split(',')
    
    
    resp_corr = "<p>La respuesta correcta es: $$(" + latex(answer)+')$$</p>'
    your_resp = '<p>Tu respuesta fue: $$(' + ltx + ')$$</p>'

    if len(ltx_cmps) != len(resp_cmps):
        msg = your_resp+resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    for i in range(len(ltx_cmps)):
        data_ej = {'answer': resp_cmps[i], 'symbs': data['symbs']}
        r_dat = esSolucionExpresion(data_ej, ltx_cmps[i])
        if r_dat["calif"] != 1:
            msg = your_resp+resp_corr
            res = {'calif':0, 'msg':msg}
            return res

    msg = your_resp
    res = {'calif':1, 'msg':msg}
    return res

def esSolucionExpresion(data, ltx):
    
    if data["answer"].find("=") >= 0:
        return esSolucionEcuacion(data, ltx)
    
    #verifica que el usuario haya escrito alguna respuesta    
    if len(ltx.replace(' ','')) == 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg}
                
    e_res = ltxToE(ltx,data['symbs'])

    if e_res == False or e_res == None:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg}
    else:
        sol_e = ltxToE(data['answer'], data['symbs'])
        
        calif = 1 if sol_e.equals(e_res) else 0
        
        if calif == 0:
            #print(sol_e)
            #print(e_res)
            
            n_sol_e = reescribe_terminos(sol_e)
            n_e_res = reescribe_terminos(e_res)
            calif = 1 if n_sol_e.equals(n_e_res) else 0
            
            #print(n_sol_e)
            #print(n_e_res)
        
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        if calif < 1:
            msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':calif, "msg":msg}
    
def esSolucionEcuacion(data, ltx):
    
    if ltx.find("=") <= 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg}            
    
    if ltx.count("=") != 1:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg}            
    
    [resp_li, resp_ld] = ltx.split("=")        
    
    li_e_resp = ltxToE(resp_li,data['symbs'])
    if (type(li_e_resp) == bool and li_e_resp == False) or li_e_resp == None:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg} 
        
    ld_e_resp = ltxToE(resp_ld,data['symbs'])
    if (type(ld_e_resp) == bool and ld_e_resp == False) or ld_e_resp  == None:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
        return {'calif':-1, "msg":msg} 

    e_resp = li_e_resp-ld_e_resp
    
    [sol_li, sol_ld] = data['answer'].split("=")
    li_e_sol = ltxToE(sol_li,data['symbs'])
    ld_e_sol = ltxToE(sol_ld,data['symbs'])
    
    calif = 0
    
    #prueba 1    
    e_sol = li_e_sol-ld_e_sol
    if e_sol.equals(e_resp):
        calif = 1
    
    #prueba 2
    if calif == 0:
        if e_sol.equals(-e_resp):
            calif = 1
            
    #prueba 3 (múltiplos)
    if calif == 0 and e_resp != 0:
        e = e_sol/e_resp
        e_simp = simplify(e)
        if sympify(e_simp).is_real:
            calif = 1
    
    if calif == 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['answer'] + '$$'
    else:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        
    return {'calif':calif, "msg":msg}


from sympy import Wild


def reescribe_terminos(ex):
    
    ex_changd = True
    i = 0
    
    while i < 10 and ex_changd:
        ex_changd = False
        i += 1
        
        if i == 1:
            if not type(ex) in [int, float]:
                trms = ex.as_ordered_terms()
            else:
                trms = [ex]
        else:
            if not type(ne) in [int, float]:
                trms = ne.as_ordered_terms()
            else:
                trms = [ne]
        
        '''
        if i == 1:
            trms = ex.as_ordered_terms()
        else:
            trms = ne.as_ordered_terms()
        '''
            
        
        ne = 0
        
    
        for t in trms:
                
            #verifica si el término corresponde con diferentes patrones para reescribirlo
            
            # ¿es una potencia? (las potencias de productos se reescriben como producto de potencias)
            
            if type(t) in [int, float]:
                t_facts = [t]
            else:
                t_facts = t.as_ordered_factors()
            
            #t_facts = t.as_ordered_factors()
            
            nt = 1
            for f in t_facts:
                if not sympify(f).is_real:
                    #el factor es una expresión
                    changed = False
                    #potencia
                    r_f = prod_potencias(f)
                    changed = r_f['changed']
                    
                    if changed:
                        nt = nt*r_f['f']
                    else:
                        r_f = prod_exps(f)
                        changed = r_f['changed']
                        if changed:
                            nt = nt*r_f['f']
                        else:
                            r_f = log_pot(f)
                            changed = r_f['changed']
                            if changed:
                                nt = nt*r_f['f']
                            else:
                                r_f = log_prod(f)
                                changed = r_f['changed']
                                if changed:
                                    nt = nt*r_f['f']
                                else:
                                    r_f = log_div(f)
                                    changed = r_f['changed']
                                    if changed:
                                        nt = nt*r_f['f']
                    
                    if changed:
                        ex_changd = True
                    else:
                        nt = nt*f
                        
                else:
                    nt = nt*f
                    
            ne = ne+nt
    
    return ne

#busca el patrón (b**r)**s = d**s
def prod_exps(f):
    b = Wild("b")
    d = Wild("d") # d = b**r
    r = Wild("r") 
    s = Wild("s")
    
    m = f.match(d**s) #la expresión es una potencia
    
    if m:
        if m[s] != 1:
            #verifica si la base es otra potencia
            m2 = m[d].match(b**r)
            if m2:
                if m2[r] != 1:
                    nf = m2[b]**(m2[r]*m[s])
                    return {'f':nf, 'changed':True}
                else:
                    return {'f':f, 'changed':False}
            else:
                return {'f':f, 'changed':False}
        else:
            return {'f':f, 'changed':False}
    else:
        return {'f':f, 'changed':False}

def prod_potencias(f):
    b = Wild("b")
    e = Wild("e")    
    
    m = f.match(b**e)
    
    if m:
        if m[e] != 1:
            #verifica si la base es un producto de factores
            b_t = m[b]
            facts = b_t.as_ordered_factors()
            if len(facts) > 1:
                nf = 1
                for f in facts:
                    nf = nf*f**m[e]
                return {'f':nf, 'changed':True}
            else:
                return {'f':f, 'changed':False}
            
        else:
            return {'f':f, 'changed':False}
    else:
        return {'f':f, 'changed':False}
    
#reescribe log(b**e) = e*log(b)
def log_pot(f):
    b = Wild("b")
    e = Wild("e")    
    
    m = f.match(log(b**e))
    
    if m:
        if m[e] != 1:
            nf = m[e]*log(m[b])
            return {'f':nf, 'changed':True}
        else:
            return {'f':f, 'changed':False}
    else:
        return {'f':f, 'changed':False}
    
#reescribe log(a*b) = log(a)+log(b)
def log_prod(f):
    a = Wild("a")    
    b = Wild("b")
    
    m = f.match(log(a*b))
    
    if m:
        nf = log(m[a])+log(m[b])
        return {'f':nf, 'changed':True}
        
    else:
        return {'f':f, 'changed':False}
    
def log_div(f):
    a = Wild("a")    
    b = Wild("b")
    
    m = f.match(log(a/b))
    
    if m:
        nf = log(m[a])-log(m[b])
        return {'f':nf, 'changed':True}
        
    else:
        return {'f':f, 'changed':False}
    
'''
if __name__ == "__main__":
    
    ltx=r'-\frac{4}{3}\sec\left(x\right)'
    data={u'answer': u'- \\frac{4 \\tan^{2}{\\left(x \\right)}}{3} - \\frac{4}{3}', u'clase': u'alg_free', u'prec': 0, u'symbs': [u'x'], u'vector': 0}
    #data={u'answer': u'\\frac{6}{5}\\tan(x)^2+\\frac{6}{5}', u'clase': u'alg_free', u'prec': 0, u'symbs': [u'x'], u'vector': 0}
    
    print(esSolucionExpresion(data, ltx))
'''    

if __name__ == "__main__":
    ltx = "\\exp(-5x)"
    data = {'answer': "\\exp(-5x)", 'symbs':["x","y"]}
    
    res = esSolucionExpresion(data, ltx)
    print(res)

