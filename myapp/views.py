from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from fbprophet import Prophet
import yfinance as yf
import matplotlib.pyplot as plt
import mpld3

@csrf_exempt
def graph(request):
    data = yf.download("AAPL", start = '2022-01-01')

    data = data.rename(columns={'Close':'y'})
    data['ds'] = data.index 
    data = data[['ds', 'y']]

    m = Prophet(daily_seasonality = True)
    m.fit(data)

    future = m.make_future_dataframe(periods=100)
    prediction = m.predict(future)

    fig = plt.figure(figsize=(10, 6))
    plt.plot(data['ds'], data['y'], label='price', color="black")
    plt.plot(prediction['ds'], prediction['yhat'], label='prediction', color="red")
    plt.plot(prediction['ds'], prediction['yhat_lower'], color="red")
    plt.plot(prediction['ds'], prediction['yhat_upper'], color="red")

    graph = mpld3.fig_to_html(fig, figid='THIS_IS_FIGID')
    return HttpResponse(graph)

nextId = 4
topics = [
    {'id':1, 'title': 'routing', 'body': 'Routing is ..'},
    {'id':2, 'title': 'view', 'body': 'view is ..'},
    {'id':3, 'title': 'Model', 'body': 'Model is ..'},
]

def HTMLTemplate(articleTag, id=None):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <li><a href="/create/">Create</a></li>
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>            
            <li>
                <a href="/graph/">graph</a>
            </li>
        </ul>
    </body>
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, django
    '''
    return HttpResponse(HTMLTemplate(article))


@csrf_exempt
def create(request):
    global nextId
    if request.method == "GET":
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        url = '/read/'+str(nextId)
        topics.append(newTopic)
        nextId = nextId + 1
        return redirect(url)

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))
    
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        id = request.POST['id']
        print('id', id)