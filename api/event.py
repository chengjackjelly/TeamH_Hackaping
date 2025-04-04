from opperai import Opper
import os
import json

# Your API key will be loaded from the environment variable OPPER_API_KEY if not provided
OPPER_API_KEY = os.getenv("OPPER_API_KEY")
opper = Opper(api_key=OPPER_API_KEY)
def ai_analyzer(news):
    result, _ = opper.call(name="onboarding", input='''
    News: China hits back at Trump tariffs with extra 34% tax on US goods, deepening market turmoil


    Supply-chain:

    Default:

        "Stages": [
            "Raw Material Extraction",
            "Component Manufacturing",
            "Final Assembly",
        ],
        "Default Choice": [
            "Global mix (Rio Tinto, Glencore, Exxon)",
            "TSMC (Taiwan), CATL (China), Samsung (Korea)",
            "Foxconn (China)",
        ],

    Alternative:

    "Raw Material Extraction": {
            "Conflict-free minerals": {"Suppliers": "Pact-certified (Rwanda, Canada)"},
            "Recycled materials": { "Suppliers": "Redwood Materials (US)"}
    },
        "Component Manufacturing": {
            "US chips (Intel)": {"Suppliers": "Intel (US), Tesla (batteries)"},
            "India-based": { "Suppliers": "Tata Electronics, BYD India"}
        },
        "Final Assembly": {
            "Vietnam (renewables)": { "Suppliers": "Luxshare (Vietnam)"},
            "Mexico (NAFTA)": {"Suppliers": "Flex (Mexico)"}
        },

    Tell us which stages of the default choice will or will not affected and if it's affected, which alternative choice should we switch to.
    return me with this json format:

    [
  {
    "stage": "Raw Material Extraction",
    "affected": true/false,
    "choice": "Default" or "Alternative name",
    "reason": "Explain briefly why or why not this stage is affected and your choice rationale."
  },
  {
    "stage": "Component Manufacturing",
    "affected": true/false,
    "choice": "Default" or "Alternative name",
    "reason": "Explain briefly why or why not this stage is affected and your choice rationale."
  },
  {
    "stage": "Final Assembly",
    "affected": true/false,
    "choice": "Default" or "Alternative name",
    "reason": "Explain briefly why or why not this stage is affected and your choice rationale."
  }
]


    ''')
    return result

