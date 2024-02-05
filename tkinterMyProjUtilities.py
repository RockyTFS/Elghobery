#tkinterMyProjUtilities.py
#from Elgobary "GUI Window App using Python Tkinter Mysql"

from tkinter import *
from tkinter.ttk import *
import re

def validatePhone(phoneInput):
    phonePattern = r'\d{3}-\d{3}-\d{4}'#(r'(\d{3}|\(\d{3}\)-)?\d{3}-\d{4}')
    
    result = re.search(phonePattern, phoneInput)
    if result:
        return True
    else:
        return False
    
def validateEmail(emailInput):
    emailPattern =  r'^(\w|\.|\_|\-)+[@](\w|\.|\_|\-)+[.]\w{2,}$'
    result = re.search(emailPattern, emailInput)
    if result:
        return True
    else:
        return False


def winSizeAndPos(winName, w,h):
    ws=winName.winfo_screenwidth()
    hs=winName.winfo_screenheight()
    x=((ws-w)/2)
    y=((hs-h)/2)
    winName.geometry("%sx%s" %(w,h))
    winName.geometry("+%d+%d"%(x,y))

def btnConfig():
    fontTuple=("Comic Sans MS",13, "bold")
    style=Style()
    style.configure('TButton',background='#848484',foreground='#0404B4',font=fontTuple)
    style.configure('TLabelFrame', background='#848484', foreground='0404B4',font=fontTuple)
    style.configure('TRadiobutton', background='#848484', foreground='#0404B4', fornt=fontTuple)

def hide(winToHide):
    winToHide.withdraw()

def showAndDestroy(parm1, parm2):
    """winShow.deiconify()
    winDest.destroy()
    winShow.takefocus=True
    """
    parm1.deiconify()
    parm2.destroy()
    parm1.takefocus=True
    """
    print("Enter showAndDestroy\n")
    print(f"winShow is type {type( winShow)} ")
    print(f"winDest is type {type( winDest)} ")
    """

