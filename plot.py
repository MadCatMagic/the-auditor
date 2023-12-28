import matplotlib.pyplot as plt
import os

def EnsureTempDir():
    folder_path = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'/temp' directory created.")

def CreateHorizBarChart(data: list[tuple[str, int]], filename: str):
    # put files in here always
    EnsureTempDir()

    # Create a horizontal bar chart with minimal elements
    fig, ax = plt.subplots(figsize=(8, len(data) * 0.5))  # Adjust the figure size

    bars = ax.barh(*zip(*data), color='dodgerblue')  # Use a light color for bars

    # Set the background color of the plot to black
    ax.set_facecolor('black')

    # Display the bar lengths as numbers next to the bars
    for bar, (thing, count) in zip(bars, data):
        yval = bar.get_y() + bar.get_height() / 2
        ax.text(bar.get_width() + 0.1, yval, f'{thing}: {count}', color='white', va='center')

    # Hide unnecessary elements
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_yticklabels([])  # Hide y-axis labels
    ax.set_xticklabels([])  # Hide x-axis labels
    
    # save plot to file
    plt.savefig("temp/" + filename, transparent=True, bbox_inches='tight')

if __name__ == "__main__":
    #words = [("apple", 2), ("pear", 5), ("orange", 10), ("sussy", 0), ("baka", 3)]
    #CreateHorizBarChart(words, "temp.png")
    import random
    import calendar

    data = [(str(i), random.randint(0, 50)) for i in range(365)]
    maxData = max(data, key=lambda x: x[1])
    col = [(v / maxData * 0.8, 0, 1 - v / maxData) for _, v in data]

    # Create a horizontal bar chart with minimal elements
    fig, ax = plt.subplots(figsize=(8, len(data) * 0.5))
    bars = ax.bar(*zip(*data), color=col, width=1)

    # Set the background color of the plot to black
    ax.set_facecolor('black')

    # Display the bar lengths as numbers next to the bars
    #for bar, (thing, count) in zip(bars, data):
        #yval = bar.get_y() + bar.get_height() / 2
        #ax.text(bar.get_width() + 0.1, yval, f'{thing}: {count}', color='white', va='center')

    # Hide unnecessary elements
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_yticklabels([])  # Hide y-axis labels
    ax.set_xticklabels([])  # Hide x-axis labels

    plt.show()