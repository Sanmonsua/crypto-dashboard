from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import Coin

# Create your views here.
def index(request):
    # Get the first 10 coins ordered by social score descending
    if request.method == 'GET':
        try :
            coins = Coin.objects.order_by(f"{request.session['order_by']}")[:10]
        except KeyError:
            coins = Coin.objects.order_by('-market_cap')[:10]
    elif request.method == 'POST':
        order_by = request.POST.get('field')
        request.session['order_by'] = order_by
        coins = Coin.objects.order_by(f"{request.session['order_by']}")[:10]
    context = {
        "coins" : coins
    }
    return render(request, 'coins/index.html', context = context)


def load_coins(request):
    page = request.POST.get('page')
    coins = Coin.objects.order_by(f"{request.session['order_by']}")

    results_per_page = 10
    paginator = Paginator(coins, results_per_page)
    try:
        coins = paginator.page(page)
    except PageNotAnInteger:
        coins = paginator.page(2)
    except EmptyPage:
        coins = paginator.page(paginator.num_pages)

    # Build a html coins list with the paginated posts
    coins_html = loader.render_to_string('coins/coins.html', {'coins': coins})

    # Package output data and return it as a JSON object
    output = {'coins_html': coins_html, 'has_another': coins.has_next()}
    return JsonResponse(output)
