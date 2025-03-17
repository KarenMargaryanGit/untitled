plt.plot(main['1'], main['2'], marker='o', label='Main', linestyle='-', color='b')
plt.plot(other['1'], other['2'], marker='s', label='Other', linestyle='--', color='r')
plt.plot(other1['1'], other1['2'], marker='^', label='Other1', linestyle='-.', color='g')
plt.plot(other2['1'], other2['2'], marker='d', label='Other2', linestyle=':', color='purple')

# Labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Multiple Data Series')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
import matplotlib.pyplot as plt
