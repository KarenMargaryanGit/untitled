import matplotlib.pyplot as plt
import numpy as np

categories = ['Category A', 'Category B', 'Category C']
values1 = [20, 35, 30]  # First set of values
values2 = [15, 25, 20]  # Second set of values
values3 = [10, 30, 10]  # Third set of values

fig, ax = plt.subplots()

ax.barh(categories, values1, label='Value 1', color='white',edgecolor='black')

bars2 = ax.barh(categories, values2, left=values1, label='Value 2', color='lightgreen', edgecolor='black')

for i, (category, value) in enumerate(zip(categories, values2)):
    # Calculate the position for the text
    x_position = values1[i] + value / 2  # Center of the second bar segment
    y_position = i  # y-position corresponds to the category index
    ax.text(x_position, y_position, f'{value}', ha='center', va='center', color='black', fontsize=10)

ax.barh(categories, values3, left=np.array(values1) + np.array(values2), label='Value 3', color='white',edgecolor='black')


ax.set_xticks([])  
plt.margins(x=0)  
plt.show()
