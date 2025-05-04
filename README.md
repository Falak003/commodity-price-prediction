# Financial Data Analysis and Machine Learning Project

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