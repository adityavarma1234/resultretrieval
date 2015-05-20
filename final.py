import sys
import mechanize
from urllib2 import HTTPError
from bs4 import BeautifulSoup


#Browser
br = mechanize.Browser()

#sys.stdout = open('output.txt','w')
#Browser options
br.set_handle_refresh(False) #can sometimes hang without this
url = 'http://dolphintechnologies.in/manit/results.html' #url to read from
scholarnumberinitial = 111112050 #starting scholar number
scholarnumberfinal = 111112050   #ending scholar number 
semester = 6  #semester 
finaldata = [] #final output data is stored in this

def open_link(link):
    '''
    str-->NONE
    link-->the link to be opened
    returns nothing
    This function tries until the site is opened
    (Since the site gives httperror, I implemented this in a recursive manner)
    '''
    try:
        response = br.open(link)
    except HTTPError, e:
        open_link(link) #recurse until url is opened

def pretty_print():
    '''
    NONE-->NONE
    return NONE
    just print the final output in a pretty fashion ^_^
    '''
    col_width = max(len(word) for row in finaldata for word in row) #padding
    for row in finaldata:
        print "".join(word.ljust(col_width) for word in row)
        
def find_marks(data,scholar):
    '''
    (str,str)-->str
    data-->str,scholar-->str
    return NONE
    '''
    temp = []
    scholar = int(scholar)
    scholar = scholar%100
    print data
    print "Currently getting the score of ",scholar
    a = data.split('\n')
    if(data.find("schnot")!=-1 or len(a)!=199):
        temp.append(str(scholar))
        temp.append("NOT FOUND")
        finaldata.append(temp)
        #print scholar,"\t\t","NOT FOUND"
        return
    a[109] = a[109].lstrip()
    a[117] = a[117].lstrip()
    a[158] = a[158].lstrip()
    a[160] = a[160].lstrip()
    a[173] = a[173].lstrip()
    temp.append(str(scholar))
    temp.append(a[109])
    temp.append(a[158])
    temp.append(a[160])
    temp.append(a[173])
    finaldata.append(temp)
    #print a[117],a[109],a[158],a[160],a[173]
    

def getcandidate(scholar,semester):
    '''
    (int,int)-->bool
    scholar -->int scholar number
    semester --> current semester
    returns false if httperror occurs('Service not available!!!') 
    returns true if http error not found
    '''
    scholar = str(scholar)
    semester = list(str(semester))
    
    br.select_form("form1")  #select the first form (there is only one form available here)
    br.form['scholar'] = scholar #take this scholar number as input
    br.form['semester'] = semester #take this semester as input
    try:
        response = br.submit() #submit the form
    except HTTPError,e:
        return False
    soup = BeautifulSoup(response.read())
    a = soup.get_text()
    a = a.encode("utf-8")
    find_marks(a,scholar)
    return True

def main():
    for scholarnumber in range(scholarnumberinitial,scholarnumberfinal+1):
        open_link(url)
        while(1):
            a = getcandidate(scholarnumber,semester)
            if(a==True):
                break;
            open_link(url)
            
if __name__ == "__main__":
    main()
    pretty_print()
