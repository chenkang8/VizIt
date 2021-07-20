import math
import general_computation

def get_grants(marital_status, estDist, num_rm, age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    # Dummy var for applicant 2 all 0
    if(marital_status == "Married"):
        return married_cal(estDist, num_rm, age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2)
    else:
        return single_cal(estDist, num_rm, age1, nationality1, mthInc1, first_time1)

def married_cal(estDist, num_rm, age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2):
    eligible_grants = []
    # Get EHG 
    ehg = general_computation.get_ehg_married_res(age1, nationality1, mthInc1, first_time1, age2, nationality2, mthInc2, first_time2)
    if ehg: 
        eligible_grants.append(ehg)
    # Get FHG
    fhg = general_computation.get_fg_married(num_rm, estDist, nationality1, mthInc1, nationality2, mthInc2)
    if fhg: 
        eligible_grants.append(fhg)
    # Get PHG
    phg = general_computation.get_phg_married(estDist, mthInc1, mthInc2)
    if phg: 
        eligible_grants.append(phg)

    return eligible_grants

def single_cal(estDist, num_rm, age1, nationality1, mthInc1, first_time1):
    eligible_grants = []
    # Get EHG 
    ehg = general_computation.get_ehg_single_res(age1, nationality1, mthInc1, first_time1)
    if ehg: 
        eligible_grants.append(ehg)
    # Get FHG
    fhg = general_computation.get_fg_single(num_rm, estDist, nationality1, mthInc1)
    if fhg: 
        eligible_grants.append(fhg)
    # Get PHG
    phg = general_computation.get_phg_single(estDist, mthInc1)
    if phg: 
        eligible_grants.append(phg)

    return eligible_grants

