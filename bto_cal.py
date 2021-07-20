import math
import general_computation

'''
age <= 35 
nationality = 4 different combi. 
    sg = 1
    pr = 2
    f = 3
    eg sg x sg = 1, sg x pr = 2, sg x f = 3, pr * pr = 4, pr * f = 6, f * f = 9
    classify according to numbers
    both sg == 1
    both f == 9 ...
monthly_income = sum
first_time = true/ false
    what about married? if one party false --> overall false or true?
'''

def get_grants(marital_status, age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    # Dummy var for applicant 2 all 0
    if(marital_status == "Married"):
        return married_cal(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2)
    else:
        return single_cal(age1, nationality1, mthInc1, first_time1)

def married_cal(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    eligible_grants = []
    # Get EHG 
    ehg = general_computation.get_ehg_married_bto(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2)
    if ehg: 
        eligible_grants.append(ehg)
    '''
    # Get FHG
    fhg = get_fg(nationality, applying_with_fam, monthly_income, marital_status, num_rm)
    if fhg: 
        eligible_grants.append(fhg)
    # Get PHG
    phg = get_phg(monthly_income, marital_status, dist_from_fam, applying_with_fam)
    if phg: 
        eligible_grants.append(phg)
    '''
    return eligible_grants

def single_cal(age1, nationality1, mthInc1, first_time1):
    eligible_grants = []
    # Get EHG 
    ehg = general_computation.get_ehg_single_bto(age1, nationality1, mthInc1, first_time1)
    if ehg: 
        eligible_grants.append(ehg)
    '''
    # Get FHG
    fhg = get_fg(nationality, applying_with_fam, monthly_income, marital_status, num_rm)
    if fhg: 
        eligible_grants.append(fhg)
    # Get PHG
    phg = get_phg(monthly_income, marital_status, dist_from_fam, applying_with_fam)
    if phg: 
        eligible_grants.append(phg)
    '''
    return eligible_grants


