from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import random
from django.shortcuts import render, redirect

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is ..'},
    {'id': 2, 'title': 'view', 'body': 'View is ..'},
    {'id': 3, 'title': 'Medel', 'body': 'Model is ..'},
]


# 이 경우 "request" 매개변수는 들어오는 HTTP 요청을 나타내며
# 요청 본문, 쿼리 매개변수, 헤더 등에 제출된 데이터에 액세스하는 데 사용할 수 있습니다


@csrf_exempt
def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI_deleteButton = ''
    if id != None:
        contextUI_deleteButton = \
        f'''                
            <li><form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}>
                <input type="submit" value="delete">
            </form></li>

            <li><a href="/update/{id}">update</a></li>
        '''

    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    style = '''        
        <style>
            .move-right {
              background-color: #4CAF50; /* Green */
              color: white;
              padding: 10px 20px;
              border: none;
              cursor: pointer;
              transition: transform 0.2s ease-in-out;
            }
            
            .move-right:hover {
              transform: translateX(10px);
            }
        </style>'''


    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <button class="move-right">Hover over me!</button>

            <ul>
                {ol}
            </ul>
                {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI_deleteButton}
            </ul>
        </body>
        {style}
    </html>
    '''

def index(requests):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))


@csrf_exempt
def create(requests):
    global topics
    if requests.method == 'GET':
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></input></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif requests.method == 'POST':
        title = requests.POST['title']
        body = requests.POST['body']
        topics_size = len(topics)
        newTopic = {'id': topics_size + 1, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/' + str(topics_size + 1)
        return redirect(url)

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = topic
                break

        article = f'''
        <form action="/update/{id}/" method="post">
            <p><input type="text" name="title" placeholder="{selectedTopic['title']}"></input></p>
            <p><textarea name="body" placeholder="{selectedTopic['body']}"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
                break

        url = '/read/' + id
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        print("id"+id)
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics

    return redirect('/')


@csrf_exempt
def read(requests, id):
    global topics

    for topic in topics:
        if (topic['id'] == int(id)):
            article = f'''
                <h2>{topic["title"]}</h2>
                {topic["body"]}
            '''
            break
    return HttpResponse(HTMLTemplate(article, id))
