from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response

home_page = Blueprint('home_page', __name__, template_folder='templates')

@home_page.route('/', methods=['GET'])
def index(): 
    # return render_template('index.html')
    return "HELLO"