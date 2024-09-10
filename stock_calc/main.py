# Hard coded and crude. 
# I Need to do some reinvest calculations that I cant do in excel, eventally this can be a add-on app for the project.
import argparse
import time

def reinvest_calc(data):
    if data == 'CONY' or data == 'cony':
        dates          = ['10/5/23', '11/7/23', '12/6/23', '01/4/24', '02/6/24', '03/5/24', '04/3/24', '05/3/24', '06/5/24', '07/3/24', '08/6/24', '09/5/24']  
        reinvest       = [1.2088,1.0776,2.4615,2.6932,1.0751,1.6619,2.7944,2.2807,1.6982,1.5732,1.0061,1.0432] # follwos oct - august
        price_at_month = [19.78,22.65,25.35,26.44,19.45,25.90,28.79,24.91,24.16,20.82,16.30,13.36]  # this follows oct - august so (10/5/23 --> 8/6/24)

    elif data == 'TSLY' or data == 'tsly':
        dates = ['01/05/2023', '02/07/2023', '03/07/2023', '04/05/2023', '05/04/2023', '06/06/2023', '07/06/2023', '08/03/2023', '09/07/2023', '10/05/2023', '11/07/2023', 
                 '12/06/2023', '01/04/2024', '02/06/2024', '03/05/2024', '04/03/2024', '05/03/2024', '06/05/2024', '07/03/2024', '08/06/2024', '09/05/2024']
        
        reinvest = [1.9972, 1.8058, 1.8046, 1.6572, 0.8804, 1.6066, 2.1322, 1.6606, 1.1698, 1.1538, 1.1692, 1.2078, 1.1130, 0.8092, 0.8109, 
                    0.6841, 0.6942, 0.6448, 1.0035, 0.9661, 0.8186]
        
        price_at_month = [21.22, 21.58, 20.84, 19.32, 19.70, 19.85, 19.65, 19.50, 19.89, 18.64, 17.87, 17.45, 16.88, 17.30, 17.74, 17.88, 18.00, 18.20, 18.12, 18.05, 17.98]








    # found values

    shares = []
    cashout = 0
    t = len(dates) 
    initial_invest = 10000 # Inital amount invested at 10/5/23

    shares.append(round(initial_invest/price_at_month[0],5)) # sets inital shares.
    print("Starting with $"+str(initial_invest)+" in " + data + " on 10/5/2023")
    print("Date    | Price  | Dist    | Shares    | NAV (re)  | NAV (no-re)")
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


def main():
    parser = argparse.ArgumentParser(description="Process a string argument.")
    parser.add_argument("input_string", type=str, help="A string input (e.g., 'goober')")
    args = parser.parse_args()
    input_str = args.input_string
    reinvest_calc(input_str)

if __name__ == "__main__":
    main()

    
