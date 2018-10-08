# importing packages
from pulp import *
import csv
import time
from numpy import matmul
from numpy import random
from numpy import zeros
from numpy import exp
from numpy import sqrt
# Define variables
pointvec=[]
cvec=[]
dvec=[]
gvec=[]
pricevec=[]
wvec=[]
utilvec=[]
initteammat=[]
namevec=[]
initcovmat=[]
initteam=[]

# Read in CSVs
with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highmeanteam.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/namevec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        namevec.append(row[0])

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/pointvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        pointvec.append(float(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/cvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        cvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/dvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        dvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/gvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        gvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/pricevec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        pricevec.append(float(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/wvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        wvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/utilvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        utilvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/teammats.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteammat.append(row)

teammat=initteammat

for i in list(range(0,len(initteammat))):
    for j in list(range(0,len(initteammat[i]))):
        teammat[i][j]=int(initteammat[i][j])

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/covmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initcovmat.append(row)

covmat=initcovmat

for i in list(range(0,len(initcovmat))):
    for j in list(range(0,len(initcovmat[i]))):
        covmat[i][j]=float(initcovmat[i][j])


# Define some useful general list functions
def uniquelist(list):
    final_list = []
    for num in list:
        if num not in final_list:
            final_list.append(num)
    return final_list

def posone(list,n):
    i=0
    j=n
    while i< len(list):
        if list[i]==1:
            j=j-1
        if j==0:
            return i
        i=i+1
    return len(list)

# Define some Draftkings specific functions
def conteam(team):
    return matmul(cvec,team)

def wonteam(team):
    return matmul(wvec,team)

def donteam(team):
    return matmul(dvec,team)

def gonteam(team):
    return matmul(gvec,team)

def utilonteam(team):
    return matmul(utilvec,team)

def teamsal(team):
    return matmul(pricevec,team)

def teampairs(team):
    return matmul(teammat,team)

# Define function to remove players from team at random
def smallteam(oldteam,numbdropped):
    team=oldteam
    for i in list(range(0,numbdropped)):
        if sum(team)>1:
            rand=random.randint(0,sum(team))
        else:
            rand=0
        removevec=zeros(len(oldteam),)
        removevec[posone(team,rand+1)]=1
        team=team-removevec
    return team

testteam=smallteam(initteam,1)

#Define function to find a suitable vector to add
def addvec(team,objvec):
    prob = LpProblem("Team", LpMaximize)
    player_vars = []
    numplayers=list(range(0,len(team)))
    for i in numplayers:
        player_vars.append(LpVariable("Player " + str(i), 0, 1, cat="Binary"))
    prob += lpSum([objvec[i] * player_vars[i] for i in numplayers])
    pairs=teampairs(team)
    initconstrs = []
    initconstrs.append(lpSum([player_vars[i] * cvec[i] for i in numplayers]) <= 3-conteam(team))
    initconstrs.append(lpSum([player_vars[i] * cvec[i] for i in numplayers]) >= 2-conteam(team))
    initconstrs.append(lpSum([player_vars[i] * wvec[i] for i in numplayers]) >= 3-wonteam(team))
    initconstrs.append(lpSum([player_vars[i] * wvec[i] for i in numplayers]) <= 4-wonteam(team))
    initconstrs.append(lpSum([player_vars[i] * dvec[i] for i in numplayers]) >= 2-donteam(team))
    initconstrs.append(lpSum([player_vars[i] * dvec[i] for i in numplayers]) <= 3-donteam(team))
    initconstrs.append(lpSum([player_vars[i] * utilvec[i] for i in numplayers]) == 8-utilonteam(team))
    initconstrs.append(lpSum([player_vars[i] * gvec[i] for i in numplayers]) == 1-gonteam(team))
    initconstrs.append(lpSum([player_vars[i] * pricevec[i] for i in numplayers]) <= 50001-teamsal(team))
    for i in numplayers:
        if team[i]==1:
            initconstrs.append(player_vars[i]==0)
    teamconstrs = []
    for j in list(range(0, len(teammat))):
        teamconstrs.append(lpSum([player_vars[i] * teammat[j][i] for i in numplayers]) <= 7-pairs[j])
    constrs = initconstrs + teamconstrs
    for i in list(range(0, len(constrs))):
        prob += constrs[i]
    prob.solve()
    teamout = []
    for i in numplayers:
        teamout.append(player_vars[i].varValue)
    return teamout

# Define function to decide if move to new team
def acceptmove(oldteam,newteam,temp,objfunc):
    newrand=random.random()
    oldobj=objfunc(oldteam)
    newobj=objfunc(newteam)
    if newobj>= oldobj:
        team=newteam
    elif newrand<= exp((newobj-oldobj)/temp):
        team=newteam
    else:
        team=oldteam
    return team

# Define simulated annealing routine
def simann(x0,numbswaps,objfunc,grad,temp,randscale,its):
    team=x0
    bestteam=x0
    dim=len(team)
    for i in list(range(0,its)):
        tempteam=smallteam(team,numbswaps)
        randpert=random.random(dim)
        gradvec=grad(tempteam)+randscale*randpert
        newplayers=addvec(tempteam,gradvec)
        trialteam=tempteam+newplayers
        team=acceptmove(team,trialteam,temp,objfunc)
        if objfunc(team) >= objfunc(bestteam):
            bestteam=team
    return bestteam

# Define test objective and grad
def testobj(team):
    return matmul(pointvec,team)+2*sqrt(matmul(team,matmul(covmat,team)))

def testgrad(team):
    return pointvec+matmul(covmat,team)/sqrt(matmul(matmul(covmat,team),team))

def testobj2(team):
    return matmul(pointvec,team)+3*sqrt(matmul(team,matmul(covmat,team)))

def testgrad2(team):
    return pointvec+(3/2)*matmul(covmat,team)/sqrt(matmul(matmul(covmat,team),team))

def testobj3(team):
    return matmul(pointvec,team)+1*sqrt(matmul(team,matmul(covmat,team)))

def testgrad3(team):
    return pointvec+(1/2)*matmul(covmat,team)/sqrt(matmul(matmul(covmat,team),team))

# Run optimization
start=time.time()
outputteam=simann(initteam,4,testobj,testgrad,0.05,0.5,30)
outputteam2=simann(initteam,4,testobj,testgrad,0.05,0.5,30)
outputteam3=simann(initteam,4,testobj2,testgrad2,0.05,0.5,30)
outputteam4=simann(initteam,4,testobj2,testgrad2,0.05,0.5,30)
outputteam5=simann(initteam,4,testobj3,testgrad3,0.05,0.5,30)
outputteam6=simann(initteam,4,testobj3,testgrad3,0.05,0.5,30)
end=time.time()


for i in list(range(0,len(outputteam))):
    if outputteam[i]==1:
        print(namevec[i])
print(conteam(outputteam))
print(teamsal(outputteam))
print(sum(outputteam))
print(matmul(pointvec,outputteam))
print(sqrt(matmul(matmul(covmat,outputteam),outputteam)))
print(testobj(outputteam))
print(end-start)

teamstring1=[]
for i in list(range(0,len(outputteam))):
    teamstring1.append(str(outputteam[i]))

teamstring2=[]
for i in list(range(0,len(outputteam2))):
    teamstring2.append(str(outputteam2[i]))

teamstring3=[]
for i in list(range(0,len(outputteam3))):
    teamstring3.append(str(outputteam3[i]))

teamstring4=[]
for i in list(range(0,len(outputteam4))):
    teamstring4.append(str(outputteam4[i]))

teamstring5=[]
for i in list(range(0,len(outputteam5))):
    teamstring5.append(str(outputteam5[i]))

teamstring6=[]
for i in list(range(0,len(outputteam6))):
    teamstring6.append(str(outputteam6[i]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam1.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring1)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam2.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring2)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam3.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring3)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam4.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring4)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam5.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring5)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam6.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring6)
