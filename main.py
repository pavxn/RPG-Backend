import math
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./rpg-webathon-firebase-adminsdk-zjj29-e18c41fe89.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

courses = db.collection(u'courses')
faculty = db.collection(u'faculty')
wishes = db.collection(u'wishes')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



def new_course(course : dict):
    doc = courses.document(course['ccode'])
    doc.set(course)

@app.get('/courses')
def get_courses():
    some_data = courses.stream()
    data = []
    for doc in some_data:
        data.append(doc.to_dict())

    return data

def new_faculty(fac : dict):
    doc = faculty.document(fac['emp_id'])
    doc.set(fac)

@app.get('/faculty')
def get_all_faculty():
    some_data = faculty.stream()
    data = []
    for doc in some_data:
        data.append(doc.to_dict())

    return data

def new_wish(wish : dict):
    doc = wishes.document(wish['ccode'])
    doc.set(wish)

@app.post('/uploadcourses')
async def make_course_list(req : Request):
    info = await req.json()
    for doc in info['csv']:
        temp = {
            "ccode" : doc["Course Code"],
            "cname" : doc['Course Name'],
            "credits" : doc['C'],
            "ltpj" : [doc['L'], doc['T'], doc['P'], doc['J']]
        }
        new_course(temp)
    return {"message" : "Success"}

@app.post('/uploadfaculty')
async def make_fac_list(req : Request):
    info = await req.json()
    for doc in info['csv']:
        temp = {
            "emp_id" : doc["Emp id"],
            "name" : doc['Name'],
            "desig" : doc['Designation'],
            "school" : doc['School'],
            "email" : doc['Email'],
            "pref" : [],
            "phno" : doc['Phno']
        }
        new_faculty(temp)
    return {"message" : "Success"}

@app.post('/preferences')
async def update_preference(req : Request):
    info = await req.json()
    emp_id = str(info['empid'])
    temp = info['preferences']
    prefs = []
    
    #prefs = [info['p1'], info['p2'], info['p3'], info['p4'], info['p5']]

    fac = faculty.document(emp_id)
    fac.update({
        'pref' : prefs
    })


@app.post('/wishlist')
async def make_wishlist(req : Request):
    info = await req.json()
    for doc in info['csv']:
        nb = math.ceil(int(doc['No Wishlist Received'])/70)
        temp = {
            "ccode" : doc['Course Code'],            
            "nwish" : doc['No Wishlist Received'],
            "nbatches" : nb,
            "navail" : nb
        }
        new_wish(temp)
    return {"message" : "Success"}
        

@app.get('/pendingfac')
def get_pending_fac():
    some_data = faculty.stream()
    data = []
    for doc in some_data:
        if doc.to_dict()["pref"] == []:
            data.append(doc)

    return data

@app.get('/filledfac')
def get_filled_fac():
    some_data = faculty.stream()
    data = []
    for doc in some_data:
        if len(doc.to_dict()["pref"]) > 0:
            data.append(doc)

    return data
    
