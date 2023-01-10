# -*- coding: utf-8 -*-
'''
Created on 09/07/2017

@author: fgome
'''
from LatexProc.Cadenas import ltxToE
from Assess.PolinomioAssess import esSolucionPolinomio

def esSolucion_CircumGeneralEqn(data,ltx):
    
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
    
    #compara ambos lados de la ecuación
    sol_li_e = ltxToE(data['li'],['x','y'])
    
    if not sol_li_e.equals(resp_li_e):
        msg = 'Tu respuesta fue $$' + ltx + '$$'
        msg += '<br>'
        msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
        return {'calif':-1, "msg":msg}
    else:
        #compara los dos polinomios
        r = esSolucionPolinomio({'ltx':data['li'], 'symbs':['x','y']}, resp_ltxi)
        if r['calif'] != 1:
            msg = 'Tu respuesta fue $$' + ltx + '$$'
            msg += '<br>'
            msg += 'La respuesta correcta es $$' + data['ltx'] + '$$'
            return {'calif':r['calif'], "msg":msg}
        else:
            msg = 'Tu respuesta fue $$' + ltx + '$$'
            return {'calif':1, "msg":msg}
     
#prueba la revisión de ecuaciones    
if __name__ == "__main__":
    ltx = '-3+x^2+y^2+2y=0'
    d = {'clase':'EqnCircGeneral', 'li':'x^2+y^2+2y-3', 'ld':'0', 'ltx': 'x^2+y^2+2y-3=0', 'symbs': ['x', 'y']}
    print esSolucion_CircumGeneralEqn(d, ltx)
