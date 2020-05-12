import requests
from bs4 import BeautifulSoup
import smtplib
import time

# set the headers and user string
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

# send a request to fetch HTML of the page
response = requests.get('https://www.amazon.in/dp/B07J2Z9WHZ/ref=gwdb_bmc_0_Apple?pf_rd_s=merchandised-search-15&pf_rd_t=Gateway&pf_rd_i=mobile&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=80KZGJVPYXK9BSPXTESD&pf_rd_p=e79863d8-9f33-48ed-bf53-66a9d303f5e4', headers=headers)

# create the soup object
soup = BeautifulSoup(response.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')

#print(soup.prettify())

# function to check if the price has dropped below 70,000
def check_price():
  title = soup.find(id= "productTitle").get_text()
  price = soup.find(id = "priceblock_ourprice").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
  #print(price)

  #converting the string amount to float
  converted_price = float(price[0:5])
  print(converted_price)
  if(converted_price < 70000):
    send_mail()

  #using strip to remove extra spaces in the title
  print(title.strip())




# function that sends an email if the prices fell down
def send_mail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('youremail@gmail.com', 'yourpassword')

  subject = 'Price Fell Down'
  body = "Check the amazon link https://www.amazon.in/dp/B07J2Z9WHZ/ref=gwdb_bmc_0_Apple?pf_rd_s=merchandised-search-15&pf_rd_t=Gateway&pf_rd_i=mobile&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_r=80KZGJVPYXK9BSPXTESD&pf_rd_p=e79863d8-9f33-48ed-bf53-66a9d303f5e4 "

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'senderemail@gmail.com',
    'receiveremail@gmail.com',
    msg
  )
  #print a message to check if the email has been sent
  print('Hey Email has been sent')
  # quit the server
  server.quit()

#loop that allows the program to regularly check for prices
while(True):
  check_price()
  time.sleep(60 * 60)
