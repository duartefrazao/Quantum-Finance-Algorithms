import numpy as np
import math

def get_result_basic(result,risk_aversion):
    solution = -result["returns"] + result['risk']*risk_aversion
    #print(result["returns"]*252, 2.52*((100*result['risk']/2)**(1/2)),252*solution)
    return solution

def calculate_terms(result,mu,sigma,num_assets_chosen):
    
    result_div = result/np.array(num_assets_chosen)
    risk =  252*(100*np.dot(result.T,np.dot(sigma,result))/2)**(1/2)  
    returns = 100*252*np.dot(mu.T,result) 
    #risk = np.dot(result.T,np.dot(sigma,result))/num_assets_chosen
    #returns = np.dot(mu.T,result) / num_assets_chosen
    """ risk =  np.matmul(result.T,np.dot(sigma,result))
    returns =  np.dot(mu.T,result) """
    """ result = trim_solution(result)
    result = trim_solution(result) """

    return risk,returns,result

def trim_solution(result):
    for i in range(len(result)):
        last_val = result[i]
        last_val= str(last_val).replace("0.0","0")
        last_val = last_val.replace("1.0","1")
        if len(last_val)>5:
            last_val=last_val[:4]
        result[i] = last_val
    return result

def format_data(mu,sigma,risk_aversion,solution,num_assets_chosen):
    result = np.zeros(len(mu))
    i = 0
    """ print(solution.variables_dict)
    solutions = solution.variables_dict
    for ticker in solutions:
        print(ticker)
        if i < len(mu):
            result[i] = solutions[ticker]
        i+=1
    print(result) """
    for ticker in solution.variables_dict:
        #print(ticker,solution.variables_dict[ticker])
        result[i] = solution.variables_dict[ticker]
        i+=1
    risk,returns,result = calculate_terms(result,mu,sigma,num_assets_chosen)

    return {"risk":risk,"returns":returns,"result":result}

def format_data_basic(mu,sigma,risk_aversion,result,num_assets_chosen):
    risk,returns,result = calculate_terms(result,mu,sigma,num_assets_chosen)
    return {"risk":risk,"returns":returns,"result":result}

def trunc(value,amount=4):
    return str(value)[:amount]

def logger_simple(solutions,risk_aversion):
    f = open('test_logger.txt', 'a+')
    for sol in solutions:
        str_info = "\n" + str([trunc(x,4) for x in sol["result"]]) + " risk=" + trunc(sol['risk']) + " returns="+ trunc(sol['returns']) + " result="+ trunc(get_result_basic(sol,risk_aversion),5)
        f.write(str_info)
    f.close()

def logger(stocks,mu,sigma,risk_aversion,solution,name,num_assets_portfolio,create=True):
    
    if create == True:
        f = open('test_logger.txt', 'w')
    else:
        f = open('test_logger.txt', 'a+')
    
    f.writelines(["\nAlgo: ",name,"\nStocks:"])
    for stock in stocks:
        f.write(" " + stock)
    f.write("\nNumber of assets in portfolio: " + str(num_assets_portfolio))
    
    f.write("\nMu: ")
    for ret in mu:
        f.write(" " +trunc(252*ret))
    
    f.write("\nSigma: ")
    for line in sigma:
        f.write("\n")
        for e in line:
            f.write(" " + str(2.52*((100*e/2)**(1/2)))[:4])
    
    f.write("\nRisk aversion: ")
    f.write(str(risk_aversion))

    sol =""
    for e in solution["result"]:
        sol=sol+str(e).replace(".0","")[:4] + "   "

    f.write("\nSolution "+ sol)
    f.write("\nRisk: " + trunc(solution['risk']))
    f.write("\nReturns: " + trunc(solution['returns']))
    f.write("\nResult: " + trunc(get_result_basic(solution,risk_aversion),5))

    f.close()
  