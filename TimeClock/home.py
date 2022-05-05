from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')