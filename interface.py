#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:20:53 2020

@author: planetmaker
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main_window():
    error = None
    if request.method == 'POST':
        if request.form['crafting_plan'] == 'ALLES':
            return
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)