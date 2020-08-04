from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import Coin
from django.contrib.postgres.search import SearchVector

# Create your views here.
def index(request):
    context = {}
    # Get the first 10 coins ordered by social score descending
    request.session['page'] = 1
    if request.method == 'GET':
        try :
            coins = Coin.objects.order_by(f"{request.session['order_by']}")[:20]
        except KeyError:
            request.session['order_by'] = '-market_cap'
            coins = Coin.objects.order_by('-market_cap')[:20]
    elif request.method == 'POST':
        request.session['order_by'] = request.POST.get('field')
        try:
            if len(request.session['search']) > 0:
                coins = Coin.objects.annotate(search=SearchVector('name', 'symbol')).filter(search=request.session['search']).order_by(f"{request.session['order_by']}")[:20]
                context["search"] = request.session['search']
            else:
                coins = Coin.objects.order_by(request.session['order_by'])[:20]
        except KeyError:
            coins = Coin.objects.order_by(request.session['order_by'])[:20]

    context["coins"] = coins
    return render(request, 'coins/index.html', context = context)


def load_coins(request):
    request.session['page'] += 1
    try :
        coins = Coin.objects.filter(symbol__icontains=request.session['search'])
    except KeyError:
        try:
            coins = coins.order_by(request.session['order_by'])
        except:
            coins = coins.order_by('-market_cap')

    results_per_page = 20
    paginator = Paginator(coins, results_per_page)
    try:
        coins = paginator.page(request.session['page'])
    except PageNotAnInteger:
        coins = paginator.page(2)
    except EmptyPage:
        coins = paginator.page(paginator.num_pages)

    # Build a html coins list with the paginated posts
    coins_html = loader.render_to_string('coins/coins.html', {'coins': coins})

    # Package output data and return it as a JSON object
    output = {'coins_html': coins_html, 'has_another': coins.has_next()}
    return JsonResponse(output)


def search_coins(request):
    request.session['page'] = 1
    request.session['search'] = request.POST.get('search')

    if len(request.session['search']) == 0:
        coins = Coin.objects.order_by(request.session['order_by'])
    else:
        try:
            coins = Coin.objects.annotate(search=SearchVector('name', 'symbol')).filter(search=request.session['search']).order_by(request.session['order_by'])
        except KeyError:
            coins = Coin.objects.annotate(search=SearchVector('name', 'symbol')).filter(search=request.session['search'])
    results_per_page = 20
    paginator = Paginator(coins, results_per_page)

    try:
        coins = paginator.page(request.session['page'])
    except PageNotAnInteger:
        coins = paginator.page(2)
    except EmptyPage:
        coins = paginator.page(paginator.num_pages)

    # Build a html coins list with the paginated posts
    coins_html = loader.render_to_string('coins/coins.html', {'coins': coins})

    # Package output data and return it as a JSON object
    output = {'coins_html': coins_html, 'has_another': coins.has_next()}
    return JsonResponse(output)
