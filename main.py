# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 18:21:38 2016

@author: JayaramK
"""


import numpy as np
import xlrd 

import scipy.stats as sp
import matplotlib.pyplot as plt
import math 

 
wb = xlrd.open_workbook('university data.xlsx')
ws = wb.sheet_by_index(0)
 
 
print("UBitName:jayaramk")
print("personNumber:50208766")
 


csscore = [] 
for row in range (1,50) :
    csscore.append(ws.cell(row,2).value)
    

researchoverhead = [] 
for row in range (1,50):
   researchoverhead.append(ws.cell(row,3).value)
   
adminbasepay = []
for row in range (1,50):
    adminbasepay.append(ws.cell(row,4).value)

tuition = []
for row in range (1,50):
     tuition.append(ws.cell(row,5).value)



mu1= np.round(np.mean(csscore),3)
print('mu1='+ str(mu1))
mu2= np.round(np.mean(researchoverhead),3)
print('mu2='+ str(mu2))
mu3= np.round(np.mean(adminbasepay),3)
print('mu3='+ str(mu3))
mu4= np.round(np.mean(tuition),3)
print('mu4='+ str(mu4))

var1= np.round (np.var(csscore),3)
print('var1='+ str(var1))
var2=np.round( np.var(researchoverhead),3)
print('var2='+ str(var2))
var3= np.round (np.var(adminbasepay),3)
print('var3='+ str(var3))
var4= np.round (np.var(tuition),3)
print('var4='+ str(var4))

sigma1= np.round(np.std(csscore),3)
print('sigma1='+ str(sigma1))
sigma2= np.round( np.std(researchoverhead),3)
print('sigma2='+ str(sigma2))
sigma3= np.round(np.std(adminbasepay),3)
print('sigma3='+ str(sigma3))
sigma4=np.round(np.std(tuition),3)
print('sigma4='+ str(sigma4))



  
t1 = np.vstack([csscore,researchoverhead,adminbasepay,tuition])


covarianceMat = []
covarianceMat = np.matrix.round(np.cov(t1),3)
print("covarianceMat=")
print(covarianceMat)


correlationMat = []
correlationMat = np.matrix.round(np.corrcoef(t1),3)
print("correlationMat=")
print(correlationMat)



'''
code for making the pairwise plots '''
names = ['csscore','researchoverhead','adminbasepay','tuition']


mainarray = [csscore,researchoverhead,adminbasepay,tuition]

count = 0 

for i in range(0,4):
    for j in range(0,4):    
        count+=1
        
        plt.subplot(4,4,count)
        plt.scatter(mainarray[i],mainarray[j])
        plt.xlabel(names[i])
        plt.ylabel(names[j])
        plt.show()


csscore_logpdf = 0 
researchoverhead_logpdf = 0 
adminbasepay_logpdf = 0
tuition_logpdf = 0
logLikelihood = 0 



for x in csscore: 
    csscore_logpdf += sp.norm.logpdf(x,mu1,sigma1)
for x in researchoverhead :    
    researchoverhead_logpdf += sp.norm.logpdf(x,mu2,sigma2)
for x in adminbasepay:    
    adminbasepay_logpdf += sp.norm.logpdf(x,mu3,sigma3)
for x in tuition:    
    tuition_logpdf += sp.norm.logpdf(x,mu4,sigma4) 

logLikelihood = csscore_logpdf +researchoverhead_logpdf+adminbasepay_logpdf+tuition_logpdf
logLikelihood = round(logLikelihood,3)

print("logLikelihood=") 
print(logLikelihood)




'Code for bayesian network'
def loglikelihoodfunction(Parent,numparents,y):
    temp = 0
    A = np.empty([numparents,numparents])
    for j in range(0,numparents):
        for i in range(0,numparents):
            temp = 0            
            for  s in range(0,49):
                temp += (Parent[i][s] *Parent[j][s])
            A[i][j] = temp
    ymod = np.zeros(shape=(1,numparents))    
 
    for u in range(0,numparents):
        temp = 0
        for  s in range(0,49):            
             temp+= y[s]*Parent[u][s]          
        ymod[0][u] = temp          
    ymod2 = np.transpose(ymod)    
        
    beta = np.linalg.solve(A,ymod2)        
   
    sum2 = 0
    sum3 = 0    
    for s in range(0,49):
      sum2 = 0  
      for i in range(0,numparents): 
          sum2+= beta[i][0]*Parent[i][s]          
      sum3+=(sum2-y[s])**2         
    sigmasqr =sum3/49         
 
    LTheta = 0
       
    
    for s in range(0,49):    
        sum2= 0       
        for i in range(0,numparents):
            sum2+= beta[i][0]*Parent[i][s]  
        LTheta +=-0.5*(math.log(2*math.pi*sigmasqr))-((0.5 *((sum2-y[s])**2))/sigmasqr)    

    
    return LTheta 
    
   
unitvec =[]
for i in range(0,49):
    unitvec.append(1)
    
BNlogLikelihood_csscore = loglikelihoodfunction([unitvec,researchoverhead,adminbasepay,tuition],4,csscore)
BNlogLikelihood_researchoverhead = loglikelihoodfunction([unitvec],1,researchoverhead)
BNlogLikelihood_adminbasepay = loglikelihoodfunction([unitvec],1,adminbasepay)
BNlogLikelihood_tuition = loglikelihoodfunction([unitvec],1,tuition)



BNlogLikelihood = BNlogLikelihood_csscore + BNlogLikelihood_researchoverhead +BNlogLikelihood_adminbasepay+BNlogLikelihood_tuition

BNgraph = np.empty([4,4])

for i in range(0,4):
    for j in range(0,4):
        BNgraph[i][j] = 0   

BNgraph[1][0] = 1
BNgraph[2][0] = 1
BNgraph[3][0] = 1

print("BNgraph=")
print(BNgraph)

print('BNlogLikelihood=')
print(BNlogLikelihood) 




    
          

               






