# Stock Risk Analyzer
Stock Risk Analyzer is a powerful, machine learning-driven application designed to help investors, traders, and financial analysts assess stock market risk levels efficiently and accurately. By leveraging historical data and key technical indicators, this tool classifies stocks into risk categories (`Low`, `Medium`, `High`), empowering users to make informed investment decisions.


![Stock Risk Analyzer](https://raw.githubusercontent.com/skytells-research/stock-risk-analyzer/refs/heads/main/static/assets/banner.jpg)


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Methodology](#methodology)
- [Why This Project is Important](#why-this-project-is-important)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
  - [Web Application](#web-application)
  - [REST API](#rest-api)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contributors](#contributors)
- [Sponsor](#sponsor)

## Introduction

**Stock Risk Analyzer** is an open-source application designed to help investors, traders, and financial analysts assess the risk levels of stocks using machine learning techniques. By leveraging historical data and technical indicators, the application classifies stocks into risk categories (Low, Medium, High), providing users with valuable insights to make informed investment decisions.


### Key Features

- 📊 Real-time stock data analysis
- 🤖 ML-based risk classification
- 📈 Technical indicator calculations
- 🌐 Web interface & REST API
- 📱 CLI support for automation

#### Features In Depth


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


## Methodology

The risk level is determined using the LightGBM Classifier with the following methodology:

1. **Risk Score Calculation** ($\alpha$):
   
   $$\alpha = w_1\sigma + w_2|R_t| + w_3\left|\frac{P_t - MA_{50}}{MA_{50}}\right| + w_4\left|\frac{P_t - MA_{200}}{MA_{200}}\right|$$
   
   where $w_i$ are the learned weights

2. **Risk Categories**:
   - Low Risk: $\alpha < \theta_1$
   - Medium Risk: $\theta_1 \leq \alpha < \theta_2$
   - High Risk: $\alpha \geq \theta_2$

>   where $\theta_1$ and $\theta_2$ are threshold values determined through model training

For more details, please see the [PoC.md](PoC.md) file.


## Why This Project is Important

In the volatile world of stock markets, understanding the risk associated with a stock is crucial for effective portfolio management. Traditional risk assessment methods can be time-consuming and may not account for all variables. This project aims to:

- **Democratize Risk Analysis**: Make sophisticated risk assessment accessible to individual investors and small firms without expensive proprietary tools.
- **Leverage AI for Better Insights**: Utilize machine learning to identify patterns and trends that may not be apparent through manual analysis.
- **Real-Time Decision Making**: Provide up-to-date risk evaluations using real-time data, enabling quicker responses to market changes.

By integrating technology and finance, **Stock Risk Analyzer** contributes to more transparent and data-driven investment strategies.

## Features

- **Real-Time Stock Data Fetching**: Uses the Yahoo Finance API to retrieve up-to-date stock information.
- **Technical Indicator Calculations**: Computes key indicators like Moving Averages (MA50, MA200) and Volatility.
- **Machine Learning-Based Risk Classification**: Implements a Random Forest classifier to categorize stocks into Low, Medium, or High risk.
- **Web Interface for Easy Interaction**: User-friendly web application built with Flask for seamless interaction.
- **CLI Support for Automation**: Command-line interface for quick assessments and integration into automated workflows.
- **Extensible Framework**: Modular code structure allowing easy addition of new features and indicators.

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/skytells-research/stock-risk-analyzer.git
   cd stock-risk-analyzer
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Train the Machine Learning Model**

   The application comes with a pre-trained model. However, to train the model yourself:

   ```bash
   python model_training.py
   ```

   *Note: Training requires an internet connection to fetch stock data.*

## Usage

### Command-Line Interface (CLI)

To analyze a stock using the CLI:

```bash
python app.py AAPL
```

Replace `AAPL` with the ticker symbol of the stock you wish to analyze.

### Web Application

1. **Run the Flask App**

   ```bash
   python web_app.py
   ```

2. **Access the Application**

   Open your web browser and navigate to `http://localhost:5000`.

3. **Analyze Stocks**

   - Enter the stock ticker symbol in the input field.
   - Click "Analyze" to view the risk assessment.

### REST API

The Stock Risk Analyzer provides a RESTful API for programmatic access to risk analysis features.

#### Base URL
```
http://localhost:5000/api/v1
```

#### Endpoints

1. **Analyze Stock Risk**
```http
GET /analyze/{ticker}
```
- Parameters:
  - `ticker` (path): Stock ticker symbol (e.g., AAPL, GOOGL)
- Response:
```json
{
    "ticker": "AAPL",
    "risk_level": "Medium",
    "confidence": 0.85,
    "indicators": {
        "volatility": 0.23,
        "rsi": 65.4,
        "ma50": 150.25,
        "ma200": 145.80
    },
    "last_updated": "2024-03-21T15:30:00Z"
}
```

2. **Batch Analysis**
```http
POST /analyze/batch
```
- Request Body:
```json
{
    "tickers": ["AAPL", "GOOGL", "MSFT"]
}
```
- Response: Array of analysis results for each ticker

#### Authentication
API requests require an API key passed in the header:
```http
Authorization: Bearer your_api_key_here
```

#### Rate Limits
- Free tier: 100 requests/day
- Premium tier: 1000 requests/day

#### Example Usage

Using Python with requests:
```python
import requests

API_KEY = 'your_api_key_here'
BASE_URL = 'http://localhost:5000/api/v1'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Analyze single stock
response = requests.get(
    f'{BASE_URL}/analyze/AAPL',
    headers=headers
)
print(response.json())

# Batch analysis
response = requests.post(
    f'{BASE_URL}/analyze/batch',
    headers=headers,
    json={'tickers': ['AAPL', 'GOOGL', 'MSFT']}
)
print(response.json())
```

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

Please ensure your code adheres to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide and passes all tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Yahoo Finance API**: For providing access to real-time and historical stock data.
- **scikit-learn**: For machine learning algorithms and tools.
- **Flask**: For the web framework used in the application.
- **Contributors**: Special thanks to all contributors who have helped improve this project.
- **Open-Source Community**: For fostering a collaborative environment that makes projects like this possible.

## Contributors
Contributors are welcomed! please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.
- **Dr. Hazem Ali**: Lead Machine Learning Engineer
- **Jennifer D.**: Developer and Maintainer


## Sponsor

If you find this project useful, consider sponsoring us on GitHub to support ongoing development and maintenance.

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-green.svg)](https://github.com/sponsors/skytells-research)

Your sponsorship helps us:

- Improve the application's features and performance.
- Keep dependencies up-to-date.
- Provide better documentation and support.

---

*This project is maintained by [skytells-research](https://github.com/skytells-research).
