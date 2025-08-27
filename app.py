import streamlit as st
from app_pages.multipage import MultiPage

from app_pages import page_summary
from app_pages import page_property_analysis
from app_pages import page_price_predictor
from app_pages import page_project_hypothesis
from app_pages import page_ml_performance

app = MultiPage(app_name= "UK Property Price Predictor")

app.add_page("Project Summary", page_summary.page_summary_body)
app.add_page("Property Analysis", page_property_analysis.page_property_body)
app.add_page("Price Predictor", page_price_predictor.page_price_predictor_body)
app.add_page("Projectg Hypothesis", page_project_hypthesis.page_project_hypthesis_body)
app.add_page("ML Performance", page_ml_performance.page_ml_performance_body)

app.run()