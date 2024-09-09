# Hard coded and crude. 
# I Need to do some reinvest calculations that I cant do in excel, eventally this can be a add-on app for the project.
import time

dates =          ['10/5/23', '11/7/23', '12/6/23', '01/4/24', '02/6/24', '03/5/24', '04/3/24', '05/3/24', '06/5/24', '07/3/24', '08/6/24']  
reinvest       = [1.2088,1.0776,2.4615,2.6932,1.0751,1.6619,2.7944,2.2807,1.6982,1.5732,1.0061] # follwos oct - august
price_at_month = [19.78,22.65,25.35,26.44,19.45,25.90,28.79,24.91,24.16,20.82,16.30]  # this follows oct - august so (10/5/23 --> 8/6/24)
initial_invest = 115000 # Inital amount invested at 10/5/23

# found values

shares = []
cashout = 0
t = len(dates) 

shares.append(round(initial_invest/price_at_month[0],5)) # sets inital shares.
print("Starting with $"+str(initial_invest)+" in CONY on 10/5/2023")
print("Date    | Price  | Dist   | Shares     | NAV (re)  | NAV (no-re)")
print("-"*80)
for i in range(0, t):
    cash = shares[i]* reinvest[i] # (shares * price per shares) is the distribution cash for the month.
    cashout += shares[0]*reinvest[i] # if you just took reimbursment and never reinvested
    shares.append(round(shares[i]+ (cash/price_at_month[i]),5)) # we take the cash and divide by the price of the stock to add on to out stock reinvest.
    NAV = round(shares[i]*price_at_month[i],2) # Net Asset Value is shares at current market pirce. 
    SADNAV = round(shares[0]*price_at_month[i],2) # Net Asset Value without reinvest.
    pam= "{:.2f}".format(price_at_month[i]) # Need to format for display...
    NAV= "{:.2f}".format(NAV) # Format
    cashprint = "{:.2f}".format(cashout)
    print(dates[i] +" | $"+pam+ " | $" + str(reinvest[i]) + " | " + str(shares[i]) + " | $" + str(NAV) + " | $" + str(SADNAV) + " with $" + cashprint + " cash.")
    time.sleep(.5)
    
