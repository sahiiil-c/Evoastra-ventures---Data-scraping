'''
Libraries need to run this code are--

1. pandas
2. selenium
3. bs4
4. numpy
5. datetime
6. time
7. os

'''
from datetime import datetime,timezone
start= datetime.now()
import time,bs4,os
import pandas as pd
from selenium import webdriver
import numpy as np


null=np.nan

#Def functions

#Title Function
def Job_title_retr(company_rows):
    title_list=[]
    for row in company_rows:
        title_t=row.select("h2")[0].text.strip()
        title_list.append(title_t)
    return title_list



#company name function
def company_name_retr(company_rows):
    company_name_list=[]
    for row in company_rows:
        
        name=row.select('[itemprop=hiringOrganization] h3')[0].text.strip()

        
        company_name_list.append(name)
        
    return company_name_list



#location Function
def location_retr(company_rows):
    location_list=[]
    for row in company_rows:
        text= row.select(".location")[0].text
        if text == "💰 Upgrade to Premium to see salary":
            location_list.append(null)
            
        elif text.split()[0] == '🌏':
            location_list.append(" ".join(text.split()[1:]))
        
        else:
            location_list.append(row.select(".location")[0].text)
            
    return location_list



#job_type function
def job_type_retr(company_rows):
    job_type_list=[]
    for row in company_rows:
        # Handling errors, exceptions and invalid data
        try:
            text= row.select(".location")[1].text.strip()
            if text == '💰 Upgrade to Premium to see salary':
                job_type_list.append(null)
            
            else:
                job_type_list.append(' '.join(text.split()[1:3]))
            
        
        except IndexError:
            job_type_list.append(null)
            
    return job_type_list



#Salary Function
def salary_retr(company_rows):    
    
    
    salarys_list_str=[]
    Min_salary=[]
    Max_salary=[]
    
    for row in company_rows :
        
        
        try:
            s_split=row.select(".salary")[0].text.strip().split()
    
            #salary string
            s_str_f =' - '.join(s_split[1:4:2])
            
            #appending to list
            salarys_list_str.append(s_str_f)
            Min_salary.append(int(s_split[1][1:-1])*1000)
            Max_salary.append(int(s_split[3][1:-1])*1000)
        
        
        except IndexError:
            salarys_list_str.append(null)
            Min_salary.append(null)
            Max_salary.append(null)
    
    return_lst=[]
    return_lst.append(salarys_list_str)
    return_lst.append(Min_salary)
    return_lst.append(Max_salary)
    return return_lst




#tags Function
def tag_retr(company_rows):
    tags_list=[]
    
    for row in company_rows:
        tag_list=[]
        tags=row.select(".tag")
        for tag in tags:
            tag_t=tag.getText(strip=True)
            if tag_t.lower() in ["other"]:
                continue
            tag_list.append(tag_t)
        tags_list.append(tag_list)
    return tags_list

# job_id parsing
def job_id_retr(company_rows):
    id_list=[]
    for row in company_rows:
        id_c=row["data-id"]
        id_list.append(id_c)
    
    return id_list



# Url function
def job_url_retr(rows):
    job_url_list=[]
    for row in rows:
        job_url="https:/"+row.a["href"]
        job_url_list.append(job_url)
    return job_url_list


#date function
def date_retr(company_rows):
    time_list=[]
    for row in company_rows:
        
        date_str=row.find("time")["datetime"]
        
        date_f = datetime.fromisoformat(date_str)
        date= date_f.date()
        
        time_list.append(date)
        
    return time_list

#clearing the recent texts
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def main(total_pg_count):
    try:
        #DataFrame
        remoteok_jobs_dfd={
            "job_id":[],
            "company":[],
            "title":[],
            "url":[],
            "location":[],
            "date":[]
        }
        
                

        
        #Browser opwning 
        web_page= webdriver.Chrome()
        
        #opening Url in the browser
        url= "https://remoteok.com/"
        url_remote='https://remoteok.com/remote-jobs'
        web_page.get(url)
        
        
        
        #Tracking the scrolls
        pg_count=0
        
        #Time for loading the first page
        #----------v------ change here if loaing quick
        time.sleep(5)
        
        #Scroll till the page count and load the HTML code
        last_height= web_page.execute_script("return document.body.scrollHeight")
        while True:
            if pg_count==total_pg_count:
                break
        
            web_page.execute_script("window.scrollTo(0,{})".format(last_height))
            time.sleep(1)
            
            web_page.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
            new_height= web_page.execute_script("return document.body.scrollHeight")
            last_height=new_height
            
            #scroll and wait time in seconds
            #----------v---------change here for quick scrolls
            time.sleep(1)
            
            pg_count+=1
            clear_console()
            print("scraped {}/{} pages".format(pg_count,total_pg_count))
        
        # Fetching HTML code from browser and closing the browser
        html_source=web_page.page_source
        web_page.quit()
        
        print("Successfully scrapped {} pages".format(total_pg_count))
        
        time.sleep(1)
        clear_console()
        time.sleep(1)
        print("Extracting Data...")
        #converting HTML file into bs4 element
        soup = bs4.BeautifulSoup(html_source,"lxml")
        
        #Base rows where we are working
        company_rows=soup.table.tbody.select("tr[data-offset]")
        
        #job_ id
        remoteok_jobs_dfd['job_id']=job_id_retr(company_rows)
        
        #company parsing
        
        remoteok_jobs_dfd['company']=company_name_retr(company_rows)
        
        # title parsing
        remoteok_jobs_dfd['title']=Job_title_retr(company_rows)
        
        #url parsing
        remoteok_jobs_dfd['url']=job_url_retr(company_rows)
        
        #location parsing
        remoteok_jobs_dfd['location']=location_retr(company_rows)
        
        #date parsing
        remoteok_jobs_dfd['date']=date_retr(company_rows)
        
        time.sleep(1)
        clear_console()
        print("Data extracted succesfully")
        
        
        
        # pandas Exportation
        
        Remoteok_df=pd.DataFrame(remoteok_jobs_dfd)
        
        file_name="Remote_ok_jobs"
        Remoteok_df.to_csv(file_name+".csv")
        
        time.sleep(3)
        end= datetime.now()
        diff= end- start
        print("successfully scraped and retrieved data for {} jobs \n".format(len(remoteok_jobs_dfd["title"])))
        print("File has been saved as {} in {}\n".format(file_name+'.csv',os.getcwd()))
        print("\nRun time {}m {}s".format(round(diff.total_seconds()/60,2),round(diff.total_seconds(),2)))
        time.sleep(10)

    except:
        clear_console()
        print("ERROR..Your internet seems slow try again by increasing the idle time...")
        time.sleep(10)
        
if __name__ == "__main__":
    
    #ask page scrape count
    total_pg_count=int(input("How many pages do you want to scrape? ")) 

    '''convert ask input line into a def function afterwards '''
    main(total_pg_count)

    