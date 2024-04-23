from openai import OpenAI
import pandas as pd

# Read CSV file into a pandas dataframe
df = pd.read_csv('/Users/andreasbrogaard/Documents/dsp_project/Aarhus Kommune Real Estate data - Scraped from EDC.csv')

system_message = ("You are a parameter identifier you are to identify the parameters. Your output is to json and only json. do not nest any variables in the json, do not make an introduction or summary of your response")

parameters_schema = {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": 'The desired destination location. Use city, state, and country format when possible. If no destination is provided, return "unstated".',
        },
        "budget_level": {
            "type": "string",
            "enum": ["low", "medium", "high", "not_stated"],
            "description": 'The desired budget level. If no budget level is provided, return "not_stated".',
        },
        "purpose": {
            "type": "string",
            "enum": ["business", "pleasure", "other", "non_stated"],
            "description": 'The purpose of the trip. If no purpose is provided, return "not_stated".',
        },
    },
    "required": ["location", "budget_level", "purpose"],
}

function_schema = {
    "name": "record_travel_request_attributes",
    "description": "Records the attributes of a travel request",
    "parameters": parameters_schema,
}

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": df["description"].iloc[1]}
  ],
  functions=[function_schema],
  function_calls=[{"name": function_schema["name"]}]
)



