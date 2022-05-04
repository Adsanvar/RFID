from flask_login import UserMixin
from flask import flash
from sqlalchemy import and_

class Database:
    def __init__(self, db):
        self.db = db

#this is the model for the user table in the db
class User(UserMixin, self.self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    username = self.db.Column(self.db.String(45))
    password = self.db.Column(self.db.String(100))
    firstname = self.db.Column(self.db.String(45))
    lastname = self.db.Column(self.db.String(45))
    role = self.db.Column(self.db.String(45))
    
    def __repr__(self):
        return self.username

#events model
class Event(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    title = self.db.Column(self.db.String(100))
    start = self.db.Column(self.db.String(45))
    end = self.db.Column(self.db.String(45))
    className = self.db.Column(self.db.String(45))
    
    def __repr__(self):
        return self.title

class Timeclock(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    fobid = self.db.Column(self.db.String(45))
    date = self.db.Column(self.db.Date)
    clockin = self.db.Column(self.db.DateTime)
    clockout = self.db.Column(self.db.DateTime)
    nolunch = self.db.Column(self.db.Boolean(1))

class Device(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    serial = self.db.Column(self.db.String(100))

class Employee(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    firstname = self.db.Column(self.db.String(45))
    lastname = self.db.Column(self.db.String(45))
    fobid = self.db.Column(self.db.String(45))
    payrate = self.db.Column(self.db.Numeric(6,2))
    cash = self.db.Column(self.db.Boolean(1))
    employment_type = self.db.Column(self.db.String(45))

    def __repr__(self):
        return self.firstname + " " + self.lastname
    
class Payroll(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    employee_id = self.db.Column(self.db.Integer)
    start = self.db.Column(self.db.DateTime)
    end = self.db.Column(self.db.DateTime)
    total_hours = self.db.Column(self.db.Numeric(5,2))
    date = self.db.Column(self.db.DateTime)
    cash_hours = self.db.Column(self.db.Numeric(5,2))
    payroll_hours = self.db.Column(self.db.Numeric(5,2))
    cash_amount = self.db.Column(self.db.Numeric(7,2))
    total_hours_after_lunch = self.db.Column(self.db.Numeric(5,2))

class Fob(self.db.Model):
    id = self.db.Column(self.db.Integer, primary_key=True)
    fobid = self.db.Column(self.db.String(45))
    text = self.db.Column(self.db.String(45))
    employeeId = self.db.Column(self.db.Integer)

#user_query returns the first instance of username that is found by query 
def user_query(usr):
    try:
        return User.query.filter_by(username = usr).first()
    except:
        self.db.session.rollback()
        raise 

#get user by ID
def user_id_query(id):
    try:
        return User.query.get(int(id))
    except Exception as e:
        self.db.session.rollback()
        print(e)

def query_user_by_id(ref):
    try:
        return User.query.filter_by(id = ref).first()
    except:
        self.db.session.rollback()
        raise

#Query User By Email
def query_userByEmail(rEmail):
    try:
        return User.query.filter_by(email = rEmail).first()
    except:
        self.db.session.rollback()
        raise

#Create user call api - Adrian
def create_user(usr):
    try:
        self.db.session.add(usr)
        self.db.session.commit()
    except:
        flash('Error Adding User', 'error')
        self.db.session.rollback()
        raise

def delete_user(username):
    try:
        usr = user_query(username)
        self.db.session.delete(usr)
        self.db.session.commit()
    except:
        flash('Error Deleting User', 'error')
        self.db.session.rollback()
        raise

#change user password
def update_pass(usrname, password):
    try:
        usr = user_query(usrname)
        usr.password = password
        self.db.session.commit()
        flash('Password Successful Changed', 'success')
    except:
        self.db.session.rollback()
        raise

#update user role
def update_role(user, role):
    try:
        usr = user_query(user)
        usr.role = role
        self.db.session.commit()
        flash('Role Successful Changed', 'success')
    except:
        self.db.session.rollback()
        raise

# Gets all members
def get_members():
    try:
        return User.query.all()
    except:
        self.db.session.rollback()
        raise

# Creates an event
def createEvent(event):
    try:
        self.db.session.add(event)
        self.db.session.commit()
        return "success"
    except:
        flash('Error Adding Event', 'error')
        self.db.session.rollback()
        raise

#gets all events
def getEvents():
    try:
        return Event.query.all()
    except:
        self.db.session.rollback()
        raise

def getEventById(id):
    try:
        return Event.query.get(int(id))
    except:
        self.db.session.rollback()

# Updates events
def updateEvent(evnt):
    try:
        event = getEventById(evnt.id)
        event.title = evnt.title
        event.start = evnt.start
        event.end = evnt.end
        event.className = evnt.className
        self.db.session.commit()
        # flash('Event Successful Changed', 'success')
        return "success"
    except:
        flash('Error Changing Event', 'error')
        self.db.session.rollback()
        raise

def deleteEvent(id):
    try:
        evnt = getEventById(id)
        self.db.session.delete(evnt)
        self.db.session.commit()
        return "success"
    except:
        flash('Error Deleting Event', 'error')
        self.db.session.rollback()
        raise

def createDevice(serial):
    try:
        self.db.session.add(serial)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        return "error"

def getDevices():
    try:
        return Device.query.all()
    except:
        self.db.session.rollback()
        return "error"

def createTimeclock(tc):
    try:
        self.db.session.add(tc)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise

def createTimeclocks(tcs):
    try:
        for tc in tcs:
            self.db.session.add(tc)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise

def getTimeclockRow(date, fobid):
    try:    
        return Timeclock.query.filter_by(date = date, fobid=fobid).all()
    except:
        self.db.session.rollback()
        raise 

def getTimeclockRowById(id):
    try:
        return Timeclock.query.filter_by(id = id).first()
    except:
        self.db.session.rollback()
        raise

def updateTimeclockClockout(tc, clkout, nolunch):
    try:
        t = getTimeclockRowById(tc.id)
        t.clockout = clkout
        t.nolunch = nolunch
        self.db.session.commit()
        # flash('Event Successful Changed', 'success')
        return "success"
    except:
        # flash('Error Changing Event', 'error')
        self.db.session.rollback()
        raise    

def updateTimeclock(tcid, clkin, clkout, nolunch):
    try:
        t = getTimeclockRowById(tcid)
        if clkin != '':
            t.clockin = clkin
        if clkout != '':
            t.clockout = clkout
        if nolunch != t.nolunch:
            t.nolunch = nolunch

        self.db.session.commit()
        # flash('Event Successful Changed', 'success')
        return "success"
    except:
        # flash('Error Changing Event', 'error')
        self.db.session.rollback()
        raise    

def delete_Timeclock(tcid):
    try:
        tc = getTimeclockRowById(tcid)
        self.db.session.delete(tc)
        self.db.session.commit()
        return "success"
    except:
        flash('Error Deleting Event', 'error')
        self.db.session.rollback()
        raise   

def createPayroll(recs):
    try:
        for pr in recs:
            self.db.session.add(pr)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise
def searchFob(id):
    try:
        return Fob.query.filter_by(fobid = id).first()
    except:
        self.db.session.rollback()
        raise

def createFob(fob):
    try:
        self.db.session.add(fob)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise

# Gets all members
def getFobs():
    try:
        return Fob.query.all()
    except:
        self.db.session.rollback()
        raise

def create_employee(emp):
    try:
        self.db.session.add(emp)
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise

def deleteEmployee(id):
    try:
        emp = searchEmployee(id)
        self.db.session.delete(emp)
        self.db.session.commit()
        return "success"
    except:
        flash('Error Deleting Event', 'error')
        self.db.session.rollback()
        raise

#Gets empolyee's that have a non associated fobid
def getEmployeeForWrite():
    try:
        return Employee.query.filter_by(fobid = None).all()
    except:
        self.db.session.rollback()
        raise

# Gets all employees
def get_employees():
    try:
        return Employee.query.all()
    except:
        self.db.session.rollback()
        raise

def searchEmployee(emp_id):
    try:
        return Employee.query.filter_by(id = emp_id).first()
    except:
        self.db.session.rollback()
        raise

def updateEmployee(what, id, value):
    """
    Single Transcation
    what: which attribute you was to update ex: firstname, lastname
    id: employee row record
    value: the value of what you want to update
    """
    try:
        if what == "fobid":
                emp = Employee.query.filter_by(id = id).first()
                emp.fobid = value
                self.db.session.commit()
                return "success"
        elif what == "cash":
                emp = Employee.query.filter_by(id = id).first()
                emp.cash = value
                self.db.session.commit()
                return "success"
        elif what == "payrate":
                emp = Employee.query.filter_by(id = id).first()
                emp.payrate = value
                self.db.session.commit()
                return "success"
    except:
        self.db.session.rollback()
        raise

def update_employee_attributes(id, clear, payrate, cash, emp_type):
    """
    id: employee row record
    clear: clear the fobid?
    payrate: payrate
    cash: cash
    """
    try:
        emp = Employee.query.filter_by(id = id).first()
        emp.cash = cash
        emp.payrate = payrate
        emp.employment_type = emp_type
        if clear:
            emp.fobid = None
        self.db.session.commit()
        return "success"
    except:
        self.db.session.rollback()
        raise  
     
def get_hours():
    try:
        return Timeclock.query.all()
    except:
        self.db.session.rollback()
        raise

def get_hours_by_dates(d1, d2):
    try:
        # return Timeclock.query.filter(Timeclock.date <= d2).filter(Timeclock.date >= d1).all()
        return Timeclock.query.filter(Timeclock.date.between(d1, d2)).all()
    except:
        self.db.session.rollback()
        raise

def query_payroll_hours(d1, d2):
    try:
        return Timeclock.query.filter(Timeclock.date >= d1).filter(Timeclock.date <= d2).order_by(Timeclock.fobid).all()
    except:
        self.db.session.rollback()
        raise

def get_hours_by_dates_fobid(start, end, fobid):
    try:
        return Timeclock.query.filter(Timeclock.date >= start).filter(Timeclock.date <= end).filter(Timeclock.fobid == fobid).all()
    except:
        self.db.session.rollback()
        raise

def update_hours(list_of_ids, xhour):
    try:
        for i in list_of_ids:
            tc = Timeclock.query.filter_by(id = int(i)).first()
            dt = tc.clockin
            new_dt = dt.replace(hour=xhour, minute=0)
            tc.clockin = new_dt
        self.db.session.commit()
        return "success"
    except Exception as e:
        self.db.session.rollback()
        print(e)
        return "failed"
        