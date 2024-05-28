import yaml
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

TRAVELLER_FILE="../test/input.yml"

class Traveller(object):
    def __init__(self, input = TRAVELLER_FILE):
        self.travellerCounts = {"adult": 0, "children": 0, "infant": 0}
        try:
            self.travelPlan=load(open(input), Loader=Loader)
            #print(self.travelPlan, input)
        except Exception as E:
            print("Error loading input:", E, input)
        self.fetchTravellers()

    def getPortal(self):
        return self.travelPlan["TravelPlan"]["url"]

    def getTravellerCounts(self):
        return self.travellerCounts

    def fetchTravellers (self):
        travellers = self.travelPlan["Travellers"]
        for item in travellers:
            self.travellerCounts[item["userType"]] +=1
        return self.travellerCounts

    def plan(self):
        return self.travelPlan["TravelPlan"]

if __name__=="__main__":
    traveller = Traveller()
    print(traveller.travelPlan)
    print(traveller.getPortal())

