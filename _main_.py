import time
import threading as th
import datetime as dt
import os
from algo import stock_predictions
from xl_modu import process_workbook

# For measure the running time
start = time.time()

# Data containers
stock_names = ['KO', 'T', 'PFE', 'GE', 'ABT', 'VZ', 'SBUX', 'NKE', 'BAC', 'WFC', 'CSCO', 'INTC', 'BMY', 'MRK']
predictions = [[], [], [], [], [], [], [], [], [], []]
r2_scores = [[], [], [], [], [], [], [], [], [], []]
scores = [[], [], [], [], [], [], [], [], [], []]
days = [0, 1, 2, 3, 4, 5, 6, 7, 14, 30]
prices = []
score_avgs = []
r2_avgs = []
algo_use = [0, 0, 0, 0, 0, 0]  # 1-lin_reg, 2-poly1, 3-poly2, 4-lasso, 5-bayesian, 6-ridgeCV

# Delete existing file of the current day for reusing
today = dt.datetime.today().date()
if os.path.exists(f'xl_Static_analyzes/Data_Anlaz_{today}.xlsx'):
    os.remove(f'xl_Static_analyzes/Data_Anlaz_{today}.xlsx')

# Activation of the algorithm
print('Start iterate on the stocks list')
for stock_name in stock_names:
    print(f'Activate Algorithm for {stock_name}')
    t2 = th.Thread(target=stock_predictions, args=(stock_name, predictions, prices, days, r2_scores, scores, algo_use, score_avgs, r2_avgs))
    t2.start()
    t2.join()

print('Results:\n', predictions, '\n', prices, '\n', r2_scores, '\n', scores, '\n', algo_use, '\n', score_avgs, '\n', r2_avgs)

# Create xl file to display the analyzed data
print("Create result\'s xl file")
process_workbook(stock_names, predictions, prices, r2_scores, scores, score_avgs, r2_avgs)

# For the running time of the program
end = time.time()
print("Running time of the program:", (end-start)/60, " min")