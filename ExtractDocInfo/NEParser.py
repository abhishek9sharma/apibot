


class NEntParent:
    def __init__(self,name,packagename,type):
        if packagename is None:
            self.name=name
            self.EntType=type
        else:
            self.name=name
            self.packagename = packagename
            self.EntType = type

