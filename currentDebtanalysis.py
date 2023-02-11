import matplotlib.pyplot as plt
from datetime import datetime 
import sys


month_tracker={}
length_month_tracker={}
calander_dic={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
today = datetime.now()
current_month=today.month

if current_month==12:
    next_month=1
else: 
    next_month=current_month+1

delta_t={next_month:calander_dic[next_month]}


#variables
debt=[] 
all_debts={}

#debt_1 = {"Wells_Fargo":{"amount_due_info":{"inital_amount_due": 5000,"amount_due_data":[]}, "payment_info":{"monthly_payment": 200, "min_payment":[]},"interest_info":{"interest_rate":12, "interest_paid":[], "interest_total":0}, "month_info":{"month_tracker":[], "total_months":0}}}
debt_1 = {"Wells_Fargo":{"amount_due_info":{"inital_amount_due": 5000}, "payment_info":{"monthly_payment": 200},"interest_info":{"interest_rate":12}, "month_info":{}}}
debt_2 = {"Financial_Services":{"amount_due_info":{"inital_amount_due": 2500}, "payment_info":{"monthly_payment": 175},"interest_info":{"interest_rate":10}, "month_info":{}}}
debt_3 = {"BOA":{"amount_due_info":{"inital_amount_due": 50000}, "payment_info":{"monthly_payment": 1100},"interest_info":{"interest_rate":6}, "month_info":{}}}
debt_4 = {"Visa":{"amount_due_info":{"inital_amount_due": 14000}, "payment_info":{"monthly_payment": 265},"interest_info":{"interest_rate":9}, "month_info":{}}}
debt_5 = {"Visa_2":{"amount_due_info":{"inital_amount_due": 30000}, "payment_info":{"monthly_payment": 520},"interest_info":{"interest_rate":12}, "month_info":{}}}
debt_6 = {"Visa_3":{"amount_due_info":{"inital_amount_due": 36000}, "payment_info":{"monthly_payment": 750},"interest_info":{"interest_rate":15}, "month_info":{}}}
debt=[debt_1,debt_2,debt_3,debt_4,debt_5,debt_6]

#################################################################################################################################################################

#turn debt list into the dirctonary all_debt{}    
for i in debt:
    all_debts.update(i)

#sorting all_debt from least "amount_due" to greatest "amount_due"
sorted_debt_by_amount_due=dict(sorted(all_debts.items(),key=lambda x: x[1]["amount_due_info"]["inital_amount_due"]))


def currentDebtanalysis(all_debts_dic):
    global delta_t
    global next_month

    total_debt_info={"debt_dic":{},"total_debt_lists":[], "debt_lengths":{}, "longest_debt":{}, "total_interest":0 }

    for i,j in all_debts_dic.items():
        
        #adding new empty dictionary to each debt
        j["plotting_info"]={}

        #adding to amount_due_info dictionary
        j["amount_due_info"]["amount_due_data"]= [j["amount_due_info"]["inital_amount_due"]]
        j["amount_due_info"]["number_of_payments"] = 0

        #adding to payment_info dictionary
        j["payment_info"]["min_payment"] = []

        #adding to interest_info dictionary
        j["interest_info"]["interest_paid"] = []
        j["interest_info"]["interest_total"] = 0

        #adding to month_info dictionary 
        j["month_info"]["month_tracker"] = [next_month]
        j["month_info"]["total_months"] = 0

        #adding to plotting_info dictionary
        #j["plotting_info"]["x_axis_data"]=[]
    
        #check to make sure minimun payment > monthly_payment
        inital_interest = round(j["interest_info"]["interest_rate"] / 100 * (delta_t[next_month] / 365) * j["amount_due_info"]["inital_amount_due"], 2) 
        min_payment = round(inital_interest+(inital_interest*0.01),2)
        j["payment_info"]["min_payment"].append(min_payment)
        if j["payment_info"]["min_payment"][0] > j["payment_info"]["monthly_payment"]:
            sys.exit(f'The monthly payment for {i} must be greater then the minimum payment for this project.\n  Currently your monthly payment is ${j["payment_info"]["monthly_payment"]} and minimum payment is ${j["payment_info"]["min_payment"][0]}')

        #creating data for all_debts_dic created above
        while j["amount_due_info"]["amount_due_data"][-1]>=0:

            amount_due = j["amount_due_info"]["amount_due_data"][-1]
            payments = j["payment_info"]["monthly_payment"]
            interest = round(j["interest_info"]["interest_rate"] / 100 * (delta_t[next_month] / 365) * j["amount_due_info"]["amount_due_data"][-1], 2) 
            
            next_amount_due=amount_due-payments+interest    
            next_min_payment = round(interest+(interest*0.01),2)
            
            j["payment_info"]["min_payment"].append(next_min_payment)
            j["amount_due_info"]["amount_due_data"].append(round(next_amount_due,2)) 
            j["interest_info"]["interest_paid"].append(interest)
            
            #month iteration through calander dictionary
            if j["amount_due_info"]["amount_due_data"][-1]>=0:
                if next_month==12:
                    next_month=1
                    delta_t={next_month:calander_dic[next_month]}
                    j["month_info"]["month_tracker"].append(next_month)
                else:
                    next_month= next_month + 1
                    delta_t={next_month:calander_dic[next_month]}
                    j["month_info"]["month_tracker"].append(next_month) 
            else:
                next_month=current_month + 1
                delta_t= {next_month:calander_dic[next_month]}

        
            #clculating the sums
            j["month_info"]["total_months"]=len(j["month_info"]["month_tracker"])
            j["interest_info"]["interest_total"]=round(sum(j["interest_info"]["interest_paid"]),2)
            

            #creating x axis data for each debt to be plotted individually
            j["plotting_info"]["x_axis_data"]=(list(range(1,j["month_info"]["total_months"]+1)))

            #creating the dictionary debt_lengths to find the longest debt
            total_debt_info["debt_lengths"].update({i:j["month_info"]["total_months"]})

        #updating total_debt_info to have creditor and the list of amount_due_data    
        total_debt_info["debt_dic"].update({i:j["amount_due_info"]["amount_due_data"]})    

        #removing last data point because it is going past zero makes graph look jagged and adding the number of payments made to amount_due_info
        j["amount_due_info"]["amount_due_data"].pop()
        j["amount_due_info"]["number_of_payments"]=len(j["amount_due_info"]["amount_due_data"])

        #calculating the total interest accured from all debts
        total_debt_info["total_interest"]=round(total_debt_info["total_interest"]+j["interest_info"]["interest_total"],2)
            
    total_debt_info["longest_debt"]={max(total_debt_info["debt_lengths"]): max(total_debt_info["debt_lengths"].values())}

    print(all_debts_dic["Financial_Services"])

    #create debt total lists
    for i,j in total_debt_info["debt_dic"].items():
        length_diff=max(total_debt_info["longest_debt"].values())-len(j)
        length_diff_list=[0]*length_diff
        total_debt_info["total_debt_lists"].append((j+length_diff_list))

    #summing total_debt_lists to create total_debt_data
    total_debt_data=[round(sum(x),2) for x in zip(*total_debt_info["total_debt_lists"])]
    x_axis_total_data=(list(range(1,len(total_debt_data)+1)))

    ##########################################################################################

    #data summary
    print('\nHere is your current debt analysis based off your current monthly payment and intrest rate. \n')
    for i,j in all_debts_dic.items():
        print(f'If you owe {i} ${j["amount_due_info"]["inital_amount_due"]} at a fixed intrest rate of {j["interest_info"]["interest_rate"]}% and you are making a monthly payment of ${j["payment_info"]["monthly_payment"]} then it will take you {j["month_info"]["total_months"]} months to pay off the total amount due.\n In that time you will have paid a total of ${j["interest_info"]["interest_total"]} in intrest to {i}.\n' )

    print(f'At the end of {max(total_debt_info["longest_debt"].values())} months you will have paid a total of ${total_debt_info["total_interest"]} in intrest to your creditors.\n')  



    ##########################################################################################

    store_legend=[]
    #creating plots for all debts
    for i,j in all_debts_dic.items():
        plt.plot(j["plotting_info"]["x_axis_data"],j["amount_due_info"]["amount_due_data"])
        store_legend.append(i)
        plt.xlabel("time (months)")
        plt.ylabel("amount due ($)")
        plt.title("all debts")
    plt.legend(store_legend)
    plt.show()

    #plotting total data ready for snowballeffect comparison
    plt.plot(x_axis_total_data,total_debt_data)
    plt.xlabel("time (months)")
    plt.ylabel("amount due ($)")
    plt.title("Debt total")
    plt.legend(["total debt"])
    plt.show()

currentDebtanalysis(sorted_debt_by_amount_due)
  

    
    
    

