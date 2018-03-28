
class CheckTags:
    tagDict = {}
    def __init__(self):
        pass

    def AddKey(self,key):
        if(key in CheckTags.tagDict):
            pass
        else:
            CheckTags.tagDict[key]=key

