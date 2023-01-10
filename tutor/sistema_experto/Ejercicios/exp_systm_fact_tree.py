# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:19:30 2015

@author: fernando
"""

from tutor.sistema_experto.LatexProc.Cadenas import factores3, ajusta_cad_latex, str2expr, ltx_terminos3, valida_ltx
from sympy import Rational, gcd, sqrt, integer_nthroot, latex, symbols, factorint
from copy import copy
import operator
from tutor.sistema_experto.Assess.ComplejosAssess import ltxToE

class polinomio(object):
    def __init__(self, **kwargs): #kwargs es un diccionario con los argumentos necesarios para la función
        if 'pol_ltx' in kwargs.keys(): #se construye el polinomio a partir de una cadena de latex
            pol_ltx = kwargs['pol_ltx']
            symbs = kwargs['symbs']
            self.latex = pol_ltx
            self.symbs = symbs
            self.trms_fact = self.extrae_terms_fact()            
            self.ntrms = len(self.trms_fact)
            self.trms = [self.extrae_termino(i) for i in range(self.ntrms)]
        elif 'pol' in kwargs.keys(): #el polinomio es una expresión de sympy
            pol = kwargs['pol']            
            self.latex = latex(pol)
            self.symbs = kwargs['symbs']
            if not type(pol) in [int]:
                self.trms = pol.as_ordered_terms()
            else:
                self.trms = [pol]
            self.ntrms = len(self.trms)
            #separa los factores de cada término del polinomio
            self.trms_fact = []
            for t in self.trms:
                #factoriza el término
                fcts = t.as_ordered_factors()
                #averigua si la lista de factores tiene un coeficiente negativo
                if fcts[0] == -1 and len(fcts) > 1:
                    fcts[1] = -fcts[1]
                    fcts = fcts[1:]
                d = []
                for f in fcts:
                    fd = {}
                    fd['c'] = f
                    fd['in_num'] = True
                    d.append(fd)
                self.trms_fact.append(d)
                
    def getPoly(self):
        res = 0
        for t in self.trms:
            res = res+t
        return res 
        
    def getSize(self):
        return self.ntrms
        
    #indica si el término i-ésimo es un cuadrado
    def esCuadrado(self, i, coef):
        num_types = [type(Rational(1,2)), type(Rational(3,2)), type(1), type(Rational(1,1)), type(Rational(2,1))]
                    
        ap = False
            
        for f in self.trms_fact[i]: #cada factor debe ser un cuadrado perfecto
            if not ap:
                v = coef*f['c']
                ap = True
            else:
                v = f['c']
            if type(v) in num_types: #es un racional o entero
                sq = sqrt(v)
                if not type(sq) in num_types:
                    return False
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                if v_be[1]%2 != 0:
                    return False
        return True

    #indica si el término i-ésimo es un cubo
    def esCubo(self, i, coef):
        rat_types = [type(Rational(1,2)), type(Rational(3,2)), type(Rational(1,1)), type(Rational(2,1))]
        int_types = [type(1)]
                    
        ap = False
            
        for f in self.trms_fact[i]: #cada factor debe ser un cubo
            if not ap:
                v = coef*f['c']
                ap = True
            else:
                v = f['c']
            
            if type(v) in rat_types: #si el coeficiente es un racional o entero
                vp = v.p #se supone que cada uno es un entero
                vq = v.q
                sp = integer_nthroot(vp,3)
                sq = integer_nthroot(vq,3)
                if not sp[1] or not sq[1]:
                    return False
            elif type(v) in int_types:
                rv = integer_nthroot(v,3)
                if not rv[1]:
                    return False                                
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                if v_be[1]%3 != 0:
                    return False
        return True
        
    #indica si el término i-ésimo es un cubo
    def esCuboTrm(self, t, coef):
        rat_types = [type(Rational(1,2)), type(Rational(3,2)), type(Rational(1,1)), type(Rational(2,1))]
        int_types = [type(1)]
        
        if type(t) in rat_types:
            vp = coef*t.p #se supone que cada uno es un entero
            vq = t.q
            if vp >= 0:
                sp = integer_nthroot(vp,3)
            else:
                sp = integer_nthroot(-vp,3)                
            if vq >= 0:
                sq = integer_nthroot(vq,3)
            else:
                sq = integer_nthroot(-vq,3)                
            if not sp[1] or not sq[1]:
                return False
            else:
                return True
        elif type(t) in int_types:
            vp = coef*t #se supone que cada uno es un entero
            if vp >= 0:
                sp = integer_nthroot(vp,3)
            else:
                sp = integer_nthroot(-vp,3)                
            if not sp[1]:
                return False
            else:
                return True
                                            
        ap = False
                
        fcts = t.as_ordered_factors()
            
        for f in fcts: #cada factor debe ser un cubo
            if not ap:
                v = coef*f
                ap = True
            else:
                v = f
            
            if type(v) in rat_types: #si el coeficiente es un racional o entero
                vp = v.p #se supone que cada uno es un entero
                vq = v.q
                if vp >= 0:
                    sp = integer_nthroot(vp,3)
                else:
                    sp = integer_nthroot(-vp,3)                
                if vq >= 0:
                    sq = integer_nthroot(vq,3)
                else:
                    sq = integer_nthroot(-vq,3)
                if not sp[1] or not sq[1]:
                    return False                
            elif type(v) in int_types:
                if v >= 0:
                    sp = integer_nthroot(vp,3)
                else:
                    sp = integer_nthroot(-vp,3)                
                if not sp[1]:
                    return False                                    
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                if v_be[1]%3 != 0:
                    return False
        return True
    
    #raíz cuadrada del término i-ésimo
    def t_sqrt(self,i,coef):
        num_types = [type(0.1), type(Rational(1,2)), type(Rational(3,2)), type(1), type(Rational(1,1)), type(Rational(2,1))]
        res = 1
        ap = False
        for f in self.trms_fact[i]: #cada factor debe ser un cuadrado perfecto
            if not ap:
                v = coef*f['c']
                ap = True
            else:
                v = f['c']
            if type(v) in num_types: #es un racional o entero
                sq = sqrt(v)
                if f['in_num']:
                    res = res*sq
                else:
                    res = res*Rational(1,sq)
                
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                res = res*v_be[0]**Rational(v_be[1],2)
        return res
        
    #raíz cúbica del término i-ésimo
    def t_cubic_rooth(self,i,coef):
        rat_types = [type(Rational(1,2)), type(Rational(3,2)), type(Rational(1,1))]
        int_types = [type(1), type(Rational(2,1))]
        
        res = 1
        ap = False
        for f in self.trms_fact[i]: #cada factor debe ser un cuadrado perfecto
            if not ap:
                v = coef*f['c']
                ap = True
            else:
                v = f['c']
            if type(v) in rat_types: #es un racional
                rn = integer_nthroot(v.p,3) 
                rd = integer_nthroot(v.q,3)
                if not (rn[1] and rd[1]):
                    return False
                                
                r = Rational(rn[0],rd[0])
                if f['in_num']:
                    res = res*r
                else:
                    res = res/r
            elif type(v) in int_types:
                r = integer_nthroot(v,3)
                if f['in_num']:
                    res = res*r[0]
                else:
                    res = res/r[0]                                
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                res = res*v_be[0]**Rational(v_be[1],3)
        return res
        
    #raíz cúbica del término i-ésimo
    def t_cubic_roothTrm(self,t,coef):
        rat_types = [type(Rational(1,2)), type(Rational(3,2)), type(Rational(1,1))]
        int_types = [type(1), type(Rational(2,1))]
        
        if type(t) in rat_types:
            vp = coef*t.p #se supone que cada uno es un entero
            vq = t.q
            if vp >= 0:
                sp = integer_nthroot(vp,3)
            else:
                sp = integer_nthroot(-vp,3)                
            if vq >= 0:
                sq = integer_nthroot(vq,3)                
            else:
                sq = integer_nthroot(-vq,3)                
            if not sp[1] or not sq[1]:
                return False
            else:
                if (vp >= 0 and vq >= 0) or (vp < 0 and vq < 0):
                    return Rational(sp[0],sq[0])
                else:
                    return Rational(-sp[0],sq[0])
                
        elif type(t) in int_types:
            vp = coef*t #se supone que cada uno es un entero
            if vp >= 0:
                sp = integer_nthroot(vp,3)
            else:
                sp = integer_nthroot(-vp,3)
            if not sp[1]:
                return False
            else:
                if vp >= 0:
                    return sp[0]
                else:
                    return -sp[0]

        fcts = t.as_ordered_factors()        
        
        res = 1
        ap = False
        for f in fcts: #cada factor debe ser un cubo perfecto
            if not ap:
                v = coef*f
                ap = True
            else:
                v = f
            if type(v) in rat_types: #es un racional
                rn = integer_nthroot(v.p,3) 
                rd = integer_nthroot(v.q,3)
                
                if not rn[1] or not rd[1]:
                    return False
                    
                r = Rational(rn[0],rd[0])
                res = res*r                
            elif type(v) in int_types:
                r = integer_nthroot(v,3)
                if not r[1]:
                    return False                
                res = res*r[0]                
            else:#debe ser una expresión
                v_be = v.as_base_exp()
                res = res*v_be[0]**Rational(v_be[1],3)
        return res
    
    def getTerm(self,i):
        if i >= 0 and i < self.ntrms:
            return self.trms[i]
        else:
            return 0
    
    #extrae cada término y cada factor de cada término 
    def extrae_terms_fact(self):
        ltx_v = valida_ltx(self.latex, self.symbs, [])
        ltx_ajst = ajusta_cad_latex(ltx_v['cad'],self.symbs)
        trms = ltx_terminos3(ltx_ajst,self.symbs)
        
        res = []
        
        for t in trms:
            f = factores3(t,True)
            for e in f: 
                e['c'] = str2expr(e['c'],self.symbs)
            res.append(f)
        return res
        
    def extrae_termino(self, i):
        #produce el término completo
        t = self.trms_fact[i]
        t_exp = 1
        for e in t:
            if e['in_num']:
                t_exp = t_exp*e['c']
            else:
                if type(t_exp) == type(1) and type(t_exp) == type(e['c']):
                    t_exp = Rational(t_exp,e['c'])
                else:
                    t_exp = t_exp/e['c']
        return t_exp
        
    #averigua el máximo común divisor del polinomio
    def factor_comun(self):
        r_types = [type(Rational(3,2)), type(Rational(1,2))]
        n_types = [type(1), type(0.1)]
        
        #extrae el máximo común divisor de todos los términos     
        for i,t_exp in enumerate(self.trms):
            if not type(t_exp) in n_types:             
                [coef,t_exp] = t_exp.as_coeff_Mul()
            else:
                coef = t_exp
                t_exp = 1
            
            if i == 0:
                mcd = t_exp
                if type(coef) in r_types:
                    mcd_num = coef.p
                    mcd_den = coef.q
                else:
                    mcd_num = coef
                    mcd_den = 1
            
            else:
                mcd = gcd(mcd,t_exp)
                #extrae el coeficiente de la expresión
                if type(coef) in r_types:
                    n_coef = coef.p
                    d_coef = coef.q
                else:
                    n_coef = coef
                    d_coef = 1
                
                mcd_num = gcd(mcd_num,n_coef)
                mcd_den = gcd(mcd_den,d_coef)
                
        return Rational(mcd_num,mcd_den)*mcd
        
        
###################################################
#        Sistema experto para factorizar polinomios
###################################################
        
class explica_fact(object):        
    def __init__(self,ltx_prob = ''): #kwargs es un diccionario con los argumentos necesarios para la función
        self.explic = []
        self.ltx_prob = ltx_prob
        
    def factoriza(self, poly, symbs, ind_pat):
        #busca factorizar el polinomio aplicando diferentes reglas
    
        if len(self.explic) == 0: #inicia el nodo raíz
            nod = {'val':latex(poly), 'ind':0, 'ind_pat':None, 'type':'root'}
            self.explic.append(nod)
            ind_pat = 0
        
        fc = self.fact_mon_comun(poly,symbs) #monomio común (máximo común divisor)
        if fc != poly:
            
            ind1 = len(self.explic)            
            n1 = {'val':latex(fc[0]),'ind':ind1,'ind_pat':ind_pat,'type':'fc','nf':1}
            self.explic.append(n1)
            
            ind2 = ind1+1
            n2 = {'val':'\\left(' + latex(fc[1])+'\\right)','ind':ind2,'ind_pat':ind_pat,'type':'fc','nf':2}
            self.explic.append(n2)            
            
            #actualiza la información del padre
            #ahora tiene dos hijos
            pat = self.explic[ind_pat]
            pat['h1'] = ind1
            pat['h2'] = ind2
                
            f = self.factoriza(fc[1],symbs,ind2)
            
            return fc[0]*f
        else:
            fc = self.fact_bin_cuad(poly,symbs) #binomios al cuadrado
            if fc != poly:                
                ind = len(self.explic)            
                n = {'val':latex(fc),'ind':ind,'ind_pat':ind_pat,'type':'bin_cuad'}
                self.explic.append(n)
    
                pat = self.explic[ind_pat]
                pat['h1'] = ind
                pat['h2'] = None                
                
                return fc
            else:
                fc = self.fact_bin_cub(poly,symbs) #binomio al cubo
                if fc != poly:                
                    ind = len(self.explic)            
                    n = {'val':latex(fc),'ind':ind,'ind_pat':ind_pat,'type':'bin_cub'}
                    self.explic.append(n)
        
                    pat = self.explic[ind_pat]
                    pat['h1'] = ind
                    pat['h2'] = None                
                    
                    return fc
            
                else:
                    fc = self.fact_trinomio_al_cuad(poly,symbs) #trinomio al cuadrado
                    if fc != poly:                
                        ind = len(self.explic)            
                        n = {'val':latex(fc),'ind':ind,'ind_pat':ind_pat,'type':'trin_cuad'}
                        self.explic.append(n)
            
                        pat = self.explic[ind_pat]
                        pat['h1'] = ind
                        pat['h2'] = None                
                        
                        return fc
                        
                    else:                    
                        fc = self.fact_dif_cuad(poly,symbs) #binomios al cuadrado
                        if fc != poly: #regresa dos binomios que podrían factorizarse                                    
                            
                            ind1 = len(self.explic)
                            n1 = {'val':'\\left(' + latex(fc[0])+'\\right)','ind':ind1,'ind_pat':ind_pat,'type':'dif_cuad','nf':1}
                            self.explic.append(n1)
                    
                            ind2 = ind1+1
                            n2 = {'val':'\\left(' + latex(fc[1])+'\\right)','ind':ind2,'ind_pat':ind_pat,'type':'dif_cuad','nf':2}
                            self.explic.append(n2)            
                            
                            #actualiza la información del padre
                            #ahora tiene dos hijos
                            pat = self.explic[ind_pat]
                            pat['h1'] = ind1
                            pat['h2'] = ind2
                            
                            f1 = self.factoriza(fc[0],symbs,ind1)
                            f2 = self.factoriza(fc[1],symbs,ind2)
                            
                            return f1*f2
                        else:
                            fc = self.fact_dif_cub(poly,symbs) #binomios al cuadrado
                            if fc != poly: #regresa dos binomios que podrían factorizarse                                    
                                
                                ind1 = len(self.explic)            
                                n1 = {'val':'\\left(' + latex(fc[0])+'\\right)','ind':ind1,'ind_pat':ind_pat,'type':'dif_cub','nf':1}
                                self.explic.append(n1)
                        
                                ind2 = ind1+1
                                n2 = {'val':'\\left(' + latex(fc[1])+'\\right)','ind':ind2,'ind_pat':ind_pat,'type':'dif_cub','nf':2}
                                self.explic.append(n2)            
                                
                                #actualiza la información del padre
                                #ahora tiene dos hijos
                                pat = self.explic[ind_pat]
                                pat['h1'] = ind1
                                pat['h2'] = ind2
                                
                                f1 = self.factoriza(fc[0],symbs,ind1)
                                f2 = self.factoriza(fc[1],symbs,ind2)
                                
                                return f1*f2
                            else:
                                fc = self.fact_prod_bin(poly,symbs)
                                if fc != poly:                    
                                    
                                    ind1 = len(self.explic)            
                                    n1 = {'val':'\\left(' + latex(fc[0])+'\\right)','ind':ind1,'ind_pat':ind_pat,'type':'prod_bin','nf':1}
                                    self.explic.append(n1)
                            
                                    ind2 = ind1+1
                                    n2 = {'val':'\\left(' + latex(fc[1])+'\\right)','ind':ind2,'ind_pat':ind_pat,'type':'prod_bin','nf':1}
                                    self.explic.append(n2)            
                                    
                                    #actualiza la información del padre
                                    #ahora tiene dos hijos
                                    pat = self.explic[ind_pat]
                                    pat['h1'] = ind1
                                    pat['h2'] = ind2
                                    
                                    f1 = self.factoriza(fc[0],symbs,ind1)
                                    f2 = self.factoriza(fc[1],symbs,ind2)
                                    
                                    return f1*f2                            
                                else:
                                    fc = self.fact_prod_mix2(poly,symbs,ind_pat)
                                    if fc != poly:
                
                                        #la factorización mezclada generó un nuevo nodo padre
                                        #en ese nodo se explica la factorización mezclada                        
                                        ind_pat = fc[2]
                                        
                                        ind1 = len(self.explic)            
                                        n1 = {'val':'\\left(' + latex(fc[0])+'\\right)','ind':ind1,'ind_pat':ind_pat, 'type':'mix'}
                                        self.explic.append(n1)
                                
                                        ind2 = ind1+1
                                        n2 = {'val':'\\left(' + latex(fc[1])+'\\right)','ind':ind2,'ind_pat':ind_pat, 'type':'mix'}
                                        self.explic.append(n2)     
                                        
                                        #actualiza la información del padre
                                        #ahora tiene dos hijos
                                        pat = self.explic[ind_pat]
                                        pat['h1'] = ind1
                                        pat['h2'] = ind2
                                        
                                        f1 = self.factoriza(fc[0],symbs,ind1)
                                        f2 = self.factoriza(fc[1],symbs,ind2)
                                        self.explic.append([poly,f1*f2])
                                        return f1*f2                            
                                    else:
                                        return poly
    

    def signo_mon(self, t):
        cm = t.as_coeff_Mul()
        if cm[0] >= 0:
            return 1
        else:
            return -1
            
    #averigua si el término t es numérico
    # decimal, Racional, entero          
    def es_num(self, t):
        n_types = [type(1), type(0.1), type(Rational(3,2)), type(Rational(1,2)), type(Rational(4,2))]
        return type(t) in n_types
    
    #factoriza un polinimo extrayendo algún monomio 
    #que aparezca como factor común de cada término
    def fact_mon_comun(self, poly,symbs):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        fc = pol.factor_comun()
        if fc != 1:
            f2 = 0
            nnegs = 0
            #divide cada término del polinomio
            for i in range(pol.getSize()):
                t = pol.getTerm(i)
                td = t/fc
                if self.es_num(td):
                    if td < 0:
                        nnegs += 1
                else:
                    cm = td.as_coeff_Mul()
                    if cm[0] < 0:
                        nnegs += 1
                f2 = f2 + t/fc
            if 2*nnegs > pol.getSize():
                return [-fc, -f2]
            else:
                return [fc, f2]
        else:
            return poly
            
    #factorización de un binomio al cubo
    def fact_bin_cub(self, poly,symbs):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        #si no es un trinomio no puede factorizarse como binimio al cuadrado        
        if pol.getSize() != 4:
            return poly
        
        #ordena los términos del polinomio
        trms_ord = ordena_pol_leading_var_deg(pol.trms,symbs)     
        
        if not (pol.esCuboTrm(trms_ord[0],1) or pol.esCuboTrm(trms_ord[0],-1)):
            return poly
        if not (pol.esCuboTrm(trms_ord[-1],1) or pol.esCuboTrm(trms_ord[-1],-1)):
            return poly
        
        #evalúa las raíces cúbicas de los términos extremos
        s = self.signo_mon(trms_ord[0])
        if s > 0:
            r1 = pol.t_cubic_roothTrm(trms_ord[0],1)
        else:
            r1 = -pol.t_cubic_roothTrm(trms_ord[0],-1)
            
        s = self.signo_mon(trms_ord[-1])
        if s > 0:
            r2 = pol.t_cubic_roothTrm(trms_ord[-1],1)
        else:
            r2 = -pol.t_cubic_roothTrm(trms_ord[-1],-1)
            
        if trms_ord[1] != 3*r1**2*r2:
            return poly
        if trms_ord[2] != 3*r1*r2**2:
            return poly
            
        return (r1+r2)**3
        
                    
    #factorización de trinomios cuadrados perfectos
    #en binomios al cuadrado
    def fact_bin_cuad(self, poly,symbs):
        if type(poly) in [int]:
            return poly
        
        pol = polinomio(pol=poly,symbs=symbs)
        #si no es un trinomio no puede factorizarse como binimio al cuadrado        
        if pol.getSize() != 3:
            return poly
        else:
            #identifica si el polinomio es un trinomio cadrado perfecto
            t1 = pol.getTerm(0)
            t2 = pol.getTerm(1)
            t3 = pol.getTerm(2)
            
            #trinomio cuadrado perfecto
            if 4*t1*t3 == t2**2: #el termino t2 es el doble del primero por el segundo
                i1 = 0
                i2 = 2
                i3 = 1
                
            elif 4*t1*t2 == t3**2:
                i1 = 0
                i2 = 1
                i3 = 2 
                
            elif 4*t2*t3 == t1**2:
                i1 = 1
                i2 = 2
                #i3 = 0
                
            else:
                return poly
            
            if (pol.esCuadrado(i1,1) or pol.esCuadrado(i1,-1)) and (pol.esCuadrado(i2,1) or pol.esCuadrado(i2,-1)):
                #averigua el signo de los términos
                s1 = self.signo_mon(pol.getTerm(i1))            
                #s2 = signo_mon(pol.getTerm(i2))
                #if s1*s2 < 0:
                #    return [False, pol]
                if s1<0: #accede a los términos                
                    sq_t1 = pol.t_sqrt(i1,-1)
                    sq_t2 = pol.t_sqrt(i2,-1)
                    t3 = pol.getTerm(i3)
                    s = self.signo_mon(pol.getTerm(i3))
                    if s*s1 > 0:
                        return -(sq_t1+sq_t2)**2
                    else:
                        return -(sq_t1-sq_t2)**2
                else:
                    sq_t1 = pol.t_sqrt(i1,1)
                    sq_t2 = pol.t_sqrt(i2,1)
                    t3 = pol.getTerm(i3)
                    s = self.signo_mon(pol.getTerm(i3))
                    if s*s1 > 0:
                        return (sq_t1+sq_t2)**2
                    else:
                        return (sq_t1-sq_t2)**2
                
            else:
                return poly      

    #factorización de diferencia de cuadrados 
    #en binomios al cuadrado
    def fact_dif_cuad(self, poly,symbs):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        #si no es un binomio no puede factorizarse como binomios conjungados        
        if pol.getSize() != 2:
            return poly
        else:
            #identifica si el polinomio es una diferencia de cuadrados
            
            if (pol.esCuadrado(0,1) or pol.esCuadrado(0,-1)) and (pol.esCuadrado(1,1) or pol.esCuadrado(1,-1)):
                s1 = self.signo_mon(pol.getTerm(0))            
                s2 = self.signo_mon(pol.getTerm(1))
                if not s1*s2 < 0:
                    return poly
                else:
                    if s1<0: #
                        sq_t1 = pol.t_sqrt(0,-1)
                        sq_t2 = pol.t_sqrt(1,1)
                        return [(sq_t2+sq_t1),(sq_t2-sq_t1)]
                    else:
                        sq_t1 = pol.t_sqrt(0,1)
                        sq_t2 = pol.t_sqrt(1,-1)
                        return [(sq_t1+sq_t2),(sq_t1-sq_t2)]
            else:
                return poly
                
    #factorización de diferencia de cuadrados 
    #en binomios al cuadrado
    def fact_dif_cub(self, poly,symbs):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        #si no es un binomio no puede factorizarse como binomios conjungados        
        if pol.getSize() != 2:
            return poly
        else:
            #identifica si el polinomio es una diferencia de cubos
            s1 = self.signo_mon(pol.getTerm(0))            
            s2 = self.signo_mon(pol.getTerm(1))
            if not s1*s2 < 0:
                return poly
            else:
                if s1 > 0:
                    if not pol.esCubo(0,1):
                        return poly
                    if not pol.esCubo(1,-1):
                        return poly
                else:
                    if not pol.esCubo(0,-1):
                        return poly
                    if not pol.esCubo(1,1):
                        return poly
                #aquí ya estoy seuro que es una diferencia de cubos
                if s1<0: #
                    sq_t1 = pol.t_cubic_rooth(0,-1)
                    sq_t2 = pol.t_cubic_rooth(1,1)
                    return [(sq_t2-sq_t1),(sq_t2**2+sq_t2*sq_t1+sq_t1**2)]
                else:
                    sq_t1 = pol.t_cubic_rooth(0,1)
                    sq_t2 = pol.t_cubic_rooth(1,-1)
                    return [(sq_t1-sq_t2),(sq_t1**2+sq_t1*sq_t2+sq_t2**2)]
                
                        
    def fact_prod_bin(self, poly, symbs):
        if type(poly) in [int]:
            return poly
        t_ent = [type(1), type(Rational(4,2)), type(Rational(2,2)), type(Rational(-1,1))]        
        pol = polinomio(pol=poly,symbs=symbs)
        
        #si no es un trinomio no puede factorizarse como binimio al cuadrado        
        if pol.getSize() != 3:
            return poly
        else:
            
            #identifica si el polinomio es un trinomio que proviene 
            #del producto de dos binomios del tipo (x+a)(x+b)
            
            perm = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
                    
            for p in perm:
                #t1 = pol.getTerm(p[0])
                t2 = pol.getTerm(p[1])
                t3 = pol.getTerm(p[2])
            
                if self.es_num(t3):
                    sig = 0
                    if pol.esCuadrado(p[0],1):#el primero es un cuadrado
                        sq1 = pol.t_sqrt(p[0],1)
                        s = t2/sq1
                        pp = t3
                        sig = 1 
                    elif pol.esCuadrado(p[0],-1):
                        sq1 = pol.t_sqrt(p[0],-1)
                        s = -t2/sq1
                        pp = -t3
                        sig = -1
                        
                    if sig != 0:
                        if type(s) in t_ent:
                            rad1 = s+sqrt(s**2-4*pp)
                            rad2 = s-sqrt(s**2-4*pp)
                            if type(rad1) in t_ent and type(rad2) in t_ent:
                                a = Rational(rad1,2)
                                b = Rational(rad2,2)
                                if type(a) in t_ent and type(b) in t_ent:
                                    return [sig*(sq1+a),(sq1+b)]
                    
                    t1 = pol.getTerm(p[0])
                    cm = t1.as_coeff_Mul()
                    if pol.esCuadrado(p[0],cm[0]):#el primero es un cuadrado
                        sq1 = pol.t_sqrt(p[0],cm[0])
                        s = cm[0]*t2/sq1
                        pp = cm[0]*t3
                        if type(s) in t_ent:
                            rad1 = s+sqrt(s**2-4*pp)
                            rad2 = s-sqrt(s**2-4*pp)
                            if type(rad1) in t_ent and type(rad2) in t_ent:
                                a = Rational(rad1,2)
                                b = Rational(rad2,2)
                                if a%cm[0] == 0:
                                    return [(sq1/cm[0]+a/cm[0]),(sq1+b)]
                                else:
                                    return [(sq1+a),(sq1/cm[0]+b/cm[0])]
            return poly
            
    def fact_trinomio_al_cuad(self, poly, symbs):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        
        if pol.getSize() != 6:
            return poly
        
        #los primeros tres deben ser cuadrados        
        prms = [[0,1,2,3,4,5], [0,1,3,2,4,5], [0,1,4,2,3,5], [0,1,5,2,3,4],
                [0,2,3,1,4,5], [0,2,4,1,3,5], [0,2,5,1,3,4],
                [0,3,4,1,2,5], [0,3,5,1,2,4],
                [0,4,5,1,2,3],
                [5,4,3,2,1,0], [5,4,2,3,1,0], [5,3,2,4,1,0], [4,3,2,5,1,0],
                [5,4,1,3,2,0], [5,3,1,4,2,0], [4,3,1,5,2,0],
                [5,2,1,4,3,0], [4,2,1,5,3,0],
                [3,2,1,5,4,0]]
        
        for p in prms:
            #los tres primeros deben ser cuadrados
            if (pol.esCuadrado(p[0],1) and pol.esCuadrado(p[1],1) and pol.esCuadrado(p[2],1)):
                #los otros tres términos deben ser el doble producto de las raíces de los primeos tres
                a = pol.t_sqrt(p[0],1)
                b = pol.t_sqrt(p[1],1)
                c = pol.t_sqrt(p[2],1)
                
                trms = [pol.getTerm(p[3]), pol.getTerm(p[4]), pol.getTerm(p[5])]
                
                t = 2*a*b #ambos positivos                 
                s1 = 0
                if t in trms:
                    trms.remove(t)
                    s1 = 1
                elif -t in trms:
                    trms.remove(-t)
                    s1 = -1
                if s1 == 0:
                    return poly

                t = 2*a*c #ambos positivos                 
                s2 = 0
                if t in trms:
                    trms.remove(t)
                    s2 = 1
                elif -t in trms:
                    trms.remove(-t)
                    s2 = -1
                if s2 == 0:
                    return poly                                   
                    
                t = 2*b*c #ambos positivos                 
                s3 = 0
                if t in trms:
                    trms.remove(t)
                    s3 = 1
                elif -t in trms:
                    trms.remove(-t)
                    s3 = -1
                if s3 == 0:
                    return poly                                   
                
                if s1 < 0:
                    b = -b
                if s2 < 0:
                    c = -c
                
                return (a+b+c)**2
        
        return poly
        
    #se supone que el polinomio fue factorizado buscando un factor común        
    def fact_prod_mix2(self, poly, symbs, ind_pat):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)        
        colrs = ['blue', 'green', 'red', 'teal', 'purple', 'violet', 'yellow']
        
        #empieza por ordenar los términos
        gps = ordena_grupos(pol.trms, symbs)
        if len(gps) == 1:
            trms_ord = ordena_pol_leading_var_deg(pol.trms,symbs)  
            gps = ordena_grupos(trms_ord, symbs)
            if len(gps) == 1:
                return poly
        else:
            trms_ord = pol.trms
        
        #forma cada uno de los subpolinomios
        fac_com = 0
        facts = 0
        pols = 0
        res_ltx = ''
        regpd_ltx = ''
        for i,g in enumerate(gps):
            #forma el subpolinomio
            p = 0
            for t in g:
                p = p+trms_ord[t]
            #manda factorizar el subpolinomio
            f = self.fact_mon_comun(p,symbs)
            
            colr = colrs[i%len(gps)]
            
            ltx = latex(p)
            if i == 0 or ltx[0] == '-':
                regpd_ltx = regpd_ltx+'\\color{'+colr+'}'+'{'+ltx+'}'
            else:
                regpd_ltx = regpd_ltx+'+\\color{'+colr+'}'+'{'+ltx+'}'
                    
            if f != p: #pudo factorizarse
                pols = pols+f[0]*f[1] # ¿si f[0] es constante?
                coef_Mul = f[0].as_coeff_Mul()
                if coef_Mul[0] > 0:
                    if res_ltx != '':
                        res_ltx = res_ltx+ '+\\color{'+colr+'}'+'{'+latex(f[0])+'\\left('+latex(f[1])+'\\right)}'                        
                    else:
                        res_ltx = res_ltx+'\\color{'+colr+'}'+'{'+latex(f[0])+'\\left('+latex(f[1])+'\\right)}'
                else:
                    res_ltx = res_ltx+'\\color{'+colr+'}'+'{'+latex(f[0])+'\\left('+latex(f[1])+'\\right)}'
                    
                if i == 0:
                    fac_com = f[1]
                    facts = f[0]
                else:
                    if f[1] == fac_com:
                        facts = facts+f[0]
                    elif f[1] == -fac_com:
                        facts = facts-f[0]
                    else:
                        return poly
            else:
                pols = pols+p
                
                if res_ltx != '':
                    res_ltx = res_ltx+'+\\color{'+colr+'}'+'{'+ '\\left('+latex(p)+'\\right)}'
                else:
                    res_ltx = res_ltx+'\\color{'+colr+'}'+'{'+ '\\left('+latex(p)+'\\right)}'
                    
                if i == 0:
                    fac_com = f
                    facts = 0
                else:
                    if f == fac_com:
                        facts = facts+1
                    elif f == -fac_com:
                        facts = facts-1
                    else:
                        return poly

        ind = len(self.explic)
        
        n = {'val':'\\left('+regpd_ltx+'\\right)','ind':ind,'ind_pat':ind_pat,'type':'rgpd'}
        self.explic.append(n)
        
        pat = self.explic[ind_pat]
        pat['h1'] = ind
        pat['h2'] = None
        
        ind2 = len(self.explic)
        
        n = {'val':'\\left\\{'+res_ltx+'\\right\\}','ind':ind2,'ind_pat':ind,'type':'rgpd2'}
        self.explic.append(n)
        
        pat = self.explic[ind]
        pat['h1'] = ind2
        pat['h2'] = None
                                
        return [fac_com,facts,ind2]
                
                    
    #puede factorizar polinomios con 6 términos
    def fact_prod_mix(self, poly, symbs, ind_pat):
        if type(poly) in [int]:
            return poly
        pol = polinomio(pol=poly,symbs=symbs)
        
        if pol.getSize() != 6:
            return poly
        
        #forma cada pareja de grupos de tres términos
        prms = [[1, 2, 3, 4, 5, 0], [1, 2, 4, 3, 5, 0], [1, 2, 5, 3, 4, 0], [1, 2, 0, 3, 4, 5], [1, 3, 4, 2, 5, 0], [1, 3, 5, 2, 4, 0], [1, 3, 0, 2, 4, 5], [1, 4, 5, 2, 3, 0], [1, 4, 0, 2, 3, 5], [1, 5, 0, 2, 3, 4]]
        for p in prms:
            t1 = pol.getTerm(p[0])
            t2 = pol.getTerm(p[1])
            t3 = pol.getTerm(p[2])
            t4 = pol.getTerm(p[3])
            t5 = pol.getTerm(p[4])
            t6 = pol.getTerm(p[5])
            
            p1 = t1+t2+t3
            p2 = t4+t5+t6
            
            #busca un factor común en cada polinomio
            f1 = self.fact_mon_comun(p1,symbs)
            if f1 != p1:
                f2 = self.fact_mon_comun(p2,symbs)
                if f2 != p2:
                    if f1[1] == f2[1]:
                        
                        ind = len(self.explic)            
                        n = {'val':latex(f1[0]*f1[1] + f2[0]*f1[1]),'ind':ind,'ind_pat':ind_pat}
                        self.explic.append(n)
                        
                        pat = self.explic[ind_pat]
                        pat['h1'] = ind
                        pat['h2'] = None                
                                                
                        return [(f1[0]+f2[0]),(f1[1]), ind]
        return poly
        
    def explicacion(self):                   
        exp_orden = [[self.explic[0]]] #inicia con el nodo padre
        
        #revisa cada elemento de la explicación actual
        lev = 0
        solo_hojas = False
        
        while not solo_hojas:
            solo_hojas = True
            exp_act = []
            for e in exp_orden[lev]:                
                if not 'h1' in e.keys(): #el nod o tiene hojas
                    exp_act.append(e)
                else:
                    solo_hojas = False
                    h1 = self.explic[e['h1']]
                    exp_act.append(h1)
                    if 'h2' in e.keys():
                        ind2 = e['h2']
                        if ind2 != None:
                            h2 = self.explic[ind2]
                            exp_act.append(h2)                
            if not solo_hojas:
                exp_orden.append(exp_act)
                lev = lev+1
        return exp_orden
        
    def latex_explicacion(self):
        symbs = ['a','b','c','x','y','z']        
        
        ex = self.explicacion()
                    
        #explicación    
        res = '\\begin{align}'
               
        for i,e in enumerate(ex):
            if i == 0:
                res += '\\color{red}{'
                clsd = False
            else:
                res += '&='
            
            if not e[0]['type'] == 'root':
                pat = self.explic[e[0]['ind_pat']]
            
            if e[0]['type'] == 'fc' and not 'explnd' in pat.keys():
                c1 = e[0]['val']
                c1 = c1.replace('\\left(','(')
                c1 = c1.replace('\\right)',')')
                c2 = e[1]['val']
                c2 = c2.replace('\\left(','(')
                c2 = c2.replace('\\right)',')')                
                trms2 = ltx_terminos3(c2,symbs)
                ex_fc = ''
                ec = ltxToE(c1, symbs)
                if not type(ec) in [int]:
                    cm = ec.as_coeff_Mul()
                else:
                    cm = [ec,ec]
                s = '' if cm[0] < 0 else '+'
                for j,t in enumerate(trms2):
                    if j == 0:                        
                        ex_fc += c1+'\\left('+t+'\\right)'
                    else:
                        ex_fc += s+c1+'\\left('+t+'\\right)'
                res += ex_fc+'\\\\ '
                res += '&='
                pat['explnd'] = True
                
            #############################################3
            #busca insertar un paso intermedio
            n = e[0]
            if n['type'] != 'root':                 
                ltx_int = ''
                insrtd = False
                for f in e:                    
                    pat = self.explic[f['ind_pat']]
                    if 'h1' in pat.keys():
                        if pat['h2']:
                            h1 = self.explic[pat['h1']]                    
                    if 'h2' in pat.keys():
                        if pat['h2']:
                            h2 = self.explic[pat['h2']]
                    
                    #############################################
                    if f['type'] == 'trin_cuad' and not 'explnd' in pat.keys() and not 'dev' in f.keys():
                        ltx = f['val']
                        #if f['nf'] == 1:
                        ltx = ltx.replace('\\right)^{2}',')')
                        ltx = ltx.replace('\\left(','(')
                        ltx = ltx.replace('\\right)',')')                        
                        
                        trms = ltx_terminos3(ltx, symbs)
                        et1 = ltxToE(trms[0], symbs)
                        et2 = ltxToE(trms[1], symbs)
                        et3 = ltxToE(trms[2], symbs)
                        
                        if len(e) > 1:
                            ltx_int += '\\left[\\left('+latex(et1)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et3)+'\\right)'
                            ltx_int += '+\\left('+latex(et2)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et2)+'\\right)\\left('+latex(et3)+'\\right)'
                            ltx_int += '+\\left('+latex(et3)+'\\right)^2\\right]'                                                        
                        else:
                            ltx_int += '\\left('+latex(et1)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et3)+'\\right)'
                            ltx_int += '+\\left('+latex(et2)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et2)+'\\right)\\left('+latex(et3)+'\\right)'
                            ltx_int += '+\\left('+latex(et3)+'\\right)^2'
                        insrtd = True
                        pat['explnd'] = True
                        f['dev'] = True
                        
                    if f['type'] == 'dif_cub' and not 'explnd' in pat.keys() and not 'dev' in f.keys():
                        ltx = f['val']
                        #if f['nf'] == 1:
                        ltx = ltx.replace('\\left(','(')
                        ltx = ltx.replace('\\right)',')')                           
                        
                        trms = ltx_terminos3(ltx, symbs)
                        et1 = ltxToE(trms[0], symbs)
                        et2 = ltxToE(trms[1], symbs)
                        
                        if len(e) > 2:
                            ltx_int += '\\left[\\left('+latex(et1)+'\\right)^3'
                            ltx_int += '-\\left('+latex(-et2)+'\\right)^3\\right]'
                        else:
                            ltx_int += '\\left('+latex(et1)+'\\right)^3'
                            ltx_int += '-\\left('+latex(-et2)+'\\right)^3'
                        insrtd = True
                        pat['explnd'] = True
                        f['dev'] = True
                        h2['dev'] = True
                            
                    if f['type'] == 'bin_cuad' and not 'explnd' in pat.keys() and not 'dev' in f.keys():
                        ltx = f['val']
                        if ltx.find('\\left(')>=0:
                            ltx = ltx.replace('\\right)^{2}',')')
                            ltx = ltx.replace('\\left(','(')
                            ltx = ltx.replace('\\right)',')')
                        trms = ltx_terminos3(ltx, symbs)                        
                        et1 = ltxToE(trms[0], symbs)
                        et2 = ltxToE(trms[1], symbs)
                        
                        if len(e) > 1:
                            ltx_int += '\\left[\\left('+latex(et1)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)+'
                            ltx_int += '\\left('+latex(et2)+'\\right)^2\\right]'
                        else:
                            ltx_int += '\\left('+latex(et1)+'\\right)^2'
                            ltx_int += '+2\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)+'
                            ltx_int += '\\left('+latex(et2)+'\\right)^2'
                        insrtd = True
                        pat['explnd'] = True
                        f['dev'] = True
                        
                    if f['type'] == 'bin_cub' and not 'explnd' in pat.keys() and not 'dev' in f.keys():
                        
                        ltx = f['val']
                        if ltx.find('\\left(')>=0:
                            ltx = ltx.replace('\\right)^{3}',')')
                            ltx = ltx.replace('\\left(','(')
                            ltx = ltx.replace('\\right)',')')                            
                        trms = ltx_terminos3(ltx, symbs)
                        
                        et1 = ltxToE(trms[0], symbs)
                        et2 = ltxToE(trms[1], symbs)
                        
                        if len(e) > 1:
                            ltx_int += '\\left[\\left('+latex(et1)+'\\right)^3'
                            ltx_int += '+3\\left('+latex(et1)+'\\right)^2\\left('+latex(et2)+'\\right)'
                            ltx_int += '+3\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)^2+'
                            ltx_int += '\\left('+latex(et2)+'\\right)^3\\right]'
                        else:
                            ltx_int += '\\left('+latex(et1)+'\\right)^3'
                            ltx_int += '+3\\left('+latex(et1)+'\\right)^2\\left('+latex(et2)+'\\right)'
                            ltx_int += '+3\\left('+latex(et1)+'\\right)\\left('+latex(et2)+'\\right)^2+'
                            ltx_int += '\\left('+latex(et2)+'\\right)^3'
                        insrtd = True
                        pat['explnd'] = True
                        f['dev'] = True                                                
                        
                    elif f['type'] == 'dif_cuad' and not 'explnd' in pat.keys() and not 'dev' in h1.keys() and not 'dev' in h2.keys():
                        #evalúa la raíz cuadrada de los dos términos
                        #h2 = self.explic[pat['h2']]
                        #extrae los términos de padre
                        ltx_pat = pat['val']                        
                        if ltx_pat.find('\\left(')>=0:
                            ltx_pat = ltx_pat.replace('\\left(','(')
                            ltx_pat = ltx_pat.replace('\\right)',')')                            
                        trms = ltx_terminos3(ltx_pat, symbs)
                        e1 = ltxToE(trms[0], symbs)
                        e2 = ltxToE(trms[1], symbs)
                        #exp_dc += '\\left('+latex(sqrt(e1))
                        
                        if not type(e1) in [int]:
                            pd1 = e1.as_powers_dict()
                        else:
                            pd1 = {e1:1}
                        
                        s1 = 1
                        for k in pd1:
                            if not type(k) in [int]:
                                s1 = s1*k**(pd1[k]/2)
                            else:
                                s1 = s1*sqrt(k)
                         
                        if not type(e2) in [int]:
                            pd2 = e2.as_powers_dict()
                        else:
                            pd2 = {e2:1}
                        
                        s2 = 1
                        for k in pd2:
                            if not type(k) in [int]:
                                s2 *= k**(pd2[k]/2)
                            else:
                                if k > 0:
                                    s2 *= sqrt(k)
                                else:
                                    s2 *= sqrt(-k)
                        if len(e) > 2:
                            ltx_int += '\\left[\\left('+latex(s1)+'\\right)^2-'+'\\left('+latex(s2)+'\\right)^2\\right]'
                        else:
                            ltx_int += '\\left('+latex(s1)+'\\right)^2-'+'\\left('+latex(s2)+'\\right)^2'
                        insrtd = True
                        pat['explnd'] = True
                        h1['dev'] = True
                        h2['dev'] = True
                                                                                                           
                    elif not 'dev' in f.keys():
                        ltx_int += f['val']                    
                        
                if insrtd:
                    res += ltx_int
                    res += '\\\\'
                    res += '&='
                    #extrae las claves de "dev" de cada nodo
                    #dejando listo el nodo para que pueda mostrarse después
                    for f in e:
                        if 'dev' in f.keys():
                            f.pop('dev',None)                                           
            
            #sin pasos intermedios
            for f in e:                                                
                if i < len(ex)-1:
                    ltx = f['val']
                else:
                    ltx = '\\color{blue}{'+f['val']+'}'
                res = res + ltx
            
            if not clsd:
                res += '}'
                clsd=True
            else:
                res = res+'\\\\ '
                
        proc = {}
        for f in ex[-1]: #último nivel de explicación
            if 'type' in f.keys():
                t = f['type']
                if t in proc.keys():
                    proc[t] = proc[t]+1
                else:
                    proc[t] = 1
        
        comp = 0        
        for p in proc:
            if p in ['fc','bin_cuad', 'bin_cub', 'trin_cuad','mix']:
                comp = comp + proc[p]
            else:
                comp = comp+proc[p]/2 #complejidad?            
        res = res + '\\end{align}'
        return {'exp':res, 'comp':comp, 'proc':proc}
                                                               
#ordena un polinomo por el grado de la variable dominante
def ordena_pol_leading_var_deg(pol_trms, symbs):
    if len(pol_trms) == 1:
        return pol_trms
            
    t_ent = [type(1), type(Rational(4,2)), type(Rational(2,2)), type(Rational(-1,1))]
    
    #llena un diccionario con los símbolos
    #y sus potencias
    pot_symb = {}
    cts = [] #guarda los términos constantes
    
    #recorre cada término 
    #y averigua la potencia de cada símbolo
    for t in pol_trms:
        if not type(t) in t_ent:
            d = t.as_powers_dict()
            for k in d.keys():
                if str(k) in symbs:
                    if not k in pot_symb:
                        pot_symb[k] = d[k]
                    elif pot_symb[k] < d[k]:
                        pot_symb[k] = d[k]
        else:
            cts.append(t)
    
    #ordena las variables de acuerdo a la potencia con la que aparecen 
    srt_symbs = sorted(pot_symb.items(), key=operator.itemgetter(1),reverse=True)
    
    #ordena los términos de acuerdo a la potencia del símbolo dominante    
    s = srt_symbs[0][0]
    
    trms = []
    for t in pol_trms:
        if not type(t) in t_ent:
            d = t.as_powers_dict()
            trms.append([t,d[s]])
        
    llave = lambda item: item[1]
    srt_trms_t = sorted(trms, key=llave,reverse=True)
    srt_trms = []
    for t in srt_trms_t:
        srt_trms.append(t[0])   
    
    if len(cts) > 0:
        for c in cts:
            srt_trms.append(c)
    return srt_trms                                            


#ordena términos de un polinomio
#de acuerdo al grado de alguna de las variables
def ordena_pol_var_deg(pol_trms, s, symbs):
    t_ent = [type(1), type(Rational(4,2)), type(Rational(2,2)), type(Rational(-1,1))]
    
    #llena un diccionario con los símbolos
    #y sus potencias
    trms = []
    not_s_trms = []
    for t in pol_trms:
        if not type(t) in t_ent:
            d = t.as_powers_dict()
            if s in d.keys():
                trms.append([t,d[s]])
            else:
                not_s_trms.append(t)
        else:
            not_s_trms.append(t)
            
    #ordena los términos de acuerdo a las potencias de la variable s    
    llave = lambda item: item[1]
    srt_trms_t = sorted(trms, key=llave,reverse=True)
    srt_trms = []
    for t in srt_trms_t:
        srt_trms.append(t[0])   
    
    if len(not_s_trms) > 0:
        othr_trms = ordena_pol_leading_var_deg(not_s_trms, symbs)    
        for t in othr_trms:
            srt_trms.append(t)
    return srt_trms   
    
#reordena los términos de un polinomio 
#en caso de existir varios teérminos 
#con la misma potencia de la variable líder
#se regrupan

## trms: son los términos ordenados de acuerdo a la 
##      potencia de la variable líder
## symbs: el conjunto de símbolos
## tup_var_pot): tuplas con pares del tipo variable-potencia, ordenados
def reordena_trms_pot_empate(trms,symbs,tup_var_pot):
    t_ent = [type(1), type(Rational(4,2)), type(Rational(2,2)), type(Rational(-1,1))]
    s1 = tup_var_pot[0][0]
    s2 = tup_var_pot[1][0]
    
    ord_trms = []
    not_ord_trms = []
    
    pot_ant = 0
    
    #revisa cada término y determina si existe empate de potencias de la variable líder
    for i,t in enumerate(trms):
        if i > 0:
            if not type(t) in t_ent:
                d = t.as_powers_dict()
                if s1 in d.keys():
                    pot_n = d[s1]                    
                else:
                    pot_n = 0
                if pot_n < pot_ant:
                    pot_ant = pot_n
                    if len(not_ord_trms) > 1:
                        tmp_ord = ordena_pol_var_deg(not_ord_trms, s2, symbs)
                        for tt in tmp_ord:
                            ord_trms.append(tt)
                    elif len(not_ord_trms) == 1:
                        for tt in not_ord_trms:
                            ord_trms.append(tt)
                    not_ord_trms = [t]
                else:
                    not_ord_trms.append(t)
            else: #constante
                not_ord_trms.append(t)            
                    
        else:
            d = t.as_powers_dict()
            pot_ant = d[s1]
            not_ord_trms.append(t)
            
    if len(not_ord_trms) > 1:
        tmp_ord = ordena_pol_var_deg(not_ord_trms, s2, symbs)
        for t in tmp_ord:
            ord_trms.append(t)
    elif len(not_ord_trms) == 1:
        for t in not_ord_trms:
            ord_trms.append(t)
            
    return ord_trms
    
    
#regresa un vector con duplas símbolo-potencia_max
#que indican la máxima potencia de cada símbolo en 
#el conjunto de términos
def ord_pot_trms(pol_trms, symbs):
    t_ent = [type(1), type(Rational(4,2)), type(Rational(2,2)), type(Rational(-1,1))]
    
    #llena un diccionario con los símbolos
    #y sus potencias
    pot_symb = {}
    
    #recorre cada término 
    #y averigua la potencia de cada símbolo
    for t in pol_trms:
        if not type(t) in t_ent:
            d = t.as_powers_dict()
            for k in d.keys():
                if str(k) in symbs:
                    if not k in pot_symb:
                        pot_symb[k] = d[k]
                    elif pot_symb[k] < d[k]:
                        pot_symb[k] = d[k]
    
    #ordena las variables de acuerdo a la potencia con la que aparecen 
    srt_symbs = sorted(pot_symb.items(), key=operator.itemgetter(1),reverse=True)
    return srt_symbs   
                                                                   
'''
def explora_divisores(trms):
    #extrae los coeficienets de cada término
       
    for t in trms:
        c_e = t.as_coeff_Mul()
        print (c_e[0], factorint(c_e[0]))
'''
   
# d no puede ser cero
# v1 y v2 deben ser diferentes  (si fueran iguales se reducirìa el polinomio)   
def v1_v2_mult_esc_d(v1,v2,d):
    diff = []
    found = False
    id0 = False
    for i in range(len(v1)):
        df = v1[i]-v2[i]
        if df != 0 and not found:
            id0 = i 
        diff.append(df)
        
    #if not id0: #ambos vectores son iguales (se supone que no debe llamarse con vectores iguales)
    #    return 'ig'
    
    if d[id0] != 0:
        r = Rational(diff[id0],d[id0])        
    else:
        return False
    
    for i in range(len(v1)):
        if diff[i] != r*d[i]:
            return False
    
    return r            
        
def vect_diffs_exps(v1,v2):
    res = []
    for i in range(len(v1)):
        res.append(v1[i]-v2[i])
    return res
        
#recibe los términos ordenados de acuerdo 
#a la potencia del símbolo dominante
def ordena_grupos(trms_ord, symbs):        
    typs = [type(1), type(0)]   
    
    indx = {}
    for i,s in enumerate(symbs):
        indx[s] = i
            
    #recorrre cada término y crea un diccionario con las variables como llave y sus potencias
    pot = []
    n_symbs = len(symbs)
    for t in trms_ord:
        v_exp = [0]*n_symbs
        if not type(t) in typs:
            p = t.as_powers_dict()            
            for v in p.keys():
                sv = str(v)  
                if sv in symbs:
                    v_exp[indx[sv]] = p[v]                
        pot.append(v_exp)
       
    #forma los grupos de términos
    trms_indx = list(range(1,len(trms_ord)))
    found = False #indica si se formaron los grupos
    
    #ningún término está agrupado
    for i in trms_indx:
        #prueba para ver si el vector d es 
        #el que permite agrupar los términos
        d = vect_diffs_exps(pot[0],pot[i])
        gps = []
        indx_left = list(range(len(trms_ord)))
        while len(indx_left)>0:
            #extrae un índice 
            l = indx_left[0]
            indx_left.remove(indx_left[0])
            gp = [l] #inicia un grupo
            indx_test = copy(indx_left)
            for m in indx_test:
                if v1_v2_mult_esc_d(pot[l],pot[m],d):
                    gp.append(m)
                    indx_left.remove(m)
            if len(gp) == 1:
                break                            
            gps.append(gp)
            if len(indx_left) == 0:
                found = True
        if found:
            break
        
    return gps
    
    '''        
    for g in gps:
        for e in g:
            print trms_ord[e]
        print '\n'
    '''
    
if __name__ == '__main__':
    symbs = ['a','b','c','x','y','z']
    #symbs = ['a','b','c']
    #symbs = ['x','y','z']

    ltx = 'a^{6} b^{3} c^{12} - 6 a^{6} b^{3} c^{11} + 12 a^{6} b^{3} c^{10} - 8 a^{6} b^{3} c^{9}'
    poly = polinomio(pol_ltx = ltx, symbs = symbs)
    pol = poly.getPoly()
    
    exp_f = explica_fact()
    #print latex(exp_f.factoriza(pol,symbs,None))
    
    ex = exp_f.latex_explicacion()
    #print ex['exp']
    #print poly.esCuboTrm(-8,1)
    
    