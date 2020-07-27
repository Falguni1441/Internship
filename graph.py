
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from tkinter import * 
from tkinter.ttk import *
from facedetectandtrack import *
 
x_vals = []
root = Tk()


counter=0
#def graph():
plt.style.use('seaborn')

def animate(i):
    data = pd.read_csv('data.csv')
    global x_vals
    global counter
    x_vals.append(counter)
    try:
        x = data.iloc[x_vals,0]
        y = data.iloc[x_vals,1]   
        if counter>10:
            x_vals.pop(0)

        plt.cla()
        axes=plt.gca()
        axes.set_ylim([0,30])
        #plt.plot(x, y)
        counter=counter+1

        height = root.winfo_screenheight() 
        width = root.winfo_screenwidth() 
        screen_x1 = width/2
        screen_y1 = height/2
        X = screen_x1 - face_x2
        Y = screen_y1 - face_y2
        d_x = (X*X)
        d_y = (Y*Y)
        D = d_x + d_y
        distance = math.sqrt(D)
        #print(distance)
        plt.scatter(counter ,distance, s= 50,linewidth=1)

        plt.xlabel("Time")
        plt.ylabel("Movement of student from the center of screen")


        plt.tight_layout()
    except IndexError as e:
        print('Graph ended')
        exit(0)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.savefig("Scatter_Graph.png")

plt.tight_layout()
plt.show()