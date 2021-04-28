from flask import Flask, request

app = Flask(__name__)

from app_module import routes