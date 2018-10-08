# Make sure PuLP and CSV are Installed

from pulp import *
import csv
import time

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

# Read in CSVs
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

# list of players and variables
players=list(range(0,len(pointvec)))
player_vars=[]

# start timer
start=time.time()

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Maximum Point Team", LpMaximize)

# A dictionary called 'player_vars' is created to contain the referenced Variables
for i in players:
    player_vars.append(LpVariable("Player "+str(i),0,1,cat="Binary"))

# The objective function is added to 'prob' first
prob += lpSum([pointvec[i]*player_vars[i] for i in players]), "Total Points"

# Create positional/price constraints
initconstrs=[]
initconstrs.append(lpSum([player_vars[i]*cvec[i] for i in players]) <= 3)
initconstrs.append(lpSum([player_vars[i]*cvec[i] for i in players]) >= 2)
initconstrs.append(lpSum([player_vars[i]*wvec[i] for i in players]) >= 3)
initconstrs.append(lpSum([player_vars[i]*wvec[i] for i in players]) <= 4)
initconstrs.append(lpSum([player_vars[i]*dvec[i] for i in players]) >= 2)
initconstrs.append(lpSum([player_vars[i]*dvec[i] for i in players]) <= 3)
initconstrs.append(lpSum([player_vars[i]*utilvec[i] for i in players]) == 8)
initconstrs.append(lpSum([player_vars[i]*gvec[i] for i in players]) == 1)
initconstrs.append(lpSum([player_vars[i]*pricevec[i] for i in players]) <= 50001)

# Create team constraints and combine
teamconstrs=[]
for j in list(range(0,len(teammat))):
    teamconstrs.append(lpSum([player_vars[i]*teammat[j][i] for i in players]) <=7)

constrs=initconstrs+teamconstrs

# Add constraints
for i in list(range(0,len(constrs))):
    prob += constrs[i]

# The problem data is written to an .lp file
prob.writeLP("MaximumPoints.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# end timer
end=time.time()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
   print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Points = ", value(prob.objective))
print("Total C = ",sum(cvec[i]*player_vars[i].varValue for i in players))
print("Total W = ",sum(wvec[i]*player_vars[i].varValue for i in players))
print("Total D = ",sum(dvec[i]*player_vars[i].varValue for i in players))
print("Total G = ",sum(gvec[i]*player_vars[i].varValue for i in players))
print("Total Price = ",sum(pricevec[i]*player_vars[i].varValue for i in players))
for i in players:
    if player_vars[i].varValue==1:
        print(namevec[i])

teamstring=[]
for i in players:
    teamstring.append(str(player_vars[i].varValue))

print(teamstring)

print(end-start)

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/highmeanteam.csv","w") as csvfile:
    writer=csv.writer(csvfile,lineterminator="\n")
    writer.writerows(teamstring)
