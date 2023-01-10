# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:58:23 2018

@author: fgome
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 11:19:23 2014

@author: fernando
"""

from Tipos.TiposBasicos import procedureExcercise
from Ejercicios.Racionales import ej_oper_rat_proc
from LatexProc.Cadenas import valida_ltx, str2expr
from sympy import Rational
import json        

#la cadena debe tener alguna de estas estructuras:
# 1.-  '\\frac{n}{d}' #fracción
#       n y d deben ser primos entre sí
# 2.-  'm' #entero 

#debe aparecer una sola fracción
#no dbe haber operadores

def rat_oper_pasoCorrecto(data,ltx):
    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        return -1
    #verifica que el usuario haya escrito una cadena correctamente (sin errores de sintaxis)
    #verifica que el usuario haya escrito una cadena correctamente (sin errores de sintaxis)
    d = valida_ltx(ltx,data['symbs'],data['funcs'])

    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return -1
    
    #utilizar la función de la clase
    cad = d['cad']
    e = str2expr(cad,data['symbs'])

    num = int(data['num'])
    den = int(data['den'])
    answer = Rational(num,den)
    if e == answer:
        return 1
    else:
        return 0    
    
#es necesario enviar symbols, funcs, num, den, 
def rat_oper_esSolucion(data,ltx):
    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        return -1
    
    #verifica que el usuario haya escrito una cadena correctamente (sin errores de sintaxis)
    d = valida_ltx(ltx,data['symbs'],data['funcs'])

    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return -1
    
    cad = d['cad']
    e = str2expr(cad,data['symbs'])
    
    num = int(data['num'])
    den = int(data['den'])
    answer = Rational(num,den)

    #extiende la cadena la compara con el resultado
    if e == answer:
        #verifica que la cadena esté simplificada
        simp = ltx_simp(ltx)
        if not simp:
            return 0
        elif simp['frac']:
            f_res = int(answer)
            dif = answer-f_res
            if abs(dif) > 0: #respuesta racional
                n = answer.p
                if abs(n) != abs(simp['num']):
                    return 0
                d = answer.q
                if abs(d) != abs(simp['den']):
                    return 0
                #verifica que el signo coincida
                if (simp['num']*simp['den'])*(n*d) < 0:
                    return 0
                return 1                        
            else: #entero
                return 0 #la solución es entera y el usuario ingresó un racional
        else:#la respuesta es un entero
            return 1 #ya se verificó que e == answer                
    else:
        return 0
    
def ltx_simp(ltx):      
    #cuenta las veces que aparece una fracción
    nfrac = ltx.count('\\frac')
    if nfrac > 1:
        return False
    else:
        #al borrar los corchetes 
        #debe haber solamente números 
        #(o el signo de '-' en primer lugar)
        frac = False
        if nfrac == 1:
            nltx = ltx.replace('\\frac','')
            nltx = nltx.replace('{','')
            nltx = nltx.replace('}','')
            frac = True
        else:
            nltx = ltx
        #verifica que solamnte exista un número entero
        digs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        #accede al valor guardado en la cadena
        #por ser el paso final se supone que la 
        #cadena debe guardar un valor numérico
        for i,s in enumerate(nltx):
            if s not in digs:
                if i > 0:
                    return False
                elif s != '-':
                    return False                    
        res = {'frac':frac}
        #identifica el numerador y el denominador                
        if frac:
            l = 0
            in_num = True
            num = ''
            den = ''
            for s in ltx:
                if s == '{':
                    l += 1
                elif s == '}':
                    in_num = False
                    l -= 1
                elif l == 1 and in_num:
                    in_num = True
                    num += s
                elif l == 1 and not in_num:
                    den += s
            if nltx[0] == '-':
                res['num'] = -int(num)
            else:
                res['num'] = int(num)                
            res['den'] = int(den)
        else:
            res['val'] = int(nltx)                                                                        
        return res
        
'''
#regresa el numerador y el denominador de la fracción
def num_den(ltx_frac):
    res = {}
    l = 0
    in_num = True
    num = ''
    den = ''
    for s in ltx:
        if s == '{':
            l += 1
        elif s == '}':
            in_num = False
            l -= 1
        elif l == 1 and in_num:
            in_num = True
            num += s
        elif l == 1 and not in_num:
            den += s
    res['num'] = int(num)                
    res['den'] = int(den)
    return res
'''
    
def is_dig(ltx_in):
    ltx_str = str(ltx_in)
    res = {'is_dig':True}
    #verifica que solamnte exista un número entero
    digs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #accede al valor guardado en la cadena
    #por ser el paso final se supone que la 
    #cadena debe guardar un valor numérico
    for i,s in enumerate(ltx_str):
        if s not in digs:
            if i > 0:
                res['is_dig'] = False
            elif s != '-':
                res['is_dig'] = False
    if res['is_dig']:
        res['val'] = int(ltx_str)
    return res

## verificar que el código latex sea diferente        
if __name__ == '__main__':
    ltx = '\\frac{15}{2}'
    data = {"funcs": [], "clase": "rat_oper", "num": "15", "den": "2", "ans": "\\frac{15}{2}", "symbs": []}
    print rat_oper_pasoCorrecto(data, ltx)
    
    '''
    data = {}
    data['symbs'] = []
    data['funcs'] = []
    data['num'] = '-3'
    data['den'] = '4'
    
    print data
    ltx = '-\\frac{3}{4}'
    #print rat_oper_pasoCorrecto(data,ltx)
    print rat_oper_esSolucion(data,ltx)
    
    pts_dif = {'1':2, '2':3, '3':5}
    ejercs = []
    for dif in [1,2,3]:
        n_ejs = 0
        #symbs = ['a','b','c','x','y','z']                
        while n_ejs < 1000:
            ex = procedureRacionales(n_ops=dif+2)
            d = {}
            d['question'] = ex.getQuestion()
            d['options'] = ['$$'+str(ex.getAnswer()) +'$$']
            d['answers'] = [0]
            #d['procedimiento'] = ''
            d['dificulty'] = dif
            d['points'] = pts_dif[str(dif)]
            d['exType'] = 4
                        
            sol = ex.answer
    
            print sol
            
            data = {}
            data['symbs'] = []
            data['funcs'] = []
            data['num'] = str(sol.p)
            data['den'] = str(sol.q)
            data['clase'] = 'rat_oper'

            d['dat_ext'] = data
            d['procedure'] = [ex.getLtxMathProblem()]
            
            n_ejs = n_ejs+1
            print n_ejs
            ejercs.append(d)
    with open('rat_oper.data', 'a') as outfile:
            json.dump(ejercs,outfile)    
    
    '''
    '''
    ex = procedureRacionales(n_ops=4)    
    sol = ex.answer
    
    print sol
    
    data = {}
    data['symbs'] = []
    data['funcs'] = []
    data['num'] = str(sol.p)
    data['den'] = str(sol.q)
    
    print data
    ltx = ''
    print rat_oper_pasoCorrecto(data,ltx)
    print rat_oper_esSolucion(data,ltx)
    #print jerarq_oper_pasoCorrecto(data,ltx)
    #print jerarq_oper_esSolucion(data,ltx)
        
    
    #print ex.getQuestion()
    #ltx = ''
    #print ex.pasoCorrecto(ltx)
    #print ex.esSolucion(ltx)
    
    
    #ltx = ''
    #print ex.pasoCorrecto(ltx)
    #print ex.esSolucion(ltx)
    '''
