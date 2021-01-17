from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Record, Bike, Location
from .analysis import SharingBikeAnalysis
import datetime
import pytz

utc = pytz.UTC


class MgtApi(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request):
        try:
            jsonDict = eval(request.body)
            uID = eval(jsonDict["uid"])
            operation = eval(jsonDict["operation"])
            rst = ""
            if operation == "report":
                rst = "wait for development"
            else:
                rst = "wait for development"
            return JsonResponse({"result": rst})
        except Exception:
            return JsonResponse({"error": "error"})


class OperApi(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request):
        try:
            jsonDict = eval(request.body)
            bID = eval(jsonDict["bikeid"])
            operation = eval(jsonDict["operation"])
            uID = eval(jsonDict["uid"])
            if operation == "repair":
                rst = "Succeed!"
                # bike
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.defectStatus == False:
                    rst = "Bike already repaired!"
                else:
                    bObj.defectStatus = False
                    bObj.save()
                # user
                return JsonResponse({"result": rst})
            elif operation == "track":
                bikeRst = []
                bikeRst2 = []
                balanceRst = []
                # 所有车位置
                bikeList = Bike.objects.all()
                for b in bikeList:
                    locID = b.curLocId.locId
                    locDesc = Location.objects.get(locId=locID).desc
                    bikeRst.append([b.bikeId, locDesc])
                # 所有待修的车
                bikeList2 = Bike.objects.filter(defectStatus=True)
                for b2 in bikeList2:
                    bikeRst2.append(str(b2))
                rst = {"bikeLocation": bikeRst, "NeedRepairedBike": bikeRst2}
                return JsonResponse({"result": rst})
            elif operation == "balance":
                # 动态移车
                graph_dict = {
                    "X1": {"X2": 5, "X3": 1},
                    "X2": {"X1": 5, "X3": 2},
                    "X3": {"X1": 1, "X2": 2},
                }
                sba = SharingBikeAnalysis(
                    graph_dict,
                    Record,
                    columns=[
                        "recordId",
                        "bikeID",
                        "beginTime",
                        "endTime",
                        "beginLocId",
                        "endLocId",
                    ],
                    typeOfData="DB",
                )
                balanceRst = sba.makeDecisions()
                return JsonResponse({"result": balanceRst})
        except Exception:
            return JsonResponse({"error": "error"})


class CustApi(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request):
        try:
            jsonDict = eval(request.body)
            bID = eval(jsonDict["bikeid"])
            loc = eval(jsonDict["loc"])
            operation = eval(jsonDict["operation"])
            uID = eval(jsonDict["uid"])
            rst = "Succeed!"
            if operation == "rent":
                # bike
                locId = Bike.objects.get(bikeId=bID).curLocId.locId
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.availStatus == False:
                    rst = "Fail!"
                else:
                    bObj.availStatus = False
                    bObj.save()
                # user
                uObj = User.objects.get(userId=uID)
                # time
                now = datetime.datetime.utcnow()
                # record
                Record.objects.create(
                    userID=uObj, bikeID=bObj, beginTime=now, beginLocId=locId
                )
            elif operation == "back":
                # bike
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.availStatus == True:
                    rst = "Fail!"
                else:
                    bObj.availStatus = True
                    bObj.save()
                # user
                uObj = User.objects.get(userId=uID)
                # record
                r = Record.objects.get(userID=uObj, bikeID=bObj)
                r.endTime = datetime.datetime.utcnow()
                r.endLocId = loc
                r.save()
                # 付钱
                # price每小时的价格，time使用时间，pay总金额
                price = 0.01
                time_end = utc.localize(r.endTime)
                time = (time_end - r.beginTime).seconds
                pay = time * price
                uObj.balance = float(uObj.balance) - pay
                uObj.save()
                # 管理员收钱
                manager = User.objects.filter(userClass="manager")[0]
                manager.balance = float(uObj.balance) + pay
                manager.save()
            elif operation == "report":
                # bike
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.defectStatus == True:
                    rst = "Fail!"
                else:
                    bObj.defectStatus = True
                    bObj.save()
                # user
                uObj = User.objects.get(userId=uID)
            return JsonResponse({"result": rst})
        except Exception:
            return JsonResponse({"error": "error"})


class VerifyApi(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request):
        try:
            jsonDict = eval(request.body)
            name = eval(jsonDict["name"])
            pwd = eval(jsonDict["pwd"])
            usercls = eval(jsonDict["cls"])
            operation = eval(jsonDict["operation"])
            if operation == "login":
                user = User.objects.get(name=name, password=pwd, userClass=usercls)
            elif operation == "register":
                User.objects.create(name=name, password=pwd, userClass=usercls)
                user = User.objects.get(name=name, password=pwd, userClass=usercls)
            return JsonResponse({"result": [user.userId, user.userClass]})
        except Exception:
            return JsonResponse({"error": "error"})


def home(request):
    return render(request, "index.html")
