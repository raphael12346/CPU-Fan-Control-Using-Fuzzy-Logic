import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import Entry, Button, Label

# Antecedent and Consequent objects hold universe variables and membership
temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
frequency = ctrl.Antecedent(np.arange(0, 4.6, 0.1), 'frequency')
fan_speed = ctrl.Consequent(np.arange(0, 4001, 1), 'fan speed')

# Membership functions
temperature['cold'] = fuzz.trapmf(temperature.universe, [0, 0, 20, 40])
temperature['warm'] = fuzz.trimf(temperature.universe, [35, 53, 70])
temperature['hot'] = fuzz.trapmf(temperature.universe, [60, 80, 100, 100])

frequency['silent'] = fuzz.trapmf(frequency.universe, [0, 0, 1.5, 2.5])
frequency['performance'] = fuzz.trimf(frequency.universe, [2, 3, 4])
frequency['turbo'] = fuzz.trapmf(frequency.universe, [3.5, 4.0, 4.5, 4.5])

fan_speed['slow'] = fuzz.trapmf(fan_speed.universe, [0, 0, 1250, 2000])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [1500, 2250, 3000])
fan_speed['fast'] = fuzz.trapmf(fan_speed.universe, [2500, 3200, 4000, 4000])

# Fuzzy control rules
rule1 = ctrl.Rule(temperature['cold'] & frequency['silent'], fan_speed['slow'])
rule2 = ctrl.Rule(temperature['cold'] & frequency['performance'], fan_speed['slow'])
rule3 = ctrl.Rule(temperature['cold'] & frequency['turbo'], fan_speed['medium'])
rule4 = ctrl.Rule(temperature['warm'] & frequency['silent'], fan_speed['slow'])
rule5 = ctrl.Rule(temperature['warm'] & frequency['performance'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['warm'] & frequency['turbo'], fan_speed['fast'])
rule7 = ctrl.Rule(temperature['hot'] & frequency['silent'], fan_speed['medium'])
rule8 = ctrl.Rule(temperature['hot'] & frequency['performance'], fan_speed['fast'])
rule9 = ctrl.Rule(temperature['hot'] & frequency['turbo'], fan_speed['fast'])

# Control System Creation and Simulation
fan_speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fan_speeding = ctrl.ControlSystemSimulation(fan_speed_ctrl)

# Classification of Fan Speed
def classify_fan_speed(speed):
    if speed <= 1750:
        return "Slow"
    elif speed <= 2750:
        return "Medium"
    else:
        return "Fast"
    
# A function to update the fan speed
def update_fan_speed():
    try:
        # Get user inputs from the text entry fields
        user_temperature = float(temperature_entry.get())
        user_frequency = float(frequency_entry.get())

        # Check if inputs are within the desired ranges
        if 0 <= user_temperature <= 100 and 0 <= user_frequency <= 4.5:
            # Pass inputs to the ControlSystemSimulation
            fan_speeding.input['temperature'] = user_temperature
            fan_speeding.input['frequency'] = user_frequency
            fan_speeding.compute()

            fan_speed_value = int(fan_speeding.output['fan speed'])
            fan_speed_classification = classify_fan_speed(fan_speed_value)

            # Update the fan speed label and classification
            fan_speed_label.config(text=f"Fan Speed: {fan_speed_value} RPM", font=(20))
            fan_speed_classification_label.config(text=f"Classification: {fan_speed_classification}", font=(20))
        else:
            fan_speed_label.config(text="Fan Speed: Invalid Input", font=(20))
            fan_speed_classification_label.config(text="Classification: Invalid Input", font=(20))
    except ValueError:
        fan_speed_label.config(text="Fan Speed: Invalid Input", font=(20))
        fan_speed_classification_label.config(text="Classification: Invalid Input", font=(20))
                                           
# A function to show graph
def show_graph():
    fan_speed.view(sim=fan_speeding)

# GUI
root = tk.Tk()
root.title("Fuzzy Fan Speed Control")
root.geometry("200x190")

# Labels, entry fields, and a button
temperature_label = Label(root, text="Temperature (0 - 100)°C:")
temperature_label.pack()
temperature_entry = Entry(root)
temperature_entry.pack()

frequency_label = Label(root, text="Frequency (0 - 4.5)GHz:")
frequency_label.pack()
frequency_entry = Entry(root)
frequency_entry.pack()

calculate_button = Button(root, text="Calculate Fan Speed", command=update_fan_speed)
calculate_button.pack()

show_graph_button = Button(root, text="Show Graph", command=show_graph)
show_graph_button.pack()

fan_speed_label = Label(root, text="Fan Speed: N/A", font=(20), padx=10)
fan_speed_label.pack()

fan_speed_classification_label = Label(root, text="Classification: N/A", font=(20), pady=10)
fan_speed_classification_label.pack()

root.mainloop()
