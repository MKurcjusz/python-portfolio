# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m7kkyTXCPmFOndHBoC0uKpwaXk5tlyAm
"""

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk":0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}


resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

coffee_choice = ""
profit = 0
machine_on = True

def coffee_preparation():

    def resources_check():
        water = resources["water"] - MENU[coffee_choice]["ingredients"]["water"]
        resources["water"] = water
        milk = resources["milk"] - MENU[coffee_choice]["ingredients"]["milk"]
        resources["milk"] = milk
        coffee = resources["coffee"] - MENU[coffee_choice]["ingredients"]["coffee"]
        resources["coffee"] = coffee
        if water < 0 or milk < 0 or coffee < 0:
            print("There is not enough resources.")
            global machine_on
            machine_on = False
            exit()

    def money_profit():
        print("Please insert coins.")
        exchange = -1
        while exchange < 0:
            quarters = int(input("how many quarters?: "))
            dimes = int(input("how many dimes?: "))
            nickles = int(input("how many nickles?: "))
            pennies = int(input("how many pennies?: "))
            sum = 0.25 * quarters + 0.1 * dimes + 0.05 * nickles + 0.01 * pennies
            exchange = round(sum - MENU[coffee_choice]["cost"], 2)
            sum = round(sum, 2)
            if exchange < 0:
                print(f"There is not enough money. Here is your exchange ${sum}. Please insert the coins again.")
        global profit
        profit += MENU[coffee_choice]["cost"]
        print(f"Here is ${exchange} in change.")

    if coffee_choice == "raport":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${profit}")
    elif coffee_choice == "espresso" or coffee_choice == "latte" or coffee_choice == "cappuccino":
        resources_check()
        money_profit()
        print(f"Please! Here is your {coffee_choice} ☕ - enjoy!")
    else:
        print("There is no such coffee. Choose again.")


while machine_on:
    coffee_choice = input("What would you like? (espresso/latte/cappuccino): ")
    coffee_preparation()