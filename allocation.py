"""
recieved all d
"""
courses = db.collection(u'courses')
faculty = db.collection(u'faculty')
wishes = db.collection(u'wishes')

def get_prof():
    profs = []
    docs = faculty.where(u'desig', u'==', u'Professor').stream()
    for doc in docs:
        profs.append(doc.to_dict())
    
    profs = sorted(profs, key = lambda d: d['emp_id'])
    return profs


def get_assoc_prof():
    profs = []
    docs = faculty.where(u'desig', u'==', u'Associate Professor').stream()
    for doc in docs:
        profs.append(doc.to_dict())

    profs = sorted(profs, key = lambda d: d['emp_id'])
    return profs

def get_assist_prof():
    profs = []
    docs = faculty.where(u'desig', u'==', u'Assistant Professor').stream()
    for doc in docs:
        profs.append(doc.to_dict())

    profs = sorted(profs, key = lambda d: d['emp_id'])
    return profs

