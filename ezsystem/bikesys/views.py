from django.shortcuts import get_object_or_404,render,redirect
from .models import User,Record,Bike,Location
from django.views import generic
import datetime
import pytz
utc=pytz.UTC

def rent(request):
    bID = request.POST['bikeID1']
    locId = Bike.objects.get(bikeId=bID).curLocId.locId
    bObj = Bike.objects.get(bikeId=bID)
    bObj.availStatus = False
    bObj.save()

    uID = request.POST['userID']
    uObj = User.objects.get(userId=uID)

    now = datetime.datetime.utcnow()

    Record.objects.create(userID=uObj,bikeID=bObj,beginTime=now,beginLocId=locId)
    return render(request,'user.html',{"notification1":'Rent Succeed',"object":uObj})

def back(request):
    bID = request.POST['bikeID2']
    bObj = Bike.objects.get(bikeId=bID)
    bObj.availStatus = True
    bObj.save()

    uID = request.POST['userID']
    uObj = User.objects.get(userId=uID)

    loc = request.POST['loc']

    r = Record.objects.get(userID=uObj,bikeID=bObj)
    r.endTime = datetime.datetime.utcnow()
    r.endLocId = loc
    r.save()

    # 付钱
    # price每秒的价格，time使用时间，pay总金额
    price = 0.001
    time_end = utc.localize(r.endTime) 
    time = (time_end-r.beginTime).seconds
    pay = time * price
    print(pay)
    uObj.balance = float(uObj.balance)-pay
    uObj.save()

    # 管理员收钱
    manager = User.objects.get(userClass="manager")
    manager.balance = float(uObj.balance)+pay
    manager.save()

    return render(request,'user.html',{"notification2":'Return bike Succeed',"object":uObj})

def submitRepair(request):
    bID = request.POST['bikeID3']
    bObj = Bike.objects.get(bikeId=bID)
    bObj.defectStatus = True
    bObj.save()

    uID = request.POST['userID']
    uObj = User.objects.get(userId=uID)

    return render(request,'user.html',{"notification3":'Bike which need repaired was submitted',"object":uObj})

def repair(request):
    bID = request.POST['bikeID4']
    bObj = Bike.objects.get(bikeId=bID)
    bObj.defectStatus = False
    bObj.save()

    uID = request.POST['userID']
    uObj = User.objects.get(userId=uID)

    return render(request,'user.html',{"notification4":'Bike repaired',"object":uObj})

def bikeOps(request):
    # 所有车位置
    bikeList = Bike.objects.all()
    rst = {}
    for b in bikeList:
        locID = b.curLocId.locId
        locDesc = Location.objects.get(locId=locID).desc
        rst[b.bikeId] = locDesc
    # 所有待修的车
    bikeList2 = Bike.objects.filter(defectStatus=True)
    rst2 = []
    for b2 in bikeList2:
        rst2.append(b2)
    # 动态移车
    balanceRst = "waiting for development..."
    return render(request,'bikeOps.html',{"bikeList":rst,"bikeList2":rst2,"balanceRst":balanceRst})

def visual(request):
    data = "Waiting for developent..."
    return render(request,"visual.html",{"data":data})

class userView(generic.DetailView):
    model = User
    template_name = "user.html"

def loginVerify(request):
    username = request.POST['username']
    password = request.POST['pwd']
    try:
        user = User.objects.get(name=username)
        return redirect(f"/{user.userId}/")
    except Exception:
        return render(request, 'login.html',{"notification":"Name or Password Error"})

def registerVerify(request):
    username = request.POST['username']
    password = request.POST['pwd']
    userclass = request.POST['cls']
    try:
        User.objects.create(name = username, password = password, userClass=userclass, balance=99.99)
        return render(request, 'login.html',{'notification':"Please Login"})
    except Exception:
        return render(request, 'register.html',{"notification":"Name already Existed"})
    
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')