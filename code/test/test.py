import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from algorithms.v2 import portfolio_optimization,portfolio_optimization_binary,portfolio_optimization_binary_count
from algorithms.brute_force import portfolio_optimization_all_solutions, portfolio_optimization_all_solutions_binary
from algorithms.solvers import qaoa,minimum_eigen,grover_optimizer,vqe
from plot.plotter import graph
from data.processing import format_data,logger,logger_simple
from algorithms.aux_functions import get_random_stock_market_data_final,NoDataAvailable, check_no_data
from data.basic import get_data
import qiskit.aqua.aqua_globals as globs
import numpy as np
import datetime
from time import time

#stocks = ["AAPL","GOOG","TSLA","GME","JWN","FB","CCL","NKE","JPM"]
tech = ["MSFT","TWTR"]#tech = ["TSLA","MSFT"] TWLO NVDA TWTR
tech = ["MSFT","AAPL","IBM","MMM","VZ","WMT","INTC","NVDA","TWLO","TWTR"]
travel = ["CCL","WYNN"]
retail = ["TGT","KO","HD","V"]
banking = ["JPM","WFC"]
others = ["CRSP","CLPT","GM"]
others1 = ["NVDA","TWTR"]
#Good plot: ["COST","KO","HD","V"], 2017-2020,all=7

def test_tech_travel():
    qaoa_graph_data = {"name":"Qiskit solution","info":{"risk":[],"returns":[]}}
    grover_graph_data = {"name":"Grover","info":{"risk":[],"returns":[]}}
    vqe_graph_data = {"name":"VQE","info":{"risk":[],"returns":[]}}
    exact_graph_data = {"name":"Exact solution","info":{"risk":[],"returns":[]}}
    brute_force_graph_data = {"name":"Brute Force solutions","info":{"risk":[],"returns":[],"result":[]}}
    
    #Parameters preparation
    stocks =["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA", "CRSP","TWTR","GM","CLPT","JPM","WFC","WMT" , "HD" , "NVDA" , "CRSP","TWTR", "GM"]##retail #tech # + tech#  others #+ travel# +others 
    start_date = datetime.datetime(2017,1,1)
    end_date=datetime.datetime(2020,1,1)
    mu,sigma = get_data(stocks,start_date,end_date)
    risk_aversion = 0.01
    num_assets_portfolio = 8
    penalty = 10
    max_allocation = 3
    binary_encoding = False


    #check if no info
    check_no_data(stocks,mu)

    #Solve qubo
    iterations = 6
    total_time = 0 

    #Build qubo
    """ if binary_encoding == True:
        qubo = portfolio_optimization_binary(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,max_allocation)
    else:
        qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,True) """
    #qaoa_res = qaoa(qubo,len(stocks),num_assets_portfolio)

    

    """ qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,ansatz)

    start = time()
    qaoa_res = qaoa(qubo,len(stocks),num_assets_portfolio,ansatz)
    total_time =(time() - start)
    print("Time = ", total_time)
    qaoa_graph_data["info"] = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
    print(qaoa_graph_data) """

    ansatz=False


    """   data = stocks[:num_ass]
        mu,sigma = get_data(data,start_date,end_date)


        qubo = portfolio_optimization(data,mu,sigma,num_assets_portfolio,risk_aversion,penalty,False)
        total_time= 0
        for i in range(iterations):
            start = time()
            qaoa_res = qaoa(qubo,len(data),num_assets_portfolio, ansatz)
            total_time = total_time + (time() - start)
            print((time() - start))
        f = open('qaoa.txt', 'a')
        f.write("QAOA - " + str(len(data)) + " - " + str(ansatz) +  " - " +str(total_time/iterations) + "\n")
        f.close()
    """
    #for num_ass in range(4,len(stocks) + 1,+1):
    for num_ass in range(10,len(stocks),+1):
        print("here")
        data = stocks[:num_ass]
        mu,sigma = get_data(data,start_date,end_date)


        qubo = portfolio_optimization(data,mu,sigma,num_assets_portfolio,risk_aversion,penalty,False)
        f = open('qaoa.txt', 'a')
        f.write("QAOA - " + str(len(data)) + "\n")
        rets = 0
        risk = 0
        f.close()
        for i in range(iterations):
            f = open('qaoa.txt', 'a')
            qaoa_res = qaoa(qubo,len(data),num_assets_portfolio, ansatz)
            qaoa_data = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
            curr_risk = qaoa_data['risk']
            curr_rets = qaoa_data['returns']

            rets = rets + curr_rets
            risk = risk + curr_risk
            
            f.write(str(curr_risk) + "\n")
            f.write(str(curr_rets)+ "\n")
            f.close()

        f = open('qaoa.txt', 'a')
        f.write(str(risk/iterations)+ "\n")
        f.write(str(rets/iterations)+ "\n")
        
        
        qubo = portfolio_optimization(data,mu,sigma,num_assets_portfolio,risk_aversion,penalty,True)
        f.write("\nQAOA+ - " + str(len(data)) + "\n")
        rets = 0
        risk = 0
        f.close()
        for i in range(iterations):
            f = open('qaoa.txt', 'a')
            qaoa_res = qaoa(qubo,len(data),num_assets_portfolio, ansatz)
            qaoa_data = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
            curr_risk = qaoa_data['risk']
            curr_rets = qaoa_data['returns']

            rets = rets + curr_rets
            risk = risk + curr_risk
            
            f.write(str(curr_risk)+ "\n")
            f.write(str(curr_rets)+ "\n")
            f.close()

        f = open('qaoa.txt', 'a')
        f.write(str(rets/iterations))
        f.write(str(curr_rets/iterations))

        f.write("\nExact - " + str(len(data)) + "\n")
        exact_data = format_data(mu,sigma,risk_aversion,minimum_eigen(qubo),num_assets_portfolio)
        f.write(str(exact_data['risk'])+ "\n")
        f.write(str(exact_data['returns'])+ "\n")

        f.close()

    """ ansatz=True
    for num_ass in range(14,len(stocks) + 1,+1):
        data = stocks[:num_ass]
        mu,sigma = get_data(data,start_date,end_date)
        qubo = portfolio_optimization(data,mu,sigma,num_assets_portfolio,risk_aversion,penalty,ansatz)
        total_time= 0
        for i in range(iterations):
            start = time()
            qaoa_res = qaoa(qubo,len(data),num_assets_portfolio, ansatz)
            total_time = total_time + (time() - start)
            print((time() - start))
        f = open('qaoa.txt', 'a')
        f.write(str(len(data)) + " - " + str(ansatz) +  " - " +str(total_time/iterations) + "\n")
        f.close() """
    #print(qaoa_res)
    #qaoa_graph_data["info"] = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
    #print(qaoa_graph_data)

    """ if binary_encoding == True:
        qubo = portfolio_optimization_binary(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,max_allocation)
    else:
        qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,False) """
    """ for num_ass in range(len(tech + others),3,-1):
        data = (tech+others)[:num_ass]
        mu,sigma = get_data(data,start_date,end_date)
        qubo = portfolio_optimization(data,mu,sigma,len(data) -2 ,risk_aversion,penalty,True)
        total_time = 0
        for i in range(iterations):
            start = time()
            exact_graph_data["info"] = format_data(mu,sigma,risk_aversion,minimum_eigen(qubo),num_assets_portfolio)
            total_time = total_time + (time() - start)
            print((time() - start))
        f = open('exact.txt', 'a')
        f.write(str(len(data)) +  " - " +str(total_time/iterations) + "\n")
        f.close()
    exact_graph_data["info"] = format_data(mu,sigma,risk_aversion,minimum_eigen(qubo),num_assets_portfolio)
    """
    #qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,False)
    exact_graph_data["info"] = format_data(mu,sigma,risk_aversion,minimum_eigen(qubo),num_assets_portfolio)
    #print(exact_graph_data)
    brute_force_graph_data["info"] = portfolio_optimization_all_solutions(mu,sigma,risk_aversion,num_assets_portfolio,max_allocation)
    #grover_graph_data["info"] = format_data(mu,sigma,risk_aversion,grover_optimizer(qubo,len(stocks)),max_allocation)

    #logger(stocks,mu,sigma,risk_aversion,qaoa_graph_data['info'],"QAOA",num_assets_portfolio)
    #logger(stocks,mu,sigma,risk_aversion,exact_graph_data['info'],"Exact",num_assets_portfolio,False)
    #logger_simple(brute_force_graph_data["info"],risk_aversion)
    graph(stocks,exact_graph_data,[qaoa_graph_data],brute_force_graph_data)

def test_graph():
    qaoa_graph_data = {"name":"QAOA solution","qaoa" : True,"info":{"risk":[],"returns":[]}}
    qaoa_plus_graph_data = {"name":"QAOA+ solution","qaoa" : False,"info":{"risk":[],"returns":[]}}
    grover_graph_data = {"name":"Grover","info":{"risk":[],"returns":[]}}
    vqe_graph_data = {"name":"VQE","info":{"risk":[],"returns":[]}}
    exact_graph_data = {"name":"Exact solution","info":{"risk":[],"returns":[]}}
    brute_force_graph_data = {"name":"Brute Force solutions","info":{"risk":[],"returns":[],"result":[]}}
    
    #Parameters preparation
    #["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA"]
    #[ "CRSP","TWTR","GM","CLPT","JPM","WFC","WMT" , "HD"]
    #["HD","WMT","CRSP","JPM","WFC","TWTR","GM","CLPT"]
    
    stocks =["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA","CRSP","TWTR"]#,"GM","CLPT","JPM","WFC","WMT" , "HD"] # , "NVDA" , "CRSP","TWTR", "GM"]##retail #tech # + tech#  others #+ travel# +others 
    stocks = ["MSFT","MA","DIS","GOOG","KO","MCD"]
    stocks = ["TGT","KO","HD","V","MSFT","TWTR"]
    stocks = ["TGT","KO","HD","V"]
    stocks =["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA","CRSP","TWTR","GM","CLPT","JPM","WFC"]#,"WMT" , "HD","V"]
    #stocks =["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA","CRSP"]#,"TWTR","GM","CLPT"]#,"JPM","WFC","WMT" , "HD","V"]
    #stocks = ["TGT","KO","HD","V","MSFT","AAPL","TWTR","GM","CCL"]
    stocks =["MSFT","AAPL","IBM","MMM","VZ", "CCL", "NVDA"]#,"CRSP","TWTR","GM","CLPT","JPM"]#,"WFC","WMT" ]#, "HD","V"]
    stocks = ["GOOG","IBM","BABA","JPM","CRSP","KO","TGT","GM","HD","V","MCD"]
    start_date = datetime.datetime(2017,1,1)
    end_date=datetime.datetime(2020,1,1)
    mu,sigma = get_data(stocks,start_date,end_date)
    risk_aversion = 1
    num_assets_portfolio = 4
    penalty = 100
    max_allocation = 3

    #check if no info
    check_no_data(stocks,mu)

    ansatz=False
    qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,ansatz)
    qaoa_res = qaoa(qubo,len(stocks),num_assets_portfolio, ansatz)
    qaoa_graph_data["info"] = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
    print(qaoa_graph_data)

    ansatz=True
    qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,ansatz)
    qaoa_res = qaoa(qubo,len(stocks),num_assets_portfolio, ansatz)
    qaoa_plus_graph_data["info"] = format_data(mu,sigma,risk_aversion,qaoa_res,num_assets_portfolio)
    
    
    qubo = portfolio_optimization(stocks,mu,sigma,num_assets_portfolio,risk_aversion,penalty,False)
    exact_graph_data["info"] = format_data(mu,sigma,risk_aversion,minimum_eigen(qubo),num_assets_portfolio)
    print(exact_graph_data)

    brute_force_graph_data["info"] = portfolio_optimization_all_solutions(mu,sigma,risk_aversion,num_assets_portfolio,max_allocation)
    logger(stocks,mu,sigma,risk_aversion,qaoa_graph_data['info'],"QAOA",num_assets_portfolio)
    logger(stocks,mu,sigma,risk_aversion,qaoa_plus_graph_data['info'],"QAOA+",num_assets_portfolio,False)
    logger(stocks,mu,sigma,risk_aversion,exact_graph_data['info'],"Exact",num_assets_portfolio,False)
    logger_simple(brute_force_graph_data["info"],risk_aversion)
    graph(stocks,exact_graph_data,[qaoa_graph_data,qaoa_plus_graph_data],brute_force_graph_data)

#test_graph()
test_tech_travel()