import pdfplumber
import glob
import pymssql
import datetime
import os

UID='TW000626'
PWD='77078088'
def pdfreader(number,userip):

    #擷取該資料夾內所有pdf檔案
    pdf_list=glob.glob('./web/pdfreader_test/pdf/pdf_storge/*.pdf')

    #開啟此檔案確認資料是否輸入過
    f=open('./web/pdfreader_test/pdf/pdf_storge/pdf.txt','r')
    exist_pdf=f.read().split('\n')

    #如沒輸入過則加到list
    new_pdf_list=[]
    for x1 in pdf_list:
        if x1  in exist_pdf:
           #print('已存在')
            message='資料已存在'
           # return message
        else:
            new_pdf_list.append(x1)
    #連接資料庫
    with pymssql.connect(server="OKBANK-OC-TEST\MSSQLSERVER_2017",
                            DATABASE="OK_AMS",
                            user=UID,
                            password=PWD) as conn :
        with conn.cursor() as cursor:
            cursor.execute('SELECT OBEB_CheckCode FROM OKBorn_ElectricBill WHERE Del_tag=0')
            row=cursor.fetchall()
            new_row=[]
            for data1 in row:
                new_row.append(data1[0])
            
            for x in new_pdf_list:
                
                #開啟文字檔追加
                f=open('./web/pdfreader_test/pdf/pdf_storge/pdf.txt','a')
                
                #打開pdf
                with pdfplumber.open(x,password='83505532') as pdf:
                    first_page=pdf.pages[0]
                    y=first_page.extract_words()
                    
                    #追加新的pdf到文字檔
                    f.write(x+'\n')
                    
                    #日期擷取 top=67.351
                    date=[]
                    for y1 in y:
                        if y1['top'] == 67.351 :
                            date.append(y1['text'])
                    
                    #起
                    date_s=[]
                    date_s.append(str(int(date[0])+1911))
                    date_s.append(date[1])
                    date_s.append(date[2])
                    date_ss=''.join(date_s)
                    OBEB_StartDate=datetime.datetime.strptime(date_ss,'%Y%m%d')
                    
                    #迄
                    date_e=[]
                    date_e.append(str(int(date[3])+1911))
                    date_e.append(date[4])
                    date_e.append(date[5])
                    date_ee=''.join(date_e)
                    OBEB_EndDate=datetime.datetime.strptime(date_ee,'%Y%m%d')
                    
                        
                    #電號擷取 
                    OBED_ENo=y[11]['text']
                    
                    #電費合計擷取 
                    OBEB_TotalAmount=y[15]['text']
                    OBEB_TotalAmount=int(OBEB_TotalAmount.replace(',',''))
                    
                    #費率擷取
                    OBEB_Rate=float(y[26]['text'])
                    
                    #購電電數擷取
                    OBEB_PE=int(y[27]['text'])
                    
                    #購電電費擷取
                    OBEB_PE_Amount=y[28]['text']
                    OBEB_PE_Amount=OBEB_PE_Amount[:-1]
                    OBEB_PE_Amount=int(OBEB_PE_Amount.replace(',',''))
                    
                    #電表租費小計 x0=531.2
                    try:
                        for y1 in y:
                           if y1['top'] == 331.4509999999999:
                               OBEB_RentSubTotal=int(y1['text'][:-1])
                    except:
                        for y1 in y:
                           if y1['top'] == 355.45200000000006:
                               OBEB_RentSubTotal=int(y1['text'][:-1])
                 
                    #服務部門 x1=176.363
                    for y1 in y:
                        if y1['x1'] == 176.363:
                            OBEB_ServiceDept=y1['text']
                    
                    #檢核碼擷取 top=772.091
                    check_num=[]
                    for y1 in y:
                        if y1['top'] == 772.091 :
                            check_num.append(y1['text'])
                    OBEB_CheckCode=''.join(check_num)
                    
                    if isinstance(number , str) == False:
                        number=str(number)

                    
                    #資料庫新增
                    if OBEB_CheckCode in new_row:
                        message='未重複資料已上傳'
                    else:
                        cursor.execute("""INSERT INTO OKBorn_ElectricBill 
                                (OBED_ENo,OBEB_TotalAmount,OBEB_StartDate,OBEB_EndDate,
                                    OBEB_Rate,OBEB_PE,OBEB_PE_Amount,OBEB_RentSubTotal,
                                    OBEB_CheckCode,OBEB_ServiceDept,Add_User,Add_IP) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
                                ,(OBED_ENo,OBEB_TotalAmount,OBEB_StartDate,OBEB_EndDate,
                                    OBEB_Rate,OBEB_PE,OBEB_PE_Amount,OBEB_RentSubTotal,
                                    OBEB_CheckCode,OBEB_ServiceDept,number,userip))
                        conn.commit()
                        message='已成功上傳'
            
    f.close()
    return message            

def handle_file(file):
    import datetime
    file_name=file.name
    file_path=os.path.join('./web/pdfreader_test/pdf/pdf_storge/',str(datetime.datetime.today())+file_name)
    with open(file_path,'wb+') as des:
         for chunk in file.chunks():
             des.write(chunk)
    
