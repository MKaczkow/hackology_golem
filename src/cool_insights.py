def mock_sales_data(location_id, product_id):
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


def mock_competitive_analysis(location_id, product_id):
    return {
        "1": {
            "1": [
                "Competitors have introduced similar products at a lower price point, affecting sales performance.",
                "Market analysis shows our primary competitor has a 10% larger market share."
            ],
            "2": [
                "Competitors are investing heavily in digital marketing, impacting our visibility.",
                "A new competitor has opened nearby, focusing on sustainable products."
            ],
            "3": [
                "Several local shops are offering loyalty rewards that attract customers away from us.",
                "Competitor A has reduced prices by 15% on their top-selling items."
            ],
            "4": [
                "Product reviews indicate that our competitor’s items are perceived as higher quality.",
                "Competitor B is running aggressive social media campaigns to boost brand awareness."
            ],
            "5": [
                "Market share data suggests that our category is becoming more crowded.",
                "Competitors have recently expanded their product lines to include plant-based options."
            ]
        },
        "2": {
            "1": [
                "Competitor C has captured a significant share with aggressive pricing strategies.",
                "Local market trends show competitors are focusing on health-oriented products."
            ],
            "2": [
                "Price wars in the local market are impacting our profit margins.",
                "Competitors are leveraging influencer marketing to reach younger demographics."
            ],
            "3": [
                "Competitor D has introduced innovative packaging that attracts customers.",
                "Market analysis suggests a shift towards eco-friendly products is gaining traction."
            ],
            "4": [
                "Reviews show that competitor products receive higher ratings on quality.",
                "Competitors are conducting more in-store promotions, increasing their visibility."
            ],
            "5": [
                "Consumer feedback suggests competitors are perceived as more innovative.",
                "Competitors are focusing on expanding their online presence."
            ]
        }
    }[location_id][product_id]

def mock_profit_margins(location_id, product_id):
    return {
        "1": {
            "1": [
                "Current profit margins for similar products average around 25%, with opportunities for promotions to increase sales.",
                "Profit margins on organic items are typically higher at 30% compared to non-organic."
            ],
            "2": [
                "Promotional pricing strategies can increase margins by 5% if executed correctly.",
                "Our average margin has decreased by 3% due to increased supply costs."
            ],
            "3": [
                "Discounting too heavily can negatively impact overall profit margins.",
                "Margins on private label products are generally 35%."
            ],
            "4": [
                "Cross-merchandising has resulted in a 10% increase in margins for bundled products.",
                "Analyzing competitors' pricing reveals room to improve our margins."
            ],
            "5": [
                "Our most profitable category has a margin of 40%.",
                "Pricing optimization software suggests potential margin increases of 15%."
            ]
        },
        "2": {
            "1": [
                "Profit margins for seasonal items are fluctuating, averaging 20%.",
                "Investing in higher quality ingredients can boost margins by 10%."
            ],
            "2": [
                "New pricing strategies have led to improved margins for core products.",
                "Bulk purchasing options are increasing profit margins by 8%."
            ],
            "3": [
                "Collaborations with local brands can enhance our margins.",
                "Profitability analysis indicates that online sales have better margins than in-store."
            ],
            "4": [
                "Feedback indicates that customers are willing to pay more for premium products.",
                "Product bundling has shown an increase in overall margins."
            ],
            "5": [
                "Profit margins on new launches tend to be higher initially.",
                "Analyzing historical data reveals potential margin improvements in our pricing."
            ]
        }
    }


def mock_market_trends(location_id, product_id):
    return {
        "1": {
            "1": [
                "The market is trending towards organic and locally sourced products, creating an opportunity for our new line.",
                "Consumer interest in plant-based foods has surged by 25% this year."
            ],
            "2": [
                "Sustainability trends are influencing purchasing decisions, particularly among millennials.",
                "Health-conscious products are experiencing a rise in popularity."
            ],
            "3": [
                "Online grocery shopping is projected to grow by 20% in the next two years.",
                "There is a growing demand for gluten-free products across all demographics."
            ],
            "4": [
                "Consumers are willing to pay a premium for ethically sourced items.",
                "Convenience products are trending, with a preference for ready-to-eat meals."
            ],
            "5": [
                "Subscription-based models are gaining traction among consumers.",
                "Social media influences purchasing habits, especially among younger consumers."
            ]
        },
        "2": {
            "1": [
                "The market is seeing a shift towards more personalized shopping experiences.",
                "Trends indicate a growing preference for products with minimal packaging."
            ],
            "2": [
                "Research shows increased interest in vegan and vegetarian options.",
                "Health and wellness trends are influencing product development."
            ],
            "3": [
                "Customers are increasingly seeking products that support local communities.",
                "E-commerce trends suggest a rise in mobile shopping capabilities."
            ],
            "4": [
                "Environmental sustainability is becoming a key factor in purchasing decisions.",
                "Data shows a significant increase in demand for wellness-related products."
            ],
            "5": [
                "Market analysis indicates a rise in interest for meal kits and easy meal solutions.",
                "Young consumers are driving trends towards transparency in sourcing."
            ]
        }
    }[location_id][product_id]


def mock_feedback_and_ratings(location_id, product_id):
    return {
        "1": {
            "1": [
                "Customer feedback on similar products has been positive, with an average rating of 4.5 out of 5.",
                "Reviews indicate that 80% of customers would recommend our products to others."
            ],
            "2": [
                "Top-rated products feature excellent quality and customer service responses.",
                "Negative feedback highlights the need for improved packaging."
            ],
            "3": [
                "Survey results show that 70% of customers value eco-friendly products.",
                "Customers express satisfaction with the variety of products offered."
            ],
            "4": [
                "Some reviews suggest enhancing the in-store shopping experience.",
                "Feedback indicates a preference for more promotional events."
            ],
            "5": [
                "Ratings for organic products consistently exceed those of non-organic by 1 star.",
                "Customer suggestions include expanding the product range to include more local brands."
            ]
        },
        "2": {
            "1": [
                "Customer satisfaction ratings for new products are at 90%.",
                "Feedback indicates that customers love the new flavor options."
            ],
            "2": [
                "Product reviews show an average rating of 4.7 for quality.",
                "Customers appreciate the quick response to inquiries."
            ],
            "3": [
                "Surveys reveal that customers value our commitment to sustainability.",
                "Negative reviews often mention pricing concerns."
            ],
            "4": [
                "Customers have suggested introducing more seasonal flavors.",
                "Feedback highlights a desire for more product information online."
            ],
            "5": [
                "Community engagement initiatives have received positive feedback.",
                "Many customers report increased loyalty due to quality service."
            ]
        }
    }[location_id][product_id]
