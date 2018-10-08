import csv
import time
from numpy import *
from scipy import stats

# Initialize parameters
pointvec=[]
initcovmat=[]
initteam=[]

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/pointvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        pointvec.append(float(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/covmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initcovmat.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highmeanteam.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam.append(int(row[0]))

covmat=initcovmat

for i in list(range(0,len(initcovmat))):
    for j in list(range(0,len(initcovmat[i]))):
        covmat[i][j]=float(initcovmat[i][j])

corrmat=zeros((len(covmat),len(covmat)),)

for i in list(range(0,len(covmat))):
    for j in list(range(0,len(covmat))):
        corrmat[i][j]=covmat[i][j]/(sqrt(covmat[i][i]*covmat[j][j]))


#define negative binomial conversions
def nbinn(mean,var):
    return (mean**2)/((var)*(1-mean/(var)))

def nbinp(mean,var):
    return mean/(var)

# simulate some random variables (note simulate out of corrmat not covmat)
start=time.time()
rands=random.multivariate_normal(zeros(len(covmat),),corrmat,500)

# transform to cdf equiv to uniform dist
tranrands=zeros((len(rands),len(rands[0]),))
for i in list(range(0,len(rands))):
    for j in list(range(0,len(rands[i]))):
        tranrands[i][j]=stats.norm.cdf(rands[i][j],0,1)

# create vectors of distribution parameters
nvec=zeros(len(pointvec),)
pvec=zeros(len(pointvec),)

for i in list(range(0,len(nvec))):
    nvec[i]=nbinn(2*pointvec[i],4*covmat[i][i])

for i in list(range(0,len(nvec))):
    pvec[i]=nbinp(2*pointvec[i],4*covmat[i][i])

#inverse cdf transform to negative binom
endrands=zeros((len(rands),len(rands[0]),))
for i in list(range(0,len(rands))):
    for j in list(range(0,len(rands[i]))):
        endrands[i][j]=stats.nbinom.ppf(tranrands[i][j],nvec[j],pvec[j])

teamscores=matmul(endrands,initteam)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/simplayerscores.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    for i in list(range(0,len(endrands))):
        writer.writerow(endrands[i]/2)

end=time.time()

print(endrands[0])
print(end-start)
print(mean(teamscores)/2)
print(std(teamscores)/2)
