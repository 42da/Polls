from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Candidate, Poll, Choice
import datetime

# Create your views here.

def home(request):
    candidates = Candidate.objects.all()
    context = {'candidates': candidates}

    return render(request, 'home.html', context)

def poll_home(request):
    candidates = Candidate.objects.all()
    context = {'candidates': candidates}
    area_list = []
    for con in context['candidates']:
        if con.area in area_list:
            continue
        else:
            area_list.append(con.area)
    context['area_list'] = area_list
    print(context)
    return render(request, 'poll_home.html', context)
    # view_str = ''
    # for candidate in candidates:
        
    #     view_str += "<p>No. {}번  name. {}<br>".format(candidate.party_number, candidate.name) #<br>은 html코드로 다음줄로 줄내림할때 사용
    #     view_str += candidate.introduction+"</p>"                                              #<p>는 html코드로 단락이동할때 
    # return HttpResponse(view_str)

def areas(request, area):

    candidates = Candidate.objects.filter(area=area)
    polls = Poll.objects.filter(area=area)
    poll_result = []
    name_list = []

    for n in candidates:        # 이름 담는 dict, list
        name_list.append(n.name)
        print(name_list, 'name list')
    
    
    

    total_votes = 0
    for poll in polls:
        choices = Choice.objects.filter(poll_id=poll.id)
        result = {}
        result['names'] = name_list

        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        for candidate in choices:
            # print(candidate.Candidate.name, 'name')
            # vote_result['{}'.format(candidate.Candidate.name)] = candidate.votes
            total_votes += candidate.votes
        result['total_votes'] = total_votes
        rates = [] # 지지율
        # for candidate in Choice.objects.filter(poll_id=poll.id):
        #     vote_result['{}_rates'.format(candidate.Candidate.name)] = round(candidate.votes / total_votes * 100, 1)
        # vote_result['total_votes'] = total_votes
        for candidate in candidates:
            
            try:   
                choice = Choice.objects.get(poll_id = poll.id,
                    Candidate_id = candidate.id)
                
                rates.append(round(choice.votes * 100 / result['total_votes'], 1))
            except:#투표를 하나도 못받았을 경우. choice=0일때
                rates.append(0)
        result['rates'] = rates #result안에 rates라는 키로 rates값을 넣음
        print(result, 'resulttttttttttt')
        poll_result.append(result)
    today = datetime.datetime.now()

    try :
        poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다. 
        candidates = Candidate.objects.filter(area=area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
        
    except:
        poll = None
        candidates = None

    context = {'candidates': candidates,
    'area' : area,
    'poll' : poll,
    'poll_result': poll_result }
    # print(today, context['poll'].start_date, 'polllllllllllllllll')
    return render(request, 'areas.html', context)



def polls(request, poll_id):
    
    poll = Poll.objects.get(pk = poll_id)#Poll객체를 구분하는 녀석은 poll_id이므로 PK지정
    selection = request.POST['choice']
    
    try:
        #choice모델을 불러와서 1을 증가시킨다 
        choice = Choice.objects.get(poll_id = poll.id, Candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, Candidate_id = selection, votes = 1)
        '''
        candidate_id --> Candidate_id (대문자임. 모델보면 나옴!!!!)
        '''
        choice.save()
 
    # return HttpResponse("finish")
    print(poll.area, 'poll.area')
    return redirect('/polls/areas/' + poll.area + '/result')


def result(request, area):
    '''
    필요한것
    1. 전체 표수
    2. 각각의 후보의 표수
    3. 기간
    '''
    candidates = Candidate.objects.filter(area=area)
    polls = Poll.objects.filter(area=area)
    poll_result = []
    

    total_votes = 0
    for poll in polls:
        choices = Choice.objects.filter(poll_id=poll.id)
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        for candidate in choices:
            # print(candidate.Candidate.name, 'name')
            # vote_result['{}'.format(candidate.Candidate.name)] = candidate.votes
            total_votes += candidate.votes
        result['total_votes'] = total_votes
        rates = [] # 지지율
        # for candidate in Choice.objects.filter(poll_id=poll.id):
        #     vote_result['{}_rates'.format(candidate.Candidate.name)] = round(candidate.votes / total_votes * 100, 1)
        # vote_result['total_votes'] = total_votes
        for candidate in candidates:
            
            try:   
                choice = Choice.objects.get(poll_id = poll.id,
                    Candidate_id = candidate.id)
                
                rates.append(round(choice.votes * 100 / result['total_votes'], 1))
            except:#투표를 하나도 못받았을 경우. choice=0일때
                rates.append(0)
        result['rates'] = rates #result안에 rates라는 키로 rates값을 넣음
        poll_result.append(result)

    print('poll result', poll_result)

    context = {'candidates': candidates, 'area':area,
     'poll_result': poll_result}
    return render(request, 'result.html', context)

def add(request):
    # today = datetime.datetime.now()

    # try :
    #     poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다. 
    #     candidates = Candidate.objects.filter(area=area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
        
    # except:
    #     poll = None
    #     candidates = None

    # context = {'candidates': candidates,
    # 'area' : area,
    # 'poll' : poll,
    # 'poll_result': poll_result }
    # print(today, context['poll'].start_date, 'polllllllllllllllll')
    return render(request, 'add.html')

def create(request):
    candidates = Candidate.objects.all()
    for can in candidates:
        if can.name == request.GET['name']:
            return HttpResponse('이미 있는 이름입니다^^; 다른 이름을 추가해주세요..')

    polls = Poll.objects.all()
    poll_list = []
    for p in polls:
        poll_list.append(p.area)
    
    if request.GET['area'] in poll_list:
        candidate = Candidate()
        candidate.name = request.GET['name']
        candidate.area = request.GET['area']
        candidate.introduction = request.GET['introduction']
        candidate.party_number = request.GET['party_number']
        candidate.save()
        return redirect('/polls/pollhome')
    else:
        candidate = Candidate()
        candidate.name = request.GET['name']
        candidate.area = request.GET['area']
        candidate.introduction = request.GET['introduction']
        candidate.party_number = request.GET['party_number']
        candidate.save()
        
        poll = Poll()
        poll.area = request.GET['area']
        poll.start_date = request.GET['start_date'] + ' ' + request.GET['time']
        poll.end_date = request.GET['end_date'] + ' ' + request.GET['time']
        poll.save()

        return redirect('/polls/pollhome')

    
