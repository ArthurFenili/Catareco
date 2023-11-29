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
from cam_yolo import CamYolo

class Views:
    views = Blueprint('views', __name__)

    peso = 0

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
        return render_template("loading.html", user=current_user)

    @views.route('/separado', methods=['GET', 'POST'])
    @login_required
    def separado():
        return render_template("separeted.html", user=current_user, weight = Views.peso)

    @views.route('/processando', methods=['GET', 'POST'])
    @login_required
    def processando():
        url = 'http://192.168.1.2/cam-hi.jpg'
        cam_yolo_instance = CamYolo(url)
        total_objects = cam_yolo_instance.call_detect()
        total_bottles = int(total_objects[0])
        total_cans = int(total_objects[1])
        print("TOTAL DE GARRAFAS: ", total_bottles)
        print("TOTAL DE LATINHAS: ", total_cans)
        # Chama a função para ler os valores do Arduino
        with serial.Serial('COM4', 9600, timeout=1) as porta_serial:
            peso = ler_valor_arduino(porta_serial, total_bottles, total_cans)
        peso = 0
        time.sleep(10)
        return render_template("separeted.html", user=current_user, weight = peso)

