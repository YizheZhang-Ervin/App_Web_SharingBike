from django.db import models

class User(models.Model):
    # 用户ID
    userId = models.AutoField(primary_key=True)
    # 账户余额
    balance = models.DecimalField( max_digits=4, decimal_places=2,default=99.99)
    # 用户身份类型
    userClass = models.CharField(max_length=20,
    choices=(
        ("customer","customer"),("operator","operator"),("manager","manager")
    ))
    # 用户名
    name = models.CharField(max_length=20,unique=True)
    # 密码
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"userID:{str(self.userId)}, user Class:{str(self.userClass)}"

class Location(models.Model):
    # 地点ID
    locId = models.AutoField(primary_key=True)
    # 地点描述
    desc = models.CharField(max_length=200)

    def __str__(self):
        return f"Location ID:{str(self.locId)}, Description:{str(self.desc)}"

class Bike(models.Model):
    # 车ID
    bikeId = models.AutoField(primary_key=True)
    # 车当前位置
    curLocId = models.ForeignKey(Location, on_delete=models.CASCADE)
    # 车可租状态
    availStatus = models.BooleanField()
    # 车破损状态
    defectStatus = models.BooleanField()

    def __str__(self):
        return f"bikeID:{str(self.bikeId)}, current Location ID:{str(self.curLocId)}"

class Record(models.Model):
    # 记录ID
    recordId = models.AutoField(primary_key=True)
    # 用户ID
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    # 车ID
    bikeID = models.ForeignKey(Bike, on_delete=models.CASCADE)
    # 开始时间
    beginTime = models.DateTimeField('date published')
    # 结束时间
    endTime = models.DateTimeField(null = True)
    # 触发地id
    beginLocId = models.CharField(max_length=200)
    # 结束地id
    endLocId = models.CharField(max_length=200,null = True)

    def __str__(self):
        return f"RecordID:{str(self.recordId)}, userID:{str(self.userID)}, bikeID:{str(self.bikeID)}"
         
    
