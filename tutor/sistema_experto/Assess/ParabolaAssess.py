# -*- coding: utf-8 -*-
'''
Created on 09/07/2017

@author: fgome
'''
from Ejercicios.excercise_num_input import ltxToE
from Assess.PolinomioAssess import esSolucionPolinomio
from sympy.core import add, mul, symbol
from sympy import symbols, Wild

def esSolucion_ParabGeneralEqn(data,ltx):
    x,y = symbols('x,y')
    #tps = [int, numbers.One, numbers.Integer, numbers.NegativeOne, numbers.Rational, numbers.Half, add.Add, mul.Mul, symbol.Symbol]
    tps = [add.Add, mul.Mul, symbol.Symbol]
    ltx_nsp = ltx.replace(' ','') 
    
    #verifica que el usuario haya escrito alguna respuesta    
    if len(ltx_nsp) == 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
        
    resp_sides = ltx_nsp.split('=')
    
    if len(resp_sides) != 2:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    
    resp_ltxi = resp_sides[0]
    resp_ltxd = resp_sides[1]
        
    resp_li_e = ltxToE(resp_ltxi,['x','y'])
    resp_ld_e = ltxToE(resp_ltxd,['x','y'])
    
    if resp_li_e == None or resp_ld_e == None:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    
    #uno de los lados debe ser cero
    if resp_ld_e != 0 and resp_li_e != 0:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    
    if not resp_ld_e == 0:
        resp_li_e = resp_ld_e
        resp_ld_e = 0        
        resp_ltxi = resp_ltxd
    
    if type(resp_li_e) not in tps:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
        
    
    #compara ambos lados de la ecuación
    sol_li_e = ltxToE(data['li'],['x','y'])
    
    #la ecuación debe tener la estructura ay+bx^2+cx+d
    a_r = Wild('a', exclude=[x,y])
    b_r = Wild('b', exclude=[x,y])
    c_r = Wild('c', exclude=[x,y])
    d_r = Wild('d', exclude=[x,y])
    
    a_s = Wild('a', exclude=[x,y])
    b_s = Wild('b', exclude=[x,y])
    c_s = Wild('c', exclude=[x,y])
    d_s = Wild('d', exclude=[x,y])
    
    calif = 1        
    
    if data['li'].find('x^2') >= 0 or data['li'].find('x^{2}') >= 0:
    #if data['or'] == 'vert':        
        mr = resp_li_e.match(a_r*y+b_r*x**2+c_r*x+d_r)
        ms = sol_li_e.match(a_s*y+b_s*x**2+c_s*x+d_s)
    else:
        mr = resp_li_e.match(a_r*x+b_r*y**2+c_r*y+d_r)
        ms = sol_li_e.match(a_s*x+b_s*y**2+c_s*y+d_s)
        
    if not mr:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}        
        
    #revisa que cada parámetro de la solución sea un múltiplo de la respuesta
    esc = None
    
    if ms[a_s] != 0 and calif == 1:
        ea = mr[a_r]/ms[a_s]
        if esc == None:
            esc = ea
        else:
            if ea != esc:
                calif = 0
    elif ms[a_s] == 0 and mr[a_r] != 0:
        calif = 0       
        
    if ms[b_s] != 0  and calif == 1:
        eb = mr[b_r]/ms[b_s]
        if esc == None:
            esc = eb
        else:
            if eb != esc:
                calif = 0
    elif ms[b_s] == 0 and mr[b_r] != 0:
        calif = 0
        
    if ms[c_s] != 0 and calif == 1:
        ec = mr[c_r]/ms[c_s]
        if esc == None:
            esc = ec
        else:
            if ec != esc:
                calif = 0    
    elif ms[c_s] == 0 and mr[c_r] != 0:
        calif = 0
    
    if ms[d_s] != 0 and calif == 1:
        ed = mr[d_r]/ms[d_s]
        if esc == None:
            esc = ed
        else:
            if ed != esc:
                calif = 0
    elif ms[d_s] == 0 and mr[d_r] != 0:
        calif = 0
                
    if calif != 1:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':0, "msg":msg}
    else:
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        return {'calif':1, "msg":msg}        
             
#prueba la revisión de ecuaciones    
if __name__ == "__main__":
    ltx = '32x-y^2-2y-161=0'
    d = {'clase':'EqnParabGeneral', 'li':'32y-x^2-2x-161', 'ld':'0', 'ltx': '32y-x^2-2x-161=0', 'symbs': ['x', 'y']}
    print esSolucion_ParabGeneralEqn(d, ltx)
