import re
import tkinter as tk
from tkinter import messagebox
from methods import *
import numpy as np

'''Patterns'''
empty_pattern = re.compile(r'^$')
num_pattern = re.compile(r'[-+]?\d*\.?\d+')
size_pattern = re.compile(r'^[1-9]\d*$')


entry_list = []
label_list = []
solution_list = []
sol_label_list = []


'''Validation'''
# input system info validation 
def valid_input(inpt, pattern, message):
    if pattern.fullmatch(inpt): return True
    elif empty_pattern.fullmatch(inpt): return ' Fields must not be empty'
    else: return message

# test if a number match to users boards 
def check_boards(min, max, inpt):
    return inpt>= min and inpt<=max 


'''Create fields'''
def create_fields(mat_y, mat_x):
    # clear previous entries
    for entry in entry_list:
        entry.destroy()
    # clear previous labels
    for label in label_list:
        label.destroy()
    
    #clear previous solution list
    for sol in solution_list:
        sol.destroy()

    #clear previous solution-label list
    for label in sol_label_list:
        label.destroy()
    
    #create new labels
    for i in range(mat_x):
        label = tk.Label(window, text='X'+str(i))
        label.grid(row=0, column=i+4)
        label_list.append(label)
    label = tk.Label(window, text='B')
    label.grid(row=0, column=mat_x+4)
    label_list.append(label)
    
    # create new entries
    for j in range(mat_y): #rows
        for i in range(mat_x+1): #columns
            entry = tk.Entry(window)
            entry_list.append(entry)
            entry.grid(row=j+1, column=i+4)



def show_error_window(message):
    messagebox.showerror("Error", message)

def get_a_b():
    sys_x, sys_y = validation1()

    if sys_x!=None and sys_y!=None:
        b = []
        A = []

        i_x = 0 
        a_array = []

        for element in entry_list:
            element.config(bg='white')

            #validation
            el = element.get()
            val_el = valid_input(el, num_pattern, ' The value must be numeric! ')
            if val_el != True:
                show_error_window(val_el)
                element.config(bg='red')
                A = None
                b = None
                break
        
            if i_x < sys_x:
                a_array.append(float(el))
            else: 
                b.append(float(el))
                A.append(a_array) 
                i_x = -1
                a_array = []

            i_x += 1

        return A, b
    else: return None, None



def validation1():
    mat_y = entry_sm1.get()
    mat_x = entry_sm2.get()

    message = ''

    val1 = valid_input(mat_y, size_pattern, ' The value must be a positive integer!')
    val2 = valid_input(mat_x, size_pattern, ' The value must be a positive integer!')
    if val1==True and val2==True:
        if check_boards(1, 7, int(mat_y)) == False or check_boards(1, 7, int(mat_x))== False: 
            show_error_window('The value is to high! Select up to 7')
        else:
            return int(mat_x), int(mat_y) 
    else: 
        if val1 != True: message = val1
        if val2 != True: message +=val2
        show_error_window(message)
    return None, None
    
def create_sol_fields(x, b):
    #clear previous solution list
    for sol in solution_list:
        sol.destroy()

    #clear previous solution-label list
    for label in sol_label_list:
        label.destroy()
        
    #create solution fields with labels
    for i in range(len(x)):
        sol = tk.Label(window, text=str(x[i]))
        sol.grid(row=len(b)+3, column=i+4)
        label = tk.Label(window, text='X'+str(i))
        label.grid(row=len(b)+2, column=i+4) 
        solution_list.append(sol)
        sol_label_list.append(label)

'''Buttons commandos'''
def sys_button_click():
    sys_x, sys_y = validation1()
    if sys_x != None and sys_y != None: create_fields(sys_y, sys_x)

def ls_button_click():
    A, b = get_a_b()
    if A != None and b!= None:
        x = least_squares(A, b)
        create_sol_fields(x, b)

def pi_button_click():
    A, b = get_a_b()
    if A != None and b!= None:
        x = pinv(A, b)
        create_sol_fields(x, b)

def qr_button_click():
    A, b = get_a_b()
    if A != None and b!= None:
        x = qr(A, b)
        create_sol_fields(x, b)

'''Create main windows '''
window = tk.Tk()
window.title("Solver: System of linear equations")

'''Row and columns configurations'''
window.rowconfigure(0, minsize=20)
#window.columnconfigure(0, minsize=20)
window.rowconfigure(3, minsize=20)

'''Create size of matrix field'''
empty_label = tk.Label(window, text="  ")
empty_label.grid(row=0, column=0)
label_sm1 = tk.Label(window, text='Number of equations ')
label_sm2 = tk.Label(window, text='Number of unknown variables ')
label_sm1.grid(row=2, column=1, sticky="nw")
label_sm2.grid(row=3, column=1, sticky="nw")
entry_sm1 = tk.Entry(window, width=10)
entry_sm2 = tk.Entry(window, width=10)
entry_sm1.grid(row=2, column=2)
entry_sm2.grid(row=3, column=2)
empty_label.grid(row=0, column=3)

'''Validation of inputs with button 'Create system' '''
button_cm = tk.Button(window, text='Create system', command=sys_button_click) 
button_cm.grid(row=4, column=1, columnspan=2, sticky="ew")

'''CalculateLeast squares'''
button_ls = tk.Button(window, text='Least squares', command=ls_button_click)
button_ls.grid(row=5, column=1, columnspan=2, sticky="ew")

'''Calculate pseudo inverse matrix'''
button_im = tk.Button(window, text ='Pinv', command=pi_button_click)
button_im.grid(row=6, column=1, columnspan=2, sticky="ew")

'''Calculate  QR-decomposition'''
button_qr = tk.Button(window, text = 'QR decomposition', command=qr_button_click)
button_qr.grid(row=7, column=1, columnspan=2, sticky="ew")

'''Run the app'''
window.mainloop()







