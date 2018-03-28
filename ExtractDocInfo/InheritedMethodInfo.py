from bs4 import BeautifulSoup
import bs4
#from ExtractDocInfo import ParamaterInfo
from ParamaterInfo import  ParameterDetails


class InheritedMethodDetails:
    basicReturnTypes = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'void']

    def __init__(self,inheritedmethodrow,type,currtypename,inhfrm):
        self.curtypename=currtypename
        if('class' == inhfrm.split('.')[0]):
            inhfrm=inhfrm.replace('class.','class ')
        else:
            inhfrm=inhfrm.replace(inhfrm.split('.')[0],inhfrm.split('.')[0] +' ')
            print("Unhandled Case check and Fix teh Bug")

        if(type=='summary'):
            self.inheritedfrom=inhfrm
            self.methodname=inheritedmethodrow.text
            self.methodref=inheritedmethodrow.attrs['href']

