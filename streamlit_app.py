from DeliveryTimePrediction.pipeline.model_prediction_pipeline import (
    ModelPredictionTrainingPipeline,
)
import streamlit as st
import pandas as pd
import numpy as np

store_primary_categories = [
    "American",
    "Mexican",
    "Pizza",
    "Burger",
    "Sandwich",
    "Chinese",
    "Dessert",
    "Japanese",
    "Thai",
    "Vietnamese",
    "Indian",
    "Italian",
    "Mediterranean",
    "Fast",
    "Breakfast",
    "Other",
    "Salad",
    "Greek",
    "Seafood",
    "Asian",
    "Barbecue",
    "Cafe",
    "Alcohol",
    "Hawaiian",
    "Sushi",
    "Korean",
    "Middle-Eastern",
    "Catering",
    "Smoothie",
    "Dim-Sum",
    "Vegetarian",
    "Pasta",
    "Steak",
    "Burmese",
    "Persian",
    "Latin-American",
    "French",
    "Bubble-Tea",
    "Nepalese",
    "Brazilian",
]

days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


def main():
    st.title("Food Delivery Time Prediction")

    store_primary_category = st.selectbox(
        label="Store Primary Category",
        options=store_primary_categories,
    )

    selected_day = st.selectbox(label="Day of the Week", options=list(days.keys()))

    order_protocol = st.slider(
        label="Order Protocol",
        min_value=1,
        max_value=7,
        value=1,
        step=1,
        help="This field represents an id denoting the protocol Order features",
    )

    total_items = st.slider(
        label="Total Items",
        min_value=1,
        max_value=7,
        value=3,
        step=1,
        help="Total number of items in the order",
    )

    subtotal = st.slider(
        label="Subtotal",
        min_value=400,
        max_value=6000,
        value=400,
        step=100,
        help="Total value of the order submitted",
    )

    num_distinct_items = st.slider(
        label="Number of Distinct Items",
        min_value=1,
        max_value=6,
        value=2,
        step=1,
        help="Number of distinct items included in the order",
    )

    price_range = st.slider(
        label="Min - Max Item Price",
        min_value=0,
        max_value=2000,
        value=(100, 500),
        step=10,
        help="Price of the item with the least and highest cost in the order",
    )
    min_item_price, max_item_price = price_range

    total_outstanding_orders = st.slider(
        label="Total Outstanding Orders",
        min_value=3,
        max_value=180,
        value=3,
        step=1,
        help="Number of orders within 10 miles of this order that are currently being processed.",
    )
    dasher_latency_rate = st.slider(
        label="Dasher Latency Rate",
        min_value=0.5,
        max_value=1.25,
        value=0.5,
        step=0.05,
    )

    delay_time = st.slider(
        label="Delay Time", min_value=250, max_value=1500, value=250, step=50
    )

    hour = st.slider(label="Hour of Day", min_value=0, max_value=23, value=14, step=1)

    dashers_per_order = st.slider(
        label="Dashers Per Order", min_value=0.4, max_value=1.4, value=0.4, step=0.1
    )

    percentage_dashers_avail = st.slider(
        label="Percentage of Dashers Available",
        min_value=0.4,
        max_value=0.6,
        value=0.4,
        step=0.05,
    )

    total_busy_dashers = st.slider(
        label="Total Busy Dashers",
        min_value=0,
        max_value=150,
        value=2,
        step=1,
        help="Subset of above total_onshift_dashers who are currently working on an order",
    )

    delivery_difficulty = st.slider(
        label="Delivery Difficulty",
        min_value=100,
        max_value=1500,
        value=100,
        step=50,
    )

    historical_avg_delivery_time = st.slider(
        label="Historical Average Delivery Time",
        min_value=20,
        max_value=75,
        value=20,
        step=1,
    )

    delivery_speed = st.slider(
        label="Delivery Speed", min_value=1, max_value=12, value=5, step=1
    )

    input_data = {
        "store_primary_category": store_primary_category,
        "order_protocol": order_protocol,
        "total_items": total_items,
        "subtotal": subtotal,
        "num_distinct_items": num_distinct_items,
        "min_item_price": min_item_price,
        "max_item_price": max_item_price,
        "total_outstanding_orders": total_outstanding_orders,
        "dasher_latency_rate": dasher_latency_rate,
        "delay_time": delay_time,
        "hour": hour,
        "day_of_week_num": days[selected_day],
        "dashers_per_order": dashers_per_order,
        "%_dashers_avail": percentage_dashers_avail,
        "total_busy_dashers": total_busy_dashers,
        "delivery_difficulty": delivery_difficulty,
        "historical_avg_delivery_time": historical_avg_delivery_time,
        "delivery_speed": delivery_speed,
    }

    if st.button("Predict"):
        model_prediction = ModelPredictionTrainingPipeline()
        predicted_time = model_prediction.initiate_model_prediction(input_data)
        st.success(f"Predicted Delivery Time: {predicted_time:.2f} minutes")


if __name__ == "__main__":
    main()
