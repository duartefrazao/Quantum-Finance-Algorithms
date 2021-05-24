from data.processing import format_data_basic
import numpy as np 
import math
import itertools

def all_combinations(n,num_assets):
    combs = []
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        combs.append(list(map(int,list(s))))
    
    return filter(lambda x:sum(x)==num_assets,combs)

def all_combinations_binary(n,max_allocation):
    combs = []
    for val in itertools.product(range(max_allocation+1), repeat=n):
        combs.append(np.asarray(val))
    
    valid = filter(lambda x:sum(x)==max_allocation,combs) 
    return valid


def portfolio_optimization_all_solutions(mu,sigma,risk_aversion,num_assets_portfolio,max_allocation):

    solutions = []
    all_sols = all_combinations(len(mu),num_assets_portfolio)

    for sol in all_sols:
        res = format_data_basic(mu,sigma,risk_aversion,np.array(sol),num_assets_portfolio)
        solutions.append(res)

    return solutions

def portfolio_optimization_all_solutions_binary(mu,sigma,risk_aversion,num_assets_portfolio,max_allocation):

    all_sols = all_combinations_binary(len(mu),max_allocation)
    solutions = []

    for sol in all_sols:
        res = format_data_basic(mu,sigma,risk_aversion,np.array(sol),max_allocation)
        solutions.append(res)

    return solutions

