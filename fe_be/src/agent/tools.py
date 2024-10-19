import math
import re

import numexpr
from langchain_core.tools import BaseTool, tool


def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.

    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )


calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"

def mock_sales_data_fun(location_id, product_id) -> str:
    """Gets digeastable sales insights based on location and product id, both location and product ids are intigers

    Args:
        location_id (int): integer representing location id: 1, 2, 3
        product_id (int): integer representing product id: 1, 2, 3

    Returns:
        str: The result of the math expression.
    """
    location_id, product_id = str(location_id), str(product_id)
    return {
        "1": {
            "1": [
                "Sales have increased by 15% over the last three months, with peak sales observed during weekends.",
                "Monthly sales consistently reach $10,000, with a spike during the holiday season."
            ],
            "2": [
                "Sales dropped by 5% last quarter due to supply chain issues.",
                "Weekly sales show a 20% increase when promotional discounts are applied."
            ],
            "3": [
                "Top-selling product accounts for 30% of total sales.",
                "Customer foot traffic increased by 25% during the summer months."
            ],
            "4": [
                "Sales of organic products have doubled compared to last year.",
                "Customer loyalty program members spend 40% more than non-members."
            ],
            "5": [
                "Average transaction value is $25, with a growth trend over the past year.",
                "Sales forecast for the next quarter predicts a 10% increase due to upcoming events."
            ]
        },
        "2": {
            "1": [
                "Sales have increased by 10% during promotional events.",
                "Customer retention has improved with a 5% increase in repeat purchases."
            ],
            "2": [
                "Sales of seasonal products have shown significant growth.",
                "Average monthly sales are steady at $8,000."
            ],
            "3": [
                "Sales data shows that new product introductions lead to a 15% overall increase.",
                "A recent marketing campaign resulted in a 25% spike in sales."
            ],
            "4": [
                "Organic product sales are projected to grow by 20% next quarter.",
                "Customer feedback indicates a strong preference for local brands."
            ],
            "5": [
                "Sales reports indicate a positive trend for online orders.",
                "Discounted items see a 30% increase in sales during promotions."
            ]
        }
    }[location_id][product_id]

sales_data: BaseTool = tool(mock_sales_data_fun)
sales_data.name = "Sales_data"




def get_data_from_database() -> str:
    """Fetch data from SQL database and return it as a dictionary

    Returns:

    """
    # The best-selling products are:
    # 1. **Wimmers gute Semmelknödel** - Sold 212,968 units
    # 2. **Gorgonzola Telino** - Sold 212,882 units
    # 3. **Steeleye Stout** - Sold 211,790 units
    # 4. **Perth Pasties** - Sold 211,303 units
    # 5. **Zaanse koeken** - Sold 210,925 units
    data = {
        1: {
            "item": "Wimmers gute Semmelknödel",
            "count": 212968, 
        },
        2: {
            "item": "Gorgonzola Telino",
            "count": 212882,
        },
        3: {
            "item": "Steeleye Stout",
            "count": 211790,
        },
        4: {
            "item": "Perth Pasties",
            "count": 211303,
        },
        5: {
            "item": "Zaanse koeken",
            "count": 210925,
        },
    }

    return str(data)


data_from_database: BaseTool = tool(get_data_from_database)
data_from_database.name = "data_from_database"