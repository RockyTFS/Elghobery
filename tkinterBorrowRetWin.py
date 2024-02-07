#tkinterBorrowRetWin.py from Elgoberry 8.6 Code Listing
from tkinter import *
from tkinter.ttk import *
import mysql.connector as myConnector
from mysql.connector import Error
from tkinterMyProjUtilities import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring
from tkcalendar import *
from datetime import *
from PIL import Image, ImageTk


def getUserInf():
    pass

def getBookInf():
    pass


def borrowRetWin(root):
    borRetWin=Toplevel(root)
    borRetWin.title("Borrow and return window")
    winSizeAndPos(borRetWin,510,600)
    borRetWin.config(bg="BDBDBD")
    btnConfig()

    lblTitle=Label(borRetWin, text="Borrow and return books form", font=('bold'))
    lblTitle.grid(row=0,columnspan=3)
    lblUId=Label(borRetWin, text="Enter usser library Id", width=15)
    lblUId.grid(column=0, row=1)

    userIdIntVar=StringVar()
    txtUserID=Entry(borRetWin,textvariable=userIdIntVar,font=("bold"), width=24)
    txtUserID.grid(borRetWin, column=1, row=1)

    btnGetUser=Button(borRetWin, text="Get User", width=8, command=getUserInf)
    btnGetUser.grid(borRetWin, column=2, row=1)

    lblUN=Label(borRetWin, text="Library user name", font=('bold'), width=15)
    lblUN.grid(borRetWin, column=1, row=2)
    lblISBN=Label(borRetWin, text="Enter/Scan ISBN", font=('bold'), width=15)
    lblISBN.grid(column=0, row=3)

    bookISBNStrVar=StringVar()
    txtBookISBN=Entry(borRetWin, textvariable=bookISBNStrVar, font=('bold'), width=24)
    txtBookISBN.grid(column=1, row=3)

    btnGetBook=Button(borRetWin, text="Get Book", width=8, command=getBookInf)
    btnGetBook.grid(column=2, row=3)

    lblBT=Label(borRetWin, text="Library book title", font=('bold'), width=15)
    lblBT.grid(column=0, row=4)
    lblBookTitle

   
   
    borRetWin.mainloop

