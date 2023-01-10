# -*- coding: utf-8 -*-
from random import randint,sample, random, shuffle
from sympy import *
import copy
from tutor.sistema_experto.Ejercicios.ProdNotProc import procedureProdNot
from tutor.sistema_experto.EjerciciosClases.Ejercicios import optionsExercise
from tutor.sistema_experto.Ejercicios.PolinomioProc import procedurePolinomio
from tutor.sistema_experto.Ejercicios.PolinomioAssess import esSolucionPolinomio
from tutor.sistema_experto.Assess.FactorAssess import factorPasoCorrecto
from tutor.sistema_experto.Assess.ProdNotAssess import prodNotEsSolucion, prodNotPasoCorrecto, ltxToE

from tutor.sistema_experto.Ejercicios.FactorizacionProc import procedureFactor

from tutor.sistema_experto.Ejercicios.exp_systm_fact_tree import polinomio, explica_fact
from sympy import binomial

def rand_rat():
    a = randint(1,9)
    b = randint(1,9)
    r = Rational(a,b)
    i = 0
    
    while r.q == 1 and i < 10:        
        a = randint(1,9)
        b = randint(1,9)
        r = Rational(a,b)
        i += 1
        
    return rand_sign()*r

def perms():
    p0 = [3, 2, 1, 0]
    p1 = [3, 2, 0, 1]
    p2 = [3, 1, 2, 0]
    p3 = [3, 1, 0, 2]
    p4 = [3, 0, 2, 1]
    p5 = [3, 0, 1, 2]
    p6 = [2, 3, 1, 0]
    p7 = [2, 3, 0, 1]
    p8 = [2, 1, 3, 0]
    p9 = [2, 1, 0, 3]
    p10 = [2, 0, 3, 1]
    p11 = [2, 0, 1, 3]
    p12 = [1, 3, 2, 0]
    p13 = [1, 3, 0, 2]
    p14 = [1, 2, 3, 0]
    p15 = [1, 2, 0, 3]
    p16 = [1, 0, 3, 2]
    p17 = [1, 0, 2, 3]
    p18 = [0, 3, 2, 1]
    p19 = [0, 3, 1, 2]
    p20 = [0, 2, 3, 1]
    p21 = [0, 2, 1, 3]
    p22 = [0, 1, 3, 2]
    p23 = [0, 1, 2, 3]
    permuts = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23]
    ind = randint(0,23)
    return permuts[ind]

def rand_sign():
    s = randint(0,1)    
    if s == 0:
        s = -1
    return s

def dif_randmoncmp(ref,lits):
    i = 0    
    res = rand_mon_comp_pos(lits)            
    while(res in ref and i < 100):
        res = rand_mon_comp_pos(lits)        
        i = i+1
        
    return res
 
#algunos exponentes pueden ser cero 
def dif_randmoncmp2(ref,lits):
    i = 0    
    res = rand_mon_comp_pos2(lits)            
    while(res in ref and i < 100):
        res = rand_mon_comp_pos2(lits)        
        i = i+1
        
    return res
    
def dif_sim_randmoncmp(mod,ref,lits):
    i = 0    
    res = sim_mon_comp(mod,lits)
    while(res in ref and i < 100):
        res = sim_mon_comp(mod,lits)        
        i = i+1
        
    return res
    
def rand_poly(lit,deg,coef_width=10,norm=False):
    res = rand_sign()*randint(1,coef_width)
    if norm:
        res = res+lit**deg
    else:
        res = res+rand_sign()*randint(2,coef_width)*lit**deg
    
    for pot in range(1,deg):
        c = rand_sign()*randint(0,coef_width) 
        res = res+c*lit**pot
        
    return res
    
    
#regresa un monomio con un coeficiente
#el exponente puede ser positivo o negativo
def rand_mon_simp(lit):
    c = rand_sign()*randint(1,9)
    e = rand_sign()*randint(1,5)
    return c*lit**e
    
def rand_potlit(lit):
    e = rand_sign()*randint(1,5)
    return lit**e

#monomio compuesto por varias literales, los exponentes pueden ser negativos    
def rand_mon_comp1(lits):
    res = rand_sign()*randint(1,9) #coeficiente
    for l in lits:
        e = rand_sign()*randint(1,5)
        res = res*(l**e)
    return res
    
def rand_mon_comp2(lits,deg):
    res = rand_sign()*randint(1,9) #coeficiente
    for l in lits:
        e = rand_sign()*randint(1,deg)
        res = res*(l**e)
    return res

def rand_mon_comp3(coefs,lits,degs):
    res = sample(coefs,1)[0] #coeficiente
    for l in lits:
        e = sample(degs,1)[0]
        res = res*(l**e)
    return res

    
def rand_mon_comp(lits,deg,min_exp,exp_neg,coef):
    if coef:
        res = rand_sign()*randint(1,9) #coeficiente
    else:
        res = 1
            
    for l in lits:
        if exp_neg:
            e = rand_sign()*randint(min_exp,deg)
        else:
            e = randint(min_exp,deg)            
        res = res*(l**e)
    return res
    
#evita que los monomios sean diferentes solamente en el coeficiente
def dif_rand_mon_comp(lits,mons,deg,min_exp,exp_neg,coef):
    #extrae los coeficientes de los monomios
    nocoeff_mons = []
    for m in mons:
        d = desc_mon(m)
        nocoeff_mons.append(d[1])
        
    #genera un nuevo monomio
    nm = rand_mon_comp(lits,deg,min_exp,exp_neg,False)    
    i = 1
    while nm in nocoeff_mons and i < 100:
        nm = rand_mon_comp(lits,deg,min_exp,exp_neg,False)            
        if i%10==0:
            deg = deg+1        
        i = i+1
        
    if coef:
        nm = rand_sign()*randint(1,9)*nm
        
    return nm    
    
def desc_mon(mon):
    d = mon.as_terms()
    coeff = int(round(d[0][0][1][0][0]))
    resto = d[0][0][0]/coeff
    return [coeff,resto,d[1],d[0][0][1][1]]

'''
#coeficiente de 1    
def rand_mon_comp1(lits):
    res = 1 #coeficiente
    for l in lits:
        e = rand_sign()*randint(1,5)
        res = res*(l**e)
    return res
'''

def rand_mon_comp_pos(lits):
    res = 1 #coeficiente
    for l in lits:
        e = randint(1,5)
        res = res*(l**e)
    return res

def rand_mon_comp_pos2(lits):
    res = 1 
    for l in lits:
        e = randint(0,9)
        res = res*(l**e)
    return res
  
    
def sim_mon_comp(ref,lits):
    res = ref
    #muestrea una literal aleatoriamente
    l = lits[randint(0,len(lits)-1)]    
    #aplica una operación aleatoria
    e = rand_sign()*randint(1,3)
    res = res*(l**e)
    return res
    
def terms2poly(p_terms):
    r = 0
    for t in p_terms:
        r = r+t
    return r
    
    
def dif_pol(p_terms,pols,lits):
    #selecciona una literal y modifica un término del polinomio 
    #multiplicando por una potencia de la literal    
    np_terms = copy.copy(p_terms)    
    
    #elige algunos términos al azar y los modifica
    ind_trm = sample(range(len(np_terms)),randint(1,len(np_terms)))
    
    s_lits = set(lits) 
    
    for ind in ind_trm:
        t = np_terms[ind]
        ats = t.atoms()
        t_lits = ats.intersection(s_lits)
        if len(t_lits) > 0:
            #elige una literal al azar
            lit = sample(t_lits,1)
            d = t.as_coeff_exponent(lit[0])
            t = t*lit[0]**randint(-d[1],d[1])
            np_terms[ind] = t
            
    np = terms2poly(np_terms)
    i = 1
    w = 0
            
    while np in pols and i < 100:
        
        #elige algunos términos al azar y los modifica
        ind_trm = sample(range(len(np_terms)),randint(1,len(np_terms)))
        
        for ind in ind_trm:
            t = np_terms[ind]
            ats = t.atoms()
            t_lits = ats.intersection(s_lits)
            if len(t_lits) > 0:
                #elige una literal al azar
                lit = sample(t_lits,1)
                d = t.as_coeff_exponent(lit[0])
                if d[1] > 0:
                    t = t*lit[0]**randint(-d[1],d[1]+w)
                else:
                    t = t*lit[0]**randint(-d[1]-w,d[1])
                np_terms[ind] = t          
        
        np = terms2poly(np_terms)
        i = i+1
        if i%10 == 0 and i > 0:
            w = w+1    
        
    return [np, np_terms]
    
def dif_pol_exp_gen(p_terms,pols,lits):
    #selecciona una literal y modifica un término del polinomio 
    #multiplicando por una potencia de la literal    
    np_terms = copy.copy(p_terms)    
    #elige algunos términos al azar y los modifica
    r = range(len(p_terms))
    trms = sample(r,randint(1,len(r)-1))
    
    for t in trms:
        #escoge una literal
        lit = lits[randint(0,len(lits)-1)]
                
        m = rand_potlit(lit)
        np_terms[t] = m*np_terms[t]  
    
    np = terms2poly(np_terms)
    i = 0
    
    while np in pols and i < 100:
        np_terms = copy.copy(p_terms)    
        #elige algunos términos al azar y los modifica
        r = range(len(p_terms))
        trms = sample(r,randint(1,len(r)-1))
        
        for t in trms:
            #escoge una literal
            lit = lits[randint(0,len(lits)-1)]
            m = rand_potlit(lit)
            np_terms[t] = m*np_terms[t]  
        
        np = terms2poly(np_terms)
        i = i+1
    
        
    return [np, np_terms]
     
def poly2terms(pol):
    d = pol.as_terms()
    
    res = []
    for t in d[0]:
        res.append(t[0])
    
    return res
        
    
def prod_monomio_poly(title="",name="",nlits=2,nterms=3,deg=4,exp_neg=False):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    f1 = rand_mon_comp(lits[0],deg,1,exp_neg,coef)
    
    f2 = 0
    f2_terms = []
    nm = randint(2,nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,exp_neg,coef)
        f2_terms.append(m)        
        f2 = f2+m        
    
    preg = '$$' + latex(f1) + '\\left(' + latex(f2) + '\\right) $$ es equivalente a:'  
    
    resp = []
    res = expand(f1*f2)
    res_trms = poly2terms(res)
    
    resp.append(latex(res,mode='inline'))    
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2)
    resp.append(latex(res2,mode='inline')) 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3)
    resp.append(latex(res2,mode='inline')) 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4)
    resp.append(latex(res4,mode='inline')) 
        
    ex = optionsExercise(preg,resp[0],resp,"")    
    return ex
    
def prod_monomio_poly_proc(nlits,nterms,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    f1 = rand_mon_comp(lits[0],deg,1,False,coef)
    
    f2 = 0
    f2_terms = []
    nm = randint(nterms,nterms)
        
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,False,coef)
        f2_terms.append(m)        
        f2 = f2+m
            
    coefMul = f1.as_coeff_Mul() 
    sf1 = '' if coefMul[0] < 0 else '+' 
    dev_mul = ''
    dev2 = ''        
    ot = f2.as_ordered_terms()
    for i,t in enumerate(ot):
        dev_mul += sf1+latex(f1)+'\\left('+latex(t)+'\\right)'
        if i == 0 and dev_mul[0] == '+':
            dev_mul = dev_mul[1:]
        
        p = f1*t
        coefMul = p.as_coeff_Mul() 
        s = '' if coefMul[0] < 0 else '+'
        dev2 += s+latex(p)
        if i == 0 and dev2[0] == '+':
            dev2 = dev2[1:]
                
        
    preg = 'Desarrolla el siguiente producto notable: $$' + latex(f1) + '\\left(' + latex(f2) + '\\right) $$'
    
    res = expand(f1*f2)
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+latex(f1) + '\\left(' + latex(f2) + '\\right)} &= '+dev_mul+'\\\\'    
    proc += '&=\\color{blue}{'+latex(res)+'}\\\\'     
    proc += '\\end{align}'  
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = latex(f1) + '\\left(' + latex(f2) + '\\right)'
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex
        
    
def prod_polinomios(title,name,nlits,max_nterms,deg,exp_neg):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    
    f1 = 0
    f1_terms = []
    nm = randint(2,max_nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f1_terms,deg,0,exp_neg,coef)
        f1_terms.append(m)        
        f1 = f1+m
        
    f2 = 0
    f2_terms = []
    nm = randint(2,max_nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,exp_neg,coef)
        f2_terms.append(m)        
        f2 = f2+m        
    
    preg = '$$\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) $$ es equivalente a:'  
    
    res = expand(f1*f2)
    res_trms = poly2terms(res)
    res1 = latex(res,mode='inline')
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2,mode='inline') 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3,mode='inline') 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4,mode='inline') 
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def prod_polinomios_proc(nlits,max_nterms,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f1 = 0
    f1_terms = []
    nm = randint(3,max_nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f1_terms,deg,0,False,coef)
        f1_terms.append(m)        
        f1 = f1+m
        
    f2 = 0
    f2_terms = []
    nm = randint(2,max_nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,False,coef)
        f2_terms.append(m)        
        f2 = f2+m
        
    ot1 = f1.as_ordered_terms()
    ot2 = f2.as_ordered_terms()
    
    dev1 = ''
    prods = []
    for i,t in enumerate(ot1):
        dev1 += '\\left('+latex(t)+'\\right)\\left('+latex(f2)+'\\right)+'
        e = expand(t*f2)
        prods.append(e)        
    dev1 = dev1[:-1]
        
    dev2 = ''
    pol = {}
    for p in prods:
        dev2 += '\\left('+latex(p)+'\\right)+'
        pt = p.as_ordered_terms()
        for t in pt:
            tc = t.as_coeff_Mul()
            if not tc[1] in pol.keys():
                pol[tc[1]] = [t]
            else:        
                pol[tc[1]].append(t)
    dev2 = dev2[:-1]
        
    preg = 'Desarrolla el siguiente producto notable: $$\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) $$'  
    
    res = expand(f1*f2)    
    ltx_math_prob = '\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right)'
    
    dev3 = ''
    res_ot = res.as_ordered_terms() 
    for t in res_ot:
        tm = t.as_coeff_Mul()        
        tg = pol[tm[1]]
        if len(tg)>1:
            if dev3 != '':
                dev3 += '+\\left('
            else:
                dev3 += '\\left('
            for i,tr in enumerate(tg):            
                if i == 0:
                    s = ''
                else:
                    tm = tr.as_coeff_Mul()
                    s = '' if tm[0] < 0 else '+'                             
                dev3 += s+latex(tr)
            dev3+='\\right)'
        else: #un solo término
            if dev3 != '':
                s = '' if tm[0] < 0 else '+'
            else:
                s = ''                
            dev3 += s+latex(tg[0])
            
    if dev3[-1] == '+':
        dev3 = dev3[:-1]
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_math_prob +'}&= ' +dev1+'\\\\'
    proc += '&= ' +dev2+'\\\\'
    proc += '&= ' +dev3+'\\\\'
    proc += '&= \\color{blue}{' +latex(res)+'}\\\\'
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_math_prob
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex

    
def bin_conj(title,name,nlits,deg,exp_neg):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    
    f1 = 0
    f1_terms = []
    nm = randint(2,2) #binomios
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f1_terms,deg,0,exp_neg,coef)
        f1_terms.append(m)        
        f1 = f1+m
        
    #forma el binomio conjugado
    f2_terms = copy.copy(f1_terms)        
    f2_terms[1] = -f2_terms[1]
    f2 = terms2poly(f2_terms)           
    
    preg = '$$\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) $$ es equivalente a:'  
    
    res = expand(f1*f2)
    res_trms = poly2terms(res)
    res1 = latex(res,mode='inline')
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2,mode='inline') 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3,mode='inline') 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4,mode='inline') 
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def bin_conj_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f1 = 0
    f1_terms = []
    nm = randint(2,2) #binomios
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f1_terms,deg,0,False,coef)
        f1_terms.append(m)        
        f1 = f1+m
        
    #forma el binomio conjugado
    f2_terms = copy.copy(f1_terms)        
    f2_terms[1] = -f2_terms[1]
    f2 = terms2poly(f2_terms)           
    
    preg = 'Desarrolla el siguiente producto notable: $$\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) $$'      
    res = expand(f1*f2)
    
    ltx_prob = '\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right)'
    
    cm = f1_terms[1].as_coeff_Mul()
    t2 = -f1_terms[1] if cm[0] < 0 else f1_terms[1]        
    
    dev1 = '\\left('+latex(f1_terms[0])+'\\right)^2-''\\left('+latex(t2)+'\\right)^2'
    dev2 = latex(f1_terms[0]**2)+'-'+latex(t2**2)
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}&='+ dev1+'\\\\'
    proc += '&=\\color{blue}{'+ dev2+'}\\\\'
    proc += '\\end{align}'
    proc += '<b>Observa que</b>: al cuadrado del término que no cambia de signo, en los binomios, se le resta el cuadrado del término que sí cambia de signo.'
    
    
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_prob
    d['proc'] = proc 
    ex = procedureProdNot(d)
    return ex

def bin_term_comun_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    tc = 1
    for l in lits[0]:
        tc = tc*l**randint(1,deg)    
    tc = tc*rand_sign()*randint(1,9)
    [l1, l2] = sample(range(1,10),2)
    l1 = rand_sign()*l1
    l2 = rand_sign()*l2
    
    f1 = tc + l1
    f2 = tc + l2   
    
    preg = 'Desarrolla el siguiente producto notable: \\begin{equation}\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) \\end{equation}'      
    res = expand(f1*f2)
    
    ltx_prob = '\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right)'
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}&=('+latex(f1)+')('+latex(tc)+')+'+'('+latex(f1)+')('+latex(l2)+')\\\\'
    proc += '&=\\color{blue}{'+latex(f1*tc)+'+('+latex(f1*l2)+')}\\\\'
    proc += '&=\\color{blue}{'+latex(expand(f1*f2))+'}\\\\'
    proc += '\\end{align}'
    
    
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_prob
    d['proc'] = proc 
    ex = procedureProdNot(d)
    return ex

   
    
def bin_cuad(title="",name="",nlits=3,deg=3,exp_neg=False):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,exp_neg,coef)
        f_terms.append(m)
        f = f+m
        
    
    preg = '$$\\left(' + latex(f) + '\\right)^2 $$ es equivalente a:'  
    
    res = expand(f*f)
    res_trms = poly2terms(res)
    res1 = latex(res,mode='inline')
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2,mode='inline') 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3,mode='inline') 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4,mode='inline') 
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def bin_cuad_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,False,coef)
        f_terms.append(m)
        f = f+m       
    
    preg = 'Desarrolla el siguiente producto notable: $$\\left(' + latex(f) + '\\right)^2 $$'  
    
    res = expand(f*f)
    ltx_prob = '\\left(' + latex(f) + '\\right)^2'
    
    otf = f.as_ordered_terms()
    
    dev1 = '\\left('+latex(otf[0])+'\\right)^2'
    dev1 += '+2\\left('+latex(otf[0])+'\\right)\\left('+latex(otf[1])+'\\right)'
    dev1 += '+\\left('+latex(otf[1])+'\\right)^2'
    
    dev2 = latex(otf[0]**2)
    tm = 2*otf[0]*otf[1]
    cm = tm.as_coeff_Mul()
    s = '' if cm[0] < 0 else '+'
    dev2 += s+latex(tm)
    dev2 += '+'+latex(otf[1]**2)  
        
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}&='+dev1+'\\\\'   
    proc += '&=\\color{blue}{'+dev2+'}\\\\' 
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = '\\left(' + latex(f) + '\\right)^2'
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex
    
def trin_cuad(title="",name="",nlits=3,deg=3,exp_neg=False):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(3,3) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,exp_neg,coef)
        f_terms.append(m)
        f = f+m        
    
    preg = '$$\\left(' + latex(f) + '\\right)^2 $$ es equivalente a:'  
    
    res = expand(f*f)
    res_trms = poly2terms(res)
    res1 = latex(res,mode='inline')
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2,mode='inline') 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3,mode='inline') 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4,mode='inline') 
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def trin_cuad_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = 3
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,False,coef)
        f_terms.append(m)
        f = f+m     
        
    ltx_prob = '\\left(' + latex(f) + '\\right)^2'   
    
    preg = 'Desarrolla el siguiente producto notable: $$' + ltx_prob + '$$'  
    
    res = expand(f*f)
    
    otf = f.as_ordered_terms()
    
    dev1 = ''
    for t in otf:
        dev1 += '\\left('+latex(t)+'\\right)^2+'
    dev1 = dev1[:-1]
    dev1 += '\\\\'
    dev1 += '&\\;+'    
    cps = [(0,1),(0,2),(1,2)]
    for c in cps:
        dev1 += '2\\left('+latex(otf[c[0]])+'\\right)\\left('+latex(otf[c[1]])+'\\right)+'
    dev1 = dev1[:-1]
    
    dev2 = ''
    for t in otf:
        dev2 += latex(t**2)+'+'
    dev2 = dev2[:-1]
    dev2 += '\\\\'
    dev2 += '&\\;'    
    for c in cps:
        pc = 2*otf[c[0]]*otf[c[1]]
        cm = pc.as_coeff_Mul()
        s = '' if cm[0] < 0 else '+' 
        dev2 += s+latex(pc)
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}=&'+dev1+'\\\\'   
    proc += '=&'+dev2+'\\\\'
    proc += '=&\\color{blue}{'+latex(res)+'}\\\\'
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_prob
    d['proc'] = proc 
    ex = procedureProdNot(d)
    return ex
    
def bin_cub(title="",name="",nlits=2,deg=2,exp_neg=False):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,exp_neg,coef)
        f_terms.append(m)
        f = f+m        
    
    preg = '$$\\left(' + latex(f) + '\\right)^3 $$ es equivalente a:'  
    
    res = expand(f**3)
    res_trms = poly2terms(res)
    res1 = latex(res,mode='inline')
    [rf2,rf2t] = dif_pol(res_trms,[res],lits[0])
    res2 = latex(rf2,mode='inline') 
    [rf3,rf3t] = dif_pol(res_trms,[res,rf2],lits[0])
    res3 = latex(rf3,mode='inline') 
    [rf4,rf4t] = dif_pol(res_trms,[res,rf2,rf3],lits[0])
    res4 = latex(rf4,mode='inline') 
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex   
    
def bin_cub_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,False,coef)
        f_terms.append(m)
        f = f+m
        
    ltx_prob = '\\left(' + latex(f) + '\\right)^3'
    preg = 'Desarrolla el siguiente producto notable: \\begin{equation}'+ ltx_prob+'\\end{equation}'
    
    res = expand(f**3)
    
    oft = f.as_ordered_terms()
    
    dev1 = '\\left('+latex(oft[0])+'\\right)^3+3\\left('+latex(oft[0])+'\\right)^2\\left('+latex(oft[1])+'\\right)'
    dev1 += '+3\\left('+latex(oft[0])+'\\right)\\left('+latex(oft[1])+'\\right)^2+'+'\\left('+latex(oft[1])+'\\right)^3'
    
    dev2 = '\\left('+latex(oft[0]**3)+'\\right)+3\\left('+latex(oft[0]**2)+'\\right)\\left('+latex(oft[1])+'\\right)'
    dev2 += '+3\\left('+latex(oft[0])+'\\right)\\left('+latex(oft[1]**2)+'\\right)+'+'\\left('+latex(oft[1]**3)+'\\right)'  
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}=&'+dev1+'\\\\'
    proc += '=&'+dev2+'\\\\'   
    proc += '=&\\color{blue}{'+latex(res)+'}\\\\'
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_prob
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex

def bin_nth_pow_proc(nlits,deg,n_pow,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,False,coef)
        f_terms.append(m)
        f = f+m
        
    ltx_prob = '\\left(' + latex(f) + '\\right)^{'+latex(n_pow)+'}'
    preg = 'Desarrolla el siguiente producto notable: \\begin{equation}'+ ltx_prob+'\\end{equation}'
    
    res = expand(f**n_pow)
    
    oft = f.as_ordered_terms()
    
    proc = 'Los siguientes números son los coeficientes obtenidos mediante el triángulo de Pascal: <ul>'
    for i in range(0,n_pow+1):
        proc += '<li>$'+latex(binomial(n_pow,i))+'$</li>'
    proc += '</ul>'
    
    proc += "El desarrollo es entonces:"
    
    t1 = f_terms[0]
    t2 = f_terms[1]    
    
    proc += '\\begin{align}'
    proc += '\\color{red}{'+ltx_prob+'}=&'
    for i in range(0,n_pow+1):
        c = latex(binomial(n_pow,i)) if not (i==0 or i==n_pow) else ''
        p2 = '' if i == 0 else str(i)
        p1 = '' if i == n_pow else str(n_pow-i)
        st1 = '' if i==n_pow else '('+latex(t1)+')^{'+p1+'}'
        st2 = '' if i==0 else '('+latex(t2)+')^{'+p2+'}'
        s = '+' if i != n_pow else ''
        proc += c+st1+st2+s
    proc += '\\\\'
    proc += '=&\\color{blue}{'+latex(res)+'}\\\\'
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_prob
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex
    
def fact_prod_monomio_poly(title="",name="",nlits=2,nterms=3,deg=2,exp_neg=False):
    
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    f1 = rand_mon_comp(lits[0],deg,1,exp_neg,coef)
    
    f2 = 0
    f2_terms = []
    nm = nterms
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,exp_neg,coef)
        f2_terms.append(m)        
        f2 = f2+m        
        
    expresion = expand(f1*f2) 
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'
    
    rf2 = dif_fact_mon_poly(f1,f2,[expresion])
    rf3 = dif_fact_mon_poly(f1,f2,[expresion,rf2])
    rf4 = dif_fact_mon_poly(f1,f2,[expresion,rf2,rf3])
   
    res1 = latex(factor(expresion),mode='inline')
    res2 = latex(factor(rf2),mode='inline') 
    res3 = latex(factor(rf3),mode='inline') 
    res4 = latex(factor(rf4),mode='inline')
    
    resp = []
    resp.append(res1) 
    resp.append(res2)
    resp.append(res3)
    resp.append(res4)  
    
        
    ex = optionsExercise(preg,resp[0],resp,"")    
    return ex
    
def fact_prod_monomio_poly_proc(title,name,nlits,nterms,deg):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)     
    
    coef = True
    f1 = rand_mon_comp(lits[0],deg,1,False,coef)
    
    f2 = 0
    f2_terms = []
    nm = randint(2,nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,False,coef)
        f2_terms.append(m)        
        f2 = f2+m        
        
    e = expand(f1*f2) 
    ef = factor(e)
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]], 'e':e, 'ef':ef}
    return d
    
#toma un polinimio y modifica ligeramente algún coeficiente o exponente
#hasta que no coincida con algún término del vector 

def rand_close_zero(limmax):
    r = 1.0*randint(1,limmax)/(1.0*limmax)
    r = r*r
    return int(round(limmax*r))
    
def dif_fact_mon_poly(f1,f2,refs):
    #elige modificar aleatoriamente cualquiera d elos dos factores
    f2_terms = poly2terms(f2)
    
    r = random()
    if r < 0.5:
        nf1 = modifica_mon(f1)
        res = expand(nf1*f2)
    else:
        #elige aleatoriamente uno de los términos del polinomio 2
        
        ind = randint(0,len(f2_terms)-1) 
        nt = modifica_mon(f2_terms[ind])
        f2_terms[ind] = nt
        nf2 = terms2poly(f2_terms)
        res = expand(f1*nf2)
    
    i = 1
    
    while res in refs and i < 100:
        f2_terms = poly2terms(f2)
        r = random()
        if r < 0.5:
            nf1 = modifica_mon(f1)
            res = expand(nf1*f2)
        else:
            #elige aleatoriamente uno de los términos del polinomio 2
            
            ind = randint(0,len(f2_terms)-1) 
            nt = modifica_mon(f2_terms[ind])
            f2_terms[ind] = nt
            nf2 = terms2poly(f2_terms)
            res = expand(f1*nf2)
        
        i = i+1
        
    return res
        
    

def dif_mon(mon,mons):
    res = modifica_mon(mon)
    i = 1
    while res in mons and i < 100:
        res = modifica_mon(mon)
        i = i+1        
    return res        

def modifica_mon(mon):
    #descompone el monomio
    d = mon.as_terms()    
    #elige una literal aleatoriamente
    if len(d[1]) > 0:
        ind = randint(0,len(d[1])-1)
        lit = d[1][ind]
        l_exp = d[0][0][1][1][ind]
        pert_exp = rand_sign()*rand_close_zero(l_exp)
        res = mon*lit**pert_exp
    else:
        res = rand_sign()*rand_close_zero(10)*mon
    return res
    
    
def fact_prod_bins(title,name,nlits, deg=1):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales    
    pr = 1
    for l in lits[0]:
        deg = randint(1,deg)
        pr = pr*l**deg
        
    [a,b] = sample(range(-10,-1)+range(1,10),2)
    
    f1 = pr+a
    f2 = pr+b
    
    expresion = expand(f1*f2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'
    
    rf2 = (pr-a)*(pr+b)
    rf3 = (pr+a)*(pr-b)
    rf4 = (pr-a)*(pr-b)
    
    resps = []
    sol = factor(expresion)
    sol = '$'+latex(sol)+'$'
    res2 = '$'+latex(factor(rf2))+'$'
    res3 = '$'+latex(factor(rf3))+'$'
    res4 = '$'+latex(factor(rf4))+'$'
    resps.append(sol)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def fact_prod_bins_proc(title,name,nlits,norm=True):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l**randint(1,2)
    
    f1 = rand_poly(pr,1,5,norm)
    f2 = rand_poly(pr,1,5,True)
    
    e = expand(f1*f2)
    ef = factor(e)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]], 'e':e, 'ef':ef}
    return d
    
    
def fact_prod_bins2(title="",name="",nlits=2,nprimes=5):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l
        
    #escoge un par de valores    
    [rts,prod] = roots_for_fact_prod_bins(nprimes)
    fctrs = build_fctrs(pr,rts)
    f1 = fctrs[0]
    f2 = fctrs[1]   
    
    expresion = expand(f1*f2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'    
    
    sf2 = dif_two_rand_factors(prod,[rts]) 
    rf2 = build_fctrs(pr,sf2)
    sf3 = dif_two_rand_factors(prod,[rts,sf2]) 
    rf3 = build_fctrs(pr,sf3)
    sf4 = dif_two_rand_factors(prod,[rts,sf2,sf3])     
    rf4 = build_fctrs(pr,sf4)
    
    res1 = latex(factor(expresion),mode='inline')
    res2 = '$\\left(' + latex(rf2[0])+'\\right)\\left('+latex(rf2[1])+'\\right) $'
    res3 = '$\\left(' + latex(rf3[0])+'\\right)\\left('+latex(rf3[1])+'\\right) $'
    res4 = '$\\left(' + latex(rf4[0])+'\\right)\\left('+latex(rf4[1])+'\\right) $'
        
    perm = perms()
    d = {'title':title,'preg':preg,'name':name,'res':[res1,res2,res3,res4],'perm':perm, 'symbs':[str(s) for s in lits[0]]}
    return d

def fact_prod_bins2_optns(nlits=2,nprimes=5):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l
        
    #escoge un par de valores    
    [rts,prod] = roots_for_fact_prod_bins(nprimes)
    fctrs = build_fctrs(pr,rts)
    f1 = fctrs[0]
    f2 = fctrs[1]   
    
    expresion = expand(f1*f2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'    
    
    sf2 = dif_two_rand_factors(prod,[rts]) 
    rf2 = build_fctrs(pr,sf2)
    sf3 = dif_two_rand_factors(prod,[rts,sf2]) 
    rf3 = build_fctrs(pr,sf3)
    sf4 = dif_two_rand_factors(prod,[rts,sf2,sf3])     
    rf4 = build_fctrs(pr,sf4)
    
    res1 = latex(factor(expresion),mode='inline')
    res2 = '$\\left(' + latex(rf2[0])+'\\right)\\left('+latex(rf2[1])+'\\right) $'
    res3 = '$\\left(' + latex(rf3[0])+'\\right)\\left('+latex(rf3[1])+'\\right) $'
    res4 = '$\\left(' + latex(rf4[0])+'\\right)\\left('+latex(rf4[1])+'\\right) $'
    
    resp = []
    resp.append(res1)
    resp.append(res2)
    resp.append(res3)
    resp.append(res4)
        
    ex = optionsExercise(preg,resp[0],resp,"")    
    return ex

    
def fact_prod_bins2_proc(title,name,nlits,nprimes):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l
        
    #escoge un par de valores    
    [rts,prod] = roots_for_fact_prod_bins(nprimes)
    fctrs = build_fctrs(pr,rts)
    f1 = fctrs[0]
    f2 = fctrs[1]   
    
    e = expand(f1*f2)
    ef = factor(e)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
        
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e, 'ef':ef}
    return d
    
def build_fctrs(lit,fs):
    rts = []
    
    for e in fs:
        rts.append(e)
        
    res = []    
    if len(fs) == 2:        
        res.append(lit+rts[0])
        res.append(lit+rts[1])
    else:
        res.append(lit+rts[0])
        res.append(lit+rts[0])
        
    return res      
        
    
def dif_two_rand_factors(prod,fctrs):
    sf = two_rand_factors(prod)
    i = 1
    
    while sf in fctrs and i < 100:
        sf = two_rand_factors(prod)
        i = i+1
        
    return sf    
    
def two_rand_factors(prod):
    d = factorint(prod)
    facts = []
    for f in d:
        for m in range(d[f]):
            facts.append(f)
            
    shuffle(facts)
    f1 = 1
    p1 = randint(0,len(facts)-1)
    
    for i in range(p1):
        f1 = f1*facts[i]
    
    f2 = int(round(prod/f1))
    f1 = rand_sign()*f1
    f2 = rand_sign()*f2    
    
    return set([f1,f2])          
            
    
def roots_for_fact_prod_bins(n_primes):
    primes = [2,3,5,7]
    facts = []
    for i in range(n_primes):
        ind = randint(0,len(primes)-1)
        facts.append(primes[ind])
        
    prod = 1
    for f in facts:
        prod = prod*f
    
    #divide aleatoriamente el producto en dos factores 
            
    shuffle(facts)
    f1 = 1
    p1 = randint(0,len(facts)-1)
    
    for i in range(p1):
        f1 = f1*facts[i]
    
    f2 = int(round(prod/f1))
    f1 = rand_sign()*f1
    f2 = rand_sign()*f2    
    
    return [set([f1,f2]),f1*f2]
    
def roots_for_fact_bin_cuad(n_primes):
    primes = [2,3,5,7,11,13]
    facts = []
    for i in range(n_primes):
        ind = randint(0,len(primes)-1)
        facts.append(primes[ind])        
        
    prod = 1
    for f in facts:
        prod = prod*f
    
    #divide aleatoriamente el producto en dos factores             
    f1 = rand_sign()*prod
    f2 = f1    
    
    return [set([f1,f2]),f1*f2]
    
    
def modifica_bin(b):
    res = b+rand_close_zero(5)
    return res
    
    
def dif_fact_prod_bins(b1,b2,refs):
    #elige un términp para modificar
    r = random()
    if r < 0.5:
        nb1 = modifica_bin(b1)
        res = expand(nb1*b2)
    else:
        nb2 = modifica_bin(b2)
        res = expand(b1*nb2)
    
    i = 1
    
    while res in refs and i < 100:
        r = random()
        if r < 0.5:
            nb1 = modifica_bin(b1)
            res = expand(nb1*b2)
        else:
            nb2 = modifica_bin(b2)
            res = expand(b1*nb2)
        
        i = i+1
        
    return res
    
def fact_bin_cuad(title="",name="",nlits=2,nprimes=2):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l
    
    repts = True
    i = 0
    while repts and i < 10:    
        #escoge un par de valores    
        [rts,prod] = roots_for_fact_bin_cuad(nprimes)
        fctrs = build_fctrs(pr,rts)
        f1 = fctrs[0]
        f2 = fctrs[1]   
        
        expresion = expand(f1*f2)
        
        preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'    
        
        resps = [expresion]
        sf2 = dif_two_rand_factors(prod,[rts]) 
        rf2 = build_fctrs(pr,sf2)
        sf3 = dif_two_rand_factors(prod,[rts,rf2]) 
        rf3 = build_fctrs(pr,sf3)
        sf4 = dif_two_rand_factors(prod,[rts,rf2,rf3])     
        rf4 = build_fctrs(pr,sf4)
        sf5 = dif_two_rand_factors(prod,[rts,rf2,rf3,rf4])     
        rf5 = build_fctrs(pr,sf5)
        
        resps = [expresion, expand(rf2[0]*rf2[1]), expand(rf3[0]*rf3[1]), expand(rf4[0]*rf4[1]), expand(rf5[0]*rf5[0])]
        repts = False
        for n,r in enumerate(resps):
            for m,rr in enumerate(resps):
                if m > n and r.equals(rr):
                    repts = True
        i += 1
        
    
    res1 = latex(factor(expresion),mode='inline')
    res2 = '$\\left(' + latex(rf2[0])+'\\right)\\left('+latex(rf2[1])+'\\right) $'
    res3 = '$\\left(' + latex(rf3[0])+'\\right)\\left('+latex(rf3[1])+'\\right) $'
    res4 = '$\\left(' + latex(rf4[0])+'\\right)\\left('+latex(rf4[1])+'\\right) $'
    res5 = '$\\left(' + latex(rf5[0])+'\\right)^2$'
        
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
    resps.append(res5)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def fact_bin_cuad_proc(title,name,nlits,n_w):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    t1 = 1
    for l in lits[0]:
        t1 = t1*l**randint(0,2)
    
    t2 = 1
    for l in lits[0]:
        t2 = t2*l**randint(0,2)
    
    t1 = t1*rand_sign()*randint(1,n_w)
    t2 = t2*rand_sign()*randint(1,n_w)
        
    #escoge un par de valores
    i = 0    
    e = expand((t1+t2)**2)    
    eot = e.as_ordered_terms()
    while len(eot) == 1 and i < 10:
        #multiplica todas las literales
        t1 = 1
        for l in lits[0]:
            t1 = t1*l**randint(0,2)
        
        t2 = 1
        for l in lits[0]:
            t2 = t2*l**randint(0,2)
        
        t1 = t1*rand_sign()*randint(1,n_w)
        t2 = t2*rand_sign()*randint(1,n_w)
            
        #escoge un par de valores
            
        e = expand((t1+t2)**2)
        
        eot = e.as_ordered_terms()
        i = i+1
        
    ef = factor((t1+t2)**2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return d
    
def fact_trin_cuad_proc(title,name,nlits,n_w):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    t1 = 1
    for l in lits[0]:
        t1 = t1*l**randint(0,2)
    
    t2 = 1
    for l in lits[0]:
        t2 = t2*l**randint(0,2)
        
    t3 = 1
    for l in lits[0]:
        t3 = t3*l**randint(0,2)
    
    t1 = t1*rand_sign()*randint(1,n_w)
    t2 = t2*rand_sign()*randint(1,n_w)
    t3 = t3*rand_sign()*randint(1,n_w)
        
    #escoge un par de valores
    i = 0    
    e = expand((t1+t2+t3)**2)    
    eot = e.as_ordered_terms()
    while len(eot) == 1 and i < 10:
        #multiplica todas las literales
        t1 = 1
        for l in lits[0]:
            t1 = t1*l**randint(0,2)
        
        t2 = 1
        for l in lits[0]:
            t2 = t2*l**randint(0,2)
            
        t3 = 1
        for l in lits[0]:
            t3 = t3*l**randint(0,2)
        
        t1 = t1*rand_sign()*randint(1,n_w)
        t2 = t2*rand_sign()*randint(1,n_w)
        t3 = t3*rand_sign()*randint(1,n_w)
            
        #escoge un par de valores
            
        e = expand((t1+t2+t3)**2)
        
        eot = e.as_ordered_terms()
        i = i+1
        
    ef = factor((t1+t2+t3)**2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return d

def fact_trin_cuad(title="",name="",nlits=2,n_w=5):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    #multiplica todas las literales
    t1 = 1
    for l in lits[0]:
        t1 = t1*l**randint(0,2)
    
    t2 = 1
    for l in lits[0]:
        t2 = t2*l**randint(0,2)
        
    t3 = 1
    for l in lits[0]:
        t3 = t3*l**randint(0,0)
        
    [c1, c2, c3] = sample([1,2,3,5,7],3)
    
    t1 = t1*rand_sign()*c1
    t2 = t2*rand_sign()*c2
    t3 = t3*rand_sign()*c3
        
    #escoge un par de valores
    i = 0    
    e = expand((t1+t2+t3)**2)     
    eot = e.as_ordered_terms()
    while len(eot) != 6 and i < 10:
        #multiplica todas las literales
        t1 = 1
        for l in lits[0]:
            t1 = t1*l**randint(2,2)
    
        t2 = 1
        for l in lits[0]:
            t2 = t2*l**randint(1,1)
        
        t3 = 1
        for l in lits[0]:
            t3 = t3*l**randint(0,0)
        
        [c1, c2, c3] = sample([1,2,3,5,7],3)
    
        t1 = t1*rand_sign()*c1
        t2 = t2*rand_sign()*c2
        t3 = t3*rand_sign()*c3
    
            
        #escoge un par de valores
            
        e = expand((t1+t2+t3)**2)
        
        eot = e.as_ordered_terms()        
        i = i+1
        
    ef = factor((t1+t2+t3)**2)    
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return procedureFactor(d)
        
def dif_fact_bin_cuad(mon,facts,max_coef):
    f = mon
    f = rand_sign()*randint(1,max_coef)*f+rand_sign()*randint(1,max_coef)
    i = 1
    
    while f in facts and i < 100:
        f = mon
        f = rand_sign()*randint(1,max_coef)*f+rand_sign()*randint(1,max_coef)
        i = i+1
        
    return f

def dif_fact_bin_conj(mon,prods,max_coef):
    mr = rand_sign()*randint(1,max_coef)*mon
    oth = rand_sign()*randint(1,max_coef)
    f = mr+oth
    fc = mr-oth
    prod = f*fc
    i = 1
    
    while prod in prods:
        mr = rand_sign()*randint(1,max_coef)*mon
        oth = rand_sign()*randint(1,max_coef)
        f = mr+oth
        fc = mr-oth
        prod = f*fc
        i = i+1
        
    return [f,fc]        
    
def fact_bin_cuad2(title,name,nlits,deg,max_coef,min_exp,exp_neg,coef):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    mon = rand_mon_comp(lits[0],deg,min_exp,exp_neg,coef)    
    f = mon+rand_sign()*randint(1,max_coef)    
        
    #escoge un par de valores    
    expresion = expand(f**2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'    
    
    rf2 = dif_fact_bin_cuad(mon,[f],max_coef) 
    rf3 = dif_fact_bin_cuad(mon,[f,rf2],max_coef) 
    rf4 = dif_fact_bin_cuad(mon,[f,rf2,rf3],max_coef)     
    
    res1 = '$\\left(' + latex(f)+'\\right)^2 $'
    res2 = '$\\left(' + latex(rf2)+'\\right)^2 $'
    res3 = '$\\left(' + latex(rf3)+'\\right)^2 $'
    res4 = '$\\left(' + latex(rf4)+'\\right)^2 $'
        
    perm = perms()
    d = {'title':title,'preg':preg,'name':name,'res':[res1,res2,res3,res4],'perm':perm, 'symbs':[str(s) for s in lits[0]]}
    return d
    
def fact_bin_cuad2_proc(title,name,nlits,deg,max_coef,min_exp,exp_neg,coef):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    mon = rand_mon_comp(lits[0],deg,min_exp,exp_neg,coef)    
    f = mon+rand_sign()*randint(1,max_coef)    
        
    #escoge un par de valores    
    e = expand(f**2)
    ef = factor(f**2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return d
    
    
def fact_bin_conj(title,name,nlits,deg,max_coef,min_exp,exp_neg,coef):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    mon = rand_mon_comp(lits[0],deg,min_exp,exp_neg,coef)    
    oth = rand_sign()*randint(1,max_coef)
    f1 = mon+oth    
    f2 = mon-oth
        
    #escoge un par de valores    
    expresion = expand(f1*f2)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'    
    
    fctf2 = dif_fact_bin_conj(mon,[expresion],max_coef)
    prf2 = fctf2[0]*fctf2[1]
    fctf3 = dif_fact_bin_conj(mon,[expresion,prf2],max_coef)
    prf3 = fctf3[0]*fctf3[1]
    fctf4 = dif_fact_bin_conj(mon,[expresion,prf2,prf3],max_coef)
    
    res1 = '$'+latex(factor(expresion))+'$'
    res2 = '$'+latex(factor(expand(fctf2[0]*fctf2[1])))+'$'
    res3 = '$'+latex(factor(expand(fctf3[0]*fctf3[1])))+'$'
    res4 = '$'+latex(factor(expand(fctf4[0]*fctf4[1])))+'$'
    
    '''
    res1 = '$\\left(' + latex(f1)+'\\right)\\left('+latex(f2)+'\\right) $'
    res2 = '$\\left(' + latex(fctf2[0])+'\\right)\\left('+latex(fctf2[1])+'\\right) $'
    res3 = '$\\left(' + latex(fctf3[0])+'\\right)\\left('+latex(fctf3[1])+'\\right) $'
    res4 = '$\\left(' + latex(fctf4[0])+'\\right)\\left('+latex(fctf4[1])+'\\right) $'
    '''
       
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    
    
def fact_bin_conj_proc(title,name,nlits,deg,max_coef,min_exp,exp_neg,coef):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)        
    
    i = 0
    found = False
    while i < 10 and not found:
        mon = rand_mon_comp(lits[0],deg,min_exp,exp_neg,coef)    
        oth = rand_sign()*randint(1,max_coef)
        f1 = mon+oth    
        f2 = mon-oth        
        #escoge un par de valores    
        e = expand(f1*f2)
        ef = factor(e)
        e_trms = e.as_ordered_terms()
        if len(e_trms) > 1:
            found = True
        i = i+1
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name, 'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return d
    
def dif_sim_poly(f2,refs):   
    f2_terms = poly2terms(f2)    
    ind = randint(0,len(f2_terms)-1) 
    nt = modifica_mon(f2_terms[ind])
    f2_terms[ind] = nt
    res = terms2poly(f2_terms)    
    i = 1
    
    while res in refs and i < 100:
        f2_terms = poly2terms(f2)            
        ind = randint(0,len(f2_terms)-1) 
        nt = modifica_mon(f2_terms[ind])
        f2_terms[ind] = nt
        res = terms2poly(f2_terms)
        i = i+1
        
    return res
    
def fact_dif_cub(title="",name="",nlits=2,deg=2,min_exp=1,exp_neg=False,coef=True):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)
    
    mon1 = rand_mon_comp(lits[0],deg,min_exp,exp_neg,False)    
    mon2 = dif_rand_mon_comp(lits[0],[mon1],deg,min_exp,exp_neg,False)    
    
    if coef:
        mon1 = mon1*randint(1,3)
        mon2 = mon2*randint(1,3)
    
    mon1_3 = mon1**3
    mon2_3 = mon2**3
    
    mon_com = gcd(mon1,mon2)
    
    expresion = mon1_3-mon2_3
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(expresion)+'$$'
    
    mon1 = mon1/mon_com
    mon2 = mon2/mon_com
        
    f1 = mon1-mon2
    f2 = mon1**2+mon1*mon2+mon2**2
    
    rf2 = [mon1-mon2,dif_sim_poly(f2,[f2])]
    rf3 = [mon1-mon2,dif_sim_poly(f2,[f2,rf2[1]])]
    rf4 = [mon1-mon2,dif_sim_poly(f2,[f2,rf2[1],rf3[1]])]
    
    ltx_mon = "" if mon_com == 1 else latex(mon_com**3)     
     
    res1 = '$'+ltx_mon+'\\left(' + latex(f1)+'\\right)\\left('+latex(f2)+'\\right) $'
    res2 = '$'+ltx_mon+'\\left(' + latex(rf2[0])+'\\right)\\left('+latex(rf2[1])+'\\right) $'
    res3 = '$'+ltx_mon+'\\left(' + latex(rf3[0])+'\\right)\\left('+latex(rf3[1])+'\\right) $'
    res4 = '$'+ltx_mon+'\\left(' + latex(rf4[0])+'\\right)\\left('+latex(rf4[1])+'\\right) $'    
    
    resps = []
    sol = res1
    resps.append(res1)
    resps.append(res2)
    resps.append(res3)
    resps.append(res4)
            
    ex = optionsExercise(preg,sol,resps,name)
    return ex    

def fact_dif_cub_proc(title,name,nlits,deg,min_exp,exp_neg,coef):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)
    
    mon1 = rand_mon_comp(lits[0],deg,min_exp,exp_neg,False)    
    mon2 = dif_rand_mon_comp(lits[0],[mon1],deg,min_exp,exp_neg,False)    
    
    if coef:
        mon1 = mon1*randint(1,3)
        mon2 = mon2*randint(1,3)
    
    mon1_3 = mon1**3
    mon2_3 = mon2**3
    
    e = mon1_3-mon2_3 #problema matemático (expresión a factorizar)
    ef = factor(e) #solución (expresión algebraica factorizada)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name, 'symbs':[str(s) for s in lits[0]], 'e':e, 'ef':ef}
    return d

def rand_bin_cuad(lits,n_w):
    
    #multiplica todas las literales
    t1 = 1
    for l in lits[0]:
        t1 = t1*l**randint(0,2)
    
    t2 = 1
    for l in lits[0]:
        t2 = t2*l**randint(0,2)
    
    t1 = t1*rand_sign()*randint(1,n_w)
    t2 = t2*rand_sign()*randint(1,n_w)
        
    #escoge un par de valores
    i = 0    
    e = expand((t1+t2)**2)    
    eot = e.as_ordered_terms()
    while len(eot) == 1 and i < 10:
        #multiplica todas las literales
        t1 = 1
        for l in lits[0]:
            t1 = t1*l**randint(0,2)
        
        t2 = 1
        for l in lits[0]:
            t2 = t2*l**randint(0,2)
        
        t1 = t1*rand_sign()*randint(1,n_w)
        t2 = t2*rand_sign()*randint(1,n_w)
            
        #escoge un par de valores
            
        e = expand((t1+t2)**2)
        
        eot = e.as_ordered_terms()
        i = i+1
        
    ef = factor((t1+t2)**2)
    
    d = {'e':e,'ef':ef}
    return d
    
    
def rand_bin_conj(lits,deg,max_coef,min_exp,exp_neg,coef):
    
    i = 0
    found = False
    while i < 10 and not found:
        mon = rand_mon_comp(lits[0],deg,min_exp,exp_neg,coef)    
        oth = rand_sign()*randint(1,max_coef)
        f1 = mon+oth    
        f2 = mon-oth        
        #escoge un par de valores    
        e = expand(f1*f2)
        ef = factor(e)
        e_trms = e.as_ordered_terms()
        if len(e_trms) > 1:
            found = True
        i = i+1
    
    return {'e':e,'ef':ef}
    
    
def genera_lits(nlits):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    return sample(lits_s,1)
    
def rand_prod_bins(lits,norm=True):
    #multiplica todas las literales
    pr = 1
    for l in lits[0]:
        pr = pr*l**randint(1,2)
    
    f1 = rand_poly(pr,1,5,norm)
    f2 = rand_poly(pr,1,5,True)
    
    e = expand(f1*f2)
    ef = factor(e)
    
    d = {'e':e, 'ef':ef}
    return d
    
def rand_monomio_poly(lits,nterms,deg):    
    coef = True
    f1 = rand_mon_comp(lits[0],deg,1,False,coef)
    
    f2 = 0
    f2_terms = []
    nm = randint(2,nterms)
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,False,coef)
        f2_terms.append(m)        
        f2 = f2+m        
        
    e = expand(f1*f2) 
    ef = factor(e)
    d = {'e':e, 'ef':ef}
    return d
    
def fact_bin_cub_proc(title,name,nlits,deg,n_w):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    lits = sample(lits_s,1)
    
    #multiplica todas las literales
    t1 = 1
    for l in lits[0]:
        t1 = t1*l**randint(0,deg)
    
    t2 = 1
    for l in lits[0]:
        t2 = t2*l**randint(0,deg)
    
    t1 = t1*rand_sign()*randint(1,n_w)
    t2 = t2*rand_sign()*randint(1,n_w)
        
    #escoge un par de valores
    i = 0    
    e = expand((t1+t2)**3)    
    eot = e.as_ordered_terms()
    while len(eot) == 1 and i < 10:
        #multiplica todas las literales
        t1 = 1
        for l in lits[0]:
            t1 = t1*l**randint(0,deg)
        
        t2 = 1
        for l in lits[0]:
            t2 = t2*l**randint(0,deg)
        
        t1 = t1*rand_sign()*randint(1,n_w)
        t2 = t2*rand_sign()*randint(1,n_w)
            
        #escoge un par de valores
            
        e = expand((t1+t2)**3)
        
        eot = e.as_ordered_terms()
        i = i+1
        
    ef = factor((t1+t2)**3)
    
    preg = 'Factoriza la siguiente expresión: $$' + latex(e)+'$$'    
    
    d = {'title':title,'preg':preg,'name':name,'symbs':[str(s) for s in lits[0]],'e':e,'ef':ef}
    return d    
    

def mix_fact():

    opcs = ['bin_conj','bin_cuad','prod_bin','mon_poly']    
    
    t1 = sample(opcs,1)
    t2 = sample(opcs,1)
    
    t1 = t1[0]
    t2 = t2[0]
        
    #genera un problema de binomios conjugados        
    nlits = 2
    deg = 2 
    lits = genera_lits(nlits)
    
    if t1 == 'bin_conj':
        d1 = rand_bin_conj(lits,deg,5,0,0,4)
    elif t1 == 'bin_cuad':
        d1 = rand_bin_cuad(lits,5)
    elif t1 == 'prod_bin':
        d1 = rand_prod_bins(lits,True)
    else:
        d1 = rand_monomio_poly(lits,2,2) #monomio por binomios cuadráticos
        
    if t2 == 'bin_conj':
        d2 = rand_bin_conj(lits,deg,5,0,0,4)
    elif t2 == 'bin_cuad':
        d2 = rand_bin_cuad(lits,5)
    elif t2 == 'prod_bin':
        d2 = rand_prod_bins(lits,True)
    else:
        d2 = rand_monomio_poly(lits,2,2)
        
    e = expand(d1['e']*d2['e'])
    ef = factor(e)
    
    return {'e':e, 'ef':ef, 'lits':lits}
    
def mix_fact_2():

    opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']
    
    t1 = sample(opcs,1)
    t2 = sample(opcs,1)
    
    t1 = t1[0]
    t2 = t2[0]
        
    #genera un problema de binomios conjugados        
    #nlits = sample([1,2,3],1)[0]
    nlits = 3    
    deg = sample([2,3,4],1)[0] 
    lits = genera_lits(nlits)
    max_coef = randint(2,5)
    min_exp = randint(1,3)
    n_terms = randint(2,4)
    if min_exp >= deg:
        deg = min_exp+randint(2,3)
    
    if t1 == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d1 = e['e']
    elif t1 == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d1 = e['e']
    elif t1 == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d1 = e['e']
    elif t1 == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d1 = e['e']        
    elif t1 == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d1 = e['e']            
    elif t1 == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d1 = e['e']                    
    elif t1 == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d1 = e['e']
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d1 = e['e']                    
        
    if t2 == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d2 = e['e']
    elif t2 == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d2 = e['e']
    elif t2 == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d2 = e['e']
    elif t2 == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d2 = e['e']        
    elif t2 == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d2 = e['e']            
    elif t2 == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d2 = e['e']
    elif t2 == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d2 = e['e']                    
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d2 = e['e']
        
    #symbs = e['symbs']
    e = expand(d1*d2)
    ef = factor(e)   
    
    preg = 'Factoriza la siguiente expresión: $$'+ latex(e)+'$$'
    
    #return {'e':e, 'ef':ef, 'lits':lits, 'symbs':[str(s) for s in lits[0]]}
    d = {'title':'', 'preg':preg, 'name':'', 'symbs':['a','b','c','x','y','z'], 'e':e, 'ef':ef}
    return procedureFactor(d)
    
    
def mix_fact_1():

    #opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']
    opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin']
    
    t2 = sample(opcs,1)
    
    t2 = t2[0]
        
    #genera un problema de binomios conjugados        
    #nlits = sample([1,2,3],1)[0]
    nlits = 3    
    deg = sample([2,3,4],1)[0] 
    lits = genera_lits(nlits)
    max_coef = randint(2,5)
    min_exp = randint(1,3)
    n_terms = randint(2,4)
    if min_exp >= deg:
        deg = min_exp+randint(2,3)
    
    d1 = rand_mon_comp(lits[0],deg,1,False,max_coef)
            
    if t2 == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d2 = e['e']
    elif t2 == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d2 = e['e']
    elif t2 == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d2 = e['e']
    elif t2 == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d2 = e['e']        
    elif t2 == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d2 = e['e']            
    elif t2 == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d2 = e['e']
    elif t2 == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d2 = e['e']                    
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d2 = e['e']
    
    #symbs = e['symbs']
    e = expand(d1*d2)
    ef = factor(e)   
    
    preg = 'Factoriza la siguiente expresión: $$'+ latex(e)+'$$'
    
    d = {'title':'', 'preg':preg, 'name':'', 'symbs':['a','b','c','x','y','z'], 'e':e, 'ef':ef}
    return procedureFactor(d)
    
    
def rand_fact(t=None,nlits=3):
    opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']
    if not t:
        t = sample(opcs,1)
        t = t[0]        
    #genera un problema de binomios conjugados        
    #nlits = sample([1,2,3],1)[0]
    deg = sample([2,3,4],1)[0] 
    lits = genera_lits(nlits)
    max_coef = randint(2,5)
    min_exp = randint(1,3)
    n_terms = randint(2,4)
    if min_exp >= deg:
        deg = min_exp+randint(2,3)
            
    if t == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d = e['e']
    elif t == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d = e['e']
    elif t == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d = e['e']
    elif t == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d = e['e']        
    elif t == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d = e['e']            
    elif t == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d = e['e']
    elif t == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d = e['e']                    
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d = e['e']
        
    symbs = e['symbs']
    e = expand(d)
    ef = factor(e)
    
    preg = 'Factoriza la siguiente expresión: $$'+ latex(e)+'$$'
    
    #return {'e':e, 'ef':ef, 'lits':lits, 'symbs':[str(s) for s in lits[0]]}
    d = {'title':'', 'preg':preg, 'name':'', 'symbs':symbs, 'e':e, 'ef':ef}
    return procedureFactor(d)
    
#posibles valores de t
#opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']
'''
def selecc_fact(t):    
    nlits = 3    
    deg = sample([2,3,4],1)[0] 
    lits = genera_lits(nlits)
    max_coef = randint(2,5)
    min_exp = randint(1,3)
    n_terms = randint(2,4)
    if min_exp >= deg:
        deg = min_exp+randint(2,3)
            
    if t == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d = e['e']
    elif t == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d = e['e']
    elif t == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d = e['e']
    elif t == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d = e['e']        
    elif t == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d = e['e']            
    elif t == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d = e['e']
    elif t == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d = e['e']                    
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d = e['e']
        
    e = expand(d)
    ef = factor(e)
    
    preg = 'Factoriza la siguiente expresión: $$'+ latex(e)+'$$'
    
    symbs = [str(s) for s in lits[0]]    
    d = {'title':'', 'preg':preg, 'name':'', 'symbs':symbs, 'e':e, 'ef':ef}
    return procedureFactor(d_ext=d)
'''
    
def mix_fact_proc(title,name):
    dm = mix_fact()
    preg = 'Factoriza la siguiente expresión: $$' + latex(expand(dm['e']))+'$$'    
    d = {'title':title,'preg':preg,'name':name, 'symbs':[str(s) for s in dm['lits'][0]], 'e':dm['e'], 'ef':dm['ef']}
    return d
    
def propiedad_dist(rat=False):
    symbs = symbols('a,b,c,x,y,z')
    s = sample(symbs,1)[0]
    if not rat:            
        par = randint(2,9)*rand_sign()*s+randint(2,9)*rand_sign()
        a = randint(2,9)*rand_sign()
    else:
        cx = rand_rat() if random()>0.3 else randint(2,9)*rand_sign()
        cte = rand_rat() if random()>0.3 else randint(2,9)*rand_sign()        
        a = rand_rat() if random()>0.3 else randint(2,9)*rand_sign()
        par = cx*s+cte
    preg = "Aplica la propiedad distributiva para desarrollar la siguiente multiplicación $$" + latex(a) + "\\left("+latex(par)+'\\right)$$'
    
    sol = latex(expand(a*par))
    
    symbs = [latex(s)]
    
    return procedurePolinomio(preg,sol,symbs)

def mix_prod_not(nlits):
    lits = gen_lits(nlits)
    opcs  = ['prod_monomio_poly_proc(2,2,3,lits=lits)', 'prod_polinomios_proc(2,3,3,lits=lits)', 'bin_conj_proc(2,2,lits=lits)', 'bin_cuad_proc(2,2,lits=lits)', 'trin_cuad_proc(2,2,lits=lits)', 'bin_cub_proc(2,2,lits=lits)']
    prods = sample(opcs,2)
    p1 = eval(prods[0])
    p2 = eval(prods[1])
    
    d1 = p1.getData()
    d2 = p2.getData()
    
    pol1 = ltxToE(p1.getLtxMathProblem(), d1['dataToAssess']['symbs'])
    pol2 = ltxToE(p2.getLtxMathProblem(), d2['dataToAssess']['symbs'])
    
    p = pol1*pol2
    ltx_prob = latex(p)
    
    preg = "Desarrolla el siguiente producto: $$" + ltx_prob + "$$"
    
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    ep = expand(p)
    d['e'] = ep
    d['ef'] = ep
    d['ltx_math_prob'] = ltx_prob 
    ex = procedureProdNot(d)
    return ex 

def mix_prod_not_optns():
    if random() < 0.33:
        e = bin_cuad()
    elif random() < 0.5:
        e = trin_cuad()
    else:
        e = bin_cub_optns(nlits=3,deg=3,lits=None)
    return e
    
def gen_lits(nlits):
    #genera las literales
    [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
    if nlits == 1:
        lits_s = [[a],[b],[c],[x],[y],[z]]
    elif nlits == 2:
        lits_s = [[a,b],[x,y]]
    else:
        lits_s = [[a,b,c],[x,y,z]]
        
    return sample(lits_s,1)

def bin_cub_optns(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f = 0    
    nm = randint(2,2) #binomios
    f_terms = []
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f_terms,deg,0,False,coef)
        f_terms.append(m)
        f = f+m
        
    ltx_prob = '\\left(' + latex(f) + '\\right)^3'
    preg = 'Desarrolla el siguiente producto notable: $$'+ ltx_prob+'$$'
    
    res = expand(f**3)
    
    resp = []
    resp.append('$'+latex(res)+'$')
    rf = f_terms[0]**3+3*f_terms[0]**2*f_terms[1]+3*f_terms[0]*f_terms[1]**2+f_terms[1]**3
    if rf.equals(res):
        rf = f_terms[0]**3-3*f_terms[0]**2*f_terms[1]+3*f_terms[0]*f_terms[1]**2-f_terms[1]**3
    resp.append('$'+latex(rf)+'$')
    
    rf = f_terms[0]**3+f_terms[0]**2*f_terms[1]+f_terms[0]*f_terms[1]**2+f_terms[1]**3
    resp.append('$'+latex(rf)+'$')
    
    rf = f_terms[0]**3-f_terms[0]**2*f_terms[1]+f_terms[0]*f_terms[1]**2-f_terms[1]**3
    resp.append('$'+latex(rf)+'$')
    
    rf = f_terms[0]**3-2*f_terms[0]**2*f_terms[1]+2*f_terms[0]*f_terms[1]**2-f_terms[1]**3
    resp.append('$'+latex(rf)+'$')
    
    ex = optionsExercise(preg,resp[0],resp,"")    
    return ex  

def prod_bins_gral_proc(nlits,deg,lits=None):
    if not lits:
        #genera las literales
        [a,b,c,x,y,z] = symbols('a,b,c,x,y,z')
        if nlits == 1:
            lits_s = [[a],[b],[c],[x],[y],[z]]
        elif nlits == 2:
            lits_s = [[a,b],[x,y]]
        else:
            lits_s = [[a,b,c],[x,y,z]]
            
        lits = sample(lits_s,1)     
    
    coef = True
    
    f1 = 0
    f1_terms = []
    nm = 2
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f1_terms,deg,0,False,coef)
        f1_terms.append(m)        
        f1 = f1+m
        
    f2 = 0
    f2_terms = []
    nm = 2
    for i in range(nm):
        m = dif_rand_mon_comp(lits[0],f2_terms,deg,0,False,coef)
        f2_terms.append(m)        
        f2 = f2+m
        
    ot1 = f1.as_ordered_terms()
    ot2 = f2.as_ordered_terms()
    
    dev1 = ''
    prods = []
    for i,t in enumerate(ot1):
        dev1 += '\\left('+latex(t)+'\\right)\\left('+latex(f2)+'\\right)+'
        e = expand(t*f2)
        prods.append(e)        
    dev1 = dev1[:-1]
        
    dev2 = ''
    pol = {}
    for p in prods:
        dev2 += '\\left('+latex(p)+'\\right)+'
        pt = p.as_ordered_terms()
        for t in pt:
            tc = t.as_coeff_Mul()
            if not tc[1] in pol.keys():
                pol[tc[1]] = [t]
            else:        
                pol[tc[1]].append(t)
    dev2 = dev2[:-1]
        
    preg = 'Desarrolla el siguiente producto notable: $$\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right) $$'  
    
    res = expand(f1*f2)    
    ltx_math_prob = '\\left(' + latex(f1) + '\\right) \\left(' + latex(f2) + '\\right)'
    
    dev3 = ''
    res_ot = res.as_ordered_terms() 
    for t in res_ot:
        tm = t.as_coeff_Mul()        
        tg = pol[tm[1]]
        if len(tg)>1:
            if dev3 != '':
                dev3 += '+\\left('
            else:
                dev3 += '\\left('
            for i,tr in enumerate(tg):            
                if i == 0:
                    s = ''
                else:
                    tm = tr.as_coeff_Mul()
                    s = '' if tm[0] < 0 else '+'                             
                dev3 += s+latex(tr)
            dev3+='\\right)'
        else: #un solo término
            if dev3 != '':
                s = '' if tm[0] < 0 else '+'
            else:
                s = ''                
            dev3 += s+latex(tg[0])
            
    if dev3[-1] == '+':
        dev3 = dev3[:-1]
    
    proc = '\\begin{align}'
    proc += '\\color{red}{'+ltx_math_prob +'}&= ' +dev1+'\\\\'
    proc += '&= ' +dev2+'\\\\'
    proc += '&= ' +dev3+'\\\\'
    proc += '&= \\color{blue}{' +latex(res)+'}\\\\'
    proc += '\\end{align}'
    
    #genera un ejercicio del tipo procedimiento
    d = {}
    d['symbs'] = []
    for l in lits[0]:
        d['symbs'].append(str(l))
    d['preg'] = preg
    d['e'] = res
    d['ef'] = res
    d['ltx_math_prob'] = ltx_math_prob
    d['proc'] = proc
    ex = procedureProdNot(d)
    return ex



    
#posibles valores de t
opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']

def fact_select_proc(t=None):

    if t == None:
        opcs = ['mon_poly','bin_conj','bin_cuad','prod_bin','bin_cub','dif_cub', 'trin_cuad']
        t = sample(opcs,1)[0]
    
    #t1 = sample(opcs,1)
    #t2 = sample(opcs,1)
    
    #t1 = t1[0]
    #t2 = t2[0]
        
    #genera un problema de binomios conjugados        
    nlits = sample([1,2,3],1)[0]
    nlits = 3    
    deg = sample([2,3,4],1)[0] 
    lits = genera_lits(nlits)
    max_coef = randint(2,5)
    min_exp = randint(1,3)
    n_terms = randint(2,4)
    if min_exp >= deg:
        deg = min_exp+randint(2,3)
    
    if t == 'bin_conj':
        e = fact_bin_conj_proc('','',nlits,deg,max_coef,min_exp,False,True)
        d1 = e['e']
    elif t == 'bin_cuad':
        e = fact_bin_cuad_proc('','',nlits,max_coef)
        d1 = e['e']
    elif t == 'prod_bin':        
        e = fact_prod_bins_proc('','',nlits,True)
        d1 = e['e']
    elif t == 'prod_bin2':
        e = fact_prod_bins2_proc('','',nlits,randint(2,4))
        d1 = e['e']        
    elif t == 'bin_cub':
        e = fact_bin_cub_proc('','',nlits,deg,max_coef)
        d1 = e['e']            
    elif t == 'dif_cub':
        e = fact_dif_cub_proc('','',nlits,deg,min_exp,False,True)
        d1 = e['e']                    
    elif t == 'trin_cuad':
        e = fact_trin_cuad_proc('','',nlits,max_coef)
        d1 = e['e']
    else:
        e = fact_prod_monomio_poly_proc('','',nlits,n_terms,deg)
        d1 = e['e']                    
        
    #symbs = e['symbs']
    e = expand(d1)
    ef = factor(e)   
    
    preg = 'Factoriza la siguiente expresión: $$'+ latex(e)+'$$'
    
    #return {'e':e, 'ef':ef, 'lits':lits, 'symbs':[str(s) for s in lits[0]]}
    d = {'title':'', 'preg':preg, 'name':'', 'symbs':['a','b','c','x','y','z'], 'e':e, 'ef':ef}
    return procedureFactor(d)


if __name__ == "__main__":
    #e = fact_prod_bins2_optns()
    #e = fact_bin_cuad()
    #e = fact_dif_cub()
    #e = trin_cuad()
    #e = bin_cub_optns(nlits=3,deg=3,lits=None)        
    #e = prod_monomio_poly()
    #['mon_poly','bin_conj','bin_cuad','prod_bin','prod_bin2','bin_cub','dif_cub', 'trin_cuad']
    e = fact_select_proc('mon_poly')
    data = e.getData()

    for s in data['procedure']:
        print(s)
    #print e.getQuestion()
    #print e.getData()["dataToAssess"]['ans']
    #for r in e.getResps():
    #    print ""
    #    print r


