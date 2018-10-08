import csv
import time
from numpy import *
from scipy import stats
from pulp import *

# Set number of entries and dollars
doubledollar=5
tourndollars=8

doubleentries=10
tournentries=5

# Define and import returns
initdoublerets=[]
inittournrets=[]

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/doubleteamrets.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initdoublerets.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/tournteamrets.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        inittournrets.append(row)

doublerets=initdoublerets
for i in list(range(0,len(initdoublerets))):
    for j in list(range(0,len(initdoublerets[i]))):
        doublerets[i][j]=float(initdoublerets[i][j])

tournrets=inittournrets
for i in list(range(0,len(inittournrets))):
    for j in list(range(0,len(inittournrets[i]))):
        tournrets[i][j]=float(inittournrets[i][j])

# Combine returns and create covariance matrix
totalretmat=zeros((len(doublerets)+len(tournrets),len(tournrets[0])),)
for i in list(range(0,len(totalretmat))):
    for j in list(range(0,len(totalretmat[i]))):
        if i<len(doublerets):
            totalretmat[i][j]=doublerets[i][j]*doubledollar/(doubledollar*doubleentries+tourndollars*tournentries)
        else:
            totalretmat[i][j]=tournrets[i-len(doublerets)][j]*tourndollars/(doubledollar*doubleentries+tourndollars*tournentries)

retmeanvec=zeros(len(totalretmat),)
for i in list(range(0,len(totalretmat))):
    retmeanvec[i]=mean(totalretmat[i])

retcovmat=cov(totalretmat)

# Create inital portfolio
initport=zeros(len(totalretmat),)
for i in list(range(0,len(initport))):
    if i<len(doublerets):
        if doubleentries>=len(doublerets):
            if i==0:
                initport[i]=doubleentries-len(doublerets)+1
            else:
                initport[i]=1
        else:
            if i<doubleentries:
                initport[i]=1
            else:
                initport[i]=0
    else:
        if tournentries>=len(tournrets):
            if i==len(doublerets):
                initport[i]=tournentries-len(tournrets)+1
            else:
                initport[i]=1
        else:
            if i<tournentries+len(doublerets):
                initport[i]=1
            else:
                initport[i]=0

# Define sharpe ratio objective and grad
def srobj(port):
    return matmul(port,retmeanvec)/sqrt(matmul(port,matmul(retcovmat,port)))

def srgrad(port):
    return (retmeanvec*sqrt(matmul(port,matmul(retcovmat,port)))-matmul(port,retmeanvec)*(matmul(retcovmat,port))/(2*sqrt(matmul(port,matmul(retcovmat,port)))))/(matmul(port,matmul(retcovmat,port)))

#Define function to find vector to subtract
def subvec(startport,doubleteams,tournteams,numbswapped):
    prob = LpProblem("Port", LpMaximize)
    team_vars = []
    numteams = list(range(0, doubleteams + tournteams))
    doublevec=zeros(len(numteams),)
    tournvec=zeros(len(numteams),)
    for i in numteams:
        if i<doubleteams:
            doublevec[i]=1
        else:
            doublevec[i]=0
    for i in numteams:
        if i>=doubleteams:
            tournvec[i]=1
        else:
            tournvec[i]=0
    for i in numteams:
        team_vars.append(LpVariable("Team " + str(i), -100, 0, cat="Int"))
    objvec = random.random(len(numteams))
    prob += lpSum([objvec[i] * team_vars[i] for i in numteams])
    initconstrs = []
    initconstrs.append(lpSum([team_vars[i] * (doublevec[i]+tournvec[i]) for i in numteams]) ==-numbswapped)
    minconstrs=[]
    for i in numteams:
        minconstrs.append(team_vars[i]>=-startport[i])
    constrs = initconstrs+minconstrs
    for i in list(range(0, len(constrs))):
        prob += constrs[i]
    prob.solve()
    portout = []
    for i in numteams:
        portout.append(team_vars[i].varValue)
    return portout

#Define function to find a suitable vector to add
def addvec(startport,objvec,doubleteams,tournteams,doubleent,tournent):
    prob = LpProblem("Port", LpMaximize)
    team_vars = []
    numteams = list(range(0, doubleteams + tournteams))
    doublevec=zeros(len(numteams),)
    tournvec=zeros(len(numteams),)
    for i in numteams:
        if i<doubleteams:
            doublevec[i]=1
        else:
            doublevec[i]=0
    for i in numteams:
        if i>=doubleteams:
            tournvec[i]=1
        else:
            tournvec[i]=0
    for i in numteams:
        team_vars.append(LpVariable("Team " + str(i), 0, 100, cat="Int"))
    prob += lpSum([objvec[i] * team_vars[i] for i in numteams])
    initconstrs = []
    initconstrs.append(lpSum([team_vars[i] * doublevec[i] for i in numteams]) ==doubleentries-matmul(doublevec,startport))
    initconstrs.append(lpSum([team_vars[i] * tournvec[i] for i in numteams]) == tournentries-matmul(tournvec,startport))
    constrs = initconstrs
    for i in list(range(0, len(constrs))):
        prob += constrs[i]
    prob.solve()
    portout = []
    for i in numteams:
        portout.append(team_vars[i].varValue)
    return portout

# Define function to decide if move to new portfolio
def acceptmove(oldport,newport,temp,objfunc):
    newrand=random.random()
    oldobj=objfunc(oldport)
    newobj=objfunc(newport)
    if newobj>= oldobj:
        port=newport
    elif newrand<= exp((newobj-oldobj)/temp):
        port=newport
    else:
        port=oldport
    return port

# Define simulated annealing routine
def portsimann(x0,numbswaps,objfunc,grad,doubleteams,tournteams,doubleent,tournent,temp,randscale,its):
    port=x0
    bestport=x0
    dim=len(port)
    for i in list(range(0,its)):
        tempport=port+subvec(port,doubleteams,tournteams,numbswaps)
        randpert=random.random(dim)
        gradvec=grad(tempport)+randscale*randpert
        newteams=addvec(tempport,gradvec,doubleteams,tournteams,doubleent,tournent)
        trialport=tempport+newteams
        port=acceptmove(port,trialport,temp,objfunc)
        if objfunc(port) >= objfunc(bestport):
            bestport=port
    return bestport

start=time.time()

finalport=portsimann(initport,4,srobj,srgrad,len(doublerets),len(tournrets),doubleentries,tournentries,.001,.05,500)

end=time.time()

print(initport)
print(finalport)
print(srobj(initport))
print(srobj(finalport))
print(end-start)