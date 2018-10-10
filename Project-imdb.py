
# coding: utf-8

# In[1]:


import smtplib
import requests
from bs4 import BeautifulSoup
import datetime


# In[2]:


print("Email: ")
email = input()
print("TV series: ")
series_list = [i for i in input().strip().split(',')]
message_details = "Regarding your query about the series,\n\n"


# In[5]:


import MySQLdb 
db = MySQLdb.connect("127.0.0.1","root","","imdbdb") 

cursor = db.cursor()

for name in series_list: 
    sql =  'insert into user values (' + '"' + email + '"' + ', ' + '"' +  name + '"' + ')'
    cursor.execute(sql)
    


# In[6]:


def stoi(s):
    if(s == "Jan."):
        return "01"
    if(s == "Feb."):
        return "02"
    if(s == "Mar."):
        return "03"
    if(s == "Apr."):
        return "04"
    if(s == "May"):
        return "05"
    if(s == "Jun."):
        return "06"
    if(s == "Jul."):
        return "07"
    if(s == "Aug."):
        return "08"
    if(s == "Sep."):
        return "09"
    if(s == "Oct."):
        return "10"
    if(s == "Nov."):
        return "11"
    if(s == "Dec."):
        return "12"

def check(s):
    if(len(s) == 2):
        return s
    else:
        return "0" + s
    
def join(s):
    s1 = ""
    for i in range(len(s)):
        if(i == 4 or i == 6):
            s1 += '-'
        s1 += s[i]
    return s1


# In[7]:


actual_series_name = []


# In[8]:


for name in series_list:
    #this response is to get the url of original webpage of series on imdb
    response =  requests.get("https://www.imdb.com/find?q=" + name + "&s=all")
    soup = BeautifulSoup(response.text,"html.parser")
    url = "https://www.imdb.com/" + soup.find_all(class_ = "result_text")[0].find('a')["href"]
    name = soup.find_all(class_ = "result_text")[0].find('a').get_text()
    actual_series_name.append(name)
    
    
    #this response is to get the url of last season or next season webpage
    response2 = requests.get(url)
    soup2 = BeautifulSoup(response2.text,"html.parser")
    
    #if series deatils could not be found or if some enters a fake name 
    if(len(soup2.find_all(class_ = "seasons-and-year-nav")) == 0):
            message_details += ("Tv series name: " + name +"\n"+
                         "Status: " + " series not found" + "\n\n")
            continue
    url_season = "https://www.imdb.com/" + soup2.find_all(class_ = "seasons-and-year-nav")[0].find('a')["href"]
    
    
    
    #this is done to get all the airdates mentioned on imdb for the tv series we are searching for
    response3 = requests.get(url_season)
    soup3 = BeautifulSoup(response3.text,"html.parser")
    all_airdates = soup3.find_all(class_ = "airdate")
    
    #to get current date
    today_date = str(datetime.datetime.now().date())
    year,month,day = today_date.split('-')
    today_date = year+month+day
    
    #a list to contain all the dates in string datatype
    date_list = []
    for airdate in all_airdates:
            dat = [i for i in airdate.get_text().split()]
            date = ""
            if(len(dat) == 1):
                date = dat[0]
            if(len(dat) > 1):
                date = dat[2] + stoi(dat[1]) + check(dat[0])
            date_list.append(date)
            
    
    flag = False
    prem_date = ''
    message = ''
    
    #current date is compared with next air date lexicographically
    for date in date_list:
        if(date >= today_date):
            prem_date = date
            flag = True
            break
    if(flag):
        if(len(date) > 5):
            message = "The next episode airs on " + join(prem_date)
        else:
            message = "The next Season begins in " + prem_date

    else:
        if(len(date_list[-1]) > 1):
            message = "The Show has Finished streaming all its episode"
        else:
            date_list.sort()
            if(len(date_list[-1]) > 4):
                message = "The last episode aired on " + join(date_list[-1]) 
            else:
                message = "The last episode is scheduled to air in " + join(date_list[-1]) 
            message += " ,currently no information about the next episode air date"

    message_details += ("Tv series name: " + name +"\n"+
                         "Status: " + message + "\n\n")


# In[9]:


print(message_details)


# ###  For senders email(@gmail.com), you might need to turn on "allow less secure apps" in senders gmail account settings.
# ###### for more help , https://support.google.com/mail/answer/7126229?hl=en

# In[9]:


message_details += "Thank you"
mail = smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
#sender's email (@gmail.com)
#sender's password
mail.login(senders_email,senders_password)
mail.sendmail(senders_email,email,message_details)

