# -*- coding: utf-8 -*-
'''
Created on 12/06/2017

@author: fgomez
'''

from LatexProc.Cadenas import valida_ltx, str2expr, ajusta_cadena, factores
from Tipos.exercise_num_input import var_nom_esSolucion
#from cadenas import valida_ltx, str2expr, ajusta_cadena, factores
from sympy import factor, expand

#las coordenadas pueden ser valores numpericos
def coordsEsSolucion(data,ltx):
    
    your_ans = 'Tu respuesta fue: $$'+ltx+'$$'
    resp_corr = "La respuesta correcta es:$$\\left("+data['x_ans']+','+data['y_ans']+'\\right)$$'
    
    if len(ltx.replace(' ','')) == 0:
        return {'calif':-1,'msg':your_ans+resp_corr}
    if ltx.find(',')<0:
        return {'calif':-1,'msg':your_ans+resp_corr}
    
    ltxnsp = ltx.replace('\\left(','')
    ltxnsp = ltxnsp.replace('\\right)','')
    ltxnsp = ltxnsp.replace('(','')
    ltxnsp = ltxnsp.replace(')','')    
    
    [ltx_x,ltx_y] = ltxnsp.split(',')
    
    dx = {'nom':'x','ans':data['x_ans'],'prec':data['prec']}    
    rx = var_nom_esSolucion(dx,ltx_x)
    
    if rx['calif'] != 1:
        return {'calif':0,'msg':your_ans+resp_corr}
    
    dy = {'nom':'y','ans':data['y_ans'],'prec':data['prec']}
    ry = var_nom_esSolucion(dy,ltx_y)
    
    if ry['calif'] != 1:
        return {'calif':0,'msg':your_ans+resp_corr}
    else:
        return {'calif':1,'msg':your_ans}