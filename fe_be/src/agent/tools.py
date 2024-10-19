# import math
# import re

# import numexpr
from langchain_core.tools import BaseTool, tool
import os
import numpy as np
import pandas as pd

# def calculator_func(expression: str) -> str:
#     """Calculates a math expression using numexpr.

#     Useful for when you need to answer questions about math using numexpr.
#     This tool is only for math questions and nothing else. Only input
#     math expressions.

#     Args:
#         expression (str): A valid numexpr formatted math expression.

#     Returns:
#         str: The result of the math expression.
#     """

#     try:
#         local_dict = {"pi": math.pi, "e": math.e}
#         output = str(
#             numexpr.evaluate(
#                 expression.strip(),
#                 global_dict={},  # restrict access to globals
#                 local_dict=local_dict,  # add common mathematical functions
#             )
#         )
#         return re.sub(r"^\[|\]$", "", output)
#     except Exception as e:
#         raise ValueError(
#             f'calculator("{expression}") raised error: {e}.'
#             " Please try again with a valid numerical expression"
#         )


# calculator: BaseTool = tool(calculator_func)
# calculator.name = "Calculator"

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

def get_inspiration_tool() -> str:
    """Inspiration tool proviedes salesman inspiration to be better at his job
    
    Returns:
        inspiration (str) a invaluable tips and tricks that change life
    """
    # print(os.listdir())
    # with open("inspiration.txt", "r") as f:
    #     inspiration = f.readlines()
    inspiration = [
          "The general who wins the battle makes many calculations in his temple before the battle is fought. The general who loses makes but few calculations beforehand.",
  "A leader leads by example not by force.",
  "The control of a large force is the same principle as the control of a few men: it is merely a question of dividing up their numbers.",
  "The ultimate in disposing one's troops is to be without ascertainable shape. Then the most penetrating spies cannot pry in nor can the wise lay plans against you.",
  "If words of command are not clear and distinct, if orders are not thoroughly understood, the general is to blame. But if his orders ARE clear, and the soldiers nevertheless disobey, then it is the fault of their officers.",
  "Strategy without tactics is the slowest route to victory. Tactics without strategy is the noise before defeat.",
  "All warfare is based on deception.",
  "If fighting is sure to result in victory, then you must fight.",
  "One defends when his strength is inadaquate, he attacks when it is abundant.",
  "The quality of decision is like the well-timed swoop of a falcon which enables it to strike and destroy its victim.",
  "When the enemy is at ease, be able to weary him; when well fed, to starve him; when at rest, to make him move. Appear at places to which he must hasten; move swiftly where he does not expect you.",
  "If you know your enemy and you know yourself you need not fear the results of a hundred battles. If you know yourself but not the enemy for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself you will succumb in every battle.",
  "The general who advances without coveting fame and retreats without fearing disgrace, whose only thought is to protect his country and do good service for his sovereign, is the jewel of the kingdom.",
  "For to win one hundred victories in one hundred battles is not the acme of skill. To subdue the enemy without fighting is the acme of skill.",
  "What the ancients called a clever fighter is one who not only wins, but excels in winning with ease.",
  "To a surrounded enemy, you must leave a way of escape.",
  "To know your Enemy, you must become your Enemy.",
  "Thus, what is of supreme importance in war is to attack the enemy's strategy.",
  "A leader leads by example, not force.",
  "Too frequent rewards indicate that the general is at the end of his resources; too frequent punishments that he is in acute distress.",
  "Pretend inferiority and encourage his arrogance.",
  "All men can see these tactics whereby I conquer, but what none can see is the strategy out of which victory is evolved.",
  "If we do not wish to fight, we can prevent the enemy from engaging us even though the lines of our encampment be merely traced out on the ground. All we need to do is to throw something odd and unaccountable in his way.",
  "A military operation involves deception. Even though you are competent, appear to be incompetent. Though effective, appear to be ineffective.",
  "Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win.",
  "The best victory is when the opponent surrenders of its own accord before there are any actual hostilities... It is best to win without fighting.",
  "Opportunities multiply as they are seized.",
  "Speed is the essence of war. Take advantage of the enemy's unpreparedness; travel by unexpected routes and strike him where he has taken no precautions.",
  "If your opponent is of choleric temperament, seek to irritate him.",
  "Management of many is the same as management of few. It is a matter of organization.",
  "The good fighters of old first put themselves beyond the possibility of defeat, and then waited for an opportunity of defeating the enemy.",
  "Build your opponent a golden bridge to retreat across.",
  "Swift as the wind. Quiet as the forest. Conquer like the fire. Steady as the mountain.",
  "It is essential to seek out enemy agents who have come to conduct espionage against you and to bribe them to serve you. Give them instructions and care for them. Thus doubled agents are recruited and used.",
  "Now the reason the enlightened prince and the wise general conquer the enemy whenever they move and their achievements surpass those of ordinary men is foreknowledge.",
  "And therefore those skilled in war bring the enemy to the field of battle and are not brought there by him.",
  "There is no instance of a nation benefitting from prolonged warfare.",
  "When able to attack, we must seem unable; when using our forces, we must seem inactive; when we are near, we must make the enemy believe we are far away; when far away, we must make him believe we are near.",
  "When torrential water tosses boulders, it is because of its momentum. When the strike of a hawk breaks the body of its prey, it is because of timing.",
  "Secret operations are essential in war; upon them the army relies to make its every move.",
  "It is said that if you know your enemies and know yourself, you will not be imperilled in a hundred battles; if you do not know your enemies but do know yourself, you will win one and lose one; if you do not know your enemies nor yourself, you will be imperilled in every single battle.",
  "He who knows when he can fight and when he cannot will be victorious.",
  "Subtle and insubstantial, the expert leaves no trace; divinely mysterious, he is inaudible. Thus he is master of his enemy's fate.",
  "A skilled commander seeks victory from the situation and does not demand it of his subordinates."
    ]

    return str(inspiration)


inspiration_tool: BaseTool = tool(get_inspiration_tool)
inspiration_tool.name = "inspiration_tool"


def knowdlege_about_client_tool(client_name: str) -> str:
    """Provides knowdlege about clinets

    Args:
        client_name (str): client name

    Return:
        client_info (str): information about clinet
    
    """
    knowdlege = {
    "Biedronka": {
      "industry": "Handel detaliczny",
      "contact_person": {
        "name": "Jan Kowalski",
        "email": "jan.kowalski@biedronka.pl",
        "phone": "+48 123 456 789"
      },
      "annual_revenue": "65 miliardów PLN",
      "locations": 3300,
      "notes": "Biedronka jest największą siecią dyskontów w Polsce, znaną z szerokiej oferty produktów marek własnych, które dostępne są w niskich cenach. Sieć kładzie szczególny nacisk na atrakcyjne promocje oraz budowanie lojalności klientów dzięki konkurencyjnej ofercie."
    },
    "Lidl": {
      "industry": "Handel detaliczny",
      "contact_person": {
        "name": "Anna Nowak",
        "email": "anna.nowak@lidl.pl",
        "phone": "+48 987 654 321"
      },
      "annual_revenue": "49 miliardów PLN",
      "locations": 800,
      "notes": "Lidl, będący jedną z wiodących europejskich sieci dyskontowych, zdobył popularność dzięki oferowaniu wysokiej jakości produktów, szczególnie świeżej żywności, w atrakcyjnych cenach. Sieć rozwija także linie produktów premium, podkreślając ich jakość i różnorodność."
    },
    "Carrefour": {
      "industry": "Handel detaliczny",
      "contact_person": {
        "name": "Piotr Wiśniewski",
        "email": "piotr.wisniewski@carrefour.pl",
        "phone": "+48 456 789 123"
      },
      "annual_revenue": "24 miliardy PLN",
      "locations": 900,
      "notes": "Carrefour to jeden z najstarszych graczy na rynku hipermarketów w Polsce. Sieć oferuje zarówno szeroki wybór artykułów spożywczych, jak i produktów przemysłowych. Znana jest z organizowania licznych akcji promocyjnych oraz prowadzenia szerokiej działalności w zakresie e-commerce."
    },
    "Auchan": {
      "industry": "Handel detaliczny",
      "contact_person": {
        "name": "Ewa Jankowska",
        "email": "ewa.jankowska@auchan.pl",
        "phone": "+48 654 321 987"
      },
      "annual_revenue": "18 miliardów PLN",
      "locations": 100,
      "notes": "Auchan to globalna sieć hipermarketów, która stawia na szeroki wybór produktów oraz konkurencyjne ceny. Firma dąży do zrównoważonego rozwoju, wprowadzając liczne inicjatywy proekologiczne i dbając o lokalne społeczności, z którymi współpracuje."
    },
    "Kaufland": {
      "industry": "Handel detaliczny",
      "contact_person": {
        "name": "Tomasz Zieliński",
        "email": "tomasz.zielinski@kaufland.pl",
        "phone": "+48 321 987 654"
      },
      "annual_revenue": "16 miliardów PLN",
      "locations": 230,
      "notes": "Kaufland, niemiecka sieć supermarketów, oferuje szeroką gamę produktów, w tym żywność, artykuły gospodarstwa domowego oraz elektronikę. Sieć stawia na jakość i niskie ceny, przyciągając zarówno klientów ceniących oszczędności, jak i osoby poszukujące produktów wyższej jakości."
    }
  }


    return str(knowdlege.get(client_name, f"no information about client: {client_name}, available data for: {knowdlege.keys()}"))


knowdlege_about_client: BaseTool = tool(knowdlege_about_client_tool)
knowdlege_about_client.name = "knowdlege_about_client"


def get_explanation_tool() -> pd.DataFrame:
    """Explanation tool provides salesman explanation of the future sales prediction.
    
    Returns:
        plot (pandas.DataFrame) a data for the chart showing future sales dynamics
    """
    date_range = pd.date_range(start='2023-01-01', periods=10, freq='D')
    float_values = np.random.rand(10) * 100
    df = pd.DataFrame({
        'Date': date_range,
        'Value': float_values
    })

    return df


explanation_tool: BaseTool = tool(get_explanation_tool)
explanation_tool.name = "explanation_tool"

if __name__ == "__main__":
    print(get_inspiration_tool())

    print(knowdlege_about_client_tool("Biedronka"))

    print(get_explanation_tool())