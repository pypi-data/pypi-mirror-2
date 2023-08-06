#
# Imports
#

import sys
import os
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))
from coopr.pyomo import *

infinity = float('inf')

#
# Model
#

model = Model()

model.NUTR = Set()
model.FOOD = Set()

model.cost = Param(model.FOOD, within=PositiveReals)

model.f_min = Param(model.FOOD, within=NonNegativeReals, default=0.0)

def f_max_validate (value, j, model):
    return model.f_max[j] > model.f_min[j]
model.f_max = Param(model.FOOD, validate=f_max_validate,
			default=infinity)

model.n_min = Param(model.NUTR, within=NonNegativeReals, default=0.0)

def n_max_validate (value, j, model):
    return value > model.n_min[j]
model.n_max = Param(model.NUTR, validate=n_max_validate,
			default=infinity)

model.amt = Param(model.NUTR, model.FOOD, within=NonNegativeReals)

# --------------------------------------------------------

def Buy_bounds(i,model):
    return (model.f_min[i],model.f_max[i])
model.Buy = Var(model.FOOD, bounds=Buy_bounds)

# --------------------------------------------------------

def Total_Cost_rule(model):
    ans = 0
    for j in model.FOOD:
        ans = ans + model.cost[j] * model.Buy[j]
    return ans
model.Total_Cost = Objective(rule=Total_Cost_rule)

def Nutr_Amt_rule(i, model):
    ans = 0
    for j in model.FOOD:
      ans = ans + model.amt[i,j] * model.Buy[j]
    return ans
#model.Nutr_Amt = Objective(model.NUTR, rule=Nutr_Amt_rule)

# --------------------------------------------------------

def Diet_rule(i, model):
    expr = 0
    for j in model.FOOD:
      expr = expr + model.amt[i,j] * model.Buy[j]
    return (model.n_min[i], expr, model.n_max[i])
model.Diet = Constraint(model.NUTR, rule=Diet_rule)

