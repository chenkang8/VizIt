import logging
from flask import Flask, redirect, url_for, render_template, request, current_app, json
import calculate 

app = Flask(__name__)

def load_listings_data():
    """ Load Feature1 Listing Data """
    try:
        app.logger.debug("loading listing data...")
        with app.open_resource("sample_data.json") as f:
            listing_data = json.load(f)
            f.close()
        app.logger.debug("listing data loaded") 
        return listing_data
    except:
        app.logger.debug("Something went wrong")
        
# For use with gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.debug("THIS IS A TEST")
    app.listing_data = load_listings_data()
        
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
        sale_type = selection["sale_type"]
    except Exception as e:
        #Todo, perhaps have some exception handling 
        return e

    return render_template("feature1_form.html", listing_name = name, sale_type = sale_type,
                           price3Room = price_3room, price4Room = price_4room, price5Room = price_5room)

@app.route("/f1_form_results", methods=["POST", "GET"])
def feature1_form_results():
    if request.method == "POST":
        # Passalong values - can be replaced with lookup by ID 
        listing_name = request.form["listingName"]
        
        ## Form input retrieval & validation  
        flat_type = request.form["flatType"]
        flat_price = request.form["flatPrice"]
        
        maritial_status = request.form["mstatus"]
        
        # Details for Applicant 1 
        age1 = request.form["age"]
        age1 = 35 if age1 == '' else int(age1)
        nationality1 = request.form["nationality"]
        first_time1 = request.form["firstTime"]
        monthly_income1 = request.form["mthInc"]
        monthly_income1 = 4500 if monthly_income1 == '' else int(monthly_income1)
        
        # Details for Applicant 2 (passed in but functionally ignored if Single)
        age2 = request.form["age2"]
        age1 = 35 if age1 == '' else int(age1)
        nationality2 = request.form["nationality2"]
        first_time2 = request.form["firstTime2"]
        monthly_income2 = request.form["mthInc2"]
        monthly_income2 = 4500 if monthly_income2 == '' else int(monthly_income2)
        
        # Sale Type
        sale_type = request.form["saleType"]
        if sale_type == "resale":
            estDist = request.form["estDist"]
        else: 
            estDist = "over"
        
        ##  Calculation logic ## 
        flat_price = int(flat_price)
        num_rooms = int(flat_type[0])
        
        # Get eligible grants (as list)
        num_rm = int(flat_type[0])
        eligible_grants = calculate.get_grants(sale_type, maritial_status, estDist, num_rm, 
                                               age1, nationality1, monthly_income1, first_time1, 
                                               age2, nationality2, monthly_income2, first_time2) 
        total_grant = calculate.get_total_grant(eligible_grants)

        # Calculate other payments 
        interest_rate = 2.6
        loan_years = 25
        
        upfront_payment = calculate.get_upfront_payment(flat_price, num_rooms)
        monthly_mor = round(calculate.get_morgage(flat_price, upfront_payment, total_grant, interest_rate, loan_years), 2)
        monthly_payment = round(calculate.get_monthly_payment(monthly_mor, num_rooms), 2)

        # Get MSR and Financial status
        total_household_income = monthly_income1 if maritial_status == "Single" else monthly_income1 + monthly_income2
        msr, fin_status = calculate.get_msr_and_status(total_household_income, monthly_payment) # String
        
        # Break downs
        stamp_duty = calculate.get_stamp_duty(flat_price)
        legal_fees = calculate.get_legal_fee(flat_price)
        downpayment = calculate.get_downpayment(flat_price)
        option_fee = calculate.get_option_fee(num_rooms)
        renovation = calculate.median_renovation()
        installment = monthly_mor
        utilities = calculate.median_utilities()
        property_tax = calculate.median_housing_tax(num_rooms)
        
        return render_template("feature1_form_results.html",
                            # Passalong
                            listing_name = listing_name, 
                            flatType = flat_type, flatPrice = flat_price,
                            mthInc = "{:.2f}".format(total_household_income),
                            # Computed
                            msr = msr, fin_status = fin_status,
                            eligible_grants = eligible_grants, # List  
                            monthly_mor = "{:.2f}".format(monthly_mor),
                            total_grant = "{:.2f}".format(total_grant),
                            upfront_payment = "{:.2f}".format(upfront_payment), 
                            monthly_payment = "{:.2f}".format(monthly_payment), 
                            # Breakdowns 
                            stamp_duty = "{:.2f}".format(stamp_duty), 
                            legal_fees = "{:.2f}".format(legal_fees),
                            downpayment = "{:.2f}".format(downpayment),
                            option_fee = "{:.2f}".format(option_fee), 
                            renovation = "{:.2f}".format(renovation), 
                            installment = "{:.2f}".format(installment),
                            utilities = "{:.2f}".format(utilities),
                            property_tax = "{:.2f}".format(property_tax)
                            )
    else:
        # TODO: throw some http error here
        return render_template("feature1_form.html")
     
    
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

if __name__ == "__main__":
    app.logger.debug("APP IS RUNNING")
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.listing_data = load_listings_data()
    app.run(debug = True)
