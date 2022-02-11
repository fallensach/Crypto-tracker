import requests
from datetime import datetime

class Cryptoapi:
    TYPE_C_NAME = 1
    TYPE_SYMBOL = 2

    def __init__(self):
        pass


    """
    Check that the entered crypto is valid
    """
    def is_valid(self, c_name):
        req = requests.get(f"https://api.coingecko.com/api/v3/search?query={c_name}")
        if req.json()['coins']:
            return True
        return False

    """
    Get the correct crypto type name depending on api call
    symbol: cryptocurrency exchange name
    c_name: full name of cryptocurrency
    type: 1 is name 2 is symbol
    Expect to receive valid data
    """
    def get_c_type(self, c_name, type):
        if type == self.TYPE_C_NAME:
            return requests.get(f"https://api.coingecko.com/api/v3/search?query={c_name}").json()["coins"][0]["id"].lower()

        return requests.get(f"https://api.coingecko.com/api/v3/search?query={c_name}").json()["coins"][0]["symbol"].lower()

    """
    Get all the information about a certain cryptocurrency using its full name.
    Returns the information in a dictionary.
    """
    def get_crypto(self, c_name, curr="usd"):
        if self.is_valid(c_name):
            c = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.get_c_type(c_name, 1)}")
            info = {}
            info["name"] = c.json()["name"]
            info["price"] = c.json()["market_data"]["current_price"][curr]
            info["currency"] = curr
            info["market_cap_rank"] = c.json()["market_cap_rank"]
            return info

        return "Crypto does not exist in the database"

    """
    Get the market cap and price for x amount of days MAX 30
    Full crypto name:
    """
    def get_history(self, c_name, days, curr="usd"):
        data = requests.get(f"https://api.coingecko.com/api/v3/coins/{c_name}/market_chart?vs_currency={curr}&days={days}")
        price_data = data.json()["prices"]
        price_dic = {}
        for i in range(len(price_data)-1):
            ts = price_data[i][0]//1000
            price_dic[ts] = price_data[i][1]
        
        return price_dic
    """
    Returns a list with cryptocurrencies in ascending order of the rankings.
    """
    def get_top_100(curr="usd"):
        data = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={curr}&order=market_cap_desc&per_page=100&page=1&sparkline=false')
        crypto_list = []
        for coin in data:
            coin_data = {
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "rank": coin["market_cap_rank"],
                "current_supply": coin["circulating_suppy"],
                "max_supply": coin["max_supply"]
            }
            crypto_list.append(coin_data)

if __name__ == "__main__":
    api = Cryptoapi()
    dic = api.get_crypto("shib")
    #print(api.get_history("bitcoin", 4))
    print(dic)
