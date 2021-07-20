import math

# def conversion_married(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):

# def conversion_single(age1, nationality1, mthInc1, first_time1):
#     lst = []
#     age = age1 <= 35
#     return lst

# Enhanced Housing Grant (EHG)
def EHG_compute(monthly_income):
    min_inc = 1500
    EHG = 80000
    while(EHG >= 5000):
        if(monthly_income <= min_inc):
            return EHG
        else:
            EHG -= 5000
            min_inc += 500

## EHG For BTO
def get_ehg_married_bto(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    """ Enhanced Housing Grant (EHG) """
    ehg_amt = 0    
    monthly_income = mthInc1 + mthInc2
    if (monthly_income <= 9000 and nationality1 == "Singapore Citizen" and nationality2 == "Singapore Citizen"):
        ehg_amt = EHG_compute(monthly_income)
    '''
    # ONLY 2 ROOM FLEXI FOR BTO - NON-CITIZEN SPOUSE SCHEME
    ## SINCE WE DO NOT INCLUDE 2 ROOM BTO, IGNORE
    elif(monthly_income <= 9000 and nationality2 == "Singapore Citizen" and nationality2 != "Singapore Citizen" and age1 >= 21):
        ehg_amt = EHG_compute(monthly_income)/2
        # ref: https://dollarsandsense.sg/non-citizen-spouse-scheme-can-buy-hdb-bto-resale-flat-foreign-spouse/
    '''
    return ("EHG", ehg_amt) if ehg_amt > 0 else None

def get_ehg_single_bto(age1, nationality1, mthInc1, first_time1):
    """ Enhanced Housing Grant (EHG) """
    ehg_amt = 0
    if (mthInc1 <= 4500 and nationality1 == "Singapore Citizen" and age1 >= 35):
        ehg_amt = EHG_compute(mthInc1)/2

    return ("EHG", ehg_amt) if ehg_amt > 0 else None


## EHG For Resale
def get_ehg_married_res(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    """ Enhanced Housing Grant (EHG) """
    ehg_amt = 0    
    monthly_income = mthInc1 + mthInc2
    if (monthly_income <= 9000 and nationality1 == "Singapore Citizen" and nationality2 == "Singapore Citizen"):
        ehg_amt = EHG_compute(monthly_income)

    elif(monthly_income <= 9000 and nationality2 == "Singapore Citizen" and nationality2 != "Singapore Citizen" and age1 >= 21):
        ehg_amt = EHG_compute(monthly_income)/2
        # ref: https://dollarsandsense.sg/non-citizen-spouse-scheme-can-buy-hdb-bto-resale-flat-foreign-spouse/
    
    return ("EHG", ehg_amt) if ehg_amt > 0 else None

def get_ehg_single_res(age1, nationality1, mthInc1, first_time1):
    """ Enhanced Housing Grant (EHG) """
    ehg_amt = 0
    if (mthInc1 <= 4500 and nationality1 == "Singapore Citizen" and age1 >= 35):
        ehg_amt = EHG_compute(mthInc1)/2

    return ("EHG", ehg_amt) if ehg_amt > 0 else None


# Family grant
## Only for resale
def FG_compute(nationality1, nationality2, num_rm):
    if (nationality1 == "Foreigner" or nationality2 == "Foreigner"):
        return 0

    if num_rm < 5:
        grant = 50000
    else:
        grant = 40000

    if (nationality1 != "Singapore Citizen" or nationality2 != "Singapore Citizen"):
        grant -= 10000
        
    return grant

def get_fg_married(num_rm, estDist, nationality1, mthInc1, nationality2, mthInc2):
    fg_amt = 0
    monthly_income = mthInc1 + mthInc2   
    applying_with_fam = estDist == "Living w fam"  
    if (applying_with_fam and monthly_income <= 21000): # Applying together with more family members, such as with your parents
        fg_amt = FG_compute(nationality1, nationality2, num_rm)
    elif (not applying_with_fam and monthly_income <= 14000):
        fg_amt = FG_compute(nationality1, nationality2, num_rm)

    return ("FG", fg_amt) if fg_amt > 0 else None

def get_fg_single(num_rm, estDist, nationality1, mthInc1):
    fg_amt = 0
    applying_with_fam = estDist == "Living w fam"
    
    # Dummy var
    nationality2 = "Singapore Citizen"

    if (applying_with_fam and mthInc1 <= 10500): # Applying together with more family members, such as with your parents
        fg_amt = FG_compute(nationality1, nationality2, num_rm)/ 2
    elif (not applying_with_fam and mthInc1 <= 7000):
        fg_amt = FG_compute(nationality1, nationality2, num_rm)/ 2

    return ("FG", fg_amt) if fg_amt > 0 else None

# Proximity grant
## Only for resale
def get_phg_married(estDist): 
    phg_amg = 0     
    if estDist == "Living w fam":
        phg_amg = 30000
    elif estDist == "under":
        phg_amg = 20000

    return ("PHG", phg_amg) if phg_amg > 0 else None

def get_phg_single(estDist, mthInc1):   
    phg_amg = 0 
    if estDist == "Living w fam":
        phg_amg = 30000/2
    elif estDist == "under":
        phg_amg = 20000/2
                
    return ("PHG", phg_amg) if phg_amg > 0 else None