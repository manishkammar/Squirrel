import pymysql as py
import pandas as pd
import datetime

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
cred=credentials.Certificate("firebase.json")
app=firebase_admin.initialize_app((cred))
db=firestore.client()

import re

def validate(number):#rashmi

    #pattern = re.compile(r'(^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$)')
    pattern=re.compile(r'(^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$)')
    return pattern.match(number)



def validate2(number):
    if (validate(number)):
        n=number.strip('+91')
        return True
    else:
        return False






def get_info(doc_id):#rashika
    if db.collection('Attendance').document(doc_id).get().exists:

        return True
    else:
        return False

def check_in(check_date,id):
    doc_ref = (db.collection('Attendance').document(id).collection('Date').document(check_date))
    doc = doc_ref.get().to_dict()
    global vval
    if doc != None:
        for i in doc:
            vval = doc[i]
        if vval is None:
            return False
        else:
            return True
    else:
        return False








def register(t_id, fname,uname,mob):
    print(t_id)
    doc_ref = db.collection('Attendance').document(str(t_id))
    try:
        doc_ref.set({
            'fname': str(fname),
            'username': str(uname),
            'contact': str(mob)
        })

    except:
        return "not registered"



def update(id,mob):
    con = py.connect(host="localhost", user="root", passwd="", database="attendance")
    id=str(id)
    mob=str(mob)
    sql = "UPDATE information SET contact_no="+mob+" WHERE uid="+id+""
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


    return

def jusin(user_id,date,tim):
    print('in')
    Date='Date'
    doc_ref1 = db.collection('Attendance').document(str(user_id)).collection(Date).document(str(date))
    try:
        doc_ref1.set({
            'in': tim

        })
    except:
        return "not in"




def jusout(date,user_id,tim):
    doc_ref2 = db.collection('Attendance').document(str(user_id)).collection('Date').document(str(date))

    doc_ref2.update({
            'out': tim

        })




def check_out(user_id,date1):

    '''import pymysql as py

    con = py.connect(host="localhost", user="root", passwd="", database="attendance")
    cursor = con.cursor()
    cursor.execute("SELECT in_time FROM register WHERE r_date=%s AND user_id=%s", (date1, user_id))
    result = cursor.fetchone()
    print(result)
    if result == None:
        return 1
    else:
        return 0'''
    return  0
