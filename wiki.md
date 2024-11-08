# Stock Risk Analyzer Wiki

Welcome to the **Stock Risk Analyzer** Wiki! This project leverages machine learning techniques to analyze stock data and provide risk classifications (Low, Medium, High). It’s designed to help investors and analysts make informed decisions with real-time data.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Project Features](#project-features)
3. [Setup Guide](#setup-guide)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
4. [Usage](#usage)
    - [Web Application](#web-application)
    - [CLI Interface](#cli-interface)
5. [Contributing](#contributing)
6. [Technologies Used](#technologies-used)
7. [License](#license)

---

## Introduction

**Stock Risk Analyzer** is an open-source application that combines financial data with machine learning to evaluate stock risk levels. By leveraging historical data and advanced technical indicators, the application enables users to:
- Assess risk levels of individual stocks.
- Make informed investment decisions.
- Perform real-time analysis using an intuitive web interface or command-line tools.

---

## Project Features

- **Machine Learning Classification**:
  - Uses LightGBM for fast and accurate risk predictions.
  - Labels stocks as `Low`, `Medium`, or `High` risk.

- **Real-Time Stock Data**:
  - Integrates with the Yahoo Finance API for fetching historical and current stock data.

- **Technical Indicator Calculations**:
  - Computes key indicators such as Moving Averages (MA50, MA200), RSI, Volatility, and Bollinger Bands.

- **User-Friendly Web Interface**:
  - Built with Flask, allowing users to analyze stocks through a simple browser interface.

- **CLI Support**:
  - Analyze stocks programmatically via a command-line interface.

- **Extensibility**:
  - Modular codebase allows easy integration of new features or additional data sources.

---

## Setup Guide

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/skytells-research/stock-risk-analyzer.git
    cd stock-risk-analyzer
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. (Optional) Train the model:
    ```bash
    python model_training.py
    ```
    *Note: Pre-trained models are included in the repository.*

---

## Usage

### Web Application
1. Start the Flask app:
    ```bash
    python app.py
    ```
2. Open your browser and navigate to `http://localhost:5000`.
3. Enter a stock ticker (e.g., `AAPL`) to analyze its risk level.

### CLI Interface
1. Run the `app.py` script with the desired ticker:
    ```bash
    python app.py --ticker AAPL
    ```
    Replace `AAPL` with your desired stock ticker.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch:
    ```bash
    git checkout -b feature/your-feature
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add your feature"
    ```
4. Push to your branch:
    ```bash
    git push origin feature/your-feature
    ```
5. Open a pull request.

---

## Technologies Used

- **Languages**: Python
- **Libraries**:
  - Flask (Web Framework)
  - yfinance (Stock Data)
  - scikit-learn (ML Algorithms)
  - LightGBM (ML Classifier)
  - pandas/numpy (Data Processing)
  - TA-Lib (Technical Indicators)

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute as per the terms of the license.
