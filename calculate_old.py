import math

def get_ehg(nationality, monthly_income, marital_status, age):
    """ Enhanced Housing Grant (EHG) """
    ehg_amt = 0    
    if(marital_status == "Married"):
        monthly_income = monthly_income * 2 # Need to open up applicant 2
        if (monthly_income <= 9000 and nationality == "Singapore Citizen"):
            ehg_amt = EHG_compute(monthly_income)
    
        elif(monthly_income <= 9000 and nationality != "Singapore Citizen" and age >= 21):
            ehg_amt = EHG_compute(monthly_income)/2
    else: # Single
        if (monthly_income <= 4500 and nationality == "Singapore Citizen" and age >= 35):
            ehg_amt = EHG_compute(monthly_income)/2

    return ("EHG", ehg_amt) if ehg_amt > 0 else None

def EHG_compute(monthly_income):
    min_inc = 1500
    EHG = 80000
    while(EHG >= 5000):
        if(monthly_income <= min_inc):
            return EHG
        else:
            EHG -= 5000
            min_inc += 500

# Family grant
# Only for resale
def get_fg(nationality, applying_with_fam, monthly_income, marital_status, num_rm):
    fg_amt = 0
    if (marital_status == "Married"):
        monthly_income = monthly_income * 2 # Need to open up applicant 2      
        if applying_with_fam == "True" and monthly_income <= 21000: # Applying together with more family members, such as with your parents
            fg_amt = FG_compute(nationality, num_rm)
        elif applying_with_fam != "True" and monthly_income <= 14000:
            fg_amt = FG_compute(nationality, num_rm)
    else:
        if applying_with_fam == "True" and monthly_income <= 21000: # Applying together with more family members, such as with your parents
            fg_amt = FG_compute(nationality, num_rm)/ 2
        elif applying_with_fam != "True" and monthly_income <= 14000:
            fg_amt = FG_compute(nationality, num_rm)/ 2

    return ("FG", fg_amt) if fg_amt > 0 else None

def FG_compute(nationality, num_rm):
    if num_rm < 5:
        grant = 50000
    else:
        grant = 40000

    if nationality == "singaporePR":
        grant -= 10000
        
    return grant

# Proximity grant
## Only for resale
def get_phg(monthly_income, marital_status, dist_from_fam, applying_with_fam):
    phg_amg = 0 
    if (marital_status == "Married"):
        monthly_income = monthly_income * 2 # Need to open up applicant 2      
        if dist_from_fam == "under" and applying_with_fam == "True":
            phg_amg = 30000
        elif dist_from_fam == "under":
            phg_amg = 20000
    else:   
        if dist_from_fam == "under" and applying_with_fam == "True":
            phg_amg = 30000/2
        elif dist_from_fam == "under":
            phg_amg = 20000/2
                
    return ("PHG", phg_amg) if phg_amg > 0 else None

# Total grants for mortgage computation
def get_total_grant(eligible_grants):
    total = 0
    for grant in eligible_grants:
        total += grant[1]
    return total

# Get lists of grants
def get_grants(nationality, monthly_income, marital_status, age, applying_with_fam, num_rm, dist_from_fam):
    eligible_grants = []
    # Get EHG 
    ehg = get_ehg(nationality, monthly_income, marital_status, age)
    if ehg: 
        eligible_grants.append(ehg)
    # Get FHG
    fhg = get_fg(nationality, applying_with_fam, monthly_income, marital_status, num_rm)
    if fhg: 
        eligible_grants.append(fhg)
    # Get PHG
    phg = get_phg(monthly_income, marital_status, dist_from_fam, applying_with_fam)
    if phg: 
        eligible_grants.append(phg)
    return eligible_grants

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

def get_msr(monthly_income, monthly_payment):
    msr = monthly_payment / monthly_income * 100

    if (msr < 30):
        return "Healthy" 
    else:
        return "Un-Healthy" 

def get_status(msr):
    if (msr == "Healthy"):
        return "Good" # Green
    else:
        return "Bad" # Red 
