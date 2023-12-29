import matplotlib.pyplot as plt
import os
from utilities import counter
from datetime import date

def EnsureTempDir():
    folder_path = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'/temp' directory created.")

def CreateHorizBarChart(data: list[tuple[str, int]], filename: str):
    # put files in here always
    EnsureTempDir()
    plt.clf()
    plt.cla()
    # Create a horizontal bar chart with minimal elements
    fig, ax = plt.subplots(figsize=(8, len(data) * 0.5))  # Adjust the figure size

    bars = ax.barh(*zip(*data), color='dodgerblue')  # Use a light color for bars

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

def CreateActivityBarChart(dateData: counter, minDate: date, maxDate: date, filename: str):
    EnsureTempDir()
    plt.clf()
    plt.cla()

    maxData = 0
    for _, amount in dateData:
        if amount > maxData:
            maxData = amount
    ordering = []
    colours = []
    dateDataDict = dict(dateData)
    cd = minDate
    i = 0
    while cd <= maxDate:
        if cd in dateDataDict:
            ordering.append((i, dateDataDict[cd]))
            colours.append((dateDataDict[cd] / maxData * 0.8, 0, 1 - dateDataDict[cd] / maxData))
        else:
            ordering.append((i, 0))
            colours.append((0, 0, 0))
        cd += date.resolution
        i += 1
    
    fig, ax = plt.subplots()
    ax.bar(*zip(*ordering), color=colours)


    # Display the bar lengths as numbers next to the bars
    #for bar, (thing, count) in zip(bars, data):
        #yval = bar.get_y() + bar.get_height() / 2
        #ax.text(bar.get_width() + 0.1, yval, f'{thing}: {count}', color='white', va='center')

    # Hide unnecessary elements
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color("white")
    ax.tick_params(axis='both', which='both', length=0, colors="white")
    ax.set_yticklabels([])  # Hide y-axis labels

    plt.savefig("temp/" + filename, transparent=True, bbox_inches='tight')

if __name__ == "__main__":
    words = [("apple", 2), ("pear", 5), ("orange", 10), ("sussy", 0), ("baka", 3)]
    CreateHorizBarChart(words, "temp.png")