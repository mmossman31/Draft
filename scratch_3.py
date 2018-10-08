#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/mystic/browser/mystic/LICENSE
"""
Example:
    - Solve 8th-order Chebyshev polynomial coefficients with Powell's method.
    - Uses LatticeSolver to provide 'pseudo-global' optimization
    - Plot of fitting to Chebyshev polynomial.
	Demonstrates:
    - standard models
    - minimal solver interface
"""
# the Lattice solver
from mystic.solvers import LatticeSolver

# Powell's Directonal solver
from mystic.solvers import PowellDirectionalSolver

# Chebyshev polynomial and cost function
from mystic.models.poly import chebyshev8, chebyshev8cost
from mystic.models.poly import chebyshev8coeffs

# if available, use a pathos worker pool
try:
    from pathos.pools import ProcessPool as Pool
   #from pathos.pools import ParallelPool as Pool
except ImportError:
    from mystic.pools import SerialPool as Pool

# tools
from mystic.termination import NormalizedChangeOverGeneration as NCOG
from mystic.math import poly1d
from mystic.monitors import VerboseMonitor
from mystic.tools import getch
from mystic.symbolic import generate_constraint
from mystic.symbolic import generate_solvers

# importing points vec and covmat
import csv
from numpy import matmul
from numpy import random
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

covmat=initcovmat

for i in list(range(0,len(initcovmat))):
    for j in list(range(0,len(initcovmat[i]))):
        covmat[i][j]=float(initcovmat[i][j])

randvec=random.rand(len(pointvec))-3

# Define team points function
from mystic.constraints import integers
@integers()
def team_points(team):
    return sum(team[i]*pointvec[i] for i in list(range(0,len(pointvec))))

# Define team sd function
@integers()
def team_sd(team):
    return matmul(team, matmul(covmat, team))
@integers()
def obj_func(team):
    return -team_points(team)-2*team_sd(team)
@integers()
def test_obj(team):
    return team_points(team)+matmul(randvec,team)

# Define useful functions for constraints
@integers()
def team_c(team):
    return matmul(team, cvec)
@integers()
def team_w(team):
    return matmul(team, wvec)
@integers()
def team_d(team):
    return matmul(team, dvec)
@integers()
def team_g(team):
    return matmul(team, gvec)
@integers()
def team_util(team):
    return matmul(team, utilvec)
@integers()
def team_price(team):
    return matmul(team, pricevec)
def firstone(list):
    i=0
    while i<= len(list):
        if list[i]==1:
            return i
        i=i+1
    return len(list)

# Define constraints
cminconstr="x"+str(firstone(cvec))+" >= "
for i in list(range(0,len(cvec))):
    if cvec[i]==1 and i!=firstone(cvec):
        cminconstr=cminconstr+"x"+str(i)+" + "
cminconstr=cminconstr+"2"

solv = generate_solvers(cminconstr,nvars=len(pointvec))
constraintfunc = generate_constraint(solv)


#Run optimization
if __name__ == '__main__':


    print("Powell's Method")
    print("===============")

    # dimensional information
    from mystic.tools import random_seed
    random_seed(12)
    ndim = len(pointvec)
    nbins = 1 #[2,1,2,1,2,1,2,1,1]


    # configure monitor
    stepmon = VerboseMonitor(1)

    # use lattice-Powell to solve 8th-order Chebyshev coefficients
    solver = LatticeSolver(ndim, nbins)
    solver.SetNestedSolver(PowellDirectionalSolver)
    solver.SetMapper(Pool().map)
    solver.SetGenerationMonitor(stepmon)
    solver.SetStrictRanges(min=[0]*ndim, max=[1]*ndim)
    solver.SetConstraints(constraintfunc)
    solver.Solve(test_obj, NCOG(1e+2), disp=1)
    solution = solver.Solution()

    # use pretty print for polynomials
    print(solution)

for i in list(range(0,len(pointvec))):
    if round(solution[i])==1:
        print(namevec[i])
print(team_c(solution))

# end of file