#import os

#print(os.environ['OPENAI_API_KEY'])
#print(open('.env','r').read())

import pandas as pd
import os

df = pd.read_excel('/Users/andreasbrogaard/Documents/dsp_project/EDC w. description.xlsx')

system_message = ("You are a parameter identifier you are to identify the parameters. Your output is to json and only json. do not nest any variables in the json, do not make an introduction or summary of your response")

parameters_schema = {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": 'Divide locations into categories such as neighborhoods, districts, or proximity to amenities (downtown, suburban, rural).',
        },
        "Number of bathrooms": {
            "type": "string",
            "enum": ['1-1.5 bathrooms', '2-2.5 bathrooms', '3+ bathrooms'],
            "description": 'The stated number of bathrooms. If no number of bathrooms is provided, return "not_stated".',
        },
        "Condition of the house": {
            "type": "string",
            "enum": ["new construction", "renovated", "fixer-upper"],
            "description": 'Return the condition of the house as mentioned".',
        },
        "amenities": {
            "type": "array",
            "Balcony": {
                "type": "Boolean",
            },
            "Garden": {
                "type": "Boolean",
            },
            "Parking": {
                "type": "Boolean",
            },
            "Swimming pool": {
                "type": "Boolean",
            },
            "Fireplace": {
                "type": "Boolean",
            },
            "Garage": {
                "type": "Boolean",
            },
            "Basement": {
                "type": "Boolean",
            },
            "Elevator": {
                "type": "Boolean",
            },
            "Air conditioning": {
                "type": "Boolean",
            },
            "Heating Type": {
                "type": "string",
            },
            "description": 'Return the amenities mentioned in the description.',
        },
        "view": {
            "type": "string",
            "enum": ["city", "sea", "mountain", "no view", "not_stated"],
            "description": 'Return the view mentioned in the description.',
        },
    },
    #"required": ["location", "budget_level", "purpose"],
}

print(system_message + str(parameters_schema) + df['Description'].iloc[1])