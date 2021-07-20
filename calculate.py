import math
import bto_cal
import resale_cal


# Get lists of grants
def get_grants(sale_type, marital_status, estDist, num_rm, age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    if sale_type == "BTO":
        return bto_cal.get_grants(marital_status, age1, nationality1, mthInc1, first_time1, 
                                  age2, nationality2, mthInc2, first_time2) 
    elif sale_type == "resale":
        return resale_cal.get_grants(marital_status, estDist, num_rm, age1, nationality1, mthInc1, first_time1, 
                                     age2, nationality2, mthInc2, first_time2)
    else:
        return []

def get_total_grant(eligible_grants):
    """ Total grants for mortgage computation """
    total = 0
    for grant in eligible_grants:
        total += grant[1]
    return total

def get_stamp_duty(flat_price):
    total = 0
    if(flat_price - 180000 >= 0):
        total += 180000 * 0.01
        flat_price -= 180000
    else:
        total += flat_price * 0.01
        flat_price = -1

    if(flat_price - 180000 >= 0):
        total += 180000 * 0.02
        flat_price -= 180000
    else:
        total += flat_price * 0.02
        flat_price = -1
    
    if(flat_price - 640000 >= 0):
        total += 640000 * 0.03
        flat_price -= 640000
    else:
        total += flat_price * 0.03
        flat_price = -1
    
    if(flat_price >= 0):
        total += flat_price * 0.04
    
    return total

def get_legal_fee(flat_price):
    total = 0
    if(flat_price - 30000 >= 0):
        total += 30000 * 0.0009
        flat_price -= 30000
    else:
        total += flat_price * 0.0009
        flat_price = -1

    if(flat_price - 30000 >= 0):
        total += 30000 * 0.00072
        flat_price -= 30000
    else:
        total += flat_price * 0.00072
        flat_price = -1
    
    if(flat_price >= 0):
        total += flat_price * 0.0006
    
    return total

def get_downpayment(flat_price):
    return flat_price * 0.1

def get_option_fee(num_rm):
    if(num_rm >= 4):
        return 2000
    elif(num_rm == 3):
        return 1000
    else:
        return 500

def median_renovation():
    return 44000


def get_upfront_payment(flat_price, num_rm):
    total = get_stamp_duty(flat_price) + get_legal_fee(flat_price) + get_downpayment(flat_price) + get_option_fee(num_rm) #+ median_renovation()
    return total

def get_morgage(house_price, upfront_payment, total_grant, interest_rate, loan_years):
    p = house_price - total_grant - upfront_payment

    monthly_int_rate = (interest_rate / 100) / 12
    num_of_payment = loan_years * 12

    A = monthly_int_rate * math.pow(1 + monthly_int_rate, num_of_payment)
    B = math.pow(1 + monthly_int_rate, num_of_payment) - 1

    monthly_mor = p*(A/B)
    
    return monthly_mor

def median_housing_tax(num_rm): # Assume is owner occupied la, else need one additional input
    if num_rm <= 2:
        mav = 5100
        tax = 0
    elif num_rm == 3:
        mav = 7860
        tax = 0
    elif num_rm == 4:
        mav = 9860
        tax = 74.4
    elif num_rm == 5:
        mav = 10380
        tax = 95.2
    else:
        mav = 10680
        tax = 107.2
    return tax

def median_utilities():
    return 156.71

def get_monthly_payment(montly_installment, num_rm):
    total_expenses = montly_installment + median_housing_tax(num_rm)
    return total_expenses

def get_msr_and_status(monthly_income, monthly_payment):
    msr = monthly_payment / monthly_income * 100

    if (msr < 30):
        return ("Healthy", "Good")
    else:
        return ("Un-Healthy", "Bad")
