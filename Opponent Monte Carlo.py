import csv
import time
from numpy import *
from scipy import stats

# Set number of games, teams, sims
nmbgames=8
nmbteams=7
nmbsims=200
doubleopps=34
doublepayposition=15
tournopps=5945

# Import opponent parameters and ownership
tournoppparams=[]
doubleoppparams=[]
ownvec=[]
tournownvec=[]
doubleownvec=[]
initteam1=[]
initsimplayerscores=[]
pointvec=[]
doubleretmat=zeros((2,2),)
doubleretmat[0][0]=1
doubleretmat[1][0]=doublepayposition+1
doubleretmat[0][1]=1
doubleretmat[1][1]=-1
inittournretmat=[]
inittourncorrmat=[]
initcovmat=[]
initteam2=[]
initteam3=[]
initteam4=[]
initteam5=[]
initteam6=[]
initteam7=[]

with open("c:/users/lanmo/desktop/Draftkings - Local/Collected Data/Projection Parameters/tournopp.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        tournoppparams.append(float(row[1]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/pointvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        pointvec.append(float(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/Collected Data/Projection Parameters/doubleopp.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        doubleoppparams.append(float(row[1]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/ownvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        ownvec.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highmeanteam.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam1.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam1.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam2.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam2.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam3.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam3.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam4.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam4.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam5.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam5.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam6.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highvarteam6.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initteam7.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/simplayerscores.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initsimplayerscores.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/tournretmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        inittournretmat.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/tourncorrmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        inittourncorrmat.append(row)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/covmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initcovmat.append(row)

simplayerscores=initsimplayerscores

for i in list(range(0,len(initsimplayerscores))):
    for j in list(range(0,len(initsimplayerscores[i]))):
        simplayerscores[i][j]=float(initsimplayerscores[i][j])

tournretmat=inittournretmat

for i in list(range(0,len(inittournretmat))):
    for j in list(range(0,len(inittournretmat[i]))):
        tournretmat[i][j]=float(inittournretmat[i][j])

tourncorrmat=inittourncorrmat

for i in list(range(0,len(inittourncorrmat))):
    for j in list(range(0,len(inittourncorrmat[i]))):
        tourncorrmat[i][j]=float(inittourncorrmat[i][j])

covmat=initcovmat

for i in list(range(0,len(initcovmat))):
    for j in list(range(0,len(initcovmat[i]))):
        covmat[i][j]=float(initcovmat[i][j])

for i in list(range(0,len(ownvec))):
    tournownvec.append(float(ownvec[i][0]))
    doubleownvec.append(float(ownvec[i][1]))

tournconstant=tournoppparams[0]
tournsqrt=tournoppparams[1]
tournonedaysd=tournoppparams[2]
tournmeansd=tournoppparams[3]

doubleconstant=doubleoppparams[0]
doublesqrt=doubleoppparams[1]
doubleonedaysd=doubleoppparams[2]
doublemeansd=doubleoppparams[3]

teamlist=[]
teamlist.append(initteam1)
teamlist.append(initteam2)
teamlist.append(initteam3)
teamlist.append(initteam4)
teamlist.append(initteam5)
teamlist.append(initteam6)
teamlist.append(initteam7)

#for i in list(range(0,nmbteams)):
#    teamlist.append(initteam)

doubleteamowns=matmul(teamlist,doubleownvec)
tournteamowns=matmul(teamlist,tournownvec)

teamscores=matmul(teamlist,transpose(simplayerscores))
teammeans=matmul(teamlist,pointvec)

doublemean=doubleconstant+doublesqrt*sqrt(nmbgames)
tournmean=tournconstant+tournsqrt*sqrt(nmbgames)

# Define useful counting function
def countgreater(list,numb):
    i=0
    for j in list:
        if j>numb:
            i=i+1
    return i

# Define return from return matrix function
def teamret(retmat,place):
    if place==1:
        return retmat[0][1]
    i=-1
    for j in list(range(0,len(retmat))):
        if retmat[j][0]<=place:
            i=i+1
    return retmat[i][1]

start=time.time()

# Simulate scores for doubles
doublesimmeans=random.normal(doublemean,doublemeansd,nmbsims)

doubleoverlaps=zeros((nmbteams,nmbsims),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        doubleoverlaps[i][j]=teamscores[i][j]/teammeans[i]

doubleindsims=random.normal(0,doubleonedaysd,(nmbsims,doubleopps-1))

doublesimscores=zeros((nmbteams,nmbsims,doubleopps-1),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        for k in list(range(0,doubleopps-1)):
            doublesimscores[i][j][k]=doublesimmeans[j]*(1-doubleteamowns[i]/100)+doublesimmeans[j]*doubleoverlaps[i][j]*doubleteamowns[i]/100+doubleindsims[j][k]

intermed1=time.time()

# Calculate places and returns for doubles
doubleteamplaces=zeros((nmbteams,nmbsims),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        doubleteamplaces[i][j]=1+countgreater(doublesimscores[i][j],teamscores[i][j])

doubleteamrets=zeros((nmbteams,nmbsims),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        doubleteamrets[i][j]=teamret(doubleretmat,doubleteamplaces[i][j])

intermed2=time.time()

# Create teams for opponents in tournaments
playermean=zeros(len(pointvec),)

playerrands = random.multivariate_normal(playermean, tourncorrmat, (tournopps - 1, nmbsims))

intermed3=time.time()

unirands=stats.norm.cdf(playerrands,0,1)

intermed4=time.time()

tournoppteam=unirands
for i in list(range(0,len(unirands))):
    for j in list(range(0,len(unirands[i]))):
        for k in list(range(0,len(unirands[i][j]))):
            if unirands[i][j][k]<tournownvec[k]/100:
                tournoppteam[i][j][k]=1
            else:
                tournoppteam[i][j][k]=0

intermed5=time.time()

tournoppplayerscores=zeros((tournopps-1,nmbsims),)
for i in list(range(0,tournopps-1)):
    for j in list(range(0,nmbsims)):
        tournoppplayerscores[i][j]=matmul(tournoppteam[i][j],simplayerscores[j])

tournoppplayermeans=matmul(tournoppteam,pointvec)

intermed6=time.time()

inittournoppplayervars=matmul(tournoppteam,covmat)

tournoppplayervars=zeros((tournopps-1,nmbsims),)
for i in list(range(0,len(tournoppteam))):
    for j in list(range(0,len(tournoppteam[i]))):
       tournoppplayervars[i][j]=matmul(inittournoppplayervars[i][j],tournoppteam[i][j])

intermed7=time.time()

tournresidmeans=tournmean-tournoppplayermeans
tournresidvars=tournonedaysd**2+tournmeansd**2-tournoppplayervars

tournresidscores=zeros((tournopps-1,nmbsims),)
for i in list(range(0,len(tournresidmeans))):
    for j in list(range(0,len(tournresidmeans[i]))):
        tournresidscores[i][j]=random.normal(tournresidmeans[i][j],sqrt(max(tournresidvars[i][j],0)))

tournoppscores=transpose(tournresidscores+tournoppplayerscores)

intermed8=time.time()

# Calculate places and returns for tournaments
tournteamplaces=zeros((nmbteams,nmbsims),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        tournteamplaces[i][j]=1+countgreater(tournoppscores[j],teamscores[i][j])

tournteamrets=zeros((nmbteams,nmbsims),)
for i in list(range(0,nmbteams)):
    for j in list(range(0,nmbsims)):
        tournteamrets[i][j]=teamret(tournretmat,tournteamplaces[i][j])

end=time.time()

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/tournteamrets.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    for i in list(range(0,len(tournteamrets))):
        writer.writerow(tournteamrets[i])

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/doubleteamrets.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    for i in list(range(0,len(doubleteamrets))):
        writer.writerow(doubleteamrets[i])

print("Double Return: ",mean(doubleteamrets))
print("Tournament Scores: ",mean(tournoppscores))
print("Tournament Returns: ",mean(tournteamrets))
print("Double Scores Time: ",intermed1-start )
print("Double Returns Time: ",intermed2-intermed1)
print("Tourn Rands Time: ",intermed3-intermed2)
print("Tourn Uniform Time: ",intermed4-intermed3)
print("Tourn Team Build Time: ",intermed5-intermed4)
print("Tourn Player Scores Time: ",intermed6-intermed5)
print("Tourn Player Var Time: ",intermed7-intermed6)
print("Tourn Team Scores Time: ",intermed8-intermed7)
print("Tourn Returns Time: ",end-intermed8)
print(end-start)
