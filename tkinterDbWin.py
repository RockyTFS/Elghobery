from tkinter import *
from tkinter.ttk import*
import mysql.connector as myConnector
from  mysql.connector import Error
from tkinterMyProjUtilities import *
from tkinter.simpledialog import askstring
from tkinter import messagebox

def createDb(dbName):
    dbName=dbName.get()
    print(f"create database {dbName}" )
    """
    user=askstring('Input Database User','Enter Database User')
    passW=askstring('Input Password','Enter Database Password', show="")
    """
    user='root'; passW='green'
        
    try:
        myCon=myConnector.connect(
            host='localhost', user=f'{user}',
            password=f'{passW}'
        )
        myCursor=myCon.cursor()
        sqlStr=f'CREATE DATABASE {dbName}'
        myCursor.execute(sqlStr)
        messagebox.showinfo('show info', f'{dbName} is created successfully')
    except Error as e:
        messagebox.showinfo('show info',f'{dbName} is not created, error {e}')

def crDbaseWin(root):
    createDbWin=Toplevel(root)
    createDbWin.title("Create New Database")
    winSizeAndPos(createDbWin,550,250)
    createDbWin.configure(bg='#BDBDBD')
    btnConfig()
    lblDb=Label(createDbWin,text='Enter Database Name',font=('bold'))
    lblDb.place(x=25, y=25)
    myStr=StringVar()  
    myStr.set("")
    txtDb=Entry(createDbWin, textvariable=myStr,width=25,
                background='pink',font=('bold'))
    txtDb.place(x=25, y=75)
    txtDb.focus()

    btnDb=Button(createDbWin,text='Create MySQL Database',
                 command=lambda:createDb(myStr))
    btnDb.place(x=25, y=125)
    btnBack=Button(createDbWin,text='Back', width=20,
                   command=lambda:showAndDestroy(root,createDbWin))
    btnBack.place(x=25,y=175)
    hide(root)
    createDbWin.takefocus=True
    createDbWin.mainloop()
