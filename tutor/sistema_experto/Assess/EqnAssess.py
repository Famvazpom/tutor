# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 10:32:23 2017

@author: fernando
"""
from EjerciciosClases.Cadenas import valida_ltx, str2expr, ltx_terminos3
from EjerciciosClases.nstd_tree import ltx2nstd_tree, nstd_tree2expr
from sympy.core import numbers

#revisa la igualdad de un par de ecuaciones

def esSolucionEquation(data,ltx):
    
    ltx_nsp = ltx.replace(' ','') 
    
    #verifica que el usuario haya escrito alguna respuesta    
    if len(ltx_nsp) == 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
        
    eqn_sides = ltx_nsp.split('=')
    
    if len(eqn_sides) != 2:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    
    li = eqn_sides[0]
    ld = eqn_sides[1]
        
        
    #verifica que la cadena que escribió el usuario sea válida
    d_izq = valida_ltx(li,data['symbs'],[])
    d_der = valida_ltx(ld,data['symbs'],[])
    
    if not (d_izq['valida'] and d_der['valida']):
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
        
    #termina la verficación convirtiendo la cadena en una expresión de latex
    cad_izq = d_izq['cad']           
    res_izq = str2expr(cad_izq,data['symbs'])
    cad_der = d_der['cad']           
    res_der = str2expr(cad_der,data['symbs'])
    
    if not (res_izq and res_der):
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}   
        
    sol_li = data['li']
    sol_ld = data['ld']
    
    li_comp = compara_lados(li, sol_li, data['symbs'])
    ld_comp = compara_lados(ld, sol_ld, data['symbs'])
    
    if li_comp and ld_comp:
        msg = 'Tu respuesta fue $$' + ltx + '$$'        
        return {'calif':1, "msg":msg}
        
    li_comp = compara_lados(ld, sol_li, data['symbs'])
    ld_comp = compara_lados(li, sol_ld, data['symbs'])
    
    if li_comp and ld_comp:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        return {'calif':1, "msg":msg}
        
    else:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':0, "msg":msg}    
    
def compara_lados(resp_ltx, sol_ltx, symbs):
    
    tps = [int, numbers.One, numbers.Integer, numbers.NegativeOne, numbers.Rational, numbers.Half]
    
    resp_ltx_nx = resp_ltx.replace(' ','')
    sol_ltx_nx = sol_ltx.replace(' ','')
    resp_trms = ltx_terminos3(resp_ltx_nx,symbs)
    sol_trms = ltx_terminos3(sol_ltx_nx,symbs)
    
    if len(resp_trms) != len(sol_trms):
        return False
    
    res_nt = ltx2nstd_tree(resp_ltx,symbs,[])
    sol_nt = ltx2nstd_tree(sol_ltx,symbs,[])
    
    res_e = nstd_tree2expr(res_nt,symbs,[])
    sol_e = nstd_tree2expr(sol_nt,symbs,[])
    
    if not type(sol_e) in tps:
        return sol_e.equals(res_e)
    else:
        return sol_e == res_e
    

#prueba la revisión de ecuaciones    
if __name__ == "__main__":
    ltx = 'y = -5+3x'
    d = {'clase':'EqnRecta', 'ld':'3x-5', 'li':'y', 'ltx': 'y=3x-5', 'symbs': ['x', 'y']}
    print esSolucionEquation(d,ltx)
    
              
    
    
    
    