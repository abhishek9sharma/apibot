from bs4 import BeautifulSoup
import bs4
#from ExtractDocInfo import ParamaterInfo
from ParamaterInfo import ParameterDetails


class InheritedFieldDetails:

    def __init__(self,inheriteFieldrow,type,currtypename,inhfrm):
        self.curtypename=currtypename
        if('class' == inhfrm.split('.')[0]):
            inhfrm=inhfrm.replace('class.','class ')
        else:
            inhfrm=inhfrm.replace(inhfrm.split('.')[0],inhfrm.split('.')[0] +' ')
            print("Unahndled Case check and Fix teh Bug")

        if(type=='summary'):
            self.inheritedfrom=inhfrm
            self.fieldname=inheriteFieldrow.text
            self.fieldref=inheriteFieldrow.attrs['href']

