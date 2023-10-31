from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from . import db
import json
import csv
from sqlalchemy import or_

class Views:
    views = Blueprint('views', __name__)

    @views.route('/', methods=['GET', 'POST'])
    @login_required
    def home():
        return render_template("home.html", user=current_user)

    @views.route('/iniciar', methods=['GET', 'POST'])
    @login_required
    def iniciar():
        return render_template("separacao.html", user=current_user)

    @views.route('/precos', methods=['GET', 'POST'])
    @login_required
    def precos():
        return render_template("precos.html", user=current_user)

    @views.route('/separando', methods=['GET', 'POST'])
    @login_required
    def separando():
        return render_template("loading.html", user=current_user)
