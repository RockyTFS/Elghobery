#tkinterDbTblWin.py from Elgoberry 6.7 File Listing
from tkinter import *
from tkinter.ttk import *
import mysql.connector as myConnector
from tkinterMyProjUtilities import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring

def databaseTblWin(root):
    createTblWin=Toplevel()
    createTblWin.title('Create database tables')
    winSizeAndPos(createTblWin,550,150)
    createTblWin.configure(bg='#BDBDBD')
    btnConfig()
    lblDb=Label(createTblWin,text='Enter Database Name', font=('bold'))
    lblDb.grid(pady=10,row=1,column=0)

    myStr=StringVar()
    myStr.set('')
    txtDb=Entry(createTblWin,textvariable=myStr, width=25, font=('bold'))
    txtDb.grid(pady=10, row=1,column=1)
    txtDb.focus()

    btnDbTbl=Button(createTblWin,text='Create Db Table',
                    command=lambda:createDbTbl(myStr))
    btnDbTbl.grid(padx=25,pady=10, row=3,column=0)

    btnBack=Button(createTblWin,text='Back', width=20,
                   command=lambda:showAndDestroy(root,createTblWin))
    btnBack.grid(pady=10,row=3,column=1)
    hide(root)
    createTblWin.takefocus=True
    createTblWin.mainloop()

def createDbTbl(myDb):
    myDb=myDb.get()
    if(myDb.strip()==""):
        messagebox.showinfo('show info','you must specify the database name')
        return
    files=[('All Files',"*.*"), ('Python Files','*.py'), ('Text Document','*.txt')]
    filename=filedialog.askopenfilename(initialdir='/', title='Select a File', filetypes=files, defaultextension=files)
    filename=filename.strip()
    if (len(filename)==0):
        messagebox.showinfo('show info','tkinterDbTblWin.createDbTbl(): you did not select a file')
        return
    file = filename
    file=open(file,'r')
    mySql=(file.read())
    user = 'root' #askstring('Input User','Enter Database User')
    passW= 'green'#askstring('Input Password', 'Enter Database Password')
    try:
        myDbConn=myConnector.connect(
            host='localhost', user=f'{user}',
            password=f'{passW}',
            database=myDb
        )
        myCursor=myDbConn.cursor()
        myCursor.execute(mySql)
        messagebox.showinfo('show info','Table is created successfully')
    except Exception as error:
        print(error)
        messagebox.showinfo('show info','Table not created')

#begin debugging code, to be deleted after testing 
"""root=Tk()
root.title('tkinterDbTblWin.py Module Test')
winSizeAndPos(root, 450,300)
root.configure(bg='#BDBDBD')
btn=Button(root,text="Test this module's code",width=30,
           command=lambda:databaseTblWin(root))
btn.pack()
root.mainloop()
"""
#end debugging code


    
    