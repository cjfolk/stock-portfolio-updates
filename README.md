# Stock Portfolio Updates 

This Python script automates the process of logging into a Robinhood account, fetching the current portfolio details, and sending an email with a portfolio update and relevant news articles. 

## Features

- Automatically logs into a Robinhood and fetches the current portfolio details.
- Calculates the daily changes in portfolio value.
- Retrieves and includes links to news artciles relevant to the holdings in the portfolio using the GNews API.
- Sends an email with the portfolio update and news article.

## Setup

### Prerequisites

- Python 3._
- Robin Stocks
- gnews
- smtplib
- python-dotenv

### Installation

1. Clone the repository

2. Install the required packages
   - pip install robin-stocks gnews python-dotenv
     
3. Create a .env file in the same directory and enter credentials
   - see "example.env"

## Usage

This scrpit is intended to be ran daily for the best practical use, you can automate the process easily by using AWS Lamba or  other similar tools!
   
  
   
