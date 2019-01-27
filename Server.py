from threading import Thread
from threading import Timer
from ServerThread import ServerThread
import json
import random
import time

defaultTimeLimit = 30


def main():
    threads = {}
    while True:
        data = input("Enter JSON file\n")
        if data is not None:
            dataFile = open(data)
            newTruck = json.load(dataFile)
            dataFile.close()
            threads[newTruck["ID"]] = Thread(target=createMission, args=[newTruck])
            threads[newTruck["ID"]].start()


def createMission(jsonData):
    driverCode = random.randint(100000, 999999)
    positionPath = jsonData["positionFile"]
    positionFile = open(positionPath, "r")
    position = {
        "latitude": None,
        "longitude": None,
        "lastLength": 0
    }
    mission = ServerThread(defaultTimeLimit, jsonData["ID"], driverCode, jsonData["startLocation"], jsonData["destination"], 0.0, 0.0)
    while True:
        receiveLocation(positionFile, position)
        print(position["latitude"])
        print(position["longitude"])
        mission.setLatitude(position["latitude"])
        mission.setLongitude(position["longitude"])
        check = mission.verifyLocation()
        if not check:
            inputCode = requestCode(mission.getTimeLimit(), mission)
            mission.verifyCode(inputCode)


def receiveLocation(positionFile, previousPosition):
    while True:
        positionFile.flush()
        positionJson = json.load(positionFile)
        positionFile.seek(0)
        print(positionJson)
        time.sleep(2)
        currentLength = len(positionJson["latitude"])
        previousLength = previousPosition["lastLength"]
        if currentLength != previousLength:
            print("hello")
            previousPosition["latitude"] = positionJson["latitude"][currentLength-1]
            previousPosition["longitude"] = positionJson["longitude"][currentLength-1]
            previousPosition["lastLength"] = currentLength
            return



def requestCode(missionTimeLimit, mission):
    timer = Timer(missionTimeLimit, mission.sendAlert)
    while not mission.alert:
        inputCode = receiveCode()
        if inputCode is not None:
            timer.cancel()
            return inputCode


# TODO: Ping driver
def receiveCode():
    return input("\nPlease enter your code: ")


if __name__ == "__main__":
    main()


# def main():
#     threads = {}
#     while True:
#         data = input("Enter JSON file\n")
#         if data is not None:
#             newTruck = json.load(open(data))
#             threads[newTruck["ID"]] = Thread(target=runTest, args=[newTruck["ID"]])
#             threads[newTruck["ID"]].start()
#
#
# class Test:
#     def __init__(self, testString):
#         self.testString = testString
#
#     def printTestString(self):
#         print("\nTruck ID is: %d", self.testString)
#
#
# def runTest(testString):
#     time.sleep(10)
#     test = Test(testString)
#     test.printTestString()
