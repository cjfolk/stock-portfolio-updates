#dependancies
import robin_stocks.robinhood as r
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from gnews import GNews as gn
from datetime import datetime 
from dotenv import load_dotenv
import os

#make sure to provide file path to your .env file!!!
load_dotenv()

#gnews setup 
gnews_key = os.getenv('GNEW_API_KEY')
gn_instance  = gn(gnews_key)
gn_instance.period = '7d'
gn_instance.max_results = 2
gn_instance.language = 'english'

market_news = gn_instance.get_news('stock market')

#email updates sender and recepient info 
sender_email = os.getenv('SENDER_EMAIL')
#enter email "app password" generated for your google account 
email_password = os.getenv('SENDER_EMAIL_PW')
receiver_email = os.getenv('RECEIVER_EMAIL')

#username = email for robinhood account, password = password for robinhood account  
username = os.getenv('ROBINHOOD_USER')
password = os.getenv('ROBINHOOD_PW')

#loging into robinhood account 
login_response = r.login(username, password)

# checks if login was succesful 
if login_response.get('access_token'):
    print("successful login!\n")

    portfolio = r.profiles.load_portfolio_profile()
    equity_previous_close = float(portfolio['equity_previous_close'])
    equity = float(portfolio['equity'])
    day_change = equity - equity_previous_close

    #initialize update email  
    email_subject  = 'Daily Portfolio Update'
    email_body = ''

    if day_change > 0:
        day_change_message = f"We're up ${day_change:.2f} today!!!\n"
    else:
        day_change_message = f"Damn, down ${abs(day_change):.2f} today.\n"

    print(day_change_message)
    email_body += day_change_message + "\n"

    #fetches current holdings
    holdings = r.account.build_holdings()

    holdings_msg  = "Current Holdings:\n"
    print(holdings_msg)
    email_body += holdings_msg

    #calculate acount's total value and collects stock tickers
    total_value = 0
    for symbol, details in holdings.items():
        #fetch stock details
        quantity = float(details['quantity'])
        price_per_share = float(details['price'])
        equity =  float(details['equity'])

        #format holdings details, print, and add to email
        holding_details = f"{symbol}: {quantity:.2f} shares at ${price_per_share:.2f} each, total value: ${equity:.2f}\n"
        print(holding_details)
        email_body += holding_details

        #add equity to account's total value 
        total_value += equity

        #gets news article for holding 
        try:
            news_articles = gn_instance.get_news(symbol)
            news_msg = f"{symbol} News:\n"
            for article in news_articles:
                title = article['title']
                url = article['url']
                news_msg += f"- {title}: {url}\n"
            email_body += news_msg + "\n"
        except Exception as e:
            print(f"Failed to find {symbol} news \n error: {str(e)}")

    #total account value
    total_val_msg = "\nTotal Account Value: ${:.2f}".format(total_value)
    print(total_val_msg)
    email_body += total_val_msg

    #create/ send email update 
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_body,'plain'))

    try:
        smtp_server = 'smtp.gmail.com'
        port = 587
        context = smtplib.SMTP(smtp_server, port)
        context.starttls()
        context.login(sender_email, email_password)
        context.sendmail(sender_email, receiver_email, message.as_string())
        print("\nEmail sent")
    except Exception as e:
        print(f"\nFailed to send email, error: {str(e)}")
    finally:
        context.quit()
        
else:
    print("Login failed:", login_response)


r.logout()

