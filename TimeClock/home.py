from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')