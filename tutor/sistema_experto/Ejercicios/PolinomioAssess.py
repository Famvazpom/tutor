# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:19:02 2017

@author: fernando
"""

from tutor.sistema_experto.LatexProc.Cadenas import valida_ltx, str2expr, ltx_terminos3
from tutor.sistema_experto.LatexProc.nstd_tree import ltx2nstd_tree, nstd_tree2expr


def esSolucionPolinomio(data, ltx):    
    
    #verifica que el usuario haya escrito alguna respuesta    
    if len(ltx.replace(' ','')) == 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
                
    #verifica que la cadena que escribió el usuario sea válida
    d = valida_ltx(ltx,data['symbs'],[])
    
    if not d['valida']:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    
    
    #termina la verficación convirtiendo la cadena en una expresión de latex
    cad = d['cad']           
    e_res = str2expr(cad,data['symbs'])

    if e_res == False:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}            
    else:
        res_trms = ltx_terminos3(ltx,data['symbs'])
        sol_trms = ltx_terminos3(data['ltx'],data['symbs'])
        
        if len(res_trms) != len(sol_trms):
            msg = 'Tu respuesta fue $$' + ltx + '$$'
            msg += '<br>'
            msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
            return {'calif':0, "msg":msg}
        
        res_nt = ltx2nstd_tree(ltx,data['symbs'],[])
        sol_nt = ltx2nstd_tree(data['ltx'],data['symbs'],[])
        
        res_e = nstd_tree2expr(res_nt,data['symbs'],[])
        sol_e = nstd_tree2expr(sol_nt,data['symbs'],[])
        
        calif = 1 if sol_e.equals(res_e) else 0
        
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':calif, "msg":msg}            
        
from sympy import latex, symbols
if __name__ == "__main__":
    x = symbols('x')
    p = x**2-3*x+5
    data = {'symbs':['x'], 'ltx':latex(p)}
    ltx = '\\frac{1}{x^{-2}}-3x+5'
    s = esSolucionPolinomio(data,ltx)
    #print s['calif']
    #print s['msg']
        
        
        
            
            
        
            
        
    
    