from bs4 import BeautifulSoup
from lxml import html

class ClassUse:
    def __init__(self,phtml):
        self.html=phtml
        self.ExtractInfo()

    def ExtractInfo(self):
        soup = BeautifulSoup(self.html)
        tree=html.fromstring(self.html)
        t=soup.find_all()


