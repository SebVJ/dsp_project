from openai import OpenAI

system_message = "You are a parameter identifier you are to identify the parameters. Your output is to json and only json. do not nest any variables in the json, do not make an introduction or summary of your response The parameters are as follows: Location: Discretization: Divide locations into categories such as neighborhoods, districts, or proximity to amenities (downtown, suburban, rural). Number of bathrooms: Discretization: Similar to bedrooms, categorize into ranges (e.g., 1-1.5 bathrooms, 2-2.5 bathrooms, 3+ bathrooms). Type of property (e.g., single-family home, condominium, townhouse): Discretization: Treat as categorical variables with each type being a separate category. Amenities/features (e.g., pool, garage, fireplace): Discretization: Create binary variables for each amenity/feature indicating its presence or absence. Balcony (true/false) Hardwood floors (true/false) Modern kitchen with appliances (true/false) Washer facilities in basement (true/false) Bicycle parking (True/False) Common courtyard (True/False) Common clubhouse (True/False) Shared green area (True/False) Condition of the house (e.g., new construction, renovated, fixer-upper): Discretization: Treat as categorical variables with each condition being a separate category. Distance to important locations (schools, public transportation, shopping centers): Do not mention the name but divide into group Discretization: Group distances into categories such as close (within 1 km), moderate (1-5 km), far (more than 5 km). View (e.g., ocean view, mountain view, city view): Discretization: Create binary variables for each type of view indicating its presence or absence. Ocean view: (True/False) Mountain view: (True/False) no view: (True/False) View not mentioned in text: (True/False) If the parameter is not clear in the text mark it as "not specified""






client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
  functions=[funcition_schema]
  funciton_calls=["name"function_call_schema""]
)

print(completion.choices[0].message)

