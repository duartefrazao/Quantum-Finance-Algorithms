from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.aqua import QuantumInstance
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.aqua.algorithms import VQE, QAOA, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import COBYLA
from .aux_functions import IncompatibleArguments 
import numpy as np
import matplotlib.pyplot as plt

# initialization
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile

# import basic plot tools
from qiskit.visualization import plot_histogram

#Quadratic
from qiskit.optimization import QuadraticProgram
from docplex.mp.advmodel import AdvModel
from qiskit.optimization.converters import IntegerToBinary,LinearEqualityToPenalty,InequalityToEquality,QuadraticProgramToQubo

def portfolio_optimization(assets,mu,sigma,num_assets_portfolio,risk_aversion,penalty,qaoa):

    if len(mu) != sigma.shape[0] or len(mu) != sigma.shape[1] or len(mu) != len(assets):
        raise IncompatibleArguments("Sigma, mu and assets need to be equal in size")
    """ if not 0 <= risk_aversion <= 1:
        raise IncompatibleArguments("Risk aversion needs to be in [0,1]") """
    if not 0 < num_assets_portfolio <= len(assets):
        raise IncompatibleArguments("Number of assets to include in the portfolio needs to be smaller or equal to the number of assets passed")

    #Initialize binary variable array
    mdl = AdvModel('docplex model')
    mdl.init_numpy()
    decision_vars = np.array([])

    """ if qaoa:
        ancila_odd = mdl.binary_var("ancila_odd")
        ancila_even = mdl.binary_var("ancila_even") """
    for asset in assets:
        decision_vars = np.append(decision_vars,[mdl.binary_var(str(asset))])
    

    #Terms
    vec_ones = np.ones(len(decision_vars)) #helper vector
    num_assets_chosen = np.matmul(vec_ones.T,decision_vars) 
    expected_returns_portfolio = np.matmul(mu.T,decision_vars)/num_assets_portfolio
    variance_portfolio = np.matmul(decision_vars.T,np.dot(sigma,decision_vars))/num_assets_portfolio #*2 as covariance is a symetric matrix

    #Objective function
    #if not  qaoa:
    if True:
        mdl.minimize(- expected_returns_portfolio + (risk_aversion * variance_portfolio) + penalty*((num_assets_chosen - num_assets_portfolio)**2))
    else:
        mdl.minimize(- expected_returns_portfolio + (risk_aversion * variance_portfolio) + ancila_even*0 + ancila_odd*0 )

    qubo = QuadraticProgram()
    qubo.from_docplex(mdl)
    print(qubo.export_as_lp_string())
    #qubo.binary_var("ancila")
    return qubo


def portfolio_optimization_binary(assets,mu,sigma,num_assets_portfolio,risk_aversion,penalty,max_allocation):

    if len(mu) != sigma.shape[0] or len(mu) != sigma.shape[1] or len(mu) != len(assets):
        raise IncompatibleArguments("Sigma, mu and assets need to be equal in size")
    """ if not 0 <= risk_aversion <= 1:
        raise IncompatibleArguments("Risk aversion needs to be in [0,1]") """
    """ if not 0 < num_assets_portfolio <= len(assets):
        raise IncompatibleArguments("Number of assets to include in the portfolio needs to be smaller or equal to the number of assets passed")
 """
    #Initialize binary variable array
    mdl = AdvModel('docplex model')
    mdl.init_numpy()
    decision_vars = np.array([])

    for asset in assets:
            decision_vars = np.append(decision_vars,[mdl.integer_var(name=str(asset),lb=0,ub=max_allocation)])
        

    #Terms
    vec_ones = np.ones(len(decision_vars)) #helper vector
    num_assets_chosen = np.matmul(vec_ones.T,decision_vars)
    expected_returns_portfolio = np.matmul(mu.T,decision_vars)
    variance_portfolio = np.matmul(decision_vars.T,np.dot(sigma,decision_vars)) #*2 as covariance is a symetric matrix

    #Objective function
    #mdl.minimize(- expected_returns_portfolio + (risk_aversion * variance_portfolio) + penalty*((num_assets_chosen - max_allocation)**2))
    mdl.minimize(((num_assets_chosen - max_allocation)**2))

    qubo = QuadraticProgram()
    qubo.from_docplex(mdl)
    
    """    int2bin = IntegerToBinary()
    qp_eq_bin = int2bin.convert(qubo) """
    conv = QuadraticProgramToQubo()
    qp_eq_bin = conv.convert(qubo)
    print(qp_eq_bin.export_as_lp_string())
    return qubo


def portfolio_optimization_binary_count(assets,mu,sigma,max_assets,risk_aversion,penalty,max_allocation):

    if len(mu) != sigma.shape[0] or len(mu) != sigma.shape[1] or len(mu) != len(assets):
        raise IncompatibleArguments("Sigma, mu and assets need to be equal in size")
    """ if not 0 <= risk_aversion <= 1:
        raise IncompatibleArguments("Risk aversion needs to be in [0,1]") """
    """ if not 0 < num_assets_portfolio <= len(assets):
        raise IncompatibleArguments("Number of assets to include in the portfolio needs to be smaller or equal to the number of assets passed")
 """
    #Initialize binary variable array
    mdl = AdvModel('docplex model')
    mdl.init_numpy()
    allocation_vars = np.array([])
    presence_vars = np.array([])

    for asset in assets:
            allocation_vars = np.append(allocation_vars,[mdl.integer_var(name=str(asset),lb=0,ub=max_allocation)])
            presence_vars = np.append(presence_vars,[mdl.binary_var(name=('b'+str(asset)))])
        

    #Terms
    vec_ones = np.ones(len(allocation_vars)) #helper vector
    num_allocations = np.matmul(vec_ones.T,allocation_vars)
    expected_returns_portfolio = 10000*np.matmul(mu.T,allocation_vars)
    variance_portfolio = 10000*np.matmul(allocation_vars.T,np.dot(sigma,allocation_vars)) / 2 #*2 as covariance is a symetric matrix

    #Objective function
    mdl.minimize(- expected_returns_portfolio 
    + (risk_aversion * variance_portfolio) 
    + penalty*((num_allocations - max_allocation)**2))

    for asset in range(len(presence_vars)):
        mdl.add_constraint(allocation_vars[0]>=presence_vars[0])
        mdl.add_constraint(allocation_vars[0]<= max_allocation * presence_vars[0])
    #mdl.add_constraint(allocation_vars[0] <= presence_vars[0] + allocation_vars[0]*presence_vars[0])
    qubo = QuadraticProgram()
    qubo.from_docplex(mdl)

    conv = QuadraticProgramToQubo()
    qp_eq_bin = conv.convert(qubo)


    """ 
    int2bin = IntegerToBinary()
    qp_eq_bin = int2bin.convert(qubo)
    lineq2penalty = LinearEqualityToPenalty()
    qp_eq_bin = lineq2penalty.convert(qp_eq_bin)  """
    #mdl.add_constraint(allocation_vars[0]*presence_vars[0] >= 0)

    print(qp_eq_bin.export_as_lp_string())
    return qubo

