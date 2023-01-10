# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 17:07:03 2016

@author: fernando
"""

from tutor.sistema_experto.LatexProc.Cadenas import valida_ltx, ajusta_cadena, cad2tree, varios_terminos, varios_factores
from sympy import Rational, sqrt, log, ln, exp, sin, cos, tan, latex, cot, csc, sec, symbols, Wild, factor
from sympy import symbols, Wild, expand 
from sympy.core import numbers, add, mul, symbol 
from copy import copy
from random import sample, randint
from sympy.core.function import expand_power_base

import networkx as nx
import matplotlib.pyplot as plt

def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0, 
                  pos = None, parent = None):
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    if parent != None:
        neighbors.remove(parent)
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos
    
'''
def plot_nstd_tree(nt):
    labs = {}        
    G = nx.Graph()
    labs = {}
    networkx_tree(nt,G,'','r',labs)
    
    pos = hierarchy_pos(G,'r')
    
    # nodes
    nx.draw_networkx_nodes(G,pos,node_color='w',node_size=500,alpha=0.8)
    # edges
    nx.draw_networkx_edges(G,pos,width=2.0,alpha=0.25)
    # some math labels
    nx.draw_networkx_labels(G,pos,labs,font_size=16)
    #nx.draw(G,pos=pos)
    e = nstd_tree2expr(nt,['a','b','c','x','y','z'],[])
    #plt.axis('off')
    #plt.xticks([],[])
    #plt.yticks([],[])
    plt.axis('off')
    plt.title('$'+latex(e)+'$')    
    plt.savefig('C:\\Users\\fgome\\Documents\\DeltaConference\\BugsLib\\tree_plot.png')
    #plt.show()
    
def plot_eqn(eqn):
    #separa los lados de la ecuación
    eqnltx = eqn.replace(' ','')
    [li,ld] = eqnltx.split('=')
    
    nti = ltx2nstd_tree(li,['a','b','c','x','y','z'],[])
    ntd = ltx2nstd_tree(ld,['a','b','c','x','y','z'],[])
    
    labs_i = {}        
    labs_d = {}        
    Gi = nx.Graph()
    Gd = nx.Graph()
    networkx_tree(nti,Gi,'','r',labs_i)
    networkx_tree(ntd,Gd,'','r',labs_d)
    
    pos_i = hierarchy_pos(Gi,'r',xcenter = 0,width=0.75)
    pos_d = hierarchy_pos(Gd,'r',xcenter = 1,width=0.75)
    
    # nodes
    nx.draw_networkx_nodes(Gi,pos_i,node_color='w',node_size=500,alpha=0.8)
    # edges
    nx.draw_networkx_edges(Gi,pos_i,width=2.0,alpha=0.25)
    # some math labels
    nx.draw_networkx_labels(Gi,pos_i,labs_i,font_size=16)
    
    # nodes
    nx.draw_networkx_nodes(Gd,pos_d,node_color='w',node_size=500,alpha=0.8)
    # edges
    nx.draw_networkx_edges(Gd,pos_d,width=2.0,alpha=0.25)
    # some math labels
    nx.draw_networkx_labels(Gd,pos_d,labs_d,font_size=16)
    #nx.draw(G,pos=pos)
    #plt.axis('off')
    plt.xticks([],[])
    plt.yticks([],[])
    plt.text(0.35,0.025,'$'+eqn+'$')
    #plt.title('$'+eqn+'$')    
    #plt.show()
'''



def ltx2nstd_tree(ltx,symbs,functs):
    cad = valida_ltx(ltx,symbs,functs) 
    if cad['valida']:
        cad_aj = ajusta_cadena(cad['cad'],symbs)
        t = cad2tree(cad_aj)
        nt = cad_tree2nstd_tree(t,0,symbs,functs)
        return nt        
    else:
        return False
        
def ltx2nstd_tree_rat_nodes(ltx,symbs,functs):
    cad = valida_ltx(ltx,symbs,functs) 
    if cad['valida']:
        cad_aj = ajusta_cadena(cad['cad'],symbs)
        t = cad2tree(cad_aj)
        nt = cad_tree2nstd_tree(t,0,symbs,functs)
        inicia_rational_escx_nodes(nt)
        return nt        
    else:
        return False
    
def ltx2nstd_tree_cmplx_nodes(ltx):
    cad = valida_ltx(ltx,['i'],[]) 
    if cad['valida']:
        cad_aj = ajusta_cadena(cad['cad'],['i'])
        t = cad2tree(cad_aj)
        nt = cad_tree2nstd_tree(t,0,['i'],[])
        inicia_cmplx_nodes1(nt)
        inicia_cmplx_nodes2(nt)
        return nt        
    else:
        return False

def inicia_cmplx_nodes1(nt):
    int_typs = [int, numbers.One, numbers.Integer, numbers.Zero, numbers.NegativeOne]
    exp_tps = [symbol.Symbol, mul.Mul, add.Add]
    
    #busca reducir nodos del tipo a+bi, o a-bi
    if nt['val'] == '*':
        int_exp = type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in exp_tps
        exp_int = type(nt['h1']['val']) in exp_tps and type(nt['h2']['val']) in int_typs         
        if int_exp or exp_int:
            nt['val'] = nt['h1']['val']*nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_cmplx_nodes1(nt['h1'])
            inicia_cmplx_nodes1(nt['h2'])
    elif nt['val'] in ['+','-','/']:
        inicia_cmplx_nodes1(nt['h1'])
        inicia_cmplx_nodes1(nt['h2'])
    
def inicia_cmplx_nodes2(nt):
    int_typs = [int, numbers.One, numbers.Integer, numbers.Zero, numbers.NegativeOne]
    exp_tps = [symbol.Symbol, mul.Mul, add.Add]
    
    #busca reducir nodos del tipo a+bi, o a-bi
    if nt['val'] == '+':
        int_exp = type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in exp_tps
        exp_int = type(nt['h1']['val']) in exp_tps and type(nt['h2']['val']) in int_typs         
        if int_exp or exp_int:
            nt['val'] = nt['h1']['val']+nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_cmplx_nodes2(nt['h1'])
            inicia_cmplx_nodes2(nt['h2'])
    elif nt['val'] == '-':        
        int_exp = type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in exp_tps
        exp_int = type(nt['h1']['val']) in exp_tps and type(nt['h2']['val']) in int_typs         
        if int_exp or exp_int:
            nt['val'] = nt['h1']['val']-nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_cmplx_nodes2(nt['h1'])
            inicia_cmplx_nodes2(nt['h2'])
    elif nt['val'] in ['*','/']:
        inicia_cmplx_nodes2(nt['h1'])
        inicia_cmplx_nodes2(nt['h2'])        
            
#resolver por recursividad      
#el árbol t debe ser validado
def cad_tree2nstd_tree(t,pos,symbs,functs):
    tp = t[pos]
    
    #el nodo e suna hoja
    if not 'ind_h1' in tp.keys(): #es una hoja
        return {'val':hoja_nstd_tree2expr(tp, symbs)} #tiene un número o un símbolo
    elif not 'ind_h2' in tp.keys(): #nodo con un solo hijos
        h1 = cad_tree2nstd_tree(t,tp['ind_h1'],symbs,functs)
        if tp['val'].find('^')>=0: #si es un exponente separa la base y el exponente
            ex = tp['val'][1:]
            #convierte el exponente en un árbol
            te = cad2tree(ex)
            exp_nt = cad_tree2nstd_tree(te,0,symbs,functs)
            return {'val':'^', 'h1':h1, 'h2':exp_nt}
        return {'val':tp['val'], 'h1':h1}
    else:
        h1 = cad_tree2nstd_tree(t,tp['ind_h1'],symbs,functs)
        h2 = cad_tree2nstd_tree(t,tp['ind_h2'],symbs,functs)
        return {'val':tp['val'], 'h1':h1,'h2':h2}

def div_zero(nt,res,symbs=["a","b","c","n","x","y","z"],functs=[],exp_pow_b=False):
    if nt['val'] == '/':
        e2 = nstd_tree2expr(nt['h2'], symbs, functs,exp_pow_b)
        if e2 == 0:
            res.append('Si')
    else:
        if 'h1' in nt.keys():
            div_zero(nt['h1'],res,symbs,functs,exp_pow_b)
        if 'h2' in nt.keys():
            div_zero(nt['h2'],res,symbs,functs,exp_pow_b)
    
#convierte un árbol anidado en una expresión
def nstd_tree2expr(n,symbs=["a","b","c","n","x","y","z"],functs=[],exp_pow_b=False):
    #averigua si es una hoja
    if not 'h1' in n.keys():
        return n['val']
    elif not 'h2' in n.keys(): #función
        return nstd_tree_func(n, symbs, functs)
    else:
        e1 = nstd_tree2expr(n['h1'], symbs, functs,exp_pow_b)
        e2 = nstd_tree2expr(n['h2'], symbs, functs,exp_pow_b)
                
        if n['val'] == '+':
            return e1+e2
        elif n['val'] == '-':
            return e1-e2
        elif n['val'] == '*':
            return e1*e2
        elif n['val'] == '/':
            if e2 == 0:
                return False
            else:
                if type(e1) == type(1) and type(e2) == type(1):
                    return Rational(e1,e2)
                else:
                    return e1/e2
        elif n['val'] == '^':
            if exp_pow_b:
                return expand_power_base(e1**e2, force=True)
            else:
                return e1**e2
        else:
            return False
        
def mult_cmplx(z1,z2):
    i = symbols('i')
    r = expand(z1*z2)
    r = r.xreplace({i**2:-1})
    return r    

def conj_cmplx(z):
    i = symbols('i')
    a = Wild('a', exclude=[i])
    b = Wild('b', exclude=[i])
    
    m = z.match(a*i+b)
    return -m[a]*i+m[b]    
    

def div_cmplx(z1,z2):
    i = symbols('i')
    
    z2c = conj_cmplx(z2)
    num = mult_cmplx(z1, z2c)
    den = mult_cmplx(z2, z2c)
    if den:
        return num/den
    else:
        return False


#convierte un árbol anidado en una expresión
def cmplxnstd_tree2expr(n):
    #averigua si es una hoja
    if not 'h1' in n.keys():
        return n['val']
    else:
        e1 = cmplxnstd_tree2expr(n['h1'])
        e2 = cmplxnstd_tree2expr(n['h2'])
                
        if n['val'] == '+':
            return e1+e2
        elif n['val'] == '-':
            return e1-e2
        elif n['val'] == '*':            
            return mult_cmplx(e1, e2)
        elif n['val'] == '/':
            if e2 == 0:
                return False
            else:
                return div_cmplx(e1, e2)
        else:
            return False


def nstd_tree_func(n, symbs, functs):
    e1 = nstd_tree2expr(n['h1'], symbs, functs)
    funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log','exp','ln']        
    
    for f in funcs:
        ind = n['val'].find(f) #raíz cuadrada
        if ind >= 0:
            if f == 'sqrt':
                return sqrt(e1) 
            elif f == 'sin':
                return sin(e1) 
            elif f == 'cos':
                return cos(e1) 
            elif f == 'tan':
                return tan(e1) 
            elif f == 'cot':
                return cot(e1) 
            elif f == 'sec':
                return sec(e1) 
            elif f == 'csc':
                return csc(e1) 
            elif f == 'log':
                return log(e1) 
            elif f == 'ln':
                return ln(e1) 
            elif f == 'exp':
                return exp(e1) 
                
    #si el nodo tiene un solo hijo, debe ser una función 
    return False
    
def hoja_nstd_tree2expr(h, symbs): #recibe una hoja y regresa el valor en ella
    digs = ['0','1','2','3','4','5','6','7','8','9']
    if h['val'][0] in digs: #es un número
        val = int(h['val'])
        return val
    elif h['val'] in symbs:
        return symbols(h['val'])
    else:
        return False
    
def is_number(cad):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    pt = False
    for i,s in enumerate(cad):
        if i == 0:
            if not (s in nums or s == "-"):
                return False
        else:
            if not s in nums:
                if s == "." and not pt:
                    pt = True
                else:
                    return False
    return True

#la cadena de latex es una sola fracción
def is_rational(cad):
    
    ind = cad.find('\\frac{')
    if ind != 0:
        return False
    
    #extrae el numerador
    in_num = cad.find('{') 
    in_num += 1 #inicio del numerador
    fin_num = cad.find('}')
    num = cad[in_num:fin_num]
    
    #extrae el denominador
    fin_num += 1
    in_den = cad[fin_num:].find('{') 
    in_den += 1 #inicio del numerador
    fin_den = cad[fin_num:].find('}')
    den = cad[fin_num:][in_den:fin_den]
    
    return is_number(num) and is_number(den)
    
          
    
#convierte un árbol en una expresión de latex
#que resume las operaciones representadas en el árbol
def nstd_tree2ltx(nt,numbs=False,pots=False):
    #averigua si el nodo es una hoja
    if not ('h1' in nt.keys()):
        return latex(nt['val'])
    elif not ('h2' in nt.keys()): #función
        l1 = nstd_tree2ltx(nt['h1'],numbs)
        funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log']
        if nt['val'] in funcs:
            if nt['val'] != 'sqrt':
                return '\\'+nt['val']+'\\left({'+l1+'}\\right)'
            else:
                return '\\'+nt['val']+'{'+l1+'}'        
    else: #dos hijos
        l1 = nstd_tree2ltx(nt['h1'],numbs,pots)
        l2 = nstd_tree2ltx(nt['h2'],numbs,pots)
        if nt['val'] == '+': 
            if l2[0] == '-':
                return l1+''+l2
            else:
                return l1 + '+' + l2
        elif nt['val'] == '-': 
            if l2[0] == '-' or varios_terminos(l2):
                if l1 == '0':
                    return '-\\left('+l2+'\\right)'
                else:
                    return l1+'-\\left('+l2+'\\right)'
            else:
                if l1 == '0':
                    return '-' + l2
                else:
                    return l1 + '-' + l2            
        elif nt['val'] == '*':
            if numbs:
                if (not nt['h1']['val'] == "sqrt") and varios_terminos(l1):
                    l1 = '\\left(' + l1 + '\\right)'
                if (not nt['h2']['val'] == "sqrt") and varios_terminos(l2):
                    l2 = '\\left(' + l2 + '\\right)'
                return l1+"\\times "+l2
            if (varios_terminos(l1) or varios_factores(l1,False)) and (not pots):
                f1 = '\\left(' + l1 + '\\right)'                
            elif l1 == '-1':
                f1 = '-'
            elif l1 == '1':
                f1 = ''
            else:
                f1 = l1
            if (l2[0] == '-' or varios_terminos(l2) or varios_factores(l2,False)) and (not pots):
                f2 = '\\left(' + l2 + '\\right)'
            else:
                f2 = l2
            #if (is_number(f1) or is_rational(f1)) or (is_number(f2) or is_rational(f2)):
            #    return f1 + '\\times ' + f2
            #elif (is_number(f1) or is_rational(f1)) or (is_number(f2) or is_rational(f2))
             
            return f1 + f2              
        elif nt['val'] == '/':            
            f1 = l1
            f2 = l2
            return '\\frac{' + f1 + '}{' + f2 +'}' # verificar si los hijos son hojas o no
        elif nt['val'] == '^':
            if varios_terminos(l1) or varios_factores(l1,False):
                f1 = '\\left(' + l1 + '\\right)'
            elif nt['h1']['val'] in ['+','-','*','/']:
                f1 = '\\left(' + l1 + '\\right)'                
            else:
                f1 = l1
            f2 = l2
            return f1 + '^{' + f2 +'}' # verificar si los hijos son hojas o no

def cmplx_latex_leaf(val):
    i = symbols('i')
    a = Wild('a', exclude=[i])
    b = Wild('b', exclude=[i])
    
    m = val.match(a*i+b)  
    
    s = '' if m[a] < 0 else '+'
    return '\\left('+latex(m[b])+s+latex(m[a]*i)+'\\right)'     

#convierte un árbol en una expresión de latex
#que resume las operaciones representadas en el árbol
def cmplxnstd_tree2ltx(nt):
    #averigua si el nodo es una hoja
    if not ('h1' in nt.keys()):
        return cmplx_latex_leaf(nt['val'])
    elif not ('h2' in nt.keys()): #función
        l1 = cmplxnstd_tree2ltx(nt['h1'])
        funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log']
        if nt['val'] in funcs:
            if nt['val'] != 'sqrt':
                return '\\'+nt['val']+'\\left({'+l1+'}\\right)'
            else:
                return '\\'+nt['val']+'{'+l1+'}'        
    else: #dos hijos
        l1 = cmplxnstd_tree2ltx(nt['h1'])
        l2 = cmplxnstd_tree2ltx(nt['h2'])
        if nt['val'] == '+': 
            if l2[0] == '-':
                return l1+''+l2
            else:
                return l1 + '+' + l2
        elif nt['val'] == '-': 
            if l1 == '0':
                return '-' + l2
            else:
                return l1 + '-' + l2            
        elif nt['val'] == '*':            
            return l1 + '\\times '+l2              
        elif nt['val'] == '/':            
            return '\\frac{' + l1 + '}{' + l2 +'}' # verificar si los hijos son hojas o no
        elif nt['val'] == '^':
            return l1 + '^{' + l2 +'}' # verificar si los hijos son hojas o no


#convierte un árbol en una expresión de latex
#que resume las operaciones representadas en el árbol
def nstd_tree2ltx_nums(nt):
    #averigua si el nodo es una hoja
    if not ('h1' in nt.keys()):
        return latex(nt['val'])
    elif not ('h2' in nt.keys()): #función
        l1 = nstd_tree2ltx_nums(nt['h1'])
        funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log']
        if nt['val'] in funcs:
            if nt['val'] != 'sqrt':
                return '\\'+nt['val']+'\\left({'+l1+'}\\right)'
            else:
                return '\\'+nt['val']+'{'+l1+'}'        
    else: #dos hijos
        l1 = nstd_tree2ltx_nums(nt['h1'])
        l2 = nstd_tree2ltx_nums(nt['h2'])
        if nt['val'] == '+': 
            if l2[0] == '-':
                return l1+''+l2
            else:
                return l1 + '+' + l2
        elif nt['val'] == '-': 
            if l2[0] == '-' or varios_terminos(l2):
                if l1 == '0':
                    return '-\\left('+l2+'\\right)'
                else:
                    return l1+'-\\left('+l2+'\\right)'
            else:
                if l1 == '0':
                    return '-' + l2
                else:
                    return l1 + '-' + l2            
        elif nt['val'] == '*':
            if varios_terminos(l1) or varios_factores(l1,False):
                f1 = '\\left(' + l1 + '\\right)'                
            elif l1 == '-1':
                f1 = '-'
            elif l1 == '1':
                f1 = ''
            else:
                f1 = l1
            if l2[0] == '-' or varios_terminos(l2) or varios_factores(l2,False):
                f2 = '\\left(' + l2 + '\\right)'
            else:
                f2 = l2
            if (is_number(f1) or is_rational(f1)) or (is_number(f2) or is_rational(f2)):
                return f1 + '\\times ' + f2
            #elif (is_number(f1) or is_rational(f1)) or (is_number(f2) or is_rational(f2))
             
            return f1 + f2              
        elif nt['val'] == '/':            
            f1 = l1
            f2 = l2
            return '\\frac{' + f1 + '}{' + f2 +'}' # verificar si los hijos son hojas o no
        elif nt['val'] == '^':
            if varios_terminos(l1) or varios_factores(l1,False):
                f1 = '\\left(' + l1 + '\\right)'
            elif nt['h1']['val'] in ['+','-','*','/']:
                f1 = '\\left(' + l1 + '\\right)'                
            else:
                f1 = l1
            f2 = l2
            return f1 + '^{' + f2 +'}' # verificar si los hijos son hojas o no

       
def nstd_tree_binary_op(nt1,nt2,op):
    nt = {'h1':nt1, 'h2':nt2, 'val':op}
    return nt         


def multiplica_terminos(nt,nt_fact,symbs,funcs):
    fact = nstd_tree2expr(nt_fact,symbs,funcs)
    if not 'h1' in nt.keys() or not 'h2' in nt.keys():
        f_nt = multiplica_termino(nt,fact,symbs,funcs)
        nt['val'] = f_nt['val']
        if 'h1' in f_nt.keys():
            nt['h1'] = f_nt['h1']
        if 'h2' in f_nt.keys():
            nt['h2'] = f_nt['h2']            
    else: #operador binario
        if nt['val'] == '+' or nt['val'] == '-':
            multiplica_terminos(nt['h1'],nt_fact,symbs,funcs)
            multiplica_terminos(nt['h2'],nt_fact,symbs,funcs)
        else:
            f_nt = multiplica_termino(nt,fact,symbs,funcs)
            nt['val'] = f_nt['val']
            if 'h1' in f_nt.keys():
                nt['h1'] = f_nt['h1']
            if 'h2' in f_nt.keys():
                nt['h2'] = f_nt['h2']          
            

#el árbol en nt debe ser un término
def multiplica_termino(nt,fact,symbs,funcs):
    exp_nt = nstd_tree2expr(nt,symbs,funcs)
    ne = fact*exp_nt
    ltx_ne = latex(ne)
    ne_t = ltx2nstd_tree(ltx_ne,symbs,funcs)       
    return ne_t
    
def denominadores(nt,s_den,symbs,funcs):
    if nt['val'] in ['+','-']:
        if nt['h1']['val'] == '/':
            e = nstd_tree2expr(nt['h1']['h2'],symbs,funcs)
            s_den.add(e)
        elif nt['h1']['val'] in ['+','-','/','*']:
            denominadores(nt['h1'],s_den,symbs,funcs)
            
        if nt['h2']['val'] == '/':
            #if type(nt['h2']['h2']['val']) == type(1):
            e = nstd_tree2expr(nt['h2']['h2'],symbs,funcs)
            s_den.add(e)
        elif nt['h2']['val'] in ['+','-','/','*']:
            denominadores(nt['h2'],s_den,symbs,funcs)
    elif nt['val'] == '*':
        d1 = 1
        d2 = 1
        if nt['h1']['val'] == '/':
            #if type(nt['h1']['h2']['val']) == type(1):
            d1 = nstd_tree2expr(nt['h1']['h2'],symbs,funcs)
        if nt['h2']['val'] == '/':
            #if type(nt['h2']['h2']['val']) == type(1):
            d2 = nstd_tree2expr(nt['h2']['h2'],symbs,funcs)
        if d1 != 1 or d2 != 1:
            s_den.add(d1*d2)      
    if nt['val'] == '/':
        #if type(nt['h2']['val']) == type(1):
        e = nstd_tree2expr(nt['h2'],symbs,funcs)
        s_den.add(e)

#la función que exxtrae los términos debe indicar s el término es un subábol o una hoja        
def terminos(nt, s_trms, symbs, funcs, sig, lev):
    tps = [int, numbers.One, numbers.Integer, numbers.NegativeOne, numbers.Rational, numbers.Half, add.Add, mul.Mul, symbol.Symbol]  
        
    if not 'h1' in nt.keys(): #si es una hoja es simplificable (las hojas tienen combinaciones lineales de variables)
        if nt['val'] != 0:
            e = nstd_tree2expr(nt,symbs,funcs)        
            if type(e) in tps:
                s_trms.append({'t':sig*e,'rt':lev})
    elif nt['val'] in ['+', '-']:
        if lev != '':
            pr = '_'
        else:
            pr = ''
            
        terminos(nt['h1'],s_trms, symbs, funcs, sig, lev+pr+'h1')
        if nt['val'] == '+':
            terminos(nt['h2'],s_trms, symbs, funcs, sig, lev+pr+'h2')
        else:
            terminos(nt['h2'],s_trms, symbs, funcs, -sig, lev+pr+'h2')
    else:
        e = nstd_tree2expr(nt,symbs,funcs)        
        s_trms.append({'t':factor(sig*e),'rt':lev})

#la función que exxtrae los términos debe indicar s el término es un subábol o una hoja
def terminos_semejantes(nt, symbs):
    int_typs = [int, numbers.One, numbers.Integer, numbers.NegativeOne]
    rat_typs = [    ]
    ex_typs = [add.Add, mul.Mul, symbol.Symbol]
    trms_sem = {}
    
    s_trms = []
    terminos(nt, s_trms, symbs, [], 1, '')

    #resume los términos semejantes    
    for t in s_trms:
        e = t['t']
        
        #averigua el tipo de término
        if type(e) in int_typs: #término constante            
            if not 'cte' in trms_sem.keys():
                trms_sem['cte'] = {'rts':[t['rt']], 'coefs':[e]}
            else:
                trms_sem['cte']['rts'].append(t['rt'])
                trms_sem['cte']['coefs'].append(e)
        elif type(e) in rat_typs:
            if not 'rat' in trms_sem.keys():
                trms_sem['rat'] = {'rts':[t['rt']], 'coefs':[e]}
            else:
                trms_sem['rat']['rts'].append(t['rt'])
                trms_sem['rat']['coefs'].append(e)
            
        elif type(t['t']) in ex_typs:
            #extrae el coeficiente                
            ec = e.as_coeff_Mul()
            coef = ec[0]
            vk = ec[1]
            if not vk in trms_sem.keys():
                trms_sem[vk] = {'rts':[t['rt']], 'coefs':[coef]}
            else:
                trms_sem[vk]['rts'].append(t['rt'])
                trms_sem[vk]['coefs'].append(coef)
        #else: #el término es más complejo ()posiblemente elr esultadod e un subárbol
        #    k = 'sub
            
    return trms_sem
            

def nodo(nt, rt):
    path = rt.split('_')
    n = nt
    if path != ['']:
        for h in path:
            n = n[h]
    return n
    
def nodo_padre(nt, rt):
    path = rt.split('_')
    n = nt
    if path != ['']:
        for h in path[:-1]:
            n = n[h]
    return n
    
#accede al nodo dentro del árbol (nt) y le cambia el valor (v)
# se da por sentado que el nodo es una hoja (rt tiene la ruta al nodo)
# si el valor no e sun entero
def nod_val(nt,rt,v):
    #int_typs = [int, numbers.Integer, numbers.One, numbers.Zero]
    #rat_typs = [numbers.Rational, numbers.Half]
    path = rt.split('_')
    n = nt
    if path != ['']:
        for h in path:
            n = n[h]
    #si el nodo es una combinación lineal de una variable, separa sus valores 
    # 3a+1, por ejempo, se convierte en [+, [*,3,a],[1]]
    #if type(v) in int_typs or type(v) in rat_typs or type(v) == symbol.Symbol:
    n['val'] = v
    if 'h1' in n.keys():
        n.pop('h1',None)
    if 'h2' in n.keys():
        n.pop('h2',None)
    '''
    elif type(v) in [mul.Mul, add.Add]:
        #separa la expresión en términos
        ot = v.as_ordered_terms()
        if len(ot) == 1:
            n['val'] = v
            if 'h1' in n.keys():
                n.pop('h1',None)
            if 'h2' in n.keys():
                n.pop('h2',None)
        elif len(ot) 
    '''
        
def comb_lin_ents(v,x):
    #int_tps = [type(0), type(1)]
    int_typs = [type(1), type(x/x), type(2*x/x), type(0*x), type(-x/x)]
    exp_tps = [type(x), type(2*x), type(2*x+2)]
    a = Wild('a', exclude=[x])
    b = Wild('b', exclude=[x])
    
    if type(v) == type(0):
        return True
    elif type(v) in exp_tps:
        m = v.match(a*x+b)
        #si fue posible empatar el patrón
        if m and type(m[a]) in int_typs and type(m[b]) in int_typs:
            return True
        else:
            return False
    else:
        return False

#reduce los nodos que tengan como valor un cero        
#simplifica la suma o resta de nodos con cero
def elimina_ceros(nt):
    if nt['val'] == '+':
        if nt['h1']['val'] == 0:
            nc = copy(nt['h2'])
            
            nt['val'] = nc['val']
            if 'h1' in nc.keys():
                nt['h1'] = nc['h1']
            elif 'h1' in nt.keys():
                nt.pop('h1',None)
            if 'h2' in nc.keys():
                nt['h2'] = nc['h2']
            elif 'h2' in nt.keys():
                nt.pop('h2',None)
            
            #se asegura de seguir eliminando los ceros en los hijos del actual nodo en caso de haberlos
            if 'h1' in nt.keys():
                elimina_ceros(nt)                
                
        elif nt['h2']['val'] == 0:
            #copia el primer hijo
            nc = copy(nt['h1'])
            nt['val'] = nc['val']
            if 'h1' in nc.keys():
                nt['h1'] = nc['h1']
            elif 'h1' in nt.keys():
                nt.pop('h1',None)
            if 'h2' in nc.keys():
                nt['h2'] = nc['h2']
            elif 'h2' in nt.keys():
                nt.pop('h2',None)
                
            #se asegura de seguir eliminando los ceros en los hijos del actual nodo en caso de haberlos
            if 'h1' in nt.keys():
                elimina_ceros(nt)
                
        else:
            elimina_ceros(nt['h1'])
            elimina_ceros(nt['h2'])
            if nt['h1']['val'] == 0 or nt['h2']['val'] == 0:
                elimina_ceros(nt)
                
    elif nt['val'] == '-':
        if nt['h1']['val'] == 0:
            #copia el segundo hijo siempre y cuando sea una hoja
            if not 'h1' in nt['h2'].keys():
                nt['val'] = -nt['h2']['val']
                nt.pop('h1',None)
                nt.pop('h2',None)
            else:
                nt['val'] = '*'
                nt['h1']['val'] = -1                
                elimina_ceros(nt['h2'])
        elif nt['h2']['val'] == 0:
            #copia el primer hijo
            nc = copy(nt['h1'])
            nt['val'] = nc['val']
            if 'h1' in nc.keys():
                nt['h1'] = nc['h1']
            elif 'h1' in nt.keys():
                nt.pop('h1',None)
            if 'h2' in nc.keys():
                nt['h2'] = nc['h2']
            elif 'h2' in nt.keys():
                nt.pop('h2',None)
            
            #se asegura de seguir eliminando los ceros en los hijos del actual nodo en caso de haberlos
            if 'h1' in nt.keys():
                elimina_ceros(nt)
        else:
            elimina_ceros(nt['h1'])
            elimina_ceros(nt['h2'])
            if nt['h1']['val'] == 0 or nt['h2']['val'] == 0:
                elimina_ceros(nt)
                
    else:
        #se asegura de seguir eliminando los ceros en los hijos del actual nodo en caso de haberlos
        if 'h1' in nt.keys():
            elimina_ceros(nt['h1'])
        if 'h2' in nt.keys():
            elimina_ceros(nt['h2'])
        if 'h1' in nt.keys() and 'h2' in nt.keys():
            if nt['h1']['val'] == 0 or nt['h2']['val'] == 0:
                elimina_ceros(nt)
    
def reduce_terminos(nt,symbs):
    single_typs = [int, numbers.Integer, numbers.One, numbers.Zero, numbers.Rational, numbers.Half, symbol.Symbol]
    ex_typs = [add.Add, mul.Mul]
    strms = []
    trms_rdcd = []
    terminos(nt, strms, symbs, [], 1, "")
    
    if len(strms) > 1:
        #revisa que exista más de un término que sea una combinación lineal de 
        x = symbols(symbs[0]) #supongo que es una sola variable
        for t in strms:
            if comb_lin_ents(t['t'],x):
                trms_rdcd.append(t)
        if len(trms_rdcd) > 1:
            res = 0
            for t in trms_rdcd:
                res = res+t['t']
                nod_val(nt,t['rt'],0)
            elimina_ceros(nt)
            #agrega un la suma de términos
            nnt = {}
            
            if nt['val'] == 0:
                #averigua si res tiene uno o más términos
                if type(res) in single_typs:
                    nnt['val'] = res
                elif type(res) in ex_typs:
                    ot = res.as_ordered_terms()
                    if len(ot) == 2 and type(ot[0]) in ex_typs and type(ot[1]) in single_typs:
                        nnt['val'] = '+'
                        nnt['h1'] = {'val':ot[0]}
                        nnt['h2'] = {'val':ot[1]}
                    else:
                        nnt['val'] = res
                else:
                    nnt['val'] = res                        
            else:
                nnt['val'] = '+' 
                nnt['h1'] = nt
                nh2 = {}
                if type(res) in single_typs:
                    nh2['val'] = res
                elif type(res) in ex_typs:
                    ot = res.as_ordered_terms()
                    if len(ot) == 2 and type(ot[0]) in ex_typs and type(ot[1]) in single_typs:
                        nh2['val'] = '+'
                        nh2['h1'] = {'val':ot[0]}
                        nh2['h2'] = {'val':ot[1]}
                    else:
                        nh2['val'] = res
                else:
                    nh2['val'] = res                    
                
                nnt['h2'] = nh2
            #copia el nuevo árbol
            return nnt
                        
#acomoda los términos racionales, los múltiplos de alguna variable
#y los deja un un nodo, por ejemplo, 3/4, 3*x podrían ser elementos de un nodo
def inicia_rational_escx_nodes(nt):
    int_typs = [int, numbers.One, numbers.Integer, numbers.Zero, numbers.NegativeOne]
    exp_tps = [symbol.Symbol, mul.Mul, add.Add]
    
    if nt['val'] == '*':        
        if type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in exp_tps:
            nt['val'] = nt['h1']['val']*nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_rational_escx_nodes(nt['h1'])
            inicia_rational_escx_nodes(nt['h2'])
    elif nt['val'] == '/':
        if type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in int_typs:
            nt['val'] = Rational(nt['h1']['val'],nt['h2']['val'])
            nt.pop('h1',None)
            nt.pop('h2',None)
        elif type(nt['h1']['val']) in exp_tps and type(nt['h2']['val']) in int_typs:
            nt['val'] = nt['h1']['val']/nt['h2']['val']
            nt.pop('h1',None)
            nt.pop('h2',None)
        elif nt['h1']['val'] == '*' and type(nt['h1']['h1']['val']) in int_typs and type(nt['h1']['h2']['val']) in exp_tps and type(nt['h2']['val']) in int_typs:
            nt['h1']['val'] = nt['h1']['h1']['val']*nt['h1']['h2']['val']
            nt['h1'].pop('h1',None)
            nt['h1'].pop('h2',None)
            nt['val'] = nt['h1']['val']/nt['h2']['val']
            nt.pop('h1',None)
            nt.pop('h2',None)                            
        else:
            inicia_rational_escx_nodes(nt['h1'])
            inicia_rational_escx_nodes(nt['h2'])        
    else:
        if 'h1' in nt.keys():
            inicia_rational_escx_nodes(nt['h1'])
        if 'h2' in nt.keys():
            inicia_rational_escx_nodes(nt['h2'])
            
#aco0moda ls términos racionales, los múltiplos de alguna variable
#y los deja un un nodo, por ejemplo, 3/4, 3*x podrían ser elementos de un nodo
def inicia_rational_nodes(nt):
    int_typs = [int, numbers.One, numbers.Integer, numbers.Zero, numbers.NegativeOne]
    exp_tps = [symbol.Symbol, mul.Mul, add.Add]
    
    if nt['val'] == '*':        
        if type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in exp_tps:
            nt['val'] = nt['h1']['val']*nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_rational_nodes(nt['h1'])
            inicia_rational_nodes(nt['h2'])
    elif nt['val'] == '/':
        if type(nt['h1']['val']) in int_typs and type(nt['h2']['val']) in int_typs:
            nt['val'] = Rational(nt['h1']['val'],nt['h2']['val'])
            nt.pop('h1',None)
            nt.pop('h2',None)
        elif type(nt['h1']['val']) in exp_tps and type(nt['h2']['val']) in int_typs:
            nt['val'] = nt['h1']['val']/nt['h2']['val']        
            nt.pop('h1',None)
            nt.pop('h2',None)
        else:
            inicia_rational_nodes(nt['h1'])
            inicia_rational_nodes(nt['h2'])        
    else:
        if 'h1' in nt.keys():
            inicia_rational_nodes(nt['h1'])
        if 'h2' in nt.keys():
            inicia_rational_nodes(nt['h2'])

               
def rand_nt(nnods, leaves, opers):
    nt = {}
    #inicia el nodo raíz
    nt['val'] = sample(leaves,1)[0]
    nods = ['']    
    
    while len(nods) < nnods:
        #selecciona una hoja aleatoriamente
        ruta = sample(nods,1)[0]
        n = nodo(nt,ruta)                
        n['val'] = sample(opers,1)[0]
        n['h1'] = {'val':sample(leaves,1)[0]}
        n['h2'] = {'val':sample(leaves,1)[0]}
        
        if ruta != '':
            nods.append(ruta+'_h1')
            nods.append(ruta+'_h2')
        else:
            nods.append(ruta+'h1')
            nods.append(ruta+'h2')
        nods.remove(ruta)    
    return nt

def mod_mon(m,degs=range(1,6)):
    fs = m.as_ordered_factors()
    nm = 1
    for f in fs:
        (b,e) = f.as_base_exp()
        nm *= b**sample(degs,1)[0]
    return nm

def rand_nt_pot(nnods, leaves, opers, exps):
    nt = {}
    #inicia el nodo raíz
    nt['val'] = sample(leaves,1)[0]
    nods = ['']
    nn = 1
    while nn < nnods:
        #selecciona una hoja aleatoriamente
        ruta = sample(nods,1)[0]
        n = nodo(nt,ruta)
        op = sample(opers,1)[0]        
        n['val'] = op
        
        nm = mod_mon(sample(leaves,1)[0],exps)
        
        n['h1'] = {'val':nm}
        if op == '^':
            n['h2'] = {'val':sample(exps,1)[0]}            
        else:
            nm = mod_mon(sample(leaves,1)[0],exps)
            n['h2'] = {'val':nm}
        if ruta != '':
            nods.append(ruta+'_h1')
            if op != '^':
                nods.append(ruta+'_h2')
        else:
            nods.append(ruta+'h1')
            if op != '^':
                nods.append(ruta+'h2')
        nods.remove(ruta)
        nn += 1    
    return nt

#supone que un ingresa un árbol binario
def reduce_nt(nt, ruta, symbs, functs):
    #sustituye el nodo marcado en n_lab on al evaluación del subárbol
    n = nodo(nt, ruta)
    e = nstd_tree2expr(n, symbs, functs,exp_pow_b=True)
    
    n['val'] = expand_power_base(e,force=True)
    n.pop('h1',None)
    n.pop('h2',None)

#guarda la etiqueta de cada nodo en el arreglo labs
def nods_labs(nt, clab, labs):
    labs.append(clab)
    if 'h1' in nt.keys():
        if clab != '':
            nods_labs(nt['h1'], clab+'_h1', labs)
        else:
            nods_labs(nt['h1'], clab+'h1', labs)
    if 'h2' in nt.keys():
        if clab != '':
            nods_labs(nt['h2'], clab+'_h2', labs)
        else:
            nods_labs(nt['h2'], clab+'h2', labs)
            
def deepest_oper_node(labs):
    lns = [len(l) for l in labs]
    m = max(lns)
    #lns = [v for v in lns]
    idx_m = lns.index(m)
    return labs[idx_m]
           

#dado un árbol, identifica la hoja a mayor profundidad
def nstd_proc(nt, symbs, functs, nums=False, pots=False):
    proc = '\\begin{align}'
    lst_stp = nstd_tree2ltx(nt,numbs=nums,pots=pots)
    proc += lst_stp    
    labs = []
    nods_labs(nt, '', labs)    
    
    rt = deepest_oper_node(labs)
    if rt.find('_')>=0:
        rt = rt[:-3]
    else:
        rt = ''
    in_root = False
    while not in_root:    
        reduce_nt(nt, rt, symbs, functs)
        new_stp = nstd_tree2ltx(nt,numbs=nums,pots=pots)
        if new_stp != lst_stp:
            proc += '&='+new_stp+'\\\\'
            lst_stp = new_stp            
             
        if rt == '':
            in_root = True
        else:
            labs = []
            nods_labs(nt, '', labs)    
            
            rt = deepest_oper_node(labs)
            if rt.find('_')>=0:
                rt = rt[:-3]
            else:
                rt = ''
    proc += '\\end{align}'
    return proc

def find_sub_forw(st1, st2):
    n1 = len(st1)
    n2 = len(st2)
    n = n1 if n1 < n2 else n2 
    for i in range(n):
        if st1[i] != st2[i]:
            return i
    return i+1

def find_sub_backw(st1, st2):
    n1 = len(st1)
    n2 = len(st2)
    n = n1 if n1 < n2 else n2 
    for i in range(n):
        if st1[-(i+1)] != st2[-(i+1)]:
            return i
    return i-1

def diff_strs(st1,st2):
    iforw = find_sub_forw(st1, st2)    
    iback = find_sub_backw(st1, st2)
    
    if iback != 0:        
        return [st1[iforw:(-iback)], st2[iforw:(-iback)]]         
    else:
        return [st1[iforw:], st2[iforw:]]

#regresa un conjunto con los operadores encontrados en el árbol
def ops_in_nstd_tree(nt,ops_set):
    ops = ["+","-","*","/","^"]
    if nt['val'] in ops:
        ops_set.add(nt['val'])
        if 'h1' in nt.keys():
            ops_in_nstd_tree(nt['h1'], ops_set)
        if 'h2' in nt.keys():
            ops_in_nstd_tree(nt['h2'], ops_set)

#genera la lista de nodos del árbol
def lista_nodos(nt,rt,lista):
    if rt == '':
        pre = rt
    else:
        pre = rt+'_'
    if 'h1' in nt.keys():
        rt = pre+'h1'
        lista.append(rt)
        lista_nodos(nt['h1'], rt, lista)
    if 'h2' in nt.keys():
        rt = pre+'h2'
        lista.append(rt)
        lista_nodos(nt['h2'], rt, lista)
        
#dado un árbol, identifica la hoja a mayor profundidad
def cmplxnstd_proc(nt):
    proc = '\\begin{align}'
    lst_stp = cmplxnstd_tree2ltx(nt)
    proc += lst_stp    
    
    labs = []
    nods_labs(nt, '', labs)    
    
    rt = deepest_oper_node(labs)
    if rt.find('_')>=0:
        rt = rt[:-3]
    else:
        rt = ''
    in_root = False
    while not in_root:    
        reduce_nt(nt, rt, ['i'], [])
        new_stp = cmplxnstd_tree2ltx(nt)
        if new_stp != lst_stp:
            proc += '&='+new_stp+'\\\\'
            lst_stp = new_stp            
             
        if rt == '':
            in_root = True
        else:
            labs = []
            nods_labs(nt, '', labs)    
            
            rt = deepest_oper_node(labs)
            if rt.find('_')>=0:
                rt = rt[:-3]
            else:
                rt = ''
    proc += '\\end{align}'
    return proc
        
if __name__ == "__main__":
    
    ltx = "\\frac{\\sin{3x}}{4x+1}"
    smbs = ['x']
    functs = ['sin']
    nt = ltx2nstd_tree(ltx,smbs,functs)
    #print nt
    #plot_nstd_tree(nt)
    
    '''    
    ltx = '(2+3i)/(5+4i)'
    nt = ltx2nstd_tree_cmplx_nodes(ltx)
    print cmplxnstd_tree2ltx(nt)
    print cmplxnstd_tree2expr(nt)
    '''
    #print nstd_tree2ltx(nt)

    
    #print nstd_tree2expr(nt)