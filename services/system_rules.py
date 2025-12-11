country_from = "country_from"
currency_from_code = "currency_from_code"
currency_from_name = "currency_from_name"
country_to = "country_to"
currency_to_code = "currency_to_code"
currency_to_name = "currency_to_name"
capital_to = "capital_to"

SYSTEM_CONTENT = f"""
If the user’s request contains the phrase "from '<country_from_name>' to '<country_to_name>'",
respond **only** with a JSON object in the following format:

{{
   "{country_from}": "<country_from_name>",
   "{currency_from_code}": "<ISO code of the origin country’s currency>",
   "{currency_from_name}": "<Name of the origin country’s currency>",
   "{country_to}": "<country_to_name>",
   "{currency_to_code}": "<ISO code of the destination country’s currency>",
   "{currency_to_name}": "<Name of the destination country’s currency>",
   "{capital_to}": "<Capital city of the destination country>"
}}
"""