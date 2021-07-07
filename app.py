from flask import Flask, redirect, url_for, render_template, request, current_app, json
import calculate 
import sys
    
    
app = Flask(__name__)

def load_listings_data():
    """ Load Feature1 Listing Data """
    try:
        print("loading listing data...")
        with app.open_resource("sample_data.json") as f:
            listing_data = json.load(f)
            f.close()
        print("listing data loaded") 
        return listing_data
    except:
        print("Something went wrong")

'''       
@app.route("/")
def feature1_main():
    #return render_template("index.html", listing_data = current_app.listing_data)\
    return render_template("feature1_main.html", listing_data = current_app.listing_data)  

@app.route("/f1_formpage")
def feature1_form():
    town = request.args.get('town', default='Woodlands', type=str)
    id = request.args.get('id', default='1', type=str)
    # Lookup the relevant record
    try: 
        selection = current_app.listing_data[town]["data"][id]
        name = selection["name"]
        prices = selection["prices"]
        price_3room = prices["3_room"] if "3_room" in prices else -1
        price_4room = prices["4_room"] if "4_room" in prices else -1
        price_5room = prices["5_room"] if "5_room" in prices else -1
    except Exception as e:
        #Todo, perhaps have some exception handling 
        return e

    return render_template("feature1_form.html", listing_name = name, 
                           price3Room = price_3room, price4Room = price_4room, price5Room = price_5room)

@app.route("/f1_form_results", methods=["POST", "GET"])
def feature1_form_results():
    if request.method == "POST":
        # Passalong values - can be replaced with lookup by ID 
        listing_name = request.form["listingName"]
        # Form input values 
        flat_type = request.form["flatType"]
        flat_price = request.form["flatPrice"]
        mstatus = request.form["mstatus"]
        age = request.form["age"]
        nationality = request.form["nationality"]
        first_time = request.form["firstTime"]
        monthly_income = request.form["mthInc"]
        estDist = request.form["estDist"]
        
        # Additional info 
        # TODO: add these inputs to form 
        applying_with_fam = "True"
        # BTO OR RESALE
        bto_or_resale = "bto"

        # Input validation & Default values
        monthly_income = 4500 if monthly_income == '' else int(monthly_income)
        age = 35 if age == '' else int(age)
            
        ##  Calculation logic ## 
        
        flat_price = int(flat_price)
        num_rooms = int(flat_type[0])
        
        # Get eligible grants (as list)
        eligible_grants = calculate.get_grants(nationality, monthly_income, mstatus, age, applying_with_fam, int(flat_type[0]), estDist) 
        total_grant = calculate.get_total_grant(eligible_grants)

        interest_rate = 2.6
        loan_years = 25
        
        upfront_payment = calculate.get_upfront_payment(flat_price, num_rooms)
        monthly_mor = round(calculate.get_morgage(flat_price, upfront_payment, total_grant, interest_rate, loan_years), 2)
        monthly_payment = round(calculate.get_monthly_payment(monthly_mor, num_rooms), 2)

        MSR = calculate.get_msr(monthly_income, monthly_payment) # String
        Fin_status = calculate.get_status(MSR)

        # Break downs
        stamp_duty = calculate.get_stamp_duty(flat_price)
        legal_fees = round(calculate.get_legal_fee(flat_price),2)
        downpayment = calculate.get_downpayment(flat_price)
        option_fee = calculate.get_option_fee(num_rooms)
        renovation = calculate.median_renovation()
        installment = monthly_mor
        utilities = calculate.median_utilities()
        property_tax = calculate.median_housing_tax(num_rooms)
        
        return render_template("feature1_form_results.html",
                            listing_name = listing_name, 
                            flatType = flat_type, flatPrice = flat_price, 
                            mstatus = mstatus, age = age, nationality = nationality, firstTime = first_time, 
                            mthInc = monthly_income, estDist = estDist, MSR = MSR, Fin_status = Fin_status,
                            eligible_grants = eligible_grants, # List  
                            monthly_mor = monthly_mor, total_grant = total_grant,
                            upfront_payment = upfront_payment, monthly_payment = monthly_payment,
                            # Breakdowns 
                            stamp_duty = stamp_duty,
                            legal_fees = legal_fees,
                            downpayment = downpayment,
                            option_fee = option_fee,
                            renovation = renovation,
                            installment = installment,
                            utilities = utilities,
                            property_tax = property_tax)
    else:
        # TODO: throw some http error here
        return render_template("feature1_form.html")
    
# @app.route("/test")
# def test_load():
#     return render_template("feature1_form_results.html")    
    
@app.route("/f2_main")
def feature2_form():
    return render_template("feature2_form.html")

@app.route("/f2_charts", methods=["POST", "GET"])
def feature2_results():
    if request.method == "POST":
        town = request.form["town"]
        flat_type = request.form["flat_type"]
        lease_commence_year = request.form["lease_commence_year"]
        
        return render_template("feature2_charts_display.html", 
                               town = town, flat_type = flat_type,
                               lease_commence_year = lease_commence_year )
    else:
        return render_template("feature2_charts_display.html")
'''
if __name__ == "__main__":
    print("THIS IS RUNNING")
    sys.stdout.flush()
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.listing_data = load_listings_data()
    app.run(debug = True)
