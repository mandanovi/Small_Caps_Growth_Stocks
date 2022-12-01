from bs4 import BeautifulSoup
import requests
import pandas as pd


URL = "https://www.morningstar.com/small-cap-growth-stocks"


response = requests.get(f"{URL}")

data = []
for i in range(1, 8):
    response = requests.get(f"{URL}?page={i}")
    response_text = response.text
    soup = BeautifulSoup(response_text, "html.parser")
    names = soup.findAll(name="span", class_="mdc-data-point")
    list_ = []
    for name in names:
        list_.append(name.getText())
    composite_list = [list_[x:x + 9] for x in range(0, len(list_), 9)]
    data.append(composite_list)


result = []
[result.extend(el) for el in data]


df = pd.DataFrame(result)
df.columns = ['Name', 'Ticker', 'Price $', 'Market Return YTD %', 'Market Return 1Y%', 'Market Return 3Y%',
              'Fair Value Uncertainty Rating', 'Fair Value $', 'Morning Star Value Rating']

df['Price $'] = df['Price $'].str.strip().replace("\u2014", 0).replace("\u2212", "-").astype('float')
# df['Market Return YTD %'] = df['Market Return YTD %'].str.strip().replace("-", "-").replace("—", "").astype('float')
# df['Market Return 1Y%'] = df['Market Return 1Y%'].apply(lambda x: float(x.split()[0].replace('\U00002013', '-')))
# df['Market Return 3Y%'] = df['Market Return 3Y%'].apply(lambda x: float(x.split()[0].replace('\U00002013', '-')))
df['Fair Value $'] = df['Fair Value $'].str.strip().replace("<", "").replace("-", "-").astype('float')


datatoexcel = pd.ExcelWriter('Small_Cap_Growth_Stocks.xlsx')

df.to_excel(datatoexcel)
datatoexcel.save()
print('DataFrame is written to Excel File successfully.')


