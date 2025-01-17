import random
from django.shortcuts import render, redirect
from .models import *
from django.core import signing
from datetime import datetime
import json
from django.db.models import Q
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
# Create your views here.

key = '011201041'
def indexPage(req):
    return render(req, "index.html") 

def signupPage(req):
    return render(req, "signup.html")

#taseen
def post_sign(req):
    if req.method == "POST":
        s_id = req.POST['mail']
        fname = req.POST['fname']
        lname = req.POST['lname']
        password = req.POST['pass']
        dept = req.POST['dept']
        batch = req.POST['batch']
        phn = req.POST['phn']
        student = students(stu_id = s_id, firstName = fname, lastName = lname, password = password, batch = batch, dept = dept, phone_number = phn)

        student.save()

        return redirect('login')
    return render("signup")

#taseen
def validate_user (req) :
    if req.method == "POST":
        __id = req.POST['email']
        __pass = req.POST['pass']

        objj = students.objects.get(stu_id = __id) 
        print(objj)
        if (objj and objj.password == __pass):
            objj.active = "true"
            objj.save()
            req.session['validate'] = objj.stu_id
            encrp = signing.dumps(objj.stu_id, key=key)
            return redirect('dashb', user=encrp)

        return render(req, "index.html")

#taseen
def logout(req, user):
    if 'validate' in req.session:
        obj = students.objects.get(stu_id = user)
        obj.active = 'false'
        obj.save()
        req.session.flush()

    return redirect('login')
        

def dashboard(req, user):
    if 'validate' in req.session:
        decrp = signing.loads(user, key=key) 
        __obj = students.objects.get(stu_id = decrp)
        _post = posts.objects.all().order_by('upvote').reverse()
        _likes = likes.objects.filter(user = __obj)
        _like = json.dumps(list(_likes.values()))
        postJS = json.dumps(list(_post.values()))
        noti = notification.objects.filter(to = __obj)
        active = students.objects.filter(active = 'true')
        alls = students.objects.all()
        data = {
            'user': __obj,
            'enp':user,
            'post':_post,
            'likes' : _like,
            'postJS':postJS,
            'noti': noti,
            'activ': active,
            'all':alls,
        }

        return render(req, 'dashboard.html', data)
    else:
        return redirect('login')

#shishir
def postText(req, user):
    if 'validate' in req.session:
        encrp = signing.loads(user, key=key)

        _obj = students.objects.get(stu_id = encrp)

        if req.method == "POST":
            text = req.POST['post']
            stu = _obj
            cat = req.POST['cat']
            idd = _obj.stu_id + "-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

            object = posts(text = text, student = stu, category = cat, iid = idd)

            object.save()

        return redirect('dashb', user=user)
    else:
        return redirect('login')
    
#shishir
def likeit(req):
    if 'validate' in req.session:
        if req.method == 'POST':
            print(req.POST.get('post_id'))
            user = students.objects.get(stu_id = req.POST.get('user'))
            post_obj = posts.objects.get(iid = req.POST.get('post_id'))
            post_obj.upvote = int(post_obj.upvote) + 1 
            post_obj.save()
            if likes.objects.filter(post=post_obj, user=user).exists():
                likeobj = likes.objects.get(post=post_obj, user=user)
                likeobj.counter = post_obj.upvote
                likeobj.save()
            else:
                like = likes(counter = post_obj.upvote, post = post_obj, user = students.objects.get(stu_id = req.POST.get('user')))
                like.save()

            message = user.firstName + " " + user.lastName + " has upvoted your post."
            notificat = notification(message = message, to=post_obj.student)
            notificat.save()

        print("Hello" + post_obj)
        return redirect('dashb', user=req.POST.get('enpp'))
    else:
        return redirect('login')



#darain
def profile(req, user):
    dumm = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = dumm)
    alls = students.objects.all()
    pObj = posts.objects.filter(student = obj)
    like = likes.objects.all()

    data = {
        'user':obj,
        'enp':user,
        'all': alls,
        'post':pObj,
        'likes':like,
    }

    return render(req, "profile.html", data)

def categorize(req, user):

    userr = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = userr)
    filtr = posts.objects.filter(category = req.GET.get('cat'))
    print(req.GET.get('cat'), filtr)
    data = {
        'post':filtr,
        'enp':user,
        'stu':obj,
    }
    return render(req, "categorize.html", data)

from django.templatetags.static import static
def notice(req, user):
    dumm = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = dumm)
    alls = students.objects.all()

    img_list = ['img1', 'img2', 'img3', 'img4', 'img5', 'uiu']
    img_urls = [static(f"img/{img}.jpg") for img in img_list]

    api_url = "http://127.0.0.1:7000/api/notice/"
    response = requests.get(api_url)
    notices = []

    for notice in response.json():
        image = random.choice(img_urls)
        month = notice["date"].split(" ")[0]
        day = notice["date"].split(" ")[1]
        title = notice["title"]
        url = notice["url"]
        details = notice["details"]

        notices.append({
            'image':image,
            'month': month,
            'day' : day,
            'title': title,
            'url': url,
            'details': details,
        })

    data = {
        'user':obj,
        'enp':user,
        'all': alls,
        'images':img_urls,
        'notices':notices
    }

    return render(req, "notice.html", data)


def club(req, user):
    dumm = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = dumm)
    alls = students.objects.all()

    clubss = clubs.objects.all()
    sortclub = json.dumps(list(clubApproval.objects.filter(studentss = obj).values()))

    data = {
        'user':obj,
        'enp': user,
        'club':clubss,
        'sort': sortclub,
        'all':alls,
    }
    

    return render(req, "club.html", data)

def createClub(req, user):
    if 'validate' in req.session:

        derc = signing.loads(user, key=key)
        obj = students.objects.get(stu_id = derc)

        if req.method == "POST":
            cname = req.POST['cname']
            ctype = req.POST['ctype']
            purpose = req.POST['purpose']
            rules = req.POST['rules']
            admin = req.POST['admin']
            print(admin)
            if admin == 'Admin':
                a_name = obj.firstName + " " + obj.lastName
                a_obj = obj
            else:
                a_name = req.POST['adminname']
                a_obj = students.objects.get(stu_id = req.POST['adminmail'])

            clu = clubs(clubname = cname, clubtype = ctype, purpose = purpose, rules = rules, adminname = a_name, adminid = a_obj)
            
            clu.save()
        
        return redirect('club', user)
    else:
        return redirect('login')

def clubApprove(req, user, club):
    if 'validate' in req.session:
        clubd = clubs.objects.get(clubname = club)
        student = students.objects.get(stu_id = signing.loads(user, key=key))
        admin = clubd.adminid
        if admin == student:
            status = "Enter"
        else:
            status = "Pending"

        clubapprv = clubApproval(clubid = clubd, studentss = student, status = status, admin = admin)
        clubapprv.save()

        return redirect('club', user=user) 
    else:
        return redirect('login')

def clubDash (req, user, club):
    if 'validate' in req.session:
        print(club)
        dumm = signing.loads(user, key=key)
        obj = students.objects.get(stu_id = dumm)
        alls = students.objects.all()
        clubb = clubs.objects.get(clubname = club)
        cposts = clubpost.objects.filter(clubidd = clubb)
        pending = clubApproval.objects.filter(clubid = clubb).filter(status = "Pending")
        members = clubApproval.objects.filter(clubid = clubb).filter(status = "Joined")
        clikes = json.dumps(list(clublikes.objects.filter(club = clubb).filter(student = obj).values()))

        events= eevent.objects.filter(club = clubb)
        data = {
            'user':obj ,
            'enp': user,
            'clb':clubb,
            'clbname':club,
            'cpost': cposts,
            'pendings': pending,
            'joined':members,
            'clikes': clikes,
            'events':events,
            'all':alls
        }
        return render(req, 'clubdashboard.html', data)
    else:
        return redirect('login')

def clubposthandling(req, user, club):
    if 'validate' in req.session:
        if req.method == "POST":
            texts = req.POST['texts']
            studnt = students.objects.get(stu_id = signing.loads(user, key=key))
            clubb = clubs.objects.get(clubname = club)
            iid = clubb.clubname + " " + datetime.now().strftime("%d-%m-%Y-%H-%S")

            clubposts = clubpost(texts = texts, clubidd = clubb, student = studnt, iid = iid)
            clubposts.save()

            return redirect('cdash', user=user, club=club)
        return HttpResponse("Hello")
    else:
        return redirect('login')

def doapprove(req, club, student):
    calab = clubs.objects.get(clubname = club)
    ishtudent = students.objects.get(stu_id = student)
    theclub = clubApproval.objects.get(clubid = calab, studentss=ishtudent)
    theclub.status = "Joined"
    theclub.save()

    return redirect('cdash', user=signing.dumps(student, key=key), club=club)
        
def likeclubpost(req):
    if req.method == "POST":
        club_obj = clubs.objects.get(clubname = req.POST.get('clubid'))
        user_obj = students.objects.get(stu_id = signing.loads(req.POST.get('studentid'), key=key))
        post = clubpost.objects.get(iid = req.POST.get('postid'))
        post.upvote = int(post.upvote) + 1
        post.save()

        clikes = clublikes(counter = post.upvote, student = user_obj, club = club_obj, post = post)

        clikes.save()
        return redirect('cdash', user=req.POST.get('studentid'), club=req.POST.get('clubid'))
    
def refreshchat(req, user):
    if 'validate' in req.session:
        stuobj = students.objects.get(stu_id = signing.loads(user, key=key))
        filtee = students.objects.filter(active = "true")
        print(stuobj)
        data = {
            'activ': filtee,
            'user':stuobj,
        }

    return render(req, "refreshchat.html", data)

def event(req, user, club):
    print(club)
    if 'validate' in req.session and req.method == "POST":
        if 'img' in req.FILES:
            bannerr = req.FILES['img']
        else:
            bannerr = ""
        print(bannerr)
        name = req.POST['ename']
        cat = req.POST['cate']
        clubss = clubs.objects.get(clubname = club)
        studentss = students.objects.get(stu_id = signing.loads(user, key=key))
        stime = req.POST['sdate']
        etime = req.POST['edate']
        details = req.POST['details']

        _vent = eevent(bannerImg = bannerr, name=name, cat=cat, club=clubss, admin = studentss, stime = stime, etime = etime, details = details)

        _vent.save()

        members = clubApproval.objects.filter(clubid = clubss).filter(status = "Joined")

        messg = studentss.firstName + " " + studentss.lastName+ " have announced an event you may interested in."
        for mems in members:
            noti = notification(message = messg, to = mems.studentss)
            noti.save()

        return redirect('cdash', user=user, club=club)
    else:
        return redirect('login')
    



def sendmsg (req, user) :

    decrp = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = decrp)
    toObj = students.objects.get(stu_id = req.POST.get('tousr')) 
    _pk = toObj.stu_id+"_"+obj.stu_id
    _orpk = obj.stu_id+"_"+toObj.stu_id

    print(_pk, _orpk)
    

    if conversations.objects.filter(pkk = _pk).exists():
        mesg = messages.objects.create(convs=conversations.objects.get(pkk = _pk), sender = obj, msg = req.POST.get('msg'))
    elif conversations.objects.filter(pkk = _orpk).exists():
        mesg = messages.objects.create(convs=conversations.objects.get(pkk = _orpk), sender = obj, msg = req.POST.get('msg'))
    else:
        convo = conversations.objects.create(pkk = _pk)
        convo.userss.add(obj, toObj)
        mesg = messages.objects.create(convs=convo, sender = obj, msg = req.POST.get('msg'))

    return HttpResponse(status=204)

def getmsg(req, user):
    derc= signing.loads(user, key=key)
    objj = students.objects.get(stu_id = derc) 

    toobj = students.objects.get(stu_id = req.GET.get('to_id'))

    pk1 = objj.stu_id + "_" + toobj.stu_id
    pk2 = toobj.stu_id+ "_"+ objj.stu_id

    if conversations.objects.filter(pkk = pk1).exists():
        msgs = messages.objects.filter(convs = conversations.objects.get(pkk = pk1)) 
    elif conversations.objects.filter(pkk = pk2).exists():
        msgs = messages.objects.filter(convs = conversations.objects.get(pkk = pk2))
    else:
        msgs = ""

    data = {
        "enp": user,
        "user": objj,
        "msgs":msgs,
    }

    return render(req, 'getmsg.html', data)

def comment(req, user):
    der = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = der) 
    comnt = req.POST.get('cmnt') 
    postid = req.POST.get('postid')
    pst = posts.objects.get(iid = postid)
    if likes.objects.filter(post=pst, user=obj).exists():
        print(comnt)
        likeobj = likes.objects.get(post=pst, user=obj)
        likeobj.comment = comnt
        likeobj.save()
    else:
        cmntobj = likes(post=pst, user=obj, comment=comnt)
        cmntobj.save()

    msg = obj.firstName + " " + obj.lastName + " has commented on your posts."
    notiobj = notification(message=msg, to=pst.student)
    notiobj.save()
    return HttpResponse(status=204)

def getbig(req, user):
    dec = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = dec) 

    postid = posts.objects.get(iid = req.GET.get('post'))
    comnts = likes.objects.filter(post = postid)

    data= {
        'user': user,
        "post": postid,
        'cmnts': comnts,
    }

    return render(req, "bigpost.html", data)

def viewDetails(req, user):
    der = signing.loads(user, key=key) 
    obj = students.objects.get(stu_id=der) 
    
    dataa = req.GET.get("event") 
    
    evnt = eevent.objects.get(name = dataa) 
    
    dat = {
        'enp':user,
        'evnt':evnt,
        'user': obj,
    }
    
    return render(req, 'viewd.html', dat)

def jobDetails(req, user):
    dumm = signing.loads(user, key=key)
    obj = students.objects.get(stu_id = dumm)
    alls = students.objects.all()

    api_url = "http://127.0.0.1:7000/api/jobs/"
    response = requests.get(api_url)

    data = {
        'user':obj,
        'enp':user,
        'all': alls,
        'jobs': response.json()
    }
    return render(req, 'jobs.html', data)


import requests

def achievements_view(request, user):
    dumm = signing.loads(user, key=key)
    obj = students.objects.get(stu_id=dumm)
    alls = students.objects.all()
    
    # Fetch paper data
    papers = fetch_papers()
    
    data = {
        'user': obj,
        'enp': user,
        'all': alls,
        'papers': papers,  # Pass the papers data to the template
    }
    return render(request, 'achievement.html', data)

def fetch_papers():
    api_url = "http://127.0.0.1:7000/api/journal/"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data  # Get the first three papers
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
