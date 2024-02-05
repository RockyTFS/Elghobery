#tkinterUserTblInputWin.py from Elgoberry 8.6 Code Listing
from tkinter import *
from tkinter.ttk import *
import mysql.connector as myConnector
from mysql.connector import Error
from tkinterMyProjUtilities import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring


def frmRefresh():
    userStrVar.set("")
    emailStrVar.set("")
    phoneStrVar.set("")
    cityComb.set("")

def getSel():
    return cityComb.get()

def saveData():
    user=userStrVar.get()
    email=emailStrVar.get()
    phone=phoneStrVar.get()
    cComb=cityComb.get()

    if (user=="" or email=="" or cComb=="" or phone==""):
        messagebox.showinfo('show info','Complete missing data, then press Save')
        return
    if not validatePhone(phone):
        messagebox.showinfo('show info','Phone format must be (nnn-nnn-nnnn)')
        return
    if not validateEmail(email):
        messagebox.showinfo('show info','Please correct email format')
        return
    mySqlStr='INSERT INTO users(name,email,city,phone) VALUES(%s,%s,%s,%s)'
    val=(user,email,cComb,phone)
    try:
        myDbConn=myConnector.connect(
            host='localhost', database='Monster',user='root',password='green'
        )
        mycursor=myDbConn.cursor()
        mycursor.execute(mySqlStr,val)
        myDbConn.commit()
        messagebox.showinfo('show info','Form data saved')
        frmRefresh()
    except Error as e:
        messagebox.showinfo('show info','Form data not saved')

def userTblEntryWin(root):
    uTblEntryWin=Toplevel()
    winSizeAndPos(uTblEntryWin,600,280)
    uTblEntryWin.title('User table data')
    uTblEntryWin.configure(bg='#BDBDBD')
   
#title, size
    lbluTitle=Label(uTblEntryWin,text='Database users table data entry', font=('bold'))
    lbluTitle.grid(padx=0,pady=10,row=0,columnspan=2,stick=N)
    lblUserName=Label(uTblEntryWin,text='Enter user name',font=('bold'),width=15)
    lblUserName.grid(padx=5,pady=10,row=1,column=0,sticky=W)
    lblEmail=Label(uTblEntryWin,text='Enter email',font=('bold'),width=15)
    lblEmail.grid(padx=5,pady=10,column=0,row=2,sticky=W)
    lblPhone=Label(uTblEntryWin,text='Enter phone', font=('bold'),width=15)
    lblPhone.grid(padx=5,pady=10,column=0,row=3,sticky=W)
    lblCity=Label(uTblEntryWin,text='Enter city', font=('bold'),width=15)
    lblCity.grid(padx=5,pady=10,column=0,row=4,sticky=W)

    global userStrVar
    userStrVar=StringVar()
    txtUserName=Entry(uTblEntryWin,textvariable=userStrVar,width=27,font=('bold'))
    txtUserName.grid(padx=3,pady=10,column=1,row=1,sticky=W)
    txtUserName.focus()

    global emailStrVar
    emailStrVar=StringVar()
    txtEmail=Entry(uTblEntryWin,textvariable=emailStrVar, width=27, font=('bold'))
    txtEmail.grid(padx=3,pady=10,column=1,row=2,sticky=W)

    global phoneStrVar
    phoneStrVar=StringVar()
    txtPhone=Entry(uTblEntryWin,textvariable=phoneStrVar,width=27,font=('bold'))
    txtPhone.grid(padx=3,pady=10,column=1,row=3,sticky=W)

    global cityComb
    cityComb=StringVar()
    cmbBox=Combobox(uTblEntryWin,textvariable=cityComb,width=25,font=('bold'))
    cmbBox.grid(padx=3,pady=10,row=4,column=1,sticky=W)
    cmbBox['state']='readonly' #or normal
    cmbBox['values']=('Nepean','Ottawa','Westboro','Vanier','Kanata')

    btnSave=Button(uTblEntryWin,text='Save Data',width=10,
                   command=saveData)
    btnSave.grid(padx=25,pady=10,row=5,column=0)
    btnBack=Button(uTblEntryWin,text="Back", width=10,
                   command=lambda:showAndDestroy(root,uTblEntryWin))
    btnBack.grid(pady=10,row=5,column=1)
    
    hide(root)
    uTblEntryWin.focus()
    uTblEntryWin.mainloop()

root=Tk()
userTblEntryWin(root)
    