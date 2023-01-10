# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 10:49:00 2014

@author: fernando
"""

import csv
from random import shuffle, sample, randint

if __name__ == '__main__':
    f = open('C:\\Users\\fgome\\Documents\\Academia\\Academia\\PropedeuticoDatos\\2017\\Verano\\Log_Eventos\\eventos3.csv','rb')
    f2 = open('C:\\Users\\fgome\\Documents\\Academia\\Academia\\PropedeuticoDatos\\2017\\Verano\\Log_Eventos\\eventos3_r.csv','wb')
    
    csv_reader = csv.reader(f, delimiter=',')
    csv_writr = csv.writer(f2, delimiter=',')
    
    for i,r in enumerate(csv_reader):
        r[6] = r[6][:-1]+'0'
        if i % 100 == 0:
            print r        
        csv_writr.writerow(r)
    f.close()
    f2.close()
    
    