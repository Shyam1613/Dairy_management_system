import mysql.connector,time
from mysql.connector import errorcode
from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
import cgi

try:
  cnx = mysql.connector.connect(user='root',host="localhost",password="12345",database='farm')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
    
cur=cnx.cursor()

options = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA',
'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH',
'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
'HDFC', 'ICICIBANK', 'ITC', 'IOC', 'INDUSINDBK', 'INFY',
'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC',
'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE',
'SHREECEM', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS',
'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']

app = Flask(__name__)
form=cgi.FieldStorage()

@app.route('/')
def dairy():
  return render_template('main.html')       

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
      user=(request.form['name'])
      passwd=(request.form['pass'])
      cur.execute("select * from admin")
      login=cur.fetchall()
      if user==login[0][0] and passwd==login[0][1]:
        return redirect(url_for('admin1'))
      else:
        return (render_template('loginfail.html'))     
    return (render_template('admin.html'))
  
@app.route('/admin1',methods=['GET','POST'])
def admin1():
  if request.method=='POST':
      stname=(request.form['stname'])
      passwd=(request.form['passwd'])
      sal=(request.form['sal'])
      now = datetime.now()
      join=now.strftime("%Y-%m-%d")
      print(join)
      cur.execute("select max(staffid) from staff")
      id=cur.fetchone()
      staffid=0
      if id[0]==None:
        staffid=1
      else:  
        staffid=id[0]+1
      list=(staffid,stname,passwd,sal,join)
      query='insert into staff(staffid,name,passwd,salary,joindate)values(%s,%s,%s,%s,%s)'
      cur.execute(query,list)
      cnx.commit()
      return (render_template('staffadd.html',list=list))  
  return (render_template('admin1.html'))  


@app.route('/adminstaff',methods=['GET','POST'])
def adminstaff():
  cur.execute("select * from staff")
  st=cur.fetchall()
  return (render_template('adminstaff.html',st=st))     

@app.route('/adminseller',methods=['GET','POST'])
def adminseller():
  cur.execute("select * from seller")
  st=cur.fetchall()
  return (render_template('adminseller.html',st=st))     

@app.route('/container',methods=['GET','POST'])
def container():
  cur.execute("select * from container where staffid IS NOT NULL")
  st=cur.fetchall()
  return (render_template('container.html',st=st)) 

@app.route('/bill',methods=['GET','POST'])
def bill():
  cn = mysql.connector.connect(user='root',host="localhost",password="12345",database='farm')  
  cursor=cn.cursor()
  cursor.execute("call get_bill(@M)")
  st=cursor.fetchall()
  cursor.close()
  cursor=cnx.cursor()
  return (render_template('bill.html',st=st))


@app.route('/billinfo',methods=['GET','POST'])
def billinfo():
    if request.method=='POST':
      bid=(request.form['bid'])
      cur.execute("select * from bill where staffid IS NOT NULL and bid=%s",(bid,))
      st=cur.fetchall()
      cur.execute("select * from container where staffid IS NOT NULL and bid=%s",(bid,))
      st1=cur.fetchall()
      return (render_template('billinfo.html',st=st,st1=st1))

@app.route('/dateinfo',methods=['GET','POST'])
def dateinfo():
    if request.method=='POST':
      date=(request.form['bid'])
      st2=(date,)
      cur.execute("select * from bill where staffid IS NOT NULL and bdate=%s",(date,))
      st=cur.fetchall()
      return (render_template('dateinfo.html',st=st,st2=st2))    
 
@app.route('/signup',methods=['GET','POST'])
def singnup():
  if request.method=='POST':
      sellername=(request.form['name'])
      passwd=(request.form['pass'])
      cattle=(request.form['cattle'])
      address=(request.form['address'])
      sellerid=0
      cur.execute("select max(sellid) from seller")
      id=cur.fetchone()
      if id[0]==None:
        sellerid=1
      else:  
        sellerid=id[0]+1
      list=(sellerid,sellername,passwd,cattle,address)
      query='insert into seller(sellid,name,passwd,cattle,address)values(%s,%s,%s,%s,%s)'
      cur.execute(query,list)
      cnx.commit()
      return (render_template('selleradd.html',list=list))  

  return (render_template('signup.html')) 


@app.route('/seller',methods=['GET','POST'])
def seller():
    if request.method=='POST':
      sellid=(request.form['name'])
      passwd=(request.form['pass'])
      cur.execute("select sellid,passwd from seller where sellid=%s",(sellid,))
      id=cur.fetchone()
      if id==None:
        return render_template('loginfail.html')       
      if sellid==str(id[0]) and passwd==id[1]:
        return redirect(url_for('seller1'))
      else:
        return render_template('loginfail.html')       
    return render_template('seller.html')       

@app.route('/seller1',methods=['GET','POST'])
def seller1():
  if request.method=='POST':
    named_tuple = time.localtime()
    time_string = time.strftime("%H:%M:%S", named_tuple)
    date_string = time.strftime("%Y-%m-%d", named_tuple)
    if int(time_string[0:2])>=5 :#and int(time_string[0:2])<=7:
      sellid=(request.form['sellid'])
      num=(request.form['n'])
      bid=0
      cur.execute("select max(bid) from bill")
      id=cur.fetchone()
      if id[0]==None:
        bid=1
      else:  
        bid=id[0]+1
      cur.execute("select * from bill")
      id=cur.fetchall()
      cur.execute("select bid,time from bill where bid=(select max(bid) from bill) and bdate=%s",(date_string,))
      id=cur.fetchone()
      if id==None:
        global btime
        btime='05:00:00'
      else:
        dtime=str(id[1])
        sec=(int(num)*30)+(int(dtime[0:2])*3600)+(int(dtime[3:5])*60)+(int(dtime[6:8]))
        btime=convert(sec)
      list=(bid,sellid,num,btime,date_string)
      query='insert into bill(bid,sellid,no_of_container,time,bdate)values(%s,%s,%s,%s,%s)'
      cur.execute(query,list)
      cnx.commit()
      return render_template('sellerbill.html',list=list)
    else:
      return render_template('timeslot.html')   
  return render_template('seller1.html')   

# Python Program to Convert seconds into hours, minutes and seconds
def convert(seconds):
	min, sec = divmod(seconds, 60)
	hour, min = divmod(min, 60)
	return '%02d:%02d:%02d' % (hour, min, sec)


@app.route('/staff',methods=['GET','POST'])
def staff():
    if request.method=='POST':
      staffid=(request.form['stname'])
      passwd=(request.form['passwd'])
      cur.execute("select staffid,passwd from staff where staffid=%s",(staffid,))
      id=cur.fetchone()
      if id==None:
        return render_template('loginfail.html')       
      if staffid==str(id[0]) and passwd==id[1]:
        return redirect(url_for('staff1'))
      else:
        return render_template('loginfail.html') 
    return render_template('staff.html')       

@app.route('/staff1',methods=['GET','POST'])
def staff1():
  if request.method=='POST':
      stid=(request.form['staffid'])
      sellid=(request.form['sellid'])
      collect=(request.form['collected'])
      fat=(request.form['fat'])
      bid=(request.form['bid'])
      named_tuple = time.localtime()
      date_string = time.strftime("%Y-%m-%d", named_tuple)
      container_id=0
      cur.execute("select max(container_id) from container")
      id=cur.fetchone()
      if id[0]==None:
        container_id=1
      else:  
        container_id=id[0]+1
      list=(container_id,sellid,stid,date_string,fat,collect,bid)
      query='insert into container values(%s,%s,%s,%s,%s,%s,%s)'
      cur.execute(query,list)
      cnx.commit()
      cur.execute("select amount from bill where bid=%s",(bid,))
      id=cur.fetchone()
      amt=0
      f=float(fat)
      if id[0]==None:
        if f>=4:
          amt=2000
        elif f<4 and f>=2:
          amt=1700
        elif f>=1 and f<2:
          amt=1500
        else:
          return render_template('error.html')
      else:  
        if f>=4:
          amt=id[0]+2000
        elif f<4 and f>=2:
          amt=id[0]+1700
        elif f>=1 and f<2:
          amt=id[0]+1500
        else:
          return render_template('error.html')
      cur.execute("update bill set amount=%s where bid=%s",(amt,bid))
      cur.execute("update bill set staffid=%s where bid=%s",(stid,bid))
      if collect=='yes':
        cnx.commit()
        return render_template('staffbill.html',list=list)
      else:
        return render_template('error.html')
  return render_template('staff1.html')  

if __name__=="__main__":
    app.run(debug=True,port=8000)
    
cnx.close()    