from flask import Flask, render_template, request, redirect, session, flash# import the class from friend.py
from flask_app.models.order import Order
from flask_app.models.user import User
from flask_app import app
from werkzeug.datastructures import ImmutableMultiDict
from datetime import *

import socket

methods_JSON=[{'method': 'Carry Out','price':0}, {'method': 'Delivery','price':10}]
size_JSON=[{'size': 'Small','price':10}, {'size': 'Medium','price':15}, {'size': 'Large','price':20}, {'size': 'X-Large','price':25}]
crust_JSON=[{'crust': 'Thin Crust','price':0}, {'crust': 'Hand Tossed','price':5}, {'crust': 'Stuffed crust','price':10}]
quantity_JSON=[{'qty': 1}, {'qty': 2}, {'qty': 3}, {'qty': 4}, {'qty': 5}]
toppings_JSON = [{'topping':'Pepperoni','price':1},{'topping':'Olives','price':1},{'topping':'Bacon','price':1},{'topping':'Peppers','price':1},{'topping':'Pineapple','price':1},{'topping':'Spinach','price':1},]

@app.route('/user/new_order')
def new_order():
    data = {
        'id':session['id']
    }
    user=User.get_by_id(data)
    return render_template("/user/craft_a_pizza.html", user=user,all_methods= methods_JSON, all_sizes=size_JSON, all_crust=crust_JSON, all_quantities=quantity_JSON,all_toppings=toppings_JSON)

@app.route('/user/favorite_order')
@app.route('/user/random_order')
def start_craft_a_pizza():
    return render_template("/user/craft_a_pizza.html")

@app.route('/user/send_order',methods=['POST'])
def send_order_details():
    
    session_data = request.form
    toppings_list = []
    for v in session_data.values():
        for t in toppings_JSON:
            if v == t['topping']:
                toppings_list.append(v)

    data = {
        'method':request.form['method'],
        'size':request.form['size'],
        'crust':request.form['crust'],
        'quantity':request.form['quantity'],
        'toppings': ", ".join(toppings_list),
        'number_of_toppings': len(toppings_list),
        'user_id': int(session['id'])
    }
    
    data['order_total'] = calcOrderTotal(data)
        
    session['user_session_orders'] = [data] + session['user_session_orders']
    
    session['user_session_grand_total'] = calcGrandTotal(session['user_session_orders'])
    
    #print("Now Printing the session data: ",session['user_session_orders'])
    
    return redirect("/user/order")

def calcOrderTotal(info):
    num_sum = 0
    
    for m in methods_JSON:
        print(m['method'], m['price'])
        if info['method'] == m['method']:
            num_sum += m['price']
            
    for s in size_JSON:
        print(s['size'], s['price'])
        if info['size'] == s['size']:
            num_sum += s['price']
            
    for c in crust_JSON:
        print(c['crust'], c['price'])
        if info['crust'] == c['crust']:
            num_sum += c['price']

    num_sum += info['number_of_toppings'] * 1

    num_sum += (num_sum * int(info['quantity']))

    return num_sum

def calcGrandTotal(info):
    num_sum = 0
    for i in info:
        #print(i['order_total'])
        num_sum += int(i['order_total'])
    return num_sum

def validate_order ( order ):
    is_valid = True

    if len(order['method']) < 1 or order['method'].isspace():
        flash("Method is blank","order")
        is_valid = False
            
    if len(order['size']) < 1 or order['size'].isspace():
        flash("Size is blank","order")
        is_valid = False

    if len(order['crust']) < 1 or order['crust'].isspace():
        flash("Crust is blank","order")
        is_valid = False
        
    if len(order['quantity']) < 1 or order['quantity'].isspace():
        flash("Quantity is less than 1","order")
        is_valid = False

    return is_valid