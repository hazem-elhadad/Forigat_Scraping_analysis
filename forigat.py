import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time
from time import sleep
import pandas as pd

AllInt_Age = []
AllMaritalState = []
AllInt_NumOfChildren = []
AllInt_RemindedMoney = []
AllInvoiceNum = []
AllOriginalDept = []
AllInt_PaiededPercent = []
AllLinks = []
AllNationality = []
AllRegion = []

""""أستخراج الداتا يكون علي هيئة text حتى الداتا 
# الرقمية ولذلك يتم حفظ الداتا علي شكل نص في قائمة وتحويل هذه الداتا الي شكل رقمى في قائمة أخري 
مثلا RemindedMoney و IntRemindedMoney"""
#nogpages=1393
for page in range(1,10):
    start4=time.time()
    start1=time.time()
    retries = 0
    while True :
        try:
            url = "https://ehsan.sa/forijat?p=" + str(page)
            link_get = requests.get(url)
            print("Page Num: " + str(page))
            print("Page Res: " + str(link_get.status_code))
            soup = BeautifulSoup(link_get.content, "lxml")
            end1 = time.time()
            print(end1 - start1)
            start2 = time.time()
            text_of_person = soup.find_all("div", {"aria-level": "4"})
            for person in text_of_person:
                person_age = re.findall(r'\s\d{2,3}\s', person.text)
                IntAge = int(person_age[0].replace(" ", ""))
                AllInt_Age.append(IntAge)
                if "متزوج" in person.text:
                    AllMaritalState.append("متزوج")
                elif "أعزب" in person.text:
                    AllMaritalState.append("أعزب")
                else:
                    AllMaritalState.append(None)

                if "طفل" in person.text:
                    AllInt_NumOfChildren.append(1)
                elif "طفلين" in person.text:
                    AllInt_NumOfChildren.append(2)
                elif "أطفال" in person.text:
                    AllInt_NumOfChildren.append(int(((re.findall(r'\s\d{1,2}\s', person.text))[1].replace(" ", ""))))
                else:
                    AllInt_NumOfChildren.append(0)
                try:
                    newreminded = float(((re.findall(r'\d{3,9}\.?\d\s*', person.text))[0].replace(" ", "")))
                    AllInt_RemindedMoney.append(newreminded)
                except:
                    newreminded = 0
                    AllInt_RemindedMoney.append(newreminded)
            end2 = time.time()
            print(end2 - start2)
            # الخطوة الجاية نحصل علي نسبة ما تم جمعه ونقوم حساب المبلغ الأصلي

            percent_payed = soup.find_all("div", {"class": "d-flex justify-content-between mt-3"})
            for pay in percent_payed:
                Children = pay.find('div')
                AllInt_PaiededPercent.append(float((re.findall(r'\d{1,3}', Children.text))[0]))
            # سنقوم بتحويل كل القيم الموجودة في list المبلغ المتبقي والنسبة الي أرقام حتى نستطيع اجراء عمليات حسابية عليها
            # تم تحويل كل القيم لأرقام لعمل عمليات حسابية عليها

            InvNum = soup.find_all("small", {
                "class": "border-rounded-8 d-block pb-1 pt-4 sdad-bill shadow text-center text-white w-100"})
            for data in InvNum:
                Children = data.find("span")
                AllInvoiceNum.append(Children.text)
            href_links = soup.find_all("a", {"class": "card-details-link"})
            for element3 in href_links:
                AllLinks.append("https://ehsan.sa" + element3['href'])
                tries = 0
                while True:
                    try:
                        url_request = requests.get("https://ehsan.sa" + element3['href'])
                        if url_request.status_code in [200, 404]:
                            print("Link Response: " + str(url_request.status_code))
                            soup = BeautifulSoup(url_request.content, 'lxml')
                            try:
                                text_box = soup.find("div" , {"class": "row no-gutters small text-center"})
                                Natio = text_box.findAll("div")

                                Nationalityforperson = Natio[0].text
                                AllNationality.append(Nationalityforperson[8:].strip())
                                Regionforperson = Natio[6].text
                                AllRegion.append(Regionforperson[8:].strip())
                            except:
                                pass
                            break
                    except Exception as e:
                        print(url_request.text)
                        tries += 1
                        time.sleep(2)
                        if tries > 3:
                            AllNationality.append(None)
                            AllRegion.append(None)
                            print(e)
                            print(" breaking while loop after scraping all data")
                            time.sleep(5)
                            break

            if link_get.status_code in [200 , 404]:
                break
        except Exception as e:
            print(url_request.text)
            tries += 1
            time.sleep(2)
            if tries > 3:
                print(e)
                print(" breaking while loop after scraping all data")
                time.sleep(5)
                break


        print("Saving The Data Of Page: " +str(page))
        print("Preparing The Data Frame")
        start3=time.time()


        end3=time.time()
        print(end3-start3)
        end4=time.time()
        print('For loop time: ' + str(end4 - start4))
    print(len(AllInvoiceNum), len(AllInt_NumOfChildren), len(AllInt_PaiededPercent), len(AllLinks),
              len(AllInt_RemindedMoney), len(AllNationality), len(AllRegion), len(AllInt_Age), len(AllMaritalState))

for i in range(len(AllInt_PaiededPercent)):
    try:
        if AllInt_PaiededPercent[i] != 0:
            Calc_original = (AllInt_RemindedMoney[i] * AllInt_PaiededPercent[i]) / (
                    100 - AllInt_PaiededPercent[i])
            rounded_number = round(Calc_original +AllInt_RemindedMoney[i] , 2)
            AllOriginalDept.append(rounded_number)
        else:
            AllOriginalDept.append(AllInt_RemindedMoney[i])
    except:
        AllOriginalDept.append(None)

percentile_list = pd.DataFrame({'InvoiceNum': AllInvoiceNum,
        'OriginalDept': AllOriginalDept,
        'Age': AllInt_Age,
        'Paid Percent':AllInt_PaiededPercent,
        'Reminded Dept' : AllInt_RemindedMoney,
        'NumberOfChildrens' : AllInt_NumOfChildren,
        'Region': AllRegion,
        'Nationality' : AllNationality,
        'MaritalStatus' : AllMaritalState,
        'PageURL' : AllLinks})
df= percentile_list.reset_index(drop=True)
df.to_excel("ForigatDataExcel33.xlsx")
# getting the timestamp
dt = datetime.now()

ts = datetime.timestamp(dt)

print("Date and time is:", dt)
print("Timestamp is:", ts)