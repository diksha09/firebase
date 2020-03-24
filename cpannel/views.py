from django.shortcuts import render
import pyrebase
from django.contrib import auth
config={
    "apiKey": "AIzaSyBVJzu1BSj93YeTdDVOU6oyykzmcZLZCWQ",
    "authDomain": "cpannel-93fa2.firebaseapp.com",
    "databaseURL": "https://cpannel-93fa2.firebaseio.com",
    "projectId": "cpannel-93fa2",
    "storageBucket": "cpannel-93fa2.appspot.com",
    "messagingSenderId": "670521480823",
    "appId": "1:670521480823:web:c7ccce087e70f1ab909872",
    "measurementId": "G-H7Z7EB1X3D"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database =firebase.database()

def signIn(request):
    return render(request,"signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signup(request):
    return render(request,"signup.html")

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message = "unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    uid = user['localId']

    data = {"name":name,"status":"1"}

    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")

def create(request):
    return render(request,"create.html")

def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("milli sf",str(millis))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    print("token",str(a))
    a =a['users']
    a = a[0]
    a = a['localId']
    print("jjjj",a)
    data = {
        "work":work,
        "progress":progress
    }
    database.child('users').child(a).child('report').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,"welcome.html",{'e':name})

def add_company(request):
    return render(request,"addcompany.html")

def post_company(request):
    
    name = request.POST.get('name')
    address = request.POST.get('address')
    idtoken = request.session['uid']
    a=authe.get_account_info(idtoken)
    print("token",str(a))
    a =a['users']
    a = a[0]
    a = a['localId']
    print("jjjj",a)
    data = {
        "name":name,
        "address":address,
        "status":"1"
    }
    database.child('Companies').child(name).set(data)

    return render(request,"welcome.html",{'e':name})

def select(request):
    name = database.child('Companies').child(name).get()

    return render(request,'welcome.html',{"name":name})
    