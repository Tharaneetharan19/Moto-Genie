from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure GenAI
genai_api_key = 'AIzaSyCXUD9xY8Vh2OlXQ19FpSkedo3TkSku3MU'  # Replace with your actual GenAI API key
genai.configure(api_key=genai_api_key)

# Load datasets
cars_df = pd.read_csv("cars-dataset.csv")  # Adjust to your dataset location
bikes_df = pd.read_csv("bike_data.csv")  # Adjust to your dataset location

# Function to generate response using GenAI
def generate_response(prompt):
    """Generate a response using GenAI."""
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
            "response_mime_type": "text/plain",
        }
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Removed SECRET_KEY since no session or flash is needed
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'mysecretkey')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/car")
def car():
    companies = cars_df["Company"].unique()
    company_models = {company: cars_df[cars_df["Company"] == company]["Model"].unique().tolist() for company in companies}
    return render_template("index.html", companies=companies, company_models=company_models)

@app.route("/car_specification", methods=["GET", "POST"])
def car_specification():
    companies = cars_df["Company"].unique()
    company_models = {company: cars_df[cars_df["Company"] == company]["Model"].unique().tolist() for company in companies}

    if request.method == "POST":
        company = request.form.get("company")
        model = request.form.get("model")
        user_query = request.form.get("user_query")

        filtered_car = cars_df[(cars_df["Company"] == company) & (cars_df["Model"] == model)]

        if not filtered_car.empty:
            car_details = filtered_car.iloc[0].to_dict()
            prompt = (
                f"You are a car expert. Based on the following details, answer the user's question:\nCar Details: {car_details}\nUser's Question: {user_query}"
                f"You are an expert in vehicle specifications.\n\n"
                "Please provide a detailed answer to the user's question."
                "The answer should be detailed and informative."
                "Please include all relevant details and comparisons with other vehicles if necessary."
                "The answer should be at least 100 words long."
                "Never answer for any other questions other than vehicle related and its related queries."
            )

            try:
                response = generate_response(prompt)
                return render_template("car_specification.html", car_details=car_details, response=response, companies=companies, company_models=company_models)
            except Exception as e:
                return render_template("car_specification.html", error=f"Error: {str(e)}", companies=companies, company_models=company_models)
        else:
            return render_template("car_specification.html", error="No car found with the specified details.", companies=companies, company_models=company_models)
    
    return render_template("car_specification.html", companies=companies, company_models=company_models)

@app.route("/car_comparison", methods=["GET", "POST"])
def car_comparison():
    companies = cars_df["Company"].unique()
    company_models = {company: cars_df[cars_df["Company"] == company]["Model"].unique().tolist() for company in companies}

    if request.method == "POST":
        company1 = request.form.get("company1")
        model1 = request.form.get("model1")
        company2 = request.form.get("company2")
        model2 = request.form.get("model2")
        user_requirements = request.form.get("user_requirements")

        car1 = cars_df[(cars_df["Company"] == company1) & (cars_df["Model"] == model1)]
        car2 = cars_df[(cars_df["Company"] == company2) & (cars_df["Model"] == model2)]

        if not car1.empty and not car2.empty:
            car1_details = car1.iloc[0].to_dict()
            car2_details = car2.iloc[0].to_dict()
            prompt = f"You are a car expert. Compare the following two cars:\nCar 1 Details: {car1_details}\nCar 2 Details: {car2_details}\nUser's Requirements: {user_requirements}"

            try:
                response = generate_response(prompt)
                return render_template("car_comparison.html", car1_details=car1_details, car2_details=car2_details, response=response, companies=companies, company_models=company_models)
            except Exception as e:
                return render_template("car_comparison.html", error=f"Error: {str(e)}", companies=companies, company_models=company_models)
        else:
            return render_template("car_comparison.html", error="One or both cars not found.", companies=companies, company_models=company_models)
    
    return render_template("car_comparison.html", companies=companies, company_models=company_models)

@app.route("/bike")
def bike():
    companies = bikes_df["company_name"].unique()
    company_models = {company: bikes_df[bikes_df["company_name"] == company]["model"].unique().tolist() for company in companies}
    return render_template("index.html", companies=companies, company_models=company_models)

@app.route("/bike_specification", methods=["GET", "POST"])
def bike_specification():
    companies = bikes_df["company_name"].unique()
    company_models = {company: bikes_df[bikes_df["company_name"] == company]["model"].unique().tolist() for company in companies}

    if request.method == "POST":
        company = request.form.get("company")
        model = request.form.get("model")
        user_query = request.form.get("user_query")

        filtered_bike = bikes_df[(bikes_df["company_name"] == company) & (bikes_df["model"] == model)]

        if not filtered_bike.empty:
            bike_details = filtered_bike.iloc[0].to_dict()
            prompt = f"You are a bike expert. Based on the following details, answer the user's question:\nBike Details: {bike_details}\nUser's Question: {user_query}"

            try:
                response = generate_response(prompt)
                return render_template("bike_specification.html", bike_details=bike_details, response=response, companies=companies, company_models=company_models)
            except Exception as e:
                return render_template("bike_specification.html", error=f"Error: {str(e)}", companies=companies, company_models=company_models)
        else:
            return render_template("bike_specification.html", error="No bike found with the specified details.", companies=companies, company_models=company_models)

    return render_template("bike_specification.html", companies=companies, company_models=company_models)

@app.route("/bike_comparison", methods=["GET", "POST"])
def bike_comparison():
    companies = bikes_df["company_name"].unique()
    company_models = {company: bikes_df[bikes_df["company_name"] == company]["model"].unique().tolist() for company in companies}

    if request.method == "POST":
        company1 = request.form.get("company1")
        model1 = request.form.get("model1")
        company2 = request.form.get("company2")
        model2 = request.form.get("model2")
        user_requirements = request.form.get("user_requirements")

        bike1 = bikes_df[(bikes_df["company_name"] == company1) & (bikes_df["model"] == model1)]
        bike2 = bikes_df[(bikes_df["company_name"] == company2) & (bikes_df["model"] == model2)]

        if not bike1.empty and not bike2.empty:
            bike1_details = bike1.iloc[0].to_dict()
            bike2_details = bike2.iloc[0].to_dict()
            prompt = f"You are a bike expert. Compare the following two bikes:\nBike 1 Details: {bike1_details}\nBike 2 Details: {bike2_details}\nUser's Requirements: {user_requirements}"

            try:
                response = generate_response(prompt)
                return render_template("bike_comparison.html", bike1_details=bike1_details, bike2_details=bike2_details, response=response, companies=companies, company_models=company_models)
            except Exception as e:
                return render_template("bike_comparison.html", error=f"Error: {str(e)}", companies=companies, company_models=company_models)
        else:
            return render_template("bike_comparison.html", error="One or both bikes were not found.", companies=companies, company_models=company_models)

    return render_template("bike_comparison.html", companies=companies, company_models=company_models)

@app.route("/fuel_cost")
def fuel_cost():
    return render_template("fuel_cost.html")

@app.route("/fuel_cost", methods=["POST"])
def calculate_fuel_cost():
    fuel_cost = None
    if request.method == "POST":
        distance = float(request.form.get("distance"))
        fuel_efficiency = float(request.form.get("fuel_efficiency"))
        fuel_price = float(request.form.get("fuel_price"))
        fuel_cost = (distance / fuel_efficiency) * fuel_price
    return render_template("fuel_cost.html", fuel_cost=fuel_cost)



if __name__ == "__main__":
    app.run(debug=True)