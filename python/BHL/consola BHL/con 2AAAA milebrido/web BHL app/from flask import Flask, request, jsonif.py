from flask import Flask, request, jsonify
import math
import random
import requests
import os
import json
import time
#variables globales
app = Flask(__name__)
base = 1000
PosC2 = (base**3) #4000000
PosX = (base**2) * 2#400000
PosC1 =(base**2)#200000
PosY = base*2 #2000
PosC = base #1000
PosZ = 1

