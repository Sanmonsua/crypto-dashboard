import requests
from coins.models import Coin
from django.core.exceptions import ObjectDoesNotExist


def get_coins_list():
    # Gets the list of the coins from coingecko api
    coingecko_url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.request('GET', coingecko_url)
    try:
        response.raise_for_status()
        return response.json()
    except:
        return None


def get_coin_base_data(id):
    # Gets the coin data from coingecko api
    coingecko_url = f"https://api.coingecko.com/api/v3/coins/{id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    response = requests.request('GET', coingecko_url)
    try:
        response.raise_for_status()
        return response.json()
    except:
        return None


def update_coins():
    coins_list = get_coins_list()
    if coins_list is not None:
        for coin_data in coins_list:
            coin_base_data = get_coin_base_data(coin_data['id'])
            if coin_base_data is not None:
                try:
                    coin = Coin.objects.get(pk=coin_base_data['id'])
                    if coin.price != 0:
                        coin.price_change = (coin_base_data['market_data']['current_price']['usd']-coin.price) / coin.price * 100
                    coin.price = coin_base_data['market_data']['current_price']['usd']
                    if coin.price_btc != 0:
                        coin.price_btc_change = (coin_base_data['market_data']['current_price']['btc']-coin.price_btc) / coin.price_btc * 100
                    coin.price_btc = coin_base_data['market_data']['current_price']['btc']
                    if coin.market_cap != 0:
                        coin.market_cap_change = (coin_base_data['market_data']['market_cap']['usd']-coin.market_cap) / coin.market_cap * 100
                    coin.market_cap = coin_base_data['market_data']['market_cap']['usd']
                    if coin.social_score != 0:
                        coin.social_score_change = (coin_base_data['public_interest_score']-coin.social_score) / coin.social_score * 100
                    coin.social_score = coin_base_data['public_interest_score']
                    if coin.total_volume != 0:
                        coin.total_volume_change = (coin_base_data['market_data']['total_volume']['usd']-coin.total_volume) / coin.total_volume * 100
                    coin.total_volume = coin_base_data['market_data']['total_volume']['usd']
                    coin.save()
                    print(f"{coin.id} updated")
                except ObjectDoesNotExist:
                    try:
                        new_coin = Coin(
                            id = coin_base_data['id'],
                            symbol = coin_base_data['symbol'],
                            name = coin_base_data['name'],
                            price = coin_base_data['market_data']['current_price']['usd'],
                            price_btc = coin_base_data['market_data']['current_price']['btc'],
                            total_volume = coin_base_data['market_data']['total_volume']['usd'],
                            market_cap = coin_base_data['market_data']['market_cap']['usd'],
                            social_score = coin_base_data['public_interest_score']

                        )
                        print(f"{coin.id} saved")
                        new_coin.save()
                    except:
                        pass
                except KeyError:
                    pass

if __name__ == '__main__':
    update_coins()
