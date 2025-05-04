# Financial Data Analysis and Machine Learning Project
App Overview
Commodity Price Prediction is a modern, interactive web application designed to help users explore, analyze, and forecast the prices of key global commodities such as Gold, Silver, Copper, Oil, and more. Built with a sleek dark-themed interface and visually engaging cards, the app provides both real-time and historical data insights, making it ideal for students, traders, and anyone interested in commodity markets.
Key Features
Live Commodity Dashboard:
Beautiful, compact cards display the latest bid/ask prices, percentage changes, and trend lines for major commodities, all styled with a golden border and dark theme for a premium look.
Data Upload & Preprocessing:
Users can upload their own datasets (CSV/XLSX), clean missing values, and remove outliers with a single click.
Feature Engineering:
Easily create moving averages and lag features to enhance model performance.
Model Training & Evaluation:
Train a linear regression model on your selected features, then evaluate its performance with R², MAE, and MSE metrics, plus visualizations of actual vs. predicted values.
Forecasting:
Generate and visualize future price forecasts, and download results for further analysis.
Educational Content:
Learn about commodity trading, market mechanisms, and the importance of commodities in global finance through dedicated info sections.
Who is it for?
Students and educators in finance, economics, and data science
Aspiring and active commodity traders
Anyone interested in understanding and predicting commodity price movements
Technologies Used
Streamlit for the interactive web interface
Pandas, NumPy, scikit-learn for data processing and modeling
Plotly for dynamic visualizations
yfinance for real-time market data

This project provides a comprehensive financial data analysis platform with machine learning capabilities. It integrates multiple data sources and offers various analytical tools for financial data processing and prediction.

## Features

- Multiple data source integration:
  - Kaggle datasets
  - Yahoo Finance API (yfinance)
  - Finnhub API
- Machine Learning Models:
  - Linear Regression
  - Logistic Regression
  - K-Means Clustering
- Interactive visualizations
- Real-time data updates
- User-friendly interface

## Setup Instructions

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main Streamlit application
- `data/`: Directory for storing datasets
- `models/`: Machine learning model implementations
- `utils/`: Utility functions and helper modules
- `config.py`: Configuration settings
- `requirements.txt`: Project dependencies

## Note

Please ensure you have the necessary API keys for:
- Finnhub API
- Any other required API services

Store your API keys in a `.env` file (not included in the repository for security reasons). 
