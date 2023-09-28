from django.shortcuts import render,redirect
from .models import *
import uuid
import os
import subprocess
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
df = pd.DataFrame()


def check_time(request, scheduler):
    details = request.session.get('details')
    email = details['email'][0]
    try:
        obj = test_status.objects.get(user=email)
        print(email," " , obj.time)

        if obj.time == 0:

            obj.status = 1
            obj.save()

            scheduler.shutdown(wait=False)

        else:
            obj.time -= 1
            obj.save()
    except:
        scheduler.shutdown(wait=False)


def send_email(email, score, schedule):
    send_mail(
        'your score in online accesment in coderbyte',
        f'you have scored {score}',
        'testiddevil@gmail.com',
        [f'{email}'],
        fail_silently=False,
    )
    schedule.shutdown(wait=False)


def execute_code(extension, code, inp):
    name = uuid.uuid1()
    with open(str(name) + '.' + extension, 'w') as f:
        f.writelines(code)

    data, temp = os.pipe()

    os.write(temp, bytes(inp, "utf-8"))
    os.close(temp)
    # output = 'Exception'

    if extension == 'py':
        try:
            s = subprocess.check_output(f"python {name}.py", stdin=data, shell=True)
            output = s
            os.remove(f'{name}.{extension}')
        except:
            os.remove(f'{name}.{extension}')


    elif extension == 'cpp':
        try:
            s = subprocess.check_output(f"g++ {name}.cpp -o out2;./out2", stdin=data, shell=True)
            output = s
            os.remove(f'{name}.{extension}')
        except:
            os.remove(f'{name}.{extension}')


    elif extension == 'java':
        try:
            subprocess.check_output(f"javac {name}.java", stdin=data, shell=True)
            s = subprocess.check_output(f"java Solution", stdin=data, shell=True)
            output = s
            os.remove(f'{name}.{extension}')
        except:
            os.remove(f'{name}.{extension}')

    else:
        try:
            s = subprocess.check_output(f"gcc {name}.c -o out2;./out2", stdin=data, shell=True)
            output = s
            os.remove(f'{name}.{extension}')
        except:
            os.remove(f'{name}.{extension}')



    return output

def home(request):
    msg = None
    if request.method == 'POST':
        val = request.POST
        name = val.get('name')
        email = val.get('email')

        try:
            print(email)
            obj = UserDetails.objects.get(email = email)
            if check_password(name, obj.psw):
                request.session['details'] = {'email': [email], 'score': [0], 'question': 0, 'question_id': []}
                return redirect(confirm)

            else:
                msg = 'Incorrect Credentials'

        except:
            msg = 'Incorrect Credentials'


    return render(request,'home.html', {'msg':msg})

def account(request):

    if request.method == 'POST':
        post_val = request.POST

        name = post_val.get('name')
        email = post_val.get('email')
        gender = post_val.get('sex')
        phone = post_val.get('contact')
        address = post_val.get('address')
        psw = post_val.get('psw')

        obj = UserDetails(name = name, email = email, gender=gender, contact=phone, address=address, psw = make_password(psw))
        obj.save()

        return redirect(home)

    return render(request, 'account.html')


def confirm(request):
    details = request.session.get('details')
    email = details['email'][0]
    obj = UserDetails.objects.get(email = email)
    return render(request, 'Confirmation.html', {'obj':obj})

def start_scheduler(request):
    details = request.session.get('details')
    email = details['email'][0]
    try:
        test_status.objects.get(user = email)
    except:
        obj = test_status(user=email, status=0)
        obj.save()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_time, 'interval', seconds = 1, args=(request,scheduler))
    scheduler.start()
    return redirect(question_page)

def question_page(request):

    details = request.session.get('details')
    email = details['email'][0]
    question = details['question']

    try:
        obj = test_status.objects.get(user = email)
        time = obj.time
    except:
        return redirect(end_session)

    if obj.status == 1:
        obj.delete()
        return redirect(end_session)

    obj = CodingQuestion.objects.all()
    return render(request,'question.html',{'obj':obj, 'question':question,'time':time})

def code(request, val):
    details = request.session.get('details')
    email = details['email'][0]

    try:
        obj = test_status.objects.get(user=email)
        time = obj.time
    except:
        return redirect(end_session)

    if obj.status == 1:
        obj.delete()
        return redirect(end_session)

    score = details['score'][0]
    question = details['question']
    question_id = details['question_id']

    if val in question_id:
        return redirect(question_page)

    obj = CodingQuestion.objects.get(id = val)
    inp = obj.input
    out = obj.output
    inp = inp.split("\n")
    out = out.split("\n")
    print(inp)
    res = ''
    code = ''
    input = ''
    lst = []
    flag = 0
    total = 0
    passed_test = 0

    if request.method == 'POST':
        extension = request.POST.get('language')
        code = request.POST.get('code')
        print(code)

    if 'run' in request.POST:
        flag = 1
        input = request.POST.get('input')
        try:

            res = execute_code(extension,code,input)

            res = res.decode()
            print(res)

        except:
            res = 'some error in code'
        res = res.split("\n")

    elif 'test' in request.POST:
        flag = 2
        case = TestCases.objects.filter(question = val)
        for i in case:
            total += 1
            try:
                res = execute_code(extension, code, i.input)
                print(res)
                res = res.decode()
                print(res)
                res = res.split("\n")
                print(res)
                if len(res) > 1:
                    res = res[:-1]
                else:
                    res = [res[0]]
                passed_test += 1
            except:
                res = ['There is Error in Your Code']

            temp_inp = i.input
            temp_inp = temp_inp.split("\n")

            temp_out = i.output
            temp_out = temp_out.split("\n")

            temp = res == temp_out
            print(res, temp_out, res == temp_out)

            d = {'inp':temp_inp, 'out':temp_out, 'res':res, 'test_res':temp}
            lst.append(d)

    elif 'submit' in request.POST:
        diff = total - passed_test
        if diff == 0:
            score += 10

        elif diff == total:
            score += 0

        else:
            score += ((diff/total)*100)

        question += 1
        question_id.append(val)

        details['score'] = [score]
        details['question'] = question
        details['question_id'] = question_id

        request.session['details'] = details

        return redirect(question_page)

    return render(request, 'code.html',{'obj':obj,'out':out,'inp':inp,'code':code,'input':input, 'res':res,'lst':lst, 'flag':flag,'time':time})


def end_session(request):
    global df
    details = request.session.get('details')
    try:
        email = details['email'][0]
        obj = test_status.objects.get(user = email)
        print('hi1')
        obj.delete()
        print('hi')
    except:
        pass

    del details['question']
    del details['question_id']

    # temp = pd.DataFrame(details)
    # # print(lst)
    # lst = [df, temp]
    # df = pd.concat(lst)
    # print(df)
    email = details['email'][0]
    score = details['score'][0]
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email, 'interval', seconds=1, args=(email, score, scheduler))
    scheduler.start()

    del request.session['details']
    return redirect(home)
