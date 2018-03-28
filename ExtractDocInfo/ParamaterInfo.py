

class ParameterDetails:

    def __init__(self,position,type,name):
        self.position=position
        self.parametername=name
        self.parameterType = type.replace('.','_')
        self.description=''
