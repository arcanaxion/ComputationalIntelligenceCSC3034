import numpy as np
from skfuzzy import control as ctrl
from skfuzzy import membership as mf
import matplotlib.pyplot as plt

service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
food = ctrl.Antecedent(np.arange(0, 11, 1), 'food')
tips = ctrl.Consequent(np.arange(0, 31, 1), 'tips')

# service['poor'] = mf.trimf(service.universe, [0, 0, 5])
# service['average'] = mf.trimf(service.universe, [0, 5, 10])
# service['good'] = mf.trimf(service.universe, [5, 10, 10])
service['poor'] = mf.trimf(service.universe, [0, 0, 3])
service['average'] = mf.trimf(service.universe, [2, 5, 8])
service['good'] = mf.trimf(service.universe, [6, 10, 10])

food['poor'] = mf.trimf(food.universe, [0, 0, 5])
food['average'] = mf.trimf(food.universe, [0, 5, 10])
food['good'] = mf.trimf(food.universe, [5, 10, 10])

tips['low'] = mf.trimf(tips.universe, [0, 0, 15])
tips['medium'] = mf.trimf(tips.universe, [0, 15, 30])
tips['high'] = mf.trimf(tips.universe, [15, 30, 30])

rule1 = ctrl.Rule(service['poor'] & food['poor'], tips['low'])
rule2 = ctrl.Rule(service['poor'] & food['average'], tips['low'])
rule3 = ctrl.Rule(service['poor'] & food['good'], tips['medium'])
rule4 = ctrl.Rule(service['average'] & food['poor'], tips['low'])
rule5 = ctrl.Rule(service['average'] & food['average'], tips['medium'])
rule6 = ctrl.Rule(service['average'] & food['good'], tips['high'])
rule7 = ctrl.Rule(service['good'] & food['poor'], tips['medium'])
rule8 = ctrl.Rule(service['good'] & food['average'], tips['high'])
rule9 = ctrl.Rule(service['good'] & food['good'], tips['high'])

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]

tip_rec_ctrl = ctrl.ControlSystem(rules=rules)

tip_rec = ctrl.ControlSystemSimulation(control_system=tip_rec_ctrl)

# define the values for the inputs
tip_rec.input['service'] = 4
tip_rec.input['food'] = 9

# compute the outputs
tip_rec.compute()

# print the output values
print(tip_rec.output)

# to extract one of the outputs
print(tip_rec.output['tips'])

tips.view(sim=tip_rec)

# Plot
plt.show()