from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for

#from gpiozero import LED
#from time import sleep

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')