#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:11:58 2021

@author: fgomez
"""

from sympy import latex, sqrt, factorint, factor, gcd, N, I, symbols, Rational
from cadenas import valida_ltx, str2expr, ltx_terminos3, factores3
from itertools import permutations

#es necesario enviar symbols, funcs, num, den
def rat_oper_esSolucion(data,ltx):
    resp_corr = "<p>La respuesta correcta es: $$" + latex(data['ans'])+'$$</p>'
    your_resp = '<p>Tu respuesta fue: $$' + ltx + '$$</p>'
    
    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        msg = your_resp + resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    
    #verifica que el usuario haya escrito una cadena correctamente (sin errores de sintaxis)
    d = valida_ltx(ltx,data['symbs'],data['funcs'])

    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        msg = your_resp + resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    
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
            msg = your_resp + resp_corr+'<p>No olvides simplificar la fracción</p>'
            res = {'calif':0, 'msg':msg}
            return res
        elif simp['frac']:
            f_res = int(answer)
            dif = answer-f_res
            if abs(dif) > 0: #respuesta racional
                n = answer.p
                if abs(n) != abs(simp['num']):
                    msg = your_resp + resp_corr
                    res = {'calif':0, 'msg':msg}
                    return res
                d = answer.q
                if abs(d) != abs(simp['den']):
                    msg = your_resp + resp_corr
                    res = {'calif':0, 'msg':msg}
                    return res
                #verifica que el signo coincida
                if (simp['num']*simp['den'])*(n*d) < 0:
                    msg = your_resp + resp_corr
                    res = {'calif':0, 'msg':msg}
                    return res
                msg = your_resp
                res = {'calif':1, 'msg':msg}
                return res
            else: #entero
                msg = your_resp + resp_corr+'<p>No olvides simplificar la fracción</p>'
                res = {'calif':0, 'msg':msg}
                return res#la solución es entera y el usuario ingresó un racional
        else:#la respuesta es un entero
            msg = your_resp + resp_corr
            res = {'calif':1, 'msg':msg}
            return res
    else:
        msg = your_resp + resp_corr
        res = {'calif':0, 'msg':msg}
        return res

def numericVector_esSolucion(ltx, answer, prec, resp_corr=None,your_resp=None):

    ltx_cmps = ltx.split(',')
    resp_cmps = answer.split(',')

    resp_corr = "<p>La respuesta correcta es: $$(" + latex(answer)+')$$</p>'
    your_resp = '<p>Tu respuesta fue: $$(' + ltx + ')$$</p>'

    if len(ltx_cmps) != len(resp_cmps):
        msg = your_resp+resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    for i in range(len(ltx_cmps)):
        r_dat = numericSimple_esSolucion(ltx_cmps[i], resp_cmps[i], prec)
        if r_dat["calif"] != 1:
            msg = your_resp+resp_corr
            res = {'calif':0, 'msg':msg}
            return res

    msg = your_resp
    res = {'calif':1, 'msg':msg}
    return res

#answer: es una variable numérica (fracción, radical, entero, número de precisión flotante)
#### importante: es necesario que la respuesta esté simplificada (no debe haber signos de suma, resta, multiplicación o división)

def numericSimple_esSolucion(ltx,answer, prec, resp_corr=None,your_resp=None):
    
    if resp_corr == None:
        resp_corr = "<p>La respuesta correcta es: $$" + latex(answer)+'$$</p>'
    if your_resp == None:
        your_resp = '<p>Tu respuesta fue: $$' + ltx + '$$</p>'
        
    if type(answer) in [str]: #se guarda la solución como látex (fracción)
        #if data["ans"].find('frac')>=0:
        answer = ltxToE(answer)
    elif type(answer) == int:
        answer = answer
    
    '''
    else:
        msg = your_resp+resp_corr
        res = {'calif':-1, 'msg':msg}
        return res
    '''

    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')

    if len(ltx_nspxc) == 0:
        msg = your_resp+resp_corr
        res = {'calif':-1, 'msg':msg}
        return res

    prec = float(prec)
    
    if type(answer) in [str]: #se guarda la solución como látex (fracción)
        ntrms_ans = ltx_terminos3(answer, [])
    else:
        ntrms_ans = []

    if len(ntrms_ans) > 1:
        d = valida_ltx(ltx_nspxc, [], ['sqrt'])

        # la cadena no es válida (error de sintaxis)
        if not d['valida']:
            msg = your_resp + resp_corr
            res = {'calif': -1, 'msg': msg}
            return res
        cad = d['cad']
        e = str2expr(cad, [])

        corr = abs(e - answer) <= prec

        if corr:
            msg = your_resp
            res = {'calif': 1, 'msg': msg}
            return res
        else:
            msg = your_resp + resp_corr
            res = {'calif': 0, 'msg': msg}
            return res

    if not simplificada(ltx_nspxc):
        msg = your_resp+resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    
    if ltx_nspxc.find('.') >= 0:
        if ltx_nspxc.count('.') > 1:
            msg = your_resp+resp_corr
            res = {'calif':-1, 'msg':msg}
            return res
    
    #accede al valor guardado en la cadena
    #por ser el paso final se supone que la 
    #cadena debe guardar un valor numérico
    
    #la cadena puede ser un número real o una fracción        
    ### fracción
    frac_f = ltx_nspxc.find('frac')
    sqrt_f = ltx_nspxc.find('sqrt')
    
    ltx_tmp = ltx_nspxc
    ltx_tmp = ltx_tmp.replace('+','')            
    ltx_tmp = ltx_tmp.replace('-','')
    ltx_tmp = ltx_tmp.replace('\\times','')            
    ltx_tmp = ltx_tmp.replace('\\div','')
    ltx_tmp = ltx_tmp.replace('\\cdot','')    

    if frac_f >= 0 or sqrt_f >= 0: #si es fracción o es raíz cuadrada       
        #reemplaza
        if frac_f >= 0:
            ltx_tmp = ltx_tmp.replace('frac','')
        if sqrt_f >= 0:
            ltx_tmp = ltx_tmp.replace('sqrt','')                
        ltx_tmp = ltx_tmp.replace('\\','')
        ltx_tmp = ltx_tmp.replace('{','')
        ltx_tmp = ltx_tmp.replace('}','')        
        if es_numero(ltx_tmp):
            d = valida_ltx(ltx_nspxc,[],['sqrt'])
            
            #la cadena no es válida (error de sintaxis)
            if not d['valida']:
                msg = your_resp+resp_corr
                res = {'calif':-1, 'msg':msg}
                return res
            cad = d['cad']
            e = str2expr(cad,[])
            
            corr = abs(e-answer) <= prec

            if not corr:
                msg = your_resp+resp_corr
                res = {'calif':0, 'msg':msg}
                return res
            
            #si es una fracción verifica que esté simplificada
            if ltx_nspxc.find('frac')>=0 and ltx_nspxc.find('sqrt')<0:
                if not fraccion_simplificada(ltx_nspxc):
                    msg = your_resp+resp_corr
                    msg += '<p>No olvides simplificar la fracción</p>'
                    res = {'calif':0, 'msg':msg}
                    return res   
    
            #si es un radical verifica que esté simplificado
            if not frac_rad_simp(ltx_nspxc,True):
                msg = your_resp+resp_corr
                msg += '<p>No olvides simplificar el radical</p>'
                res = {'calif':0, 'msg':msg}
                return res
                
            msg = your_resp
            res = {'calif':1, 'msg':msg}
            return res
            
        else:
            msg = your_resp+resp_corr
            res = {'calif':-1, 'msg':msg}
            return res
    
    elif float_number(ltx_nspxc):
        e = float(ltx_nspxc)
    else:
        d = valida_ltx(ltx_tmp,[],['sqrt'])
        if not d['valida']:
            msg = your_resp+resp_corr
            res = {'calif':-1, 'msg':msg}
            return res
        cad = d['cad']
        e = str2expr(cad,[])
    
    #extiende la cadena  la compara con el resultado
    if type(answer) in [str]:
        answer_e = ltxToE(answer)
    else:
        answer_e = answer        
        
    if abs(e-answer_e) <= prec:
        msg = your_resp
        res = {'calif':1, 'msg':msg}
        return res
    else:
        msg = your_resp+resp_corr
        res = {'calif':0, 'msg':msg}
        return res

#answer: es una variable numérica (fracción, radical, entero, número de precisión flotante)
#### importante: no es necesario que la respuesta esté simplificada
def num_input_esSolucion(ltx,answer,prec,resp_corr=None,your_resp=None):
    
    if resp_corr == None:
        resp_corr = "<p>La respuesta es: $$" + latex(answer)+'$$</p>'
    if your_resp == None:
        your_resp = '<p>Tu respuesta fue: ' + ltx + '</p>'
        
    if type(answer) in [str]: #se guarda la solución como látex (fracción)
        #if data["ans"].find('frac')>=0:
        answer = ltxToE(answer)        
    
    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        msg = your_resp+resp_corr
        res = {'calif':-1, 'msg':msg}
        return res
    
    #accede al valor guardado en la cadena
    #por ser el paso final se supone que la 
    #cadena debe guardar un valor numérico
    
    #la cadena puede ser un número real o una fracción        
    ### fracción
    frac_f = ltx_nspxc.find('frac')
    sqrt_f = ltx_nspxc.find('sqrt')
    
    ltx_tmp = ltx_nspxc
    ltx_tmp = ltx_tmp.replace('+','')            
    ltx_tmp = ltx_tmp.replace('-','')
    ltx_tmp = ltx_tmp.replace('\\times','')            
    ltx_tmp = ltx_tmp.replace('\\div','')
    ltx_tmp = ltx_tmp.replace('\\cdot','')    
    
    if frac_f >= 0 or sqrt_f >= 0: #si es fracción o es raíz cuadrada       
        #reemplaza
        if frac_f >= 0:
            ltx_tmp = ltx_tmp.replace('frac','')
        if sqrt_f >= 0:
            ltx_tmp = ltx_tmp.replace('sqrt','')                
        ltx_tmp = ltx_tmp.replace('\\','')
        ltx_tmp = ltx_tmp.replace('{','')
        ltx_tmp = ltx_tmp.replace('}','')        
        if es_numero(ltx_tmp):
            d = valida_ltx(ltx_nspxc,[],['sqrt'])
            
            #la cadena no es válida (error de sintaxis)
            if not d['valida']:
                msg = your_resp+resp_corr
                res = {'calif':-1, 'msg':msg}
                return res
            cad = d['cad']
            e = str2expr(cad,[])
            if abs(e-answer) <= prec:
                msg = your_resp
                res = {'calif':1, 'msg':msg}
                return res
            else:
                msg = your_resp+resp_corr
                res = {'calif':0, 'msg':msg}
                return res
        else:
            msg = your_resp+resp_corr
            res = {'calif':-1, 'msg':msg}
            return res
    elif float_number(ltx_nspxc):
        e = float(ltx_nspxc)
    else:
        d = valida_ltx(ltx_tmp,[],['sqrt'])
        if not d['valida']:
            msg = your_resp+resp_corr
            res = {'calif':-1, 'msg':msg}
            return res
        cad = d['cad']
        e = str2expr(cad,[])
    
    #extiende la cadena  la compara con el resultado
    if type(answer) in [str]:
        answer_e = ltxToE(answer)
    else:
        answer_e = answer 
    if abs(e-answer_e) <= prec:
        msg = your_resp
        res = {'calif':1, 'msg':msg}
        return res
    else:
        msg = your_resp+resp_corr
        res = {'calif':0, 'msg':msg}
        return res
    
def num_input_pasoCorrecto(ltx,answer,prec):
    #verifica que la cadena no esté vacía
    ltx_nspxc = ltx.replace(' ','')
    if len(ltx_nspxc) == 0:
        return -1
    
    #accede al valor guardado en la cadena
    #por ser el paso final se supone que la 
    #cadena debe guardar un valor numérico
    d = valida_ltx(ltx_nspxc,[],['sqrt'])
            
    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return -1
    cad = d['cad']
    e = str2expr(cad,[])
    
    if type(answer) in [str]:
        answer_e = ltxToE(answer)
    else:
        answer_e = answer
    
    if abs(e-answer_e) <= prec:
        return 1
    else:
        return 0

###############################################
#NO ES NECESARIO QUE LA RESPUESTA ESTÉ SIMPLIFICADA
###############################################
#entrada del tipo: x = 5/3 (no es necesario que respuesta esté simplificada)        
def var_nom_esSolucion(data,ltx):
    #extrae el nombre de la variable y su valor
    ltxr = ltx.replace(" ","")
    ltxr = ltxr.replace(data['nom'],"")
    ltxr = ltxr.replace("=","")
    ltxr = ltxr.replace("?","")
    
    if type(data["ans"]) in [str]: #se guarda la solución como látex (fracción)
        #if data["ans"].find('frac')>=0:
        a = ltxToE(data["ans"])
        data['ans'] = a
    
    your_resp = '<p>Tu respuesta fue: $$ '+ltx.replace('?','')+'$$</p>'
    resp_corr = '<p>La respuesta es:$$ '+data['nom'] + '=' + latex(data['ans'])+'$$</p>'
    return num_input_esSolucion(ltxr,data['ans'],data['prec'],resp_corr,your_resp)

def var_nom_pasoCorrecto(data,ltx):
    #extrae el nombre de la variable y su valor
    ltxr = ltx.replace(" ","")
    ltxr = ltxr.replace(data['nom'],"")
    ltxr = ltxr.replace("=","")
    ltxr = ltxr.replace("?","")
    
    ltx_e = ltxToE(ltxr)
    if not ltx_e:
        return 0
    if type(data["ans"]) in [str]: #se guarda la solución como látex (fracción)
        ans_e = ltxToE(data['ans'])
    else: 
        ans_e = data['ans']
    
    if abs(ltx_e-ans_e) <= data['prec']:
        return 1
    else:
        return 0
#######################################################
#LAS RESPUESTAS CORRECTAS DEBEN ESTAR ESCRITAS CON CÓDIGO LATEX
#######################################################
#versión vectorial de var_nom_esSolucion
def vars_nom_esSolucion(data,ltx):
    #extrae las igualdades, las cuales deben estar separadas por comas    
    sols = ltx.split(",")
    #verifica que en el vector se encuentre cada una de las variables
    your_ans = "Tu respuesta fue: $$" + ltx + "$$"
    resp_corr = "La respuesta es: $$"
    for i,n in enumerate(data['nom']):
        resp_corr += n + '=' + data['ans'][i]+','
    resp_corr = resp_corr[:-1]+'$$'
        
    if len(sols) != len(data['nom']):
        return {'calif':-1, 'msg':resp_corr}
    
    #busca separar cada subcadena en pares
    # de nombre de variable, valor
    nvars = []
    vals = []
    set_vars = set(data['nom'])
    for s in sols:
        nv = s.replace(" ","")
        nv = nv.replace("?","")
        nv = nv.split("=")
        if nv[0] in set_vars:
            if not nv[0] in nvars:
                nvars.append(nv[0])
                vals.append(nv[1])
                set_vars.remove(nv[0])
        elif nv[1] in data['nom']:
            if not nv[1] in nvars:
                nvars.append(nv[1])
                vals.append(nv[0])
                set_vars.remove(nv[1])
    if len(nvars) != len(data['nom']):
        return {'calif':-1, 'msg':your_ans+resp_corr}

    if not 'prec' in data.keys():
        prec = [0 for v in data['nom']]
    else:
        prec = data['prec']
            
    for k,v in enumerate(data['nom']):
        if not v in nvars:
            return {'calif':-1, 'msg':your_ans+resp_corr}
        i = nvars.index(v)
        
        e = ltxToE(data['ans'][k])
        
        s = num_input_esSolucion(vals[i],e,prec[k])
        if s['calif'] != 1:
            return {'calif':s['calif'], 'msg':your_ans+resp_corr}
    return {'calif':1, 'msg':your_ans}

#ltx = "-\\frac{64}{8}, 8"
#dat= {'vals': ['8','-8'], 'nom': 'x', 'prec':[0,0]}
def var_mult_vals_esSolucion(data,ltx):
    i = symbols('i')
    #extrae las igualdades, las cuales deben estar separadas por comas
    resps = ltx.split(",")
    
    #verifica que en el vector se encuentre cada una de las variables
    your_ans = "Tu respuesta fue: $$" + ltx + "$$"
    resp_corr = "La respuesta es: $$" + data['nom'] + '='
    for v in data['vals']:
        resp_corr +=  v+','
    resp_corr = resp_corr[:-1]+'$$'
        
    if len(resps) != len(data['vals']):
        return {'calif':-1, 'msg':your_ans+resp_corr}
    
    num_resps = []
    for r in resps:
        e = ltxToE(r)
        if e == None or e == False:
            return {'calif':-1,'msg':'Algo está mal escrito'}
        if r.find('i') >= 0:
            e = e.xreplace({i:I})
        num_resps.append(e)
        
    num_sols = []
    for s in data['vals']:
        e = ltxToE(s)
        if e == None:
            return {'calif':-1,'msg':'Algo está mal escrito'}
        if s.find('i') >= 0:
            e = e.xreplace({i:I})
        num_sols.append(e)
        
    #genera todas las permutaciones del vector de solución
    pms = permutations(range(len(num_sols)))
    for p in pms:
        err = False        
        for m,n in enumerate(p):
            if abs(num_sols[m]-num_resps[n]) > data['prec'][m]:
                err = True
                break
        if not err:
            break
    if not err:
        return {'calif':1,'msg':your_ans}
    else:
        return {'calif':0,'msg':your_ans+resp_corr}
    
def float_number(ltx):
    digs = ['0','1','2','3','4','5','6','7','8','9','.']
    
    if ltx.find('.')>=0:
        nc = ltx.count('.')
        if nc > 1:
            return False
    
    ind = ltx.find('-')
    if ind > 0:
        return False
    elif ind == 0:
        if ltx.count('-') > 1:
            return False
        ind = 1 
    else:
        ind = 0    
    for s in ltx[ind:]:
        if not s in digs:
            return False        
    return True

def ltxToE(ltx,symbs=['i']):
    ltx_nspxc = ltx.replace(' ','')
    
    if float_number(ltx):
        e = float(ltx)
        return e
    
    d = valida_ltx(ltx_nspxc,symbs,['sqrt'])
    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return None
    cad = d['cad']
    e = str2expr(cad,symbs)
    return e
    

'''
1.- debe ser un solo término
2.- el radicando no debe contener cuadrados 
''' 

def rad_simp(ltx):
    ind = ltx.find('-')
    if ind > 0:
        return False
    elif ltx.find('+') >= 0:
        return False
    #extrae el radicando
    elif ltx.find('sqrt') >= 0:
        rad = extrae_radicando(ltx)
        #convierte el radicando en una expresión
        d = valida_ltx(rad,[],[])
        if not d['valida']:
            return False
        else:
            if not es_numero(d['cad']):
                return False
            e = str2expr(d['cad'],[])
            #descompone la expresión
            fe = factorint(e)
            for f in fe:
                if fe[f] > 1:
                    return False
    return True
    
def rad_simp_cad(cad):
    ind = cad.find('-')
    if ind > 0:
        return False
    elif cad.find('+') >= 0:
        return False
    #extrae el radicando
    elif cad.find('sqrt') >= 0:
        rad = extrae_radicando_cad(cad)
        if not es_numero(rad):
            return False
        e = str2expr(rad,[])
        #descompone la expresión
        fe = factorint(e)
        for f in fe:
            if fe[f] > 1:
                return False
    return True

#la cadena de latex es una sola fracción
def es_fraccion(ltx):
    ind = ltx.find('\\frac')
    if ind < 0:
        return False
    #los caracteres previos a ind deben ser números
    if not es_numero(ltx[:ind]):
        return False
    pre = ltx[:ind]
    #se coloca en el inicio de la fracción y recorre el ambiente, este debe incluir a toda la cadena
    ind = ind + 6
    lev = 1
    in_num = True
    in_den = False
    num = ''
    den = ''
    for s in ltx[ind:]:
        if s == '{':
            lev += 1
            if lev == 1 and not in_num:
                in_den = True
        elif s == '}':
            lev -= 1
            if lev == 0:
                if not in_den:
                    in_num = False
                else:
                    in_den = False
        #lev == 1 and not in_num and 
        if in_num:
            num += s
        if in_den:
            if not (s == '{' and lev == 1):
                den += s
    if lev == 0:
        if pre == '':
            return {'num':num,'den':den}
        elif pre == '-':
            return {'num':'-('+num + ')','den':den}
        else:
            return {'num':'('+ pre + ')('+num + ')','den':den}
    else:
        return False

#################################### 
#recibe una fracción con radicales y verifica que 
# esté simplificada y racionalizada

'''
1.- si es una fracción, separar numerador y denominador
2.- el denominador no debe tener radicales
3.- separar cada término del numerador, 
       los radicales deben estar simplificados, 
       deben tener diferente radicando 
       no debe haber más de un término numérico
4.- el denominador debe ser un solo término numérico
5.- factorizar el numerador y el denominador y verificar que no exista un factor común
'''

def frac_rad_simp(ltx,validar):
    
    d = valida_ltx(ltx,[],['sqrt'])
    if not d['valida']:
        return False
    
    if validar:
        ncad = d['cad']
        
        #extrae raices y fracciones, el resultado debe ser un número
        if ncad.find('frac') >= 0:
            ncad = ncad.replace('frac','')
        if ncad.find('sqrt') >= 0:
            ncad= ncad.replace('sqrt','')
        if ncad.find('-') >= 0:
            ncad = ncad.replace('-','')
        if ncad.find('+') >= 0:
            ncad = ncad.replace('+','')
        if ncad.find('*') >= 0:
            ncad = ncad.replace('*','')
        if ncad.find('/') >= 0:
            ncad = ncad.replace('/','')
        if ncad.find('\\') >= 0:
            ncad = ncad.replace('\\','')
        if ncad.find('(') >= 0:
            ncad = ncad.replace('(','')
        if ncad.find(')') >= 0:
            ncad = ncad.replace(')','')
        #si lo que resta no es un número entonces noe s una cadena válida
        if not es_numero(ncad):
            return False    
    
    facts = factores3(d['cad'],True)
    
    #verifica que cada factor esté simplificado
    #num_fcts = []
    #den_fcts = []
    for f in facts:
        #extrae los términos de cada factor y verifica que estén simplifciados
        trms = ltx_terminos3(f['c'],[])
        for t in trms:
            #factoriza el término
            fact_t = factores3(t,f['in_num'])
            if len(fact_t) == 1:
                if not frac_rad_simp_unary(f): #debe regresar la lista de factores enteros en el numerador y en el denominador
                    return False
            else:
                if not frac_rad_simp(t,False):
                    return False
    
    #revisa que los factores numéricos del numerador 
    #y denominador sean primos entre sí
    #if len(num_fcts) > 0 and len(den_fcts) > 0:
    #    div = gcd(num_fcts[0],den_fcts[0])
    #    if div != 1:
    #        return False
    return True
    
def frac_rad_simp_unary(f):
    #verifica que cada factor esté simplificado (radicales simplificados)
    #num_fcts = []
    #den_fcts = []
    '''
    if es_numero(f['c']):
        if f['in_num']:
            if len(num_fcts) > 0:
                return False
            num_fcts.append(f['c'])
        else:
            if len(den_fcts) > 0:
                return False
            den_fcts.append(f['c'])
    '''
    if f['in_num']:
        trms = ltx_terminos3(f['c'],[]) # se asegura que cada término esté simplificado
        #verifica que cada término esté simplificado
        #que no tenga radicandos con factores cuadráticos
        #que los términos no tenga un factor común
        rads = []
        cte = False
        for t in trms:
            #print ltx_terminos3(t,[])
            #print factores3(t,True)
            
            if t.find('sqrt')>=0:
                rad = extrae_radicando_cad(t)
                if rad in rads:
                    return False
                rads.append(rad)
                if not rad_simp_cad(t):
                    return False
            elif es_numero(t):
                if cte:
                    return False
                cte = True
            elif t.find('/'): #fracción
                if cte:
                    return False
                cte = True
                t_fcts = factores3(t,True)
                if len(t_fcts) != 2:
                    return False
                #revisa si los factores están simplificados
                if not (es_numero(t_fcts[0]['c']) and es_numero(t_fcts[1]['c'])):
                    return False
                else:
                    n1 = int(t_fcts[0]['c'])
                    n2 = int(t_fcts[1]['c'])
                    if gcd(n1,n2) != 1:
                        return False
            
        #factoriza el factor
        e = str2expr(f['c'],[])
        ef = factor(e)
        of = ef.as_ordered_factors()
        if len(of) > 1:
            if es_numero(latex(of[0])):
                #if len(num_fcts) > 0:
                return False
                #num_fcts.append(f['c'])                    
            
    elif not f['in_num']:
        if f['c'].find('sqrt') >= 0:
            return False
        if f['c'].find('/') >= 0:
            return False
        #factoriza el factor
        #e = str2expr(f['c'],[])
        #ef = factor(e)
        #of = ef.as_ordered_factors()
        #if len(of) > 1:
        #    if es_numero(latex(of[0])):
        #        if len(den_fcts) > 0:
        #            return False
        #        den_fcts.append(f['c'])
    return True

'''
        rads = []
        cte = False
        for t in trms:
            #verifica que el término esté simplificado
            if t.find('sqrt') >= 0:
                if not rad_simp(t):
                    return False
                else:
                    r = extrae_radicando(t)
                    if r in rads:
                        return False
                    else:
                        rads.append(r)
            elif es_numero(t):
                if cte:
                    return False
                else:
                    cte = True #una sola constante
    return True
    '''
            
def extrae_radicando(ltx):
    nltx = ltx.replace(' ','')
    ind = nltx.find('sqrt{')
    if ind < 0:
        return ''
    else:
        lev = 1
        rad = ''
        ind = ind + 5
        while lev > 0 and ind < len(nltx):            
            if nltx[ind] == '{':
                lev += 1
            elif nltx[ind] == '}':
                lev -= 1
            else:
                rad = rad+nltx[ind]
            ind += 1
    return rad
    
def extrae_radicando_cad(cad):
    nltx = cad.replace(' ','')
    ind = cad.find('sqrt(')
    if ind < 0:
        return ''
    else:
        lev = 1
        rad = ''
        ind = ind + 5
        while lev > 0 and ind < len(nltx):            
            if nltx[ind] == '(':
                lev += 1
            elif nltx[ind] == ')':
                lev -= 1
            else:
                rad = rad+nltx[ind]
            ind += 1
    return rad
                
def es_numero(cad):
    if cad.count('.')>1:
        return False
    ncad = cad
    ncad = ncad.replace('.','')
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for i,c in enumerate(ncad):
        if i > 0:
            if not c in nums:
                return False
        elif (not c in nums) and c != '-':
            return False
    return True

def radical_esSolucion(data,ltx):
    d = var_nom_esSolucion(data,ltx)
    if d['calif'] != 1:
        return d
    #verifica que el radical esté simplificado
    if frac_rad_simp(ltx,True):
        return d
    else:
        d['msg'] = 'No simplificaste el radical'
        d['calif'] = 0
        return d
    

def fraccion_simplificada(ltx):
    #separa el numerador y el denominador
    i0_num = ltx.find('c{')+2
    i1_num = ltx.find('}{')
    num = ltx[i0_num:i1_num]
    
    i0_den = ltx.find('}{')+2
    den = ltx[i0_den:-1]
    
    #primera prueba (ambos son números?)
    if not (es_numero(num) and es_numero(den)):
        return False
    return abs(gcd(int(num), int(den))) == 1

def simplificada(ltx):
    if ltx.find('+')>=0:
        return False
    if ltx.find('-')>0:
        return False
    if ltx.find('times')>=0:
        return False
    if ltx.find('div')>=0:
        return False
    if ltx.find('cdot')>=0:
        return False
    if ltx.find('^')>=0:
        return False
    
    return True

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
