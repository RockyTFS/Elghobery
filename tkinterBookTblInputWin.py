#tkinterBookTblInputWin.py from Elgoberry 7.6 File Listing
from tkinter import *
from tkinter.ttk import *
import mysql.connector as myConnector
from mysql.connector import Error
from tkinterMyProjUtilities import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring

def BookExist():
    global myDb; global user; global passW
    myDb='Monster'; user='root';  passW='green'
    bookISBN=txtBkISBNStrVar.get()

    if (bookISBN==""):
        messagebox.showinfo('show info','Type or scan ISBN')
        return
    else:
        mySqlStr="SELECT * FROM books WHERE ISBN = " + bookISBN
        myDbConn=myConnector.connect(
            host='localhost', user=f'{user}',
            password=f'{passW}',
            database=f'{myDb}'
        )
        mycursor=myDbConn.cursor()
        mycursor.execute(mySqlStr)
        resultSet=mycursor.fetchall()

        if(mycursor.rowcount>=1):
            messagebox.showinfo('show info',
                f"{bookISBN} This book ISBN exists,'\n'To modify use the Book Search Window")
            frmRefresh()
            mycursor.close()
            myDbConn.close
            return
        saveData(myDb,user,passW)
        frmRefresh()

def sel(rdBtnInt):
    return rdBtnInt.get()

def frmRefresh():
    txtBkISBNStrVar.set("")
    txtBkTitleStrVar.set("")
    txtQtyStrVar.set("")
    rdBtnInt.set(0)

def saveData(myDb,user,passW):
    isbn=txtBkISBNStrVar.get()
    ttl=txtBkTitleStrVar.get()
    qty=txtQtyStrVar.get()
    i=rdBtnInt.get()
    if(len(ttl)==0 or len(qty)==0 or len(isbn)==0):
        messagebox.showinfo('show info','Complete missing data, then press Save button')
        return
    if(i==1):
        bnd="Paperback"
    elif(i==2):
        bnd='Hardcover'
    else:
        messagebox.showinfo('show info','Select cover type, then press Save button')
        return
    mySqlStr='INSERT INTO books(ISBN,title,quantity,cover,city) VALUES(%s,%s,%s,%s,%s)'
    val=(isbn,ttl,int(qty),bnd,'london')
    print(mySqlStr)
    print(val)
    try:
        myDbConn=myConnector.connect(
            host='localhost', user=f'{user}',
            password=f'{passW}',
            database=f'monster'
        )
        mycursor=myDbConn.cursor()
        mycursor.execute(str(mySqlStr), val)
        resultSet=mycursor.fetchall()
        print(resultSet)
        myDbConn.commit()
        messagebox.showinfo('show info', 'Form data successfully saved')
        frmRefresh()
    except Error as e:
        messagebox.showinfo('show info','form data not saved' )

def bookTblEntryWin(root):
    bkTblEntryWin = Toplevel(root)
    bkTblEntryWin.title('Book table data entry')
    winSizeAndPos(bkTblEntryWin, 600,280)
    bkTblEntryWin.configure(bg='#BDBDBD')
    btnConfig()

    lblTitle=Label(bkTblEntryWin,text='Database books table data entry', font=('bold'))
    lblTitle.grid(pady=10,row=0,columnspan=2,sticky=N)
    lblISBN=Label(bkTblEntryWin,text='Enter/Scan ISBN', width=15,font=('bold'))
    lblISBN.grid(padx=5, pady=10,column=0, row=1, sticky=W)
    lblBkTitle=Label(bkTblEntryWin,text='Enter book title',width=15,font=('bold'))
    lblBkTitle.grid(padx=5,pady=10,row=2,column=0,sticky=W)
    lblBkQty=Label(bkTblEntryWin,text='Enter book quantity',width=15,font=('bold'))
    lblBkQty.grid(padx=5,pady=10,column=0,row=3, sticky=W)
    
    global txtBkISBNStrVar
    txtBkISBNStrVar=StringVar()
    txtBkISBN=Entry(bkTblEntryWin, textvariable=txtBkISBNStrVar, width=25, font=('bold'))
    txtBkISBN.grid(pady=10,column=1, row=1)
    txtBkISBN.focus()

    global txtBkTitleStrVar
    txtBkTitleStrVar=StringVar()
    txtBkTitle=Entry(bkTblEntryWin,textvariable=txtBkTitleStrVar, width=25,font=('bold'))
    txtBkTitle.grid(pady=10,column=1,row=2)

    global txtQtyStrVar
    txtQtyStrVar=StringVar()
    txtQty=Entry(bkTblEntryWin,textvariable=txtQtyStrVar, width=25,font=('bold'))
    txtQty.grid(pady=10,column=1,row=3)

    lblFrame=LabelFrame(bkTblEntryWin,text='Book Cover')
    lblFrame.grid(padx=5, row=4, columnspan=2,sticky=W)
    global rdBtnInt
    rdBtnInt=IntVar()
    rdBtnPaper=Radiobutton(lblFrame, text='Paperback', variable=rdBtnInt, value=1,
	                    command=lambda:sel(rdBtnInt))
    rdBtnPaper.pack(side=LEFT,fill=X,expand=YES)
    rdBtnHard=Radiobutton(lblFrame, text='Hardcover',variable=rdBtnInt,value=2,
                          command=lambda:sel(rdBtnInt))
    rdBtnHard.pack(side=RIGHT,padx=5)
    
    btnSave=Button(bkTblEntryWin,text='Save Data',width=10,
                   command=BookExist)
    btnSave.grid(padx=25,pady=10,row=5,column=0)
    btnBack=Button(bkTblEntryWin,text='Back',width=10,
                   command=lambda:showAndDestroy(root,bkTblEntryWin))
    btnBack.grid(padx=25,pady=10,column=1,row=5)

    hide(root)
    bkTblEntryWin.focus()
    
    global myDb,user,passW
    myDb='Monster'
    user='root'
    passW='green'

    bkTblEntryWin.mainloop
    
"""
root=Tk()
root.title("Test code")
winSizeAndPos(root,450,300)
root.configure(bg='#BDBDBD')
btn=Button(root, text="Load the window under testing", width=30,
           command=lambda:bookTblEntryWin(root))
btn.pack()
root.mainloop()
"""






