from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Record, Bike, Location
from .analysis import SharingBikeAnalysis
import datetime
import pytz

utc = pytz.UTC


class SelectApi(View):
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
            rst = []
            if operation == "locations":
                loclist = Location.objects.all()
                for ll in loclist:
                    rst.append(ll.desc)
            return JsonResponse({"result": rst})
        except Exception:
            return JsonResponse({"error": "error"})


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
            if operation == "report":
                # get data
                tllis = []
                counts = {}
                data = {"time":[],"location":[],"bikeNum":[]}
                recordSet = Record.objects.all()
                for i in recordSet:
                    if (
                        i.beginTime != None
                        and i.endTime != None
                        and i.beginLocId != None
                        and i.endLocId != None
                    ):
                        tllis.append((i.beginTime.hour,i.beginLocId))
                        tllis.append((i.endTime.hour,i.endLocId))
                for i in tllis:
                    counts[(i[0],i[1])] = counts.get((i[0],i[1]),0)+1
                for i,v in counts.items():
                    data['time'].append(i[0])
                    data['location'].append(i[1])
                    data['bikeNum'].append(v)
                return JsonResponse({"result": data})
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
                    rst = "Error! Bike already repaired or Not need repair!"
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
                if len(bikeList) == 0:
                    bikeRst.append("None")
                for b in bikeList:
                    locID = b.curLocId.locId
                    locDesc = Location.objects.get(locId=locID).desc
                    bikeRst.append(f" Bike {b.bikeId} at Location {locDesc}")
                # 所有待修的车
                bikeList2 = Bike.objects.filter(defectStatus=True)
                if len(bikeList2) == 0:
                    bikeRst2.append("None")
                for b2 in bikeList2:
                    bikeRst2.append(f" Bike {b2.bikeId} at Location {b2.curLocId.desc}")
                rst = {"AllBikesLocation": bikeRst, "DefectiveBikesLocation": bikeRst2}
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
                        "beginTime",
                        "endTime",
                        "beginLocId",
                        "endLocId",
                    ],
                    typeOfData="DB",
                )
                balanceRst = sba.makeDecisions()
                if len(balanceRst) < 2:
                    balanceRst = "not enough records for analysis"
                return JsonResponse({"result": balanceRst})
        except Bike.DoesNotExist:
            return JsonResponse({"result": "Bike Not Exists"})
        except Location.DoesNotExist:
            return JsonResponse({"result": "Location Not Exists"})
        except Record.DoesNotExist:
            return JsonResponse({"result": "Record Not Exists"})
        except ValueError:
            return JsonResponse({"result": "Please enter correct content"})
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
                # bike & location
                locDesc = Bike.objects.get(bikeId=bID).curLocId.desc
                locObj = Location.objects.get(desc=locDesc)
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.availStatus == False or bObj.defectStatus == True:
                    return JsonResponse({"result": "Fail! Bike Not Available"})
                else:
                    bObj.availStatus = False
                    bObj.save()
                # user
                uObj = User.objects.get(userId=uID)
                # time
                now = datetime.datetime.utcnow()
                # record
                Record.objects.create(
                    userID=uObj,
                    bikeID=bObj,
                    beginTime=now,
                    beginLocId=locDesc,
                    beginLoc=locObj,
                )
            elif operation == "back":
                if loc == "":
                    return JsonResponse({"result": "Fail! Please choose location"})
                # bike
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.availStatus == True:
                    return JsonResponse({"result": "Fail! Wrong Bike or Location"})
                else:
                    bObj.availStatus = True
                    bObj.save()
                # location
                locObj = Location.objects.get(desc=loc)
                # user
                uObj = User.objects.get(userId=uID)
                # record
                r = Record.objects.get(userID=uObj, bikeID=bObj, finishedFlag=False)
                r.finishedFlag = True
                r.endTime = datetime.datetime.utcnow()
                r.endLocId = loc
                r.endLoc = locObj
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
                manager.balance = float(manager.balance) + pay
                manager.save()
            elif operation == "report":
                # bike
                bObj = Bike.objects.get(bikeId=bID)
                if bObj.availStatus == False:
                    return JsonResponse(
                        {"result": "Fail! Bike is in service, can't report for repair"}
                    )
                if bObj.defectStatus == True:
                    return JsonResponse(
                        {"result": "Fail! Bike already reported for repair"}
                    )
                else:
                    bObj.defectStatus = True
                    bObj.save()
                # user
                uObj = User.objects.get(userId=uID)
            return JsonResponse({"result": rst})
        except User.DoesNotExist:
            return JsonResponse({"result": "User Not Exists"})
        except Record.DoesNotExist:
            return JsonResponse({"result": "Record Not Exists"})
        except Bike.DoesNotExist:
            return JsonResponse({"result": "Bike Not Exists"})
        except Location.DoesNotExist:
            return JsonResponse({"result": "Location Not Exists"})
        except IndexError:
            return JsonResponse({"result": "Service Not open, No Manager Account now"})
        except ValueError:
            return JsonResponse({"result": "Please enter correct content"})
        # except Exception:
        #     return JsonResponse({"error": "error"})


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
            if name == "" or pwd == "":
                return JsonResponse(
                    {"error": "error", "reason": "Please enter name or password"}
                )
            if operation == "login":
                user = User.objects.get(name=name, password=pwd, userClass=usercls)
            elif operation == "register":
                User.objects.create(name=name, password=pwd, userClass=usercls)
                user = User.objects.get(name=name, password=pwd, userClass=usercls)
            return JsonResponse({"result": [user.userId, user.userClass]})
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "error": "error",
                    "reason": "User Not Exists or Wrong password or Wrong User Class",
                }
            )
        except Exception:
            return JsonResponse(
                {"error": "error", "reason": "Duplicate name or other Type in errors"}
            )


def home(request):
    return render(request, "index.html")
