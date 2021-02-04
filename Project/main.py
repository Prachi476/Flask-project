from flask import Flask,render_template,request
import datetime
from datetime import timedelta, date
import pymysql
import pandas as pd
import pyodbc
app =Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        print(request.form)
        global name
        global dob
        global mobile_no
        global city

        name = request.form.get('name')
        print("name:",name)

        dob = request.form.get('dob')
        print("dob:",dob)

        mobile_no = request.form.get('mobile_no')
        print("mobile_no:",mobile_no)

        pan_no = request.form.get('pan_no')
        print("text:",pan_no)

        address = request.form.get('address')
        print("address:",address)

        city = request.form.get('city')
        print("city:",city)

        state = request.form.get('state')
        print("state:",state)

        rate_int = [10,12,15]
        if request.method == 'POST2':
            dur_loan = request.args.get('dur_loan')
            print("dur_loan",dur_loan)
            dur_loan = request.form.get('dur_loan')
            return "second post"

        return render_template("second_page.html",name=name,rate_int=rate_int)

    return render_template("login_form.html")

@app.route("/second_page")
def second_page_App():
    amt_limi = request.args.get('amt_limi')
    print("Amount Limit :",amt_limi)
    # print("type amt_limi 1",type(amt_limi))
    amt_limi=str(amt_limi)
    amt_limi=float(amt_limi)
    print("type amt_limi 2",type(amt_limi))
    dur_loan = request.args.get('dur_loan')
    print("Duration Loan :",dur_loan)
    dur_loan=float(dur_loan)
    print("type dur_loan",type(dur_loan))
    dur_loan_yr=dur_loan
    #dur_loan_yr=dur_loan/365
    #dur_loan_yr=round(dur_loan_yr, 2)
    print("dur_loan_yr",dur_loan_yr)

    rate_int = request.args.get('rate_int')

    print("Rate of interest :",rate_int)
    print("type :",type(rate_int))
    rate_int=float(rate_int)
    print("type :",type(rate_int))
    rate_int=rate_int/100

    transc_date = request.args.get('transc_date')
    print("Transaction Date : ",transc_date)
    transc_date = pd.to_datetime(transc_date)
    transc_date=transc_date.strftime('%d-%m-%Y')
    print("Transaction Date 2 : ",transc_date)
    print("Rate of interest >>>> :",rate_int)
    rate_int_op=rate_int / 365
    print("rate_int_op : ",rate_int_op)
	

    Compund_int=amt_limi * ( 1 +  rate_int / 365)**dur_loan_yr
    Compund_int=round(Compund_int, 2)
    print("Compund_int",Compund_int)
    print("Compund_int",type(Compund_int))
    # 1. Interest Amount (Use Compounding Effect)
    # Compund_int

    # 2. Loan Payment Due Date
    print("Transaction Date is : ",transc_date)
    transc_date = pd.to_datetime(transc_date) + pd.DateOffset(days=dur_loan)
    due_Date=transc_date.strftime('%d-%m-%Y')
    print("Loan Payment Due Date : ",due_Date)
    print("Compund_due_Date typent",type(due_Date))

    # insert from variable:
    Compund_int_var=Compund_int
    due_Date_var=due_Date
    final_amount_var=Compund_int

    #print("mobile_no :",mobile_no)
    #print("city :",city)

    # CONNECTION
    import pymysql
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root123',db='test_python')
    cur=conn.cursor()

    sql1="insert into details_table(Compund_int_var,due_Date_var,final_amount_var)values({0},'{1}','{2}')".format(Compund_int_var,due_Date_var,final_amount_var)

    cur.execute(sql1)
    print("Data Inserted")
    conn.commit()



    sql1="select * from test_python.details_table;"
    cur.execute(sql1)
    print("Data displayed" ,cur)
    row_list=[]
    for row in cur:
        print(type(row))
        row_list.append(row)
        print(row)
    print("row_list",row_list)

    conn.commit()
    cur.close()
    conn.close
    columns_list=('Compund_int_var','due_Date_var','final_amount_var')
    df = pd.DataFrame(row_list, columns =['Compund_int_var', 'due_Date_var', 'final_amount_var'])
    print("df",df)

    date_time_obj = datetime.datetime.strptime(dob, '%Y-%m-%d')
    new_today_date = date_time_obj.strftime("%d/%m/%Y")
    print ("new date:",new_today_date)
    dob2=new_today_date
    return render_template("third_page.html",tables=df.to_html(),name=name,dob_date=dob2,
    mobile_no=mobile_no,city=city  )


if __name__=="__main__":
    app.run(host='localhost',port=5000,debug=True)
