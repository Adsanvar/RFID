from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response
import os


home = Blueprint('home', __name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    # data = request.args.get('data')
    # if data != None:
    #     if data == 'fromStopWrite':
    #         app.logger.info('Stopping From a Write Operation')
    #         window.load_url(base_url)
    #         readthread.resume()
    #         app.logger.info('Resuming ReadThread and Running it again')
    #         readthread.run()
    #     elif data == 'closeHours':
    #         app.logger.info('Loading base url from close hours')
    #         window.load_url(base_url)
    #         app.logger.info('Setting not_in_hours flag for reading')
    #         readthread.not_in_hours()
    #     return 'success'
    # else:
    #     # print("INDEX:")
    #     # print(loadFobs())
    #     # # tc = dbc.Timeclock(fobid=123, date=datetime.datetime.now(), clockin=datetime.datetime.now(), nolunch=False)
    #     # # dbc.createTimeclock(tc)
    #     # # print(dbc.getTimeclockRowById(123))
    #     return render_template('index.html')
    return render_template('index.html')