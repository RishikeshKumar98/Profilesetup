from django.shortcuts import render
import pyrebase
from django.contrib import auth




config={
    "apiKey": "AIzaSyCiLU_RsVkwshiJITFWG_wy7_xid4dJMzc",
    "authDomain": "myproject-8f193.firebaseapp.com",
    "databaseURL": "https://myproject-8f193-default-rtdb.firebaseio.com",
    "projectId": "myproject-8f193",
    "storageBucket": "myproject-8f193.appspot.com",
   " messagingSenderId": "193914357503",
    "appId": "1:193914357503:web:08d01dfd5e6394b7e52eca",
    "measurementId": "G-4SBHSMF14H"
}
firebase= pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()
def signin(request):
    return render(request,"signin.html")

def signup(request):
    return render(request,"signup.html")

def home(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user=authe.sign_in_with_email_and_password(email,password)
        session_id=user['idToken']
        request.session['uid']=str(session_id)

        idtoken= request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        name = database.child('users').child(a).child('details').child('name').get().val()


        return render(request,"home.html",{'e':name})
    except:
        message="invalid credentials"
        return render(request,"signin.html",{'m':message})
    

    

def postsignup(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    
    

    try:
        user=authe.create_user_with_email_and_password(email,password)
        uid=user['localId']
        data={"name":name,"status":"1"}
        database.child("users").child(uid).child("details").set(data)
        message1="User created successfull"
        return render(request,"signin.html",{'m1':message1})
    except:
        message="unable to create account please try again"
        return render(request,"signup.html",{'m':message})
    
def postprofile(request):
    name = request.POST['name']
    address = request.POST['address']
    dob = request.POST['dob']
    img = request.POST['url']

    

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    
    data = {
        "name":name,
       "address":address,
        "DOB":dob,
        "imgurl":img
    }
    
    database.child("users").child(a).child("details").set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'home.html', {'e':name})

    
def reset(request):
    return render(request,"reset.html") 
def postreset(request):
    email = request.POST['email']
    try:
        authe.send_password_reset_email(email)
        message  = "A email to reset password is successfully sent"
        return render(request, "reset.html", {"msg":message})
    except:
        message  = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "reset.html", {"msg":message})

def logout(request):
    auth.logout(request)
    return render(request,"signin.html") 

def profile(request):
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').child('name').get().val()
    addr = database.child('users').child(a).child('details').child('address').get().val()
    dob = database.child('users').child(a).child('details').child('dob').get().val()
    return render(request,"profile.html",{"n":name,"address":addr,"dob":dob}) 