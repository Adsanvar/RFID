from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response
import os
import numpy as np
from flask_login import login_user, logout_user, login_required, current_user
import Dashboard.database as database
from . import bcrypt
from Dashboard.cEvent import cEvent as cEvent
from Dashboard.Employee import Employee as Employee
from Dashboard.Fob import Fob as Fob
import json
# from weasyprint import HTML, CSS
from flask_weasyprint import HTML, render_pdf, CSS
import io
import PyPDF2
import datetime
import codecs
import csv
import datetime
from decimal import Decimal
from werkzeug.wsgi import FileWrapper
from pathlib import Path

home = Blueprint('home', __name__)

#This Route is the index page (landing page)
@home.route('/', methods=['GET'])
def index(): 
    return render_template('login.html')

@home.route('/Login', methods=['GET'])
def login():
    #code
    return render_template('login.html')

@home.route('/Dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if 'logout' in request.form:
        print("in logout")
        return redirect(url_for('auth.logout'))
    
    # if current_user.is_authenticated:
    user = current_user

    option = request.args.get('option')

    if 'member_delete' in request.form:
        usr = request.form.get('delete_user')
        database.delete_user(usr)
        flash('Member Successfully Deleted.', 'success')
        return redirect(url_for('home.dashboard'))
    
    if 'emp_delete' in request.form:
        print(request.form)
        emp = request.form.get('emp_delete') #id
        if database.deleteEmployee(emp) == "success":
            flash('Employee Successfully Deleted.', 'success')
        else:
            flash('Error Deleting Employee', 'errors')
        return redirect(url_for('home.dashboard', option='Settings', view='employees'))
    
    if 'fob_delete' in request.form:
        print(request.form)
        fob = request.form.get('fob_delete') #id
        if database.deleteFob(fob) == "success":
            flash(' Successfully Deleted Fob.', 'success')
        else:
            flash('Error Deleting Fob', 'errors')
        return redirect(url_for('home.dashboard', option='Settings', view='fobs'))

    if 'tc_delete' in request.form:
        tcid = request.form.get('tc_delete') #id
        if database.delete_Timeclock(tcid) == "success":
            flash('Timeclock Record Successfully Deleted.', 'success')
        else:
            flash('Error Deleting Timeclock Record', 'errors')
        return redirect(url_for('home.dashboard', option='Settings', view='hours'))

    if option == 'Settings':
        view = request.args.get('view')
        if view == 'employees':
            emps = database.get_employees()
            return render_template('dashboard.html', role=user.role, user=user.firstname, option=option, table_data=emps, events='None', view=view)
        elif view == 'fobs':
            fobs = database.getFobs()
            return render_template('dashboard.html', role=user.role, user=user.firstname, option=option, table_data=fobs, events='None', view=view)
        elif view == 'hours':
            table_data = None
            employees = database.get_employees()
            del employees[0]
            if request.args.get('getHours') == 'True':
                print(request.form)
                table_data = {}
                # start = datetime.datetime.strptime(request.form.get('start_date'), "%m/%d/%Y").strftime("%Y-%m-%d")
                # end = datetime.datetime.strptime(request.form.get('end_date'), "%m/%d/%Y").strftime("%Y-%m-%d")
                start = datetime.datetime.strptime(request.form.get('start_date'), "%m/%d/%Y")
                end = datetime.datetime.strptime(request.form.get('end_date'), "%m/%d/%Y")
                if start != '' and end != '':
                    if 'hour_dates' in request.form:
                        hours = database.get_hours_by_dates(start.date(), end.date())
                        table_data = hours
                        # print('in hours_dates')
                        # print(len(hours))
                        # for i in hours:
                        #     print(i.fobid, i.date)
                        #     for e in employees:
                        #         if i.fobid == e.fobid:
                        #             print(i.fobid, e.firstname, e.lastname)
                        #             if i.fobid not in [i for i in table_data]:
                        #                 table_data[i.fobid] = {}
                        #                 table_data[i.fobid][i.id] = {}
                        #                 table_data[i.fobid][i.id]['name'] = e.firstname + " " + e.lastname
                        #                 table_data[i.fobid][i.id]['date'] = i.date
                        #                 table_data[i.fobid][i.id]['clockin'] = i.clockin
                        #                 table_data[i.fobid][i.id]['clockout'] = i.clockout
                        #                 nolunch=""
                        #                 if i.nolunch:
                        #                     nolunch = 'Yes'
                        #                 else:
                        #                     nolunch = 'No'
                        #                 table_data[i.fobid][i.id]['nolunch'] = nolunch
                        #                 table_data[i.fobid][i.id]['id'] = i.id
                        #             else:
                        #                 table_data[i.fobid][i.id] = {}
                        #                 table_data[i.fobid][i.id]['name'] = e.firstname + " " + e.lastname
                        #                 table_data[i.fobid][i.id]['date'] = i.date
                        #                 table_data[i.fobid][i.id]['clockin'] = i.clockin
                        #                 table_data[i.fobid][i.id]['clockout'] = i.clockout
                        #                 nolunch=""
                        #                 if i.nolunch:
                        #                     nolunch = 'Yes'
                        #                 else:
                        #                     nolunch = 'No'
                        #                 table_data[i.fobid][i.id]['nolunch'] = nolunch
                        #                 table_data[i.fobid][i.id]['id'] = i.id  
                        #            break
                    elif 'emp_hours' in request.form:
                        merger = PyPDF2.PdfFileMerger()
                        for e in employees:
                            if e.firstname != 'Admin':
                                if e.fobid != None:
                                    objs = database.get_hours_by_dates_fobid(start, end, e.fobid)
                                    info = {}
                                    total = 0
                                    after_lunch = 0
                                    for i in range(len(objs)):
                                        print(e.firstname, e.lastname, objs[i].clockin, objs[i].clockout)
                                        info[i] = {}
                                        info[i]['date'] = objs[i].date
                                        if objs[i].clockin is None:
                                            info[i]['clk_in'] = '-'
                                        else:
                                            info[i]['clk_in'] = datetime.datetime.strptime(str(objs[i].clockin), '%Y-%m-%d %H:%M:%S').strftime("%I:%M %p")
                                        if objs[i].clockout is None:
                                            info[i]['clk_out'] = '-'
                                        else:
                                            info[i]['clk_out'] = datetime.datetime.strptime(str(objs[i].clockout), '%Y-%m-%d %H:%M:%S').strftime("%I:%M %p")
                                        
                                        if objs[i].clockin is None or objs[i].clockout is None:
                                            delta = 0
                                        else:
                                            delta = (objs[i].clockout - objs[i].clockin)
                                            info[i]['hours'] = datetime.datetime.strptime(str(delta), '%H:%M:%S').strftime('%H:%M')
                                            total += delta.total_seconds()
                                            if objs[i].nolunch:
                                                after_lunch += delta.total_seconds()
                                            else:
                                                after_lunch += (delta - datetime.timedelta(minutes=30)).total_seconds()
                                        
                                        nolunch = ''
                                        if objs[i].nolunch:
                                            nolunch = 'No'
                                        else:
                                            nolunch = 'Si'
                                        info[i]['no_lunch'] = nolunch

                                    name = e.firstname + ' ' + e.lastname
                                    total = np.round(total/3600, 2)
                                    after_lunch = np.round(after_lunch/3600, 2)
                                    html = render_template('hours.html', data=info, name=name, total=total, after_lunch=after_lunch)
                                    pdf = HTML(string=html).write_pdf(stylesheets=[CSS('/static/css/pdfprint.css')])
                                    output = io.BytesIO()
                                    with io.BytesIO(pdf) as open_pdf_file:
                                        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
                                        merger.append(read_pdf)

                        merger.write(output)
                        output.seek(0)
                        now = datetime.datetime.now()
                        fname = str(now.date())+".pdf"
                        w = FileWrapper(output)
                        return Response(w, direct_passthrough=True,content_type='application/pdf')
                        # return send_file(output, as_attachment=True, attachment_filename=fname) # to download file directly only works on dev not prod
            return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, table_data=table_data, employees=employees, events='None', view=view)
        elif view == 'payroll':
            ## This is the section for payroll request (internal), view routes for API Calls
            emps = database.get_employees()
            if request.args.get('getPayroll') == 'True':
                start = datetime.datetime.strptime(request.form.get('start_date'), "%m/%d/%Y").strftime("%Y-%m-%d")
                end = datetime.datetime.strptime(request.form.get('end_date'), "%m/%d/%Y").strftime("%Y-%m-%d")
                tc = {}
                hours = {}
                cash = {}
                salary = {}
                payroll_dates = {}
                if start != '' and end != '':
                    payroll_dates['payroll_dates'] = {"start": start, "end": end}
                    timeclock = database.query_payroll_hours(start, end)
                    for i in timeclock:
                        if i.clockout is None or i.clockin is None:
                            # print(f'{i.fobid}: Missing a value. In: {i.clockin} | Out: {i.clockout}')
                            name = ""
                            for j in emps:
                                if i.fobid == j.fobid:
                                    name = j.firstname + ' ' + j.lastname
                            flash("!!! Timeclock is missing a value for {} on {}".format(name, i.date), "error")
                            return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, show_table=False, events='None', view=view)
                        else:
                            delta = (i.clockout - i.clockin)
                            if i.fobid in tc:
                                tc[i.fobid]['total_hours'] = tc[i.fobid]['total_hours'] + delta.total_seconds()
                                if i.nolunch:
                                    tc[i.fobid]['hours'] = tc[i.fobid]['hours'] + delta.total_seconds()
                                else:
                                    tc[i.fobid]['hours'] = tc[i.fobid]['hours'] + (delta - datetime.timedelta(minutes=30)).total_seconds()
                            else:
                                tc[i.fobid] = {}
                                tc[i.fobid]['total_hours'] = delta.total_seconds()
                                if i.nolunch:
                                    tc[i.fobid]['hours'] = delta.total_seconds()
                                else:
                                    tc[i.fobid]['hours'] = (delta - datetime.timedelta(minutes=30)).total_seconds()
                            # if i.fobid in tc:
                            #     tc[i.fobid]['total_hours'] = tc[i.fobid]['total_hours'] + delta
                            #     if i.nolunch:
                            #         tc[i.fobid]['hours'] = tc[i.fobid]['hours'] + delta
                            #     else:
                            #         tc[i.fobid]['hours'] = tc[i.fobid]['hours'] + (delta - datetime.timedelta(minutes=30))
                            # else:
                            #     tc[i.fobid] = {}
                            #     tc[i.fobid]['total_hours'] = delta
                            #     if i.nolunch:
                            #         tc[i.fobid]['hours'] = delta
                            #     else:
                            #         tc[i.fobid]['hours'] = (delta - datetime.timedelta(minutes=30))
                    
                    # converts total seconds to hours. Note, that this is now a scale of 0-100 instead of 0-60 mintues
                    # 30 mintues == X.50
                    for t in tc:
                        # mm, ss = divmod(tc[i]['hours'].total_seconds(), 60)
                        # hh, mm = divmod(mm, 60)
                        # s = "%d:%02d:%02d" % (hh, mm, ss)         
                        # print(s)               
                        # print(tc[i]['hours'])
                        # days = tc[i]['hours'].days
                        # hr = tc[i]['hours'].seconds / 3600
                        # minutes = 5
                        # print(f'days: {days}, hours: {hr}, minutes: {minutes}')
                        for j in emps:
                            if t == j.fobid:
                                hours[j.id] = {}
                                hours[j.id]['hours'] = np.round(tc[t]['hours']/3600, 2)
                                hours[j.id]['total_hours'] = np.round(tc[t]['total_hours']/3600, 2)
                                hours[j.id]['employee'] = j.firstname + " " + j.lastname
                                if j.payrate is not None:
                                    rate = float('{:.2f}'.format(j.payrate))
                                else:
                                    rate = "-"
                                
                                hours[j.id]['rate'] = rate
                                if j.cash:
                                    cash[j.id] = hours[j.id]
                                break

                    # print(hours)
                    for i in cash:
                        #removes from regular employees dict
                        if i in hours:
                            del hours[i]
                        if cash[i]['rate'] != '-':
                            cash[i]['amount'] = np.round(cash[i]['hours']*cash[i]['rate'], 2)
                        else:
                            cash[i]['amount'] = '-'

                    for i in emps:
                        if i.employment_type == 'Salary':
                            salary[i.id] = {}
                            salary[i.id]['employee_name'] = i.firstname + ' ' + i.lastname
                            salary[i.id]['salary'] = str(i.payrate)
                            salary[i.id]['emp_type'] = i.employment_type
                    
                    # print(hours)
                    # print(cash)
                    # print(salary)
                    
                return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, show_table=True, employees= emps, events='None', view=view, hours=hours, cash=cash, salary=salary, payroll_dates=json.dumps(payroll_dates))

            return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, show_table=False, employees= emps, events='None', view=view)
        else:
            members_list = database.get_members()
            return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, table_data=members_list, events='None', view="users")

    if option == 'Calendar':
        return render_template('dashboard.html', role=user.role,  user=user.firstname, option=option, events=getEvents())
    
    print(get_todays_timeclock())
    return render_template('dashboard.html', role=user.role,  user=user.firstname, events='None')
    # else:
    #     return redirect(url_for('home.login'))

def get_todays_timeclock():
    dt = datetime.datetime.now()
    print("Processing CSV FILE - START: {} ".format(dt))
    data = {}
    try:
        with open(f'/home/pi/Documents/RFID/TimeClock/{dt.year}_TimeClock.csv', 'r') as f: 
            csv_reader = csv.DictReader(f)
            line_count = 0
            # No failed dates
            for row in csv_reader:
                #print(row)
                # print(dt.date())
                #print(row['date'])
                # yesterday = datetime.datetime.today() - datetime.timedelta(days=2)
                # print(d)
                # if row['date'] == f'{yesterday.date()}':
                if row['date'] == f'{dt.date()}':
                # if row['date'] in upload_dates:
                    data[line_count] = row['date'], row['name'], row['fobid'], row['in/out'], row['time'], row['nolunch']
                    # print(f"\t{row['date']}, {row['name']}, {row['fobid']}, {row['in/out']}, {row['time']}, {row['lunch']}")
                    # line_count += 1
                    line_count += 1
            # print(line_count)
            f.close()
        print(data)
    except Exception as e:
        print(e)
        raise

def getEvents():
    events = []
    for event in database.getEvents():
        ev = cEvent(id = event.id, title=event.title , className=event.className, start=event.start, end=event.end)
        events.append(ev)
    events = json.dumps(events, default=lambda x: x.__dict__)
    return events

@home.route('/getCalendarEvents', methods=['GET'])
@login_required
def getCalendarEvents():
    return getEvents()
    
@home.route('/dashboard/createEvent', methods=['POST'])
@login_required
def createEvent():
    title = request.form['title']
    start = request.form['start']
    end = request.form['end']
    className = request.form['className']
    event = database.Event(title=title, start=start, end=end, className=className)
    val = database.createEvent(event)
    # return redirect(url_for('home.dashboard', option='Calendar'))
    if val == "success":
        return val
    else:
        return "failed"

@home.route('/dashboard/updateEvent', methods=['POST'])
@login_required
def updateEvent():
    id = request.form['id']
    title = request.form['title']
    start = request.form['start']
    end = request.form['end']
    className = request.form['className']
    event = database.Event(id=id, title=title, start=start, end=end, className=className)
    # print(id, title, start, end, className)
    val = database.updateEvent(event)
    # return redirect(url_for('home.dashboard', option='Calendar'))
    if val == "success":
        return val
    else:
        return "failed"

@home.route("/dashboard/deleteEvent", methods=['POST'])
@login_required
def deleteEvent():
    id = request.form['id']
    val = database.deleteEvent(id)
    # return redirect(url_for('home.dashboard', option='Calendar'))
    if val == "success":
        return val
    else:
        return "failed"

@home.route("/printCalendar", methods=['GET'])
def printCalendar():
    result = ""
    cal = request.args.get("html")
    print(cal)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = ROOT_DIR+"/static/css/fullcalendar.css"
    pdf = HTML(string=cal).write_pdf(stylesheets=[CSS(path)])
    
    # output = io.BytesIO()
    # with io.BytesIO(pdf) as open_pdf_file:
    #     read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
    # output.seek(0)
    # print(output.read())
    return pdf

@home.route('/createMember', methods=['POST'])
@login_required
def createMember():
    print(request.form)
    if 'confirm_member' in request.form:
    #checks to see if any field is empty 
        if request.form.get('member_username') and request.form.get('member_password') and request.form.get('member_confirm_password') and request.form.get('member_firstname') and request.form.get('member_lastname'):
            #Non-empty
            uname = request.form.get('member_username')
            pas = request.form.get('member_password')
            con_pass = request.form.get('member_confirm_password')
            name = request.form.get('member_firstname')
            last = request.form.get('member_lastname')
            role = request.form.get('mem_role')
            return redirect(url_for('home.dashboard', option="Settings"))
        else:
            #empty
            flash('Member Was Not Added', 'error')
            return redirect(url_for('home.dashboard'))

@home.route('/dashboard/updateMember', methods=['POST'])
@login_required
def updateMember():
    if 'update_user' in request.form:
        username = request.form.get('username')
        pas = request.form.get('password')
        role = request.form.get('update_role')
    if pas:
        pasw = bcrypt.generate_password_hash(pas).decode('utf-8')
        database.update_pass(username, pasw)
        if role != 'Select':
            database.update_role(username, role)
        return redirect(url_for('home.dashboard', option='Settings'))
    elif pas == '' and role != 'Select':
        database.update_role(username, role)
        return redirect(url_for('home.dashboard', option='Settings'))
    else:
        flash('Member Was Not Updated', 'error')
        return redirect(url_for('home.dashboard', option='Settings'))

@home.route('/createEmployee', methods=['POST'])
@login_required
def createEmployee():
    #checks to see if any field is empty 
    if request.form.get('emp_fname') and request.form.get('emp_lname'):
        #Non-empty
        first = request.form.get('emp_fname')
        last = request.form.get('emp_lname')
        pay = request.form.get('emp_payrate')
        emp_type = request.form.get('emp_type')
        cash = False

        if request.form.get('emp_check') is not None:
            cash = True
        
        if pay == '':
            pay = None
        else:
            pay = float(pay)
        
        # print(f'first: {first}, last: {last}, pay: {pay}, cash: {cash}')
        # if first is not None and first != '':
        #     #obtaines user from database thru ORM
        emp = database.Employee(firstname=first, lastname=last, payrate = pay, cash = cash, employment_type=emp_type)
        if database.create_employee(emp) == 'success':
            flash('Your new Employee has been created!', 'success')
            return redirect(url_for('home.dashboard', option='Settings', view='employees'))
        else:
            flash('Employee Was Not Added', 'error')
            return redirect(url_for('home.dashboard', option='Settings', view='employees'))
    else:
        #empty
        flash('Employee Was Not Added', 'error')
        return redirect(url_for('home.dashboard', option='Settings', view='employees'))

@home.route('/updateEmployee', methods=['POST'])
@login_required
def updateEmployee():
    #checks to see if any field is empty 
    if request.form.get('update_emp'):
        #Non-empty
        pay = request.form.get('edit_emp_payrate')
        cash = False
        clear = False
        emp_type = request.form.get('emp_type')
        emp_id = request.form.get('update_emp')

        if request.form.get('edit_emp_check') is not None:
            cash = True

        if request.form.get('clear_fobid') is not None:
            clear = True

        if pay == '':
            pay = None
        else:
            pay = float(pay)
        
        # print(f'pay: {pay}, cash: {cash}, clear: {clear}')

        if database.update_employee_attributes(emp_id, clear, pay, cash, emp_type) == 'success':
            flash('Your new Employee has been updated!', 'success')
            return redirect(url_for('home.dashboard', option='Settings', view='employees'))
        else:
            flash('Employee Was Not Added', 'error')
        return redirect(url_for('home.dashboard', option='Settings', view='employees'))
    else:
        #empty
        flash('Employee Was Not Added', 'error')
        return redirect(url_for('home.dashboard', option='Settings', view='employees'))

@home.route('/createTimeclock', methods=['POST'])
@login_required
def createTimeclock():
    print(request.form)
    if request.form.get('confirm_timeclock'):
        clk_in = request.form.get('clk_in')
        clk_out = request.form.get('clk_out')
        emp = request.form.get('emp')
        clk_date = request.form.get('clk_date')
        no_lunch = request.form.get('no_lunch')

        if emp == 'default':
            flash("Please Select Value Other than Index Value", "error")
            return redirect(url_for('home.dashboard', option='Settings', view='hours'))
        else:
            if no_lunch is not None:
                no_lunch = True
            else:
                no_lunch = False

            dt_in = clk_date + " " + clk_in
            dt_out = clk_date + " " + clk_out
            clkin = datetime.datetime.strptime(dt_in, "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
            clkout = datetime.datetime.strptime(dt_out, "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
            clk_date = datetime.datetime.strptime(clk_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            emp = database.searchEmployee(emp)

            tc = database.Timeclock(fobid = emp.fobid, date=clk_date, clockin= clkin, clockout= clkout, nolunch=no_lunch)
            if database.createTimeclock(tc) == "success":
                flash("Successfully created Timeslot", "success")
                return redirect(url_for('home.dashboard', option='Settings', view='hours'))
            else:
                flash("Error creating Timeslot", "error")
                return redirect(url_for('home.dashboard', option='Settings', view='hours'))

    else:
        #empty
        flash('Timeslot Was Not Added', 'error')
        return redirect(url_for('home.dashboard', option='Settings', view='hours'))

@home.route('/updateHours', methods=['POST'])
@login_required
def updateHours():
    print(request.form)
    #checks to see if any field is empty 
    if request.form.get('update_timeclock'):
        #Non-empty
        clk_in_date = request.form.get('clk_in_date')
        clk_in_time = request.form.get('clk_in_time')
        clk_out_date = request.form.get('clk_out_date')
        clk_out_time = request.form.get('clk_out_time')
        tcid = request.form.get('update_timeclock')
        nolunch = request.form.get('nolunch_cbx')

        if nolunch is not None:
            nolunch = True
        else:
            nolunch = False

        try:
            clkin = ''
            clkout = ''

            if clk_in_date != '' and clk_in_time != '':
                if '-' in clk_in_date and 'M' not in clk_in_time:
                    clkin = clk_in_date + " " + clk_in_time
                elif '-' in clk_in_date and 'M' in clk_in_time:
                    dt = clk_in_date + ' ' +clk_in_time
                    clkin = datetime.datetime.strptime(dt, "%Y-%m-%d %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
                elif '/' in clk_in_date and 'M' in clk_in_time:
                    dt_out = clk_in_date + " " + clk_in_time
                    clkin = datetime.datetime.strptime(dt_out, "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
                elif '/' in clk_in_date and 'M' not in clk_in_time:
                    dt = clk_in_date + ' ' +clk_in_time
                    clkin = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                else:                 
                    flash("There has been an issue with your timeclock dates and times. Please retry.", 'error')
            if clk_out_date != '' and clk_out_time != '':
                if '-' in clk_out_date and 'M' not in clk_out_time:
                    clkout = clk_out_date + " " + clk_out_time
                elif '-' in clk_out_date and 'M' in clk_out_time:
                    dt = clk_out_date + ' ' + clk_out_time
                    clkout = datetime.datetime.strptime(dt, "%Y-%m-%d %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
                elif '/' in clk_out_date and 'M' in clk_out_time:
                    dt_out = clk_out_date + " " + clk_out_time
                    clkout = datetime.datetime.strptime(dt_out, "%m/%d/%Y %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
                elif '/' in clk_out_date and 'M' not in clk_out_time:
                    dt = clk_out_date + ' ' + clk_out_time
                    clkout = datetime.datetime.strptime(dt, "%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                else:                 
                    flash("There has been an issue with your timeclock dates and times. Please retry.", 'error')

            # print(tcid, clkin, clkout, nolunch)
            if database.updateTimeclock(tcid, clkin, clkout, nolunch) == 'success':
                flash("Timeclock has been updated successfully", 'success')
            else:
                flash("There has been as issue updating the timeclock, please try again", 'error')

            return redirect(url_for('home.dashboard', option='Settings', view='hours'))

        except Exception as e:
            flash('Oops, Seems like something went wrong with the date format. Please Try Again.', 'error')
            raise
            return redirect(url_for('home.dashboard', option='Settings', view='hours'))

        return redirect(url_for('home.dashboard', option='Settings', view='hours'))
    else:
        #empty
        flash('Employee Was Not Added', 'error')
        return redirect(url_for('home.dashboard', option='Settings', view='hours'))

@home.route('/processPayroll', methods=['POST'])
@login_required
def processPayroll():
    print(request.form)
    dic = request.form
    payroll = {}
    cash = {}
    reg_cash = {}
    dates = json.loads(request.form.get('payroll_dates'))
    start = dates['payroll_dates']['start']
    end = dates['payroll_dates']['end']
    now = datetime.datetime.now()
    for i in request.form:
        if 'Hourly' in i:
            # print(dic[i])
            vals = dic[i].split(',')
            payroll[vals[0]] = {}
            payroll[vals[0]]['id'] = vals[0]
            payroll[vals[0]]['start'] = start
            payroll[vals[0]]['end'] = end
            payroll[vals[0]]['total_hours'] = vals[2]
            payroll[vals[0]]['date'] = str(now.date())
            payroll[vals[0]]['name'] = vals[1]
            payroll[vals[0]]['cash_hours'] = vals[5]
            payroll[vals[0]]['payroll_hours'] = vals[4]
            payroll[vals[0]]['cash_amount'] = vals[6]
            payroll[vals[0]]['total_hours_after_lunch'] = vals[3]
            if float(vals[5]) > 0:
                reg_cash[vals[0]] = {}
                reg_cash[vals[0]]['name'] = vals[1]
                reg_cash[vals[0]]['cash_hours'] = vals[5]
                reg_cash[vals[0]]['cash_amount'] = vals[6]
        elif 'Salary' in i:
            # print(dic[i])
            vals = dic[i].split(',')
            payroll[vals[0]] = {}
            payroll[vals[0]]['name'] = vals[1]
            payroll[vals[0]]['id'] = vals[0]
            payroll[vals[0]]['start'] = start
            payroll[vals[0]]['end'] = end
            payroll[vals[0]]['total_hours'] = 80
            payroll[vals[0]]['date'] = str(now.date())
            payroll[vals[0]]['cash_hours'] = 0
            payroll[vals[0]]['payroll_hours'] = 'Salary'
            payroll[vals[0]]['cash_amount'] = 0
            payroll[vals[0]]['total_hours_after_lunch'] = 80
        elif 'Cash' in i:
            # print(dic[i])
            vals = dic[i].split(',')
            cash[vals[0]] = {}
            cash[vals[0]]['name'] = vals[1]
            cash[vals[0]]['id'] = vals[0]
            cash[vals[0]]['start'] = start
            cash[vals[0]]['end'] = end
            cash[vals[0]]['total_hours'] = vals[2]
            cash[vals[0]]['date'] = str(now.date())
            cash[vals[0]]['cash_hours'] = vals[3]
            cash[vals[0]]['payroll_hours'] = 0
            cash[vals[0]]['cash_amount'] = vals[4]
            cash[vals[0]]['total_hours_after_lunch'] = vals[3]
            
    # print(payroll)
    # print(cash)
    payroll_recs = []
    # employeeId = db.Column(db.Integer)
    # start = db.Column(db.DateTime)
    # end = db.Column(db.DateTime)
    # total_hours = db.Column(db.Numeric(5,2))
    # date = db.Column(db.DateTime)
    # cash_hours = db.Column(db.Numeric(5,2))
    # payroll_hours = db.Column(db.Numeric(5,2))
    # cash_amount = db.Column(db.Numeric(7,2))
    # total_hours_after_lunch = db.Column(db.Numeric(5,2))
    for i in payroll:
        if payroll[i]['payroll_hours'] == 'Salary':
            pr = database.Payroll(employee_id=int(payroll[i]['id']), start=datetime.datetime.strptime(payroll[i]['start'], "%Y-%M-%d").date(),end=datetime.datetime.strptime(payroll[i]['end'], "%Y-%M-%d").date(), total_hours=float(payroll[i]['total_hours']), date=now.date(), cash_hours=float(payroll[i]['cash_hours']), payroll_hours=80.0, cash_amount=float(payroll[i]['cash_amount']), total_hours_after_lunch=float(payroll[i]['total_hours_after_lunch']))
        else:
            pr = database.Payroll(employee_id=int(payroll[i]['id']), start=datetime.datetime.strptime(payroll[i]['start'], "%Y-%M-%d").date(),end=datetime.datetime.strptime(payroll[i]['end'], "%Y-%M-%d").date(), total_hours=float(payroll[i]['total_hours']), date=now.date(), cash_hours=float(payroll[i]['cash_hours']), payroll_hours=float(payroll[i]['payroll_hours']), cash_amount=float(payroll[i]['cash_amount']), total_hours_after_lunch=float(payroll[i]['total_hours_after_lunch']))
        payroll_recs.append(pr)
        # print(pr.employeeId, pr.start,pr.end, pr.total_hours, pr.payroll_hours)
    
    for i in cash:
        pr = database.Payroll(employee_id=int(cash[i]['id']), start=datetime.datetime.strptime(cash[i]['start'], "%Y-%M-%d").date(),end=datetime.datetime.strptime(cash[i]['end'], "%Y-%M-%d").date(), total_hours=float(cash[i]['total_hours']), date=now.date(), cash_hours=float(cash[i]['cash_hours']), payroll_hours=float(cash[i]['payroll_hours']), cash_amount=float(cash[i]['cash_amount']), total_hours_after_lunch=float(cash[i]['total_hours_after_lunch']))
        payroll_recs.append(pr)
        

    res = database.createPayroll(payroll_recs)

    print(res)
    cash.update(reg_cash)
    # print(cash)

    # print(request.path)
    # print(url_for('getPayrollPdf', payroll=payroll, cash=cash))
    # base = request.url[:-15]
    # url = base+url_for('home.getPayrollPdf', payroll=json.dumps(payroll), cash=json.dumps(cash), fname=str(now.date())+".pdf")
    # print(url)
    # webbrowser.open(url)
    
    date = now.date()
    print(payroll)
    print(payroll.items())
    # sorted_p = sorted(payroll.items(), key=lambda item: item[1])
    sorted_p = sorted(payroll, key=lambda x: (payroll[x]['name']))
    payroll_sorted = {}
    for i in sorted_p:
        payroll_sorted[i] =payroll[i]
    merger = PyPDF2.PdfFileMerger()
    html = render_template('payroll.html', data=payroll_sorted,date=date, start=start, end=end)
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS('/static/css/pdfprint.css')])
    output = io.BytesIO()
    with io.BytesIO(pdf) as open_pdf_file:
        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
        merger.append(read_pdf)
    
    html = render_template('cash_payroll.html', data=cash,date=date, start=start, end=end)
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS('/static/css/pdfprint.css')])
    output = io.BytesIO()
    with io.BytesIO(pdf) as open_pdf_file:
        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
        merger.append(read_pdf)

    merger.write(output)
    output.seek(0)
    now = datetime.datetime.now()
    fname = str(now.date())+".pdf"
    w = FileWrapper(output)
    return Response(w, direct_passthrough=True,content_type='application/pdf')
    
    # return redirect(url_for('home.dashboard', option="Settings", view="payroll"))
@home.route('/getPayrollPdf/<string:payroll>/<string:cash>/<string:fname>', methods=['GET'])
@login_required
def getPayrollPdf(payroll, cash, fname):
    payroll = json.loads(payroll)
    cash = json.loads(cash)
    date = payroll[list(payroll.keys())[0]]['date']
    start = payroll[list(payroll.keys())[0]]['start']
    end = payroll[list(payroll.keys())[0]]['end']
    print(date)
    merger = PyPDF2.PdfFileMerger()
    html = render_template('payroll.html', data=payroll, date=date, start=start, end=end)
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS('/static/css/pdfprint.css')])
    output = io.BytesIO()
    with io.BytesIO(pdf) as open_pdf_file:
        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
        merger.append(read_pdf)
    
    html = render_template('cash_payroll.html', data=cash, date=date, start=start, end=end)
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS('/static/css/pdfprint.css')])
    output = io.BytesIO()
    with io.BytesIO(pdf) as open_pdf_file:
        read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
        merger.append(read_pdf)

    merger.write(output)
    output.seek(0)
    now = datetime.datetime.now()
    # fname = str(now.date())+".pdf"
    w = FileWrapper(output)
    return Response(w, direct_passthrough=True,content_type='application/pdf')


# Validats if device is registered to system
def validateDevice(dev):
    try:
        devices = database.getDevices()
        if devices != 'error':
            if bcrypt.check_password_hash(devices[0].serial, dev):
                return True
            else:
                return False
        else:
            return False
    except:
        return False

#validates fob 
@home.route('/validateFob', methods=['GET'])
def validateFob():
    data = request.data
    if data != None:
        data = json.loads(data)
        if validateDevice(codecs.decode(data['device'], 'rot_13')):
            obj = database.searchFob(data['id'])
            if obj is not None:
                if obj.text == data['text']:
                    return jsonify(message=True)
                else:
                    return jsonify(message=False)
            else:
                return jsonify(message=False)
        else:
            return jsonify(message=False)
    else:
        return jsonify(message='Error No Data')

# API CALL
@home.route('/getFobs', methods=['GET'])
def getFobs():
    try:
        # gets all the fobs in the system, gets called upon client initialization.
        data = request.data
        if data != None:
            data = json.loads(data)
            if validateDevice(codecs.decode(data['device'], 'rot_13')):
                objs = database.getFobs()
                if objs is not None:
                    
                    fobs= []
                    for o in objs:
                        fo = Fob(o.id, o.fobid, o.text, o.employeeId)
                        fobs.append(fo)

                    fobs = json.dumps(fobs, default=lambda x: x.__dict__)
            
                    return fobs
                else:
                    return jsonify(message=False)            
            else:
                return jsonify(message=False)
        else:
            return jsonify(message=False)
    except Exception as e:
        print(e)
        return jsonify(message=False)

#API Call
@home.route('/getHours', methods=['GET'])
def getHours():
    # Gets the employees hours upon request
    data = request.data
    if data != None:
        data = json.loads(data)
        if validateDevice(codecs.decode(data['device'], 'rot_13')):
            try:
                now = datetime.datetime.now()
                before = now - datetime.timedelta(weeks=4)
                start = before.date()
                end = now.date()
                objs = database.get_hours_by_dates_fobid(start, end, data['fobid'])
                hours = {}
                
                for i in range(len(objs)):
                    hours[i] = {}
                    hours[i]['date'] = str(objs[i].date)
                    hours[i]['clock_in'] = objs[i].clockin
                    hours[i]['clock_out'] = objs[i].clockout
                    hours[i]['no_lunch'] = objs[i].nolunch
                    if objs[i].clockout is None or objs[i].clockin is None:
                        hours[i]['hours'] = '-'
                    else:
                        hours[i]['hours'] = str(objs[i].clockout - objs[i].clockin)

                return jsonify(hours)
            except Exception as e:
                print(e)

        else:
            return jsonify(message="server error")
    else:
        return jsonify(message=False)  

# API CALL
@home.route('/getWrite', methods=['GET'])
def getWrite():
    # get's all the employees with out an associated Fob ID and returns them to Client
    data = request.data
    if data != None:
        data = json.loads(data)
        #validate device
        if validateDevice(codecs.decode(data['device'], 'rot_13')):
            obj = database.searchFobWrite(data['id'])
            #validate key
            if obj is not None:
                if obj.text == data['text']:
                    objs = database.getEmployeeForWrite()
                    if objs is not None:
                        
                        emps = []
                        for o in objs:
                            em = Employee(o.id, o.firstname, o.lastname, o.fobid, str(o.payrate), o.cash)
                            emps.append(em)

                        emps = json.dumps(emps, default=lambda x: x.__dict__)
                
                        return emps
                    else:
                        print('none objs')
                        return jsonify(message="error")
                else:
                    return jsonify(message="error")
            else:
                return jsonify(message="error")
        else:
            return jsonify(message="error")
    else:
        return jsonify(message='Error No Data')

# API CALL
@home.route('/writeFob', methods=['GET'])
def writeFob():
    #writes the keyfob to the database
    data = request.data
    if data != None:
        data = json.loads(data)
        #validate device
        if validateDevice(codecs.decode(data['device'], 'rot_13')):
            emp = database.searchEmployee(data['employeeId'])
            #validate key
            if emp is not None:
                if database.updateEmployee('fobid', emp.id, data['id']) == 'success':
                    fob = database.Fob(fobid = data['id'], text = data['text'], employeeId = emp.id)
                    if database.createFob(fob) == 'success':
                        return jsonify(message="success")
                    else:
                        return jsonify(message="error")
                else:
                    return jsonify(message="error")
            else:
                return jsonify(message="error")
        else:
            return jsonify(message="error")
    else:
        return jsonify(message='Error No Data')

@home.route('/processCsv', methods=['GET'])
def processCsv():
    """
    NOTE: clockin and clockout's can occur twice each. Having a max of 2 records in the timeclock per day.
    This method is called from Client at 11pm every day
    """
    data = request.data
    if data != None:
        data = json.loads(data)
        # print(data)
        #validate device
        if validateDevice(codecs.decode(data['device'], 'rot_13')):
            del data['device']
            if len(data) != 0:
                p = Path(__file__).parents[2]
                dt = datetime.datetime.now()
                p_str ='{}/{}_TimeClock.csv'.format(p, dt.year)
                with open(p_str, 'a+') as f:
                    record = csv.writer(f, delimiter=',')
                    # header = ['date', 'name','fobid', 'in/out','time', 'lunch']
                    # record.writerow(header)
                    for i in data:
                        row = data[i]
                        record.writerow(row)
                    f.close()
                
                tcs = []
                for i in data:
                    print(data[i])
                    nolunch = False
                    if data[i][5].lower() == 'true':
                        nolunch = True
                    else:
                        nolunch = False
                    print("No Lunch: ", nolunch)
                    if data[i][3] == 'in':
                        print("clock in")
                        # case: new record
                        if data[i][2] not in [j.fobid for j in tcs]:
                            print("adding New record")
                            clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)
                            tcs.append(clkin)
                        else: # record exists
                            print("record exists")
                            values = np.array([j.fobid for j in tcs])
                            indexes = np.where(values == data[i][2])
                            if len(indexes[0]) == 1:
                                print('Length of indeces is 1')
                                # use '%S.%f' for microseconds
                            
                                print(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout)
                                if tcs[indexes[0][0]].clockin != None and tcs[indexes[0][0]].clockout == None: #clocked in but forgot to clockout or clocked in multiple times
                                    intime = datetime.datetime.strptime(data[i][4], '%Y-%m-%d %H:%M:%S')
                                    pretime = datetime.datetime.strptime(str(tcs[indexes[0][0]].clockin), '%Y-%m-%d %H:%M:%S')
                                    print('Incoming Clockin Time: {}, Stored Clockin Time: {}'.format(intime, pretime))
                                    print('{} != None and {} == None'.format(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout))
                                    delta = intime - pretime
                                    print("delta: {}".format( delta))
                                    if delta > datetime.timedelta(minutes=14): #if time delta is greater than 14 minutes create a new record
                                        print('{} > {}'.format(delta, datetime.timedelta(minutes=14) ))
                                        print("creating clockin record because incoming record has a higher value 14 minutes")
                                        clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)
                                        tcs.append(clkin)
                                elif tcs[indexes[0][0]].clockin == None and tcs[indexes[0][0]].clockout != None: #forgot to clock in but clocked out for lunch
                                    print('{} == None and {} != None'.format(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout))
                                    clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)
                                    tcs.append(clkin)
                                elif tcs[indexes[0][0]].clockin != None and tcs[indexes[0][0]].clockout != None:
                                    print('{} != None and {} != None'.format(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout))
                                    clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)
                                    tcs.append(clkin)
                    elif data[i][3] == 'out':
                        print("out")
                        # case: new case - forgot to clockin
                        if data[i][2] not in [j.fobid for j in tcs]:
                            print('new record')
                            clkout = database.Timeclock(fobid = data[i][2], date=data[i][0], clockout= data[i][4], nolunch=nolunch)
                            tcs.append(clkout)
                        else:
                            print("record exists")
                            # index = [i.fobid for i in tcs].index(data[i][2]) # find
                            values = np.array([j.fobid for j in tcs])
                            # print(values)
                            indexes = np.where(values == data[i][2])
                            print(len(indexes[0]))
                            if len(indexes[0]) == 1:
                                print('One in the list')
                                if tcs[indexes[0][0]].clockout is None:
                                    print('clockout is None, updating object value')
                                    tcs[indexes[0][0]].clockout = data[i][4]
                                    tcs[indexes[0][0]].nolunch = nolunch
                                elif tcs[indexes[0][0]].clockout is not None:
                                    print('clockout is not None, creating new object')
                                    clkout = database.Timeclock(fobid = data[i][2], date=data[i][0], clockout= data[i][4], nolunch=nolunch)
                                    tcs.append(clkout)
                            elif len(indexes[0]) == 2:
                                print('Two in the list')
                                print(indexes[0])
                                if tcs[indexes[0][1]].clockin is not None:
                                    print('{} is not None'.format(tcs[indexes[0][1]].clockin))
                                    # tcs[indexes[0][1]].clockout = data[i][4]
                                    #compare the second clock in and the comming in clockout, this is to check 
                                    intime = datetime.datetime.strptime(data[i][4], '%Y-%m-%d %H:%M:%S')
                                    pretime = datetime.datetime.strptime(str(tcs[indexes[0][1]].clockin), '%Y-%m-%d %H:%M:%S')
                                    delta = intime - pretime
                                    print('{}'.format(delta))
                                    if delta < datetime.timedelta(minutes=14):
                                        print('{} < {}'.format(delta,datetime.timedelta(minutes=14) ))
                                        if tcs[indexes[0][0]].clockin != None and tcs[indexes[0][0]].clockout == None:
                                            print('{} != None and {} == None'.format(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout ))
                                            tcs[indexes[0][0]].clockout = data[i][4]
                                            tcs[indexes[0][0]].nolunch = nolunch
                                            print("DELETE THIS!!!!", tcs[indexes[0][1]].clockin, " AT: ", indexes[0][1])
                                            print('LENGTH BEFORE: ', len(tcs))
                                            del tcs[indexes[0][1]]
                                            print('LENGTH AFTER: ', len(tcs))
                                        else:
                                            print('NOT: {} != None and {} == None'.format(tcs[indexes[0][0]].clockin, tcs[indexes[0][0]].clockout ))
                                            tcs[indexes[0][1]].clockout = data[i][4]
                                            tcs[indexes[0][1]].nolunch = nolunch
                                    else:
                                        print('{} > {}'.format(delta, datetime.timedelta(minutes=14)))
                                        tcs[indexes[0][1]].clockout = data[i][4]
                                        tcs[indexes[0][1]].nolunch = nolunch
                    
                # print('LENGTH AFTER PROCESSING: ', len(tcs))
                res = database.createTimeclocks(tcs)
                print(res)

                # if res == "success":
                #     print("done")
                # emps = database.get_employees()
                # for t in tcs:
                #     for e in emps:
                #         if t.fobid == e.fobid:
                #             print(f'{e.firstname} {e.lastname}\nIN: {t.clockin}\tOUT: {t.clockout}')

                    # Original stuff
                    # if data[i][3] == 'in':
                    #     objs = database.getTimeclockRow(data[i][0], data[i][2])
                    #     print("In clockin objs: ")
                    #     # # First time
                    #     if len(objs) == 0:
                    #         # print("Objs == None")
                    #         clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)                            
                    #         res = database.createTimeclock(clkin)                            
                    #         if res == 'success':
                    #             print('success first time, when len of objs == 0')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")
                    #     # When user has one already one record, create a new record.
                    #     elif len(objs) == 1:
                    #         # print("Objs == 1")
                    #         clkin = database.Timeclock(fobid = data[i][2], date=data[i][0], clockin= data[i][4], nolunch=nolunch)
                    #         res = database.createTimeclock(clkin)
                    #         if res == 'success':
                    #             print('success when user already has one record')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")
                    # elif data[i][3] == 'out':
                    #     objs = database.getTimeclockRow(data[i][0], data[i][2])
                    #     print("In clockout objs: ")
                    #     # When user does not clock in
                    #     if len(objs) == 0:
                    #         # print("Objs == None")
                    #         clkout = database.Timeclock(fobid = data[i][2], date=data[i][0], clockout= data[i][4], nolunch=nolunch)
                    #         res = database.createTimeclock(clkout)
                    #         if res == 'success':
                    #             print('success in creating a clock out when user does not have a clock in')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")
                    #     # normal condition
                    #     elif len(objs) == 1 and objs[0].clockin != None and objs[0].clockout == None:
                    #         # print("objs ==1 and clockin in assigned and clockout is empty")
                    #         res = database.updateTimeclockClockout(objs[0], data[i][4], nolunch)
                    #         if res == 'success':
                    #             print('success, when user has 1 record, clock in of first object != None, and clockout of obj == None')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")
                    #     # when previous record was a time out
                    #     elif len(objs) == 1 and objs[0].clockout != None:
                    #         # print("objs == 1 and and clockout is empty")
                    #         clkout = database.Timeclock(fobid = data[i][2], date=data[i][0], clockout= data[i][4], nolunch=nolunch)
                    #         res = database.createTimeclock(clkout)
                    #         if res == 'success':
                    #             print('success, when there is a previous record and the objs clockout != None')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")
                    #     # when there are two records and need to update the last clockout
                    #     elif len(objs) == 2 and objs[1].clockin != None and objs[1].clockout == None:
                    #         # print("objs == 2 and clockin in assigned and clockout is empty")
                    #         res = database.updateTimeclockClockout(objs[1], data[i][4], nolunch)
                    #         if res == 'success':
                    #             print('success, when there are 2 records and the second objs clock in != None and clockout == None')
                    #             continue
                    #         else:
                    #             return jsonify(message="error - loading csv")       
                return jsonify(message="success")
            return jsonify(message="empty")
        else:
            return jsonify(message="error")
    else:
        return jsonify(message='Error No Data')

@home.route('/change_hours', methods=['POST'])
@login_required
def change_hours():
    print("called")
    data = request.form
    data = data.to_dict(flat=False)

    if 'selected[]' in data:
        # print(type(data['hour']), type(data['hour'][0]))
        res = database.update_hours(data['selected[]'], int(data['hour'][0]))
        flash(res, 'success' )
    else:
        res = "No Time Slots To Update"
        flash(res , 'error' )
    # return redirect(url_for('home.dashboard', option='Settings', view='hours'))
    return res