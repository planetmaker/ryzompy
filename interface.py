#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:20:53 2020

@author: planetmaker
"""

from flask import Flask, render_template, request

app = Flask(__name__)

plan = None
planning = None

@app.route('/', methods=['POST', 'GET'])
def main_window():
    plans = ['eins', 'zwei', 'drei', 'vier']
    plan = None
    if request.method == 'POST' and 'plan' in request.form:
        plan = request.form.get("plan")

    return render_template('home.html',  plan=plan, plans=plans)

if __name__ == '__main__':
    app.run(debug=True)