import pandas as pd
import numpy as np
import heapq
import math
import sys
class SharingBikeAnalysis:
    def __init__(self,graph,obj,columns,typeOfData="excel",dataname="bikedata"):
        self.df = self.getData(obj,columns,typeOfData,dataname)
        self.graph_dict = graph
        self.lowLoc = int(self.df['bikeFromLoc'].min()[1])
        self.upLoc = int(self.df['bikeToLoc'].max()[1])
        self.lowTime = self.df['bikeStartTime'].min().to_pydatetime().hour
        self.upTime = self.df['bikeEndTime'].max().to_pydatetime().hour
        self.callSequence = []
    
    def getData(self,obj,columns,typeOfData,dataname):
        if typeOfData=="excel":
            return pd.read_excel(f"static/{dataname}.xlsx")
        else:
            df =  pd.DataFrame(list(obj.objects.all().values()),columns=columns)
            df.columns = ['recordID','bikeID',"bikeStartTime","bikeEndTime","bikeFromLoc","bikeToLoc"]
            return df

    def getCallSequence(self):
        return "Function call Sequence is: "+" -> ".join(self.callSequence)
    
    def bikeDistribution(self):
        self.callSequence.append("bikeDistribution")
        df = self.df
        lowTime=self.lowTime
        upTime=self.upTime
        lowLoc=self.lowLoc
        upLoc=self.upLoc
        rentBikeList = []
        returnBikeList = []
        for i in range(lowTime,upTime+1):
            for j in range(lowLoc,upLoc+1):
                time = i
                location = "X"+str(j)
                df2 = df.loc[(df['bikeFromLoc']==location) & (df['bikeStartTime']==time)]
                df3 = df.loc[(df['bikeToLoc']==location) & (df['bikeEndTime']==time+1)]
                count1 = len(df2)
                count2 = len(df3)
                rentBikeList.append([time,location,count1])
                returnBikeList.append([time+1,location,count2])
        return rentBikeList,returnBikeList
    
    def bikeDiff(self,rentBikeList,returnBikeList):
        self.callSequence.append("bikeDiff")
        diffList = []
        for i in rentBikeList:
            for j in returnBikeList:
                if i[0]==j[0] and i[1]==j[1]:
                    diff = j[2]-i[2]
                    diffList.append([i[0],i[1],diff])
        return diffList
    
    def bikeDiffByTime(self,diffList):
        self.callSequence.append("bikeDiffByTime")
        divideDiffList = []
        lowTime=self.lowTime
        upTime=self.upTime
        for i in range(lowTime,upTime+1):
            temp = [_ for _ in diffList if _[0]==i]
            if len(temp)!=0:
                divideDiffList.append(temp)
        return divideDiffList

    def init_distance(self,graph, s):
        self.callSequence.append("init_distance")
        distance = {s: 0}
        for vertex in graph:
            if vertex != s:
                distance[vertex] = math.inf
        return distance

    def dijkstra(self,graph, s):
        self.callSequence.append("dijkstra")
        pqueue = []
        heapq.heappush(pqueue, (0, s))
        seen = set()
        parent = {s: None}
        distance = self.init_distance(graph, s)
        while len(pqueue) > 0:
            pair = heapq.heappop(pqueue)
            dist = pair[0]
            vertex = pair[1]
            seen.add(s)
            nodes = graph[vertex].keys()
            for w in nodes:
                if w not in seen:
                    if dist + graph[vertex][w] < distance[w]:
                        heapq.heappush(pqueue, (dist + graph[vertex][w], w))
                        parent[w] = vertex
                        distance[w] = dist + graph[vertex][w]
        return parent, distance
    
    def computeRoute(self,fromLocation,toLocation):
        """
        输入值:(起点，终点)
        如:('X1','X2')
        返回值:(具体路径，路径长度)
        如: ('X1->X3->X2',3)
        """
        
        self.callSequence.append("computeRoute")
        parent_dict, distance_dict = self.dijkstra(self.graph_dict, fromLocation)
        middleLoc = toLocation
        record = fromLocation
        while(fromLocation != middleLoc):
            middleLoc = parent_dict[middleLoc]
            if middleLoc != fromLocation:
                record += "->"+middleLoc
            else:
                record += "->"+toLocation
        return record,distance_dict[toLocation]
    
    def balance(self,lis):
        """
        输入值:[[时间，地点，车多少情况],...]
        如: [[3, 'X1', -7], [3, 'X2', -5], [3, 'X3', 14]]
        输出值: [[调出地，调入地，路径长度，具体路径],...],{需调出地:多出的数量},{需调入地:缺少的数量}
        如: [['X3', 'X1', 7, 'X3->X1'], ...], {'X3': 2}, {"X1":-2}
        """
        
        self.callSequence.append("balance")
        posDict,negDict,fromLocationList,toLocationList = self.demandsAnalysis(lis)
        distanceDict,allDistanceDict,posDict,negDict = self.situationAnalysis(posDict,negDict,fromLocationList,toLocationList)
        bikeSend,tooMany,tooLess = self.numAnalysis(posDict,negDict,distanceDict,allDistanceDict)
        return bikeSend,tooMany,tooLess

    def demandsAnalysis(self,lis):
        """
        输入值:[[时间，地点，车多少情况],...]
        如: [[3, 'X1', -7], [3, 'X2', -5], [3, 'X3', 14]]
        输出值:{地点，车多少情况},{地点，车多少情况},[调出地],[调入地]
        如: {"X1":-2},{"X2":1},["X1","X2"],["X3"]
        """
        
        self.callSequence.append("demandsAnalysis")
        posDict = {i[1]:i[2] for i in lis if i[2]>0}
        negDict = {i[1]:i[2] for i in lis if i[2]<0}
        fromLocationList = [i for i in posDict.keys()]
        toLocationList = [i for i in negDict.keys()]
        return posDict,negDict,fromLocationList,toLocationList

    def situationAnalysis(self,posDict,negDict,fromLocationList,toLocationList):
        """
        输入值:{地点，车多少情况},{地点，车多少情况},[调出地],[调入地]
        如: {"X1":-2},{"X2":1},["X1","X2"],["X3"]
        输出值:{调出地:[路径长度，具体路径，调入地]}，{调出地:[路径长度，具体路径，调入地]},{地点，车多少情况},{地点，车多少情况}
        如: {'X3': [1, 'X3->X1', 'X1']},{'X3': [1, 'X3->X1', 'X1']},{"X1":-2}，{"X2":1}
        """
        
        self.callSequence.append("situationAnalysis")
        distanceDict = {}
        allDistanceDict = {}
        for i in fromLocationList:
            for j in toLocationList:
                r,d = self.computeRoute(i,j)
                allDistanceDict[(i,j)] = [d,r,j]
                if d<distanceDict.get(i,[sys.maxsize])[0]:
                    distanceDict[i] = [d,r,j]
        return distanceDict,allDistanceDict,posDict,negDict

    def numAnalysis(self,posDict,negDict,distanceDict,allDistanceDict):
        """
        输入值:{地点，车多少情况},{地点，车多少情况},{调出地:[路径长度，具体路径，调入地]}
        如: {"X1":-2},{"X2":1},{'X3': [1, 'X3->X1', 'X1']},{'X3': [1, 'X3->X1', 'X1']}
        输出值: [[调出地，调入地，路径长度，具体路径],...],{需调出地:多出的数量},{需调入地:缺少的数量}
        如: [['X3', 'X1', 7, 'X3->X1'], ...], {'X3': 2}, {"X1":-2}
        """

        self.callSequence.append("numAnalysis")
        loop = 0
        bikeSend = []
        while(self.hasExtraBike(posDict,negDict)):
            loop+=1
            if loop==0:
                bikeSend,negDict,posDict = self.computeNum(bikeSend,distanceDict,posDict,negDict)
            else:
                bikeSend,negDict,posDict = self.computeNum(bikeSend,allDistanceDict,posDict,negDict)
        tooMany = {i:v for i,v in posDict.items() if v>0}
        tooLess = {i:v for i,v in negDict.items() if v<0}
        return bikeSend,tooMany,tooLess

    def computeNum(self,bikeSend,distanceDict,posDict,negDict):
        """
        输入值:空列表[],{调出地:[路径长度，具体路径，调入地]},{地点，车多少情况},{地点，车多少情况}
        如:[],{'X3': [1, 'X3->X1', 'X1']},{"X1":-2},{"X2":1}
        输出值:[[调出地，调入地，路径长度，具体路径],...],{地点，车多少情况},{地点，车多少情况}
        如:[['X3', 'X1', 7, 'X3->X1'], ...],{"X1":-2},{"X2":1}
        """

        self.callSequence.append("computeNum")
        for k,v in distanceDict.items():
            if len(k)>1:
                k = k[0]
            n1 = posDict[k]
            n2 = negDict[v[2]]
            if n1>0 and n2<0:
                if n1>=abs(n2):
                    bikeSend.append([k,v[2],abs(n2),v[1]])
                    posDict[k] = posDict[k] + negDict[v[2]]
                    negDict[v[2]] = 0
                else:
                    bikeSend.append([k,v[2],n1,v[1]])
                    negDict[v[2]] = negDict[v[2]] + posDict[k]
                    posDict[k] = 0
        return bikeSend,negDict,posDict

    def hasExtraBike(self,posDict,negDict):
        self.callSequence.append("hasExtraBike")
        l1 = len([i for i in posDict.values() if i>0])
        l2 = len([i for i in negDict.values() if i<0])
        return l1 and l2
    
    def makeDecisions(self):
        self.callSequence.append("makeDecisions")
        balanceSolution = []
        rentBikeList,returnBikeList = self.bikeDistribution()
        diffList = self.bikeDiff(rentBikeList,returnBikeList)
        divideDiffList = self.bikeDiffByTime(diffList)
        for subList in divideDiffList:
            time = subList[0][0]
            sums = [i[2] for i in subList]
            isAllPositive = all([True if i>0 else False for i in sums])
            if sum(sums)<0:
                locs = ",".join([i[1] for i in subList if i[2]<0])
                balanceSolution.append(f"Time:{time} should buy new bikes for sharing, locations are {locs}")
            elif sum(sums)>=0:
                if isAllPositive:
                    locs = ",".join([i[1] for i in subList if i[2]>0])
                    balanceSolution.append(f"Time:{time} has too many bikes in service, locations are {locs}")
                else:
                    bikeSend,tooMany,tooLess = self.balance(subList)
                    balanceSolution.append(f"Time:{time} should do {bikeSend}, too many {tooMany}, too Less {tooLess}")
        return balanceSolution

if __name__ == "__main__":
    graph_dict = {
        "X1": {"X2": 5, "X3": 1},
        "X2": {"X1": 5, "X3": 2},
        "X3": {"X1": 1, "X2": 2},
    }
    sba = SharingBikeAnalysis(graph_dict)
    [print(_) for _ in sba.makeDecisions()]
    print()
    print(sba.getCallSequence())