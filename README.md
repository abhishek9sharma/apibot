# ExtractDocInfo
A set Python Scripts to Convert Java API Documentation into a more readable Natural Language Format. These related to w.r.t _Domain Adapation_ Component 
w.r.t Paper ["APIBot: Question Answering Bot for API Documentation"](https://dl.acm.org/citation.cfm?id=3155585)


# Usage

### Download the whole project and then
1. Delete the _.keep_ files in all subdirectories of folder [Data](https://github.com/abhishek9sharma/apibot/tree/master/Data/).
2. Download the Java SE Documentaion from the official [link](http://www.oracle.com/technetwork/java/javase/documentation/jdk8-doc-downloads-2133158.html).
3. Unzip the .zip file extracted in previous step to folder [Data](https://github.com/abhishek9sharma/apibot/tree/master/Data/). You should see a _docs_ folder.
4.  Go the the folder  [ExtractDocInfo](https://github.com/abhishek9sharma/apibot/tree/master/ExtractDocInfo/) and run [IterateOverAPIDocs.py](https://github.com/abhishek9sharma/apibot/tree/master/ExtractDocInfo/IterateOverAPIDocs.py).
5. You should see the converted documents in the folder [FACTS](https://github.com/abhishek9sharma/apibot/tree/master/Data/FACTS).

#### Misc:
*   In case you delete the folders in  [Data](https://github.com/abhishek9sharma/apibot/tree/master/Data) you may run the .\setup.sh file present in the same folder.




# References
* ["APIBot: Question Answering Bot for API Documentation"](https://dl.acm.org/citation.cfm?id=3155585)

## Bibtex Citation 
```
@inproceedings{
  tian2017apibot,
  title={APIBot: Question answering bot for API documentation},
  author={Tian, Yuan and Thung, Ferdian and Sharma, Abhishek and Lo, David},
  booktitle={Automated Software Engineering (ASE), 2017 32nd IEEE/ACM International Conference on},
  pages={153--158},
  year={2017},
  organization={IEEE}
}
```


###### Tested on Python 3.5.2 and Ubuntu 16.04 LTS