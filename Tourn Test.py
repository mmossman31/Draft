# importing points vec and covmat
from math import sqrt
import csv
from numpy import matmul
from mystic.constraints import integers
pointvec=[]
initcovmat=[]
cvec=[]
wvec=[]
with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/pointvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        pointvec.append(float(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/cvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        cvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/wvec.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        wvec.append(int(row[0]))

with open("c:/users/lanmo/desktop/Draftkings - Local/AWS Testing/Test Data/covmat.csv", "r") as csvfile:
    data=csv.reader(csvfile)
    for row in data:
        initcovmat.append(row)

covmat=initcovmat

for i in list(range(0,len(initcovmat))):
    for j in list(range(0,len(initcovmat[i]))):
        covmat[i][j]=float(initcovmat[i][j])

# Define team points function
@integers()
def team_points(team):
    return sum(team[i]*pointvec[i] for i in list(range(0,len(pointvec))))

# Define team sd function
def team_sd(team):
     return matmul(team,matmul(covmat,team))
#    return sqrt(sum(sum(team[i]*covmat[i][j]*team[j] for i in list(range(0,len(pointvec)))) for j in list(range(0,len(pointvec)))))

def obj_func(team):
    return -team_points(team)-2*team_sd(team)

print(team_points(list(range(0,len(pointvec)))))
print(team_sd(list(range(0,len(pointvec)))))
print(obj_func(list(range(0,len(pointvec)))))


from mystic.symbolic import generate_constraint
from mystic.symbolic import generate_solvers

def firstone(list):
    i=0
    while i<= len(list):
        if list[i]==1:
            return i
        i=i+1
    return len(list)

cminconstr="x"+str(firstone(cvec))+" >= "
for i in list(range(0,len(cvec))):
    if cvec[i]==1 and i!=firstone(cvec):
        cminconstr=cminconstr+"x"+str(i)+" + "
cminconstr=cminconstr+"2"
print(firstone(wvec))
print(cminconstr)
