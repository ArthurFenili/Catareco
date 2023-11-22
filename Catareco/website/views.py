from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from . import db
import json
import csv
from sqlalchemy import or_
from balanca import ler_valor_arduino, valor_arduino
import time
import serial
from .espe import Esp

class Views:
    views = Blueprint('views', __name__)

    my_esp = None  # Initialize my_esp to None

    @classmethod
    def get_esp_instance(cls):
        if cls.my_esp is None:
            cls.my_esp = Esp().e
        return cls.my_esp
    #porta_serial = serial.Serial('COM4', 9600, timeout=1)
    #time.sleep(2)



    @views.route('/', methods=['GET', 'POST'])
    @login_required
    def home():
        return render_template("home.html", user=current_user)

    @views.route('/iniciar', methods=['GET', 'POST'])
    @login_required
    def iniciar():
        return render_template("separacao.html", user=current_user)

    @views.route('/cotacao', methods=['GET', 'POST'])
    @login_required
    def cotacao():
        return render_template("cotacao.html", user=current_user)

    @views.route('/separando', methods=['GET', 'POST'])
    @login_required
    def separando():
        # Chama a função para ler os valores do Arduino
        porta_serial = serial.Serial('COM4', 9600, timeout=1)
       # my_esp_instance = Views.get_esp_instance()
        time.sleep(2)
        ler_valor_arduino(porta_serial)
        print("TEMPO")
        time.sleep(5)
        print("TEMPO")
        ler_valor_arduino(porta_serial)
        return render_template("loading.html", user=current_user)
