#tkinterBorrowRetWin.py
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox 
from tkinter.simpledialog import askstring 
from tkcalendar import *
from datetime import * 
import mysql.connector as myConnector 
from mysql.connector import Error 
from tkinterMyProjUtilities import * 


def frmRefresh():
	userIdIntVar.set(0) 
	bookISBNStrVar.set("") 
	lblUserNameStrVar.set("") 
	lblBookTitleStrVar.set("") 
	outDateStrVar.set("") 
	inDateStrVar.set("") 
	rdBtnInt.set("") 
	btnPickInDate.configure(state = DISABLED) 
	btnPickOutDate.configure(state = DISABLED) 

def getUserInf():
	userId = userIdIntVar.get() 
	
	
	mySqlStr = f"SELECT name FROM users where id = {userId}" 
	try:
		myDbConn = myConnector.connect(
			host='localhost', 
			database = f"{myDb}", 
			user = f'{user}', 
			password=f'{passW}')
		mycursor = myDbConn.cursor() 
		mycursor.execute(mySqlStr) 
		resultSet = mycursor.fetchone() #This is a set 

		if ( mycursor.rowcount < 1 ): 
			messagebox.showinfo(
				"show info", "User data is not found")
			lblUserNameStrVar.set("") 
			return
		val = resultSet[0] 
		lblUserNameStrVar.set(val) 
	except Error as e:
		messagebox.showinfo("show info","User data is not found")

def getBookInf():
	bookISBN = bookISBNStrVar.get() 
	mySqlStr = "SELECT title, quantity FROM books where ISBN = " + bookISBN 
	try:
		myDbConn = myConnector.connect(
			host='localhost', database = f"{myDb}",
			user = f'{user}', password = f'{passW}')
		mycursor = myDbConn.cursor() 
		mycursor.execute(mySqlStr)
		resultSet = mycursor.fetchall()   #This is a set 
		if ( mycursor.rowcount < 1 ):
			messagebox.showinfo("show info", "Book data is not found")
			lblBookTitleStrVar.set("") 
			return 
		val = resultSet[0][0] 
		lblBookTitleStrVar.set(val) 
	except Error as e: 
		messagebox.showinfo("show info", "Book data is not found")

def outDate(cal): 
	outDateStrVar.set(cal.selection_get()) 

def inDate(cal): 
	inDateStrVar.set(cal.selection_get()) 

def plusMinusQty(bookISBN): 
#in case of renew i = 1 no change in book quantity    
#in case of borrow i = 2 reduce book quantity by one 
#in case of return the book i = 3 add 1 to book quantity 
	i = rdBtnInt.get() 
	print ("i", i) 
	mySqlStr = f"SELECT quantity FROM books WHERE ISBN = {bookISBN}"
	print("plusMinus first", mySqlStr) 
	myDbConn = myConnector.connect(
		host ='localhost', database = f"{myDb}", 
		user = f'{user}', password = f'{passW}') 
	mycursor = myDbConn.cursor() 
	mycursor.execute(mySqlStr) 
	resultSet = mycursor.fetchall() 
	noStock = resultSet[0][0]
	if noStock == 0:
		#case the book out of stock
		messagebox.showinfo("show info", "Sorry, this book out of stock")
		return noStock 
	if (i == 1):
		qty = resultSet[0][0]
	elif (i == 2):
		qty = resultSet[0][0]-1 
	elif (i == 3):
		qty = resultSet[0][0]+1 
	mySqlStr = "UPDATE books SET quantity = %s WHERE ISBN = %s"
	val = (qty, bookISBN) 
	mycursor = myDbConn.cursor() 
	mycursor.execute(mySqlStr, val)
	myDbConn.commit()
	myDbConn.close()
	mycursor.close()

def saveData():
#remember to decrease the quantity after each successful operation
	userId  = (userIdIntVar.get())
	bookISBN  = (bookISBNStrVar.get()) 
	outDate = outDateStrVar.get() 
	inDate  = inDateStrVar.get() 
	i = rdBtnInt.get() 
	if (userId <= 0 or bookISBN == ""): 
		messagebox.showinfo("show info", "Complete missing Data, then press Save button") 
		return 
	if (i == 1 or i ==2): 
		if len(outDate)== 0: 
			messagebox.showinfo("show info",
			   "Complete borrow Date,then press Save button") 
			return 
	elif (i == 3):
		if (len(inDate) == 0): 
			messagebox.showinfo("show info",
			   "Complete return Date, then press Save button")
			return 
	else: 
		messagebox.showinfo("show info", "You must select renew, borrow, or return")
		return

	"""Check first, if there is a record for this userId and bookISBN exists and
	borrowedOn is NOT NULL and returnedOn is NULL return give a message
	"""

	mySqlStr = f"SELECT userId, bookISBN, borrowedOn, returnedOn FROM " + \
			"borrow WHERE userId = {userId} AND bookISBN =  {bookISBN}"
	try: 
		myDbConn = myConnector.connect(
			host='localhost', database = f"{myDb}", 
			user = f'{user}', password = f'{passW}')
		mycursor = myDbConn.cursor() 
		mycursor.execute(mySqlStr) 
		resultSet = mycursor.fetchall()   #This is a set
		if (i == 2): 
			if ( mycursor.rowcount >= 1 ):
				if (resultSet[0][2] != None and  resultSet[0][3] == None):
					messagebox.showinfo("show info",
					f"Can't complete borrow operation, this book ISBN: {bookISBN} is borrowed by this user ID: {userId}")
					messagebox.showinfo("show info",
					f"You can only select renew or return in this case") 
					return 
	except Error as e: 
		messagebox.showinfo("show info", e) #END PAGE 226
		return
	
	if (i == 1): 
		mySqlStr = "UPDATE borrow SET borrowedOn =  %s WHERE userId = %s and bookISBN= %s"
		val = (outDate, userId, bookISBN) 
#Borrow so insert new record 
	elif (i == 2): 
		mySqlStr = "INSERT INTO borrow ( userId, bookISBN, borrowedOn) VALUES (%s, %s, %s)" 
		val = (userId, bookISBN, outDate) 
		print(mySqlStr, val) 
#return book operation so update operation of existing record 
#3 for return 
	elif (i == 3):       
		mySqlStr = "UPDATE borrow SET returnedOn =  %s WHERE userId = %s and bookISBN= %s" 
		val = (inDate, userId, bookISBN) 
	else: 
		messagebox.showinfo("show info", "You must select renew, borrow, or return")
		return 
	try: 
		noStock = plusMinusQty(bookISBN) 
		if noStock == 0: 
			messagebox.showinfo("show info", "Form data is not saved")
			return 
#END PAGE 227
		myDbConn = myConnector.connect( 
			host = 'localhost', database = f"{myDb}", 
			user = f'{user}', password = f'{passW}') 
		mycursor = myDbConn.cursor() 
		mycursor.execute(mySqlStr, val) 
		myDbConn.commit() 
		mycursor.close() 
		myDbConn.close() 
		messagebox.showinfo("show info", "Form Data is saved successfully") 
		frmRefresh() 
	except Error as e:
		messagebox.showinfo("show info", "Form data is not saved") 

def sel(rdBtnInt): 
	i = rdBtnInt.get() 
	if (i == 1 or i == 2): 
		btnPickOutDate.configure(state = NORMAL) 
		btnPickInDate.configure(state = DISABLED) 
	elif (i == 3): 
		btnPickOutDate.configure(state = DISABLED)
		btnPickInDate.configure(state = NORMAL)

def borrowRetWin(root): 
	global userIdIntVar
	global bookISBNStrVar 
	global lblBookTitleStrVar 
	global lblUserNameStrVar
	global outDateStrVar 
	global btnPickOutDate
	global inDateStrVar
	global btnPickInDate
	global rdBtnInt
	global myDb, user, passW

	borRetWin = Toplevel(root) 
	borRetWin.title("Borrow and return window") 
#END PAGE 228
	winSizeAndPos(borRetWin, 700, 800) 
	borRetWin.configure(bg = '#BDBDBD') 
	btnConfig() 
	lblTitle = Label(borRetWin, text = "Borrow And Return Books Form", font = ('bold'))
	lblTitle.grid(pady = 10, row = 0, columnspan = 3, sticky = N ) 
	#lblUId = Label(borRetWin, text = "Enter user library Id", font = ('bold'), width = 18)
	lblUId = Label(borRetWin, text = "Enter user library Id", font = ("normal"),width=15)
	lblUId.grid(padx = 5, pady = 5, row = 1, column = 0, sticky = W) 

 
	userIdIntVar = IntVar()
	txtUserId = Entry(borRetWin, textvariable = userIdIntVar, width = 24, font = ('bold'))
	txtUserId.grid(padx = 3, pady = 5, row = 1, column = 1, sticky = W) 
	txtUserId.focus() 

	btnGetUser = Button(borRetWin, text = "Get User", width = 8, command = getUserInf)
	btnGetUser.grid(pady = 5, row = 1, column = 2, sticky = W) 
	lblUN = Label(borRetWin, text = "Library user name", width = 15, font = ('bold')) 
	lblUN.grid(padx = 3, pady = 5, row = 2, column = 0, sticky = W) 

	lblUserNameStrVar = StringVar() 
	lblUserName = Label(borRetWin, textvariable = lblUserNameStrVar, width = 24, font = ('bold'))
#END PAGE 229
	lblUserName.grid(padx = 3, pady = 5, row = 2, column = 1, sticky = W) 
	lblISBN = Label(borRetWin, text = "Enter/Scan ISBN", font = ('bold'), width = 15) 
	lblISBN.grid(padx = 5, pady = 5, row = 3, column = 0, sticky = W) 

	
	bookISBNStrVar = StringVar() 
	txtBookISBN = Entry(borRetWin, textvariable = bookISBNStrVar, width = 24, font = ('bold'))
	txtBookISBN.grid(padx = 3, pady = 5, row = 3, column = 1, sticky = W) 
	btnGetBook = Button(borRetWin, text = "Get Book", width = 8, command = getBookInf)
	btnGetBook.grid(pady = 5, row = 3, column = 2, sticky = W) 
	lblBT = Label(borRetWin, text = "Library book title", width = 15, font = ('bold')) 
	lblBT.grid(padx = 3, pady = 5, row = 4, column = 0, sticky = W) 
	
	
	lblBookTitleStrVar = StringVar() 
	lblBookTitle = Label(borRetWin, textvariable = lblBookTitleStrVar, width = 24, font = ('bold')) 
	lblBookTitle.grid(padx = 3, pady = 5, row = 4, column = 1, sticky = W) 
	lblOut = Label(borRetWin, text = "Borrow date", width = 15, font = ('bold')) 
	lblOut.grid(padx = 3, pady = 5, row = 5, column = 0, sticky = W) 

	
	outDateStrVar = StringVar() 
	lblOutDate = Label(borRetWin, textvariable = outDateStrVar, width = 24, font = ('bold'))
	lblOutDate.grid(padx = 3, pady = 5, row = 5, column = 1, sticky = W) 

	
#END PAGE 230
	btnPickOutDate = Button(borRetWin, text = "Get Date", width = 8, state = DISABLED, command = lambda: outDate(cal))
	btnPickOutDate.grid(pady = 5, row = 5, column = 2, sticky = W) 
	lblIn = Label(borRetWin, text = "Return date", width = 15, font = ('bold')) 
	lblIn.grid(padx = 3, pady = 5, row = 6, column = 0, sticky = W) 

 
	inDateStrVar = StringVar() 
	lblInDate = Label(borRetWin, textvariable = inDateStrVar, width = 24, font = ('bold'))
	lblInDate.grid(padx = 3, pady = 5, row = 6, column = 1, sticky = W) 

	 
	btnPickInDate = Button(borRetWin, text = "Get Date", width = 8, state = DISABLED, command = lambda: inDate(cal)) 
	btnPickInDate.grid(pady = 5, row = 6, column = 2, sticky = W) 
	#LabelFrame    

	lblFrame = LabelFrame(borRetWin, text = 'Borrow Mode', width = 25) 
	lblFrame.grid(padx = 25, pady = 5, row = 7, columnspan = 3, sticky = W) 

	 
	rdBtnInt = IntVar() 
	rdBtnRenew = Radiobutton(lblFrame, text = "Renew", variable = rdBtnInt, value = 1, command = lambda: sel(rdBtnInt)) 
	rdBtnRenew.pack(side = LEFT, padx = 7) 
	rdBtnBorrow = Radiobutton(lblFrame, text = "Borrow", variable = rdBtnInt, value = 2, command = lambda: sel(rdBtnInt)) 
	rdBtnBorrow.pack(side = LEFT, padx = 7, fill = X, expand=YES)
#END PAGE 231
	rdBtnReturn = Radiobutton(lblFrame, text = "Return", variable = rdBtnInt, value = 3, command = lambda: sel(rdBtnInt)) 
	rdBtnReturn.pack(side = LEFT, padx = 7) 
	# Create save button photoimage object img1 
	imagem="C:\\_DATA\Bitmaps\\floppy.png"
	img1 = PhotoImage(file = imagem)
	btnSave = Button(borRetWin, text = "Save Data", width = 10, image = img1, command = saveData) 
	btnSave.grid(padx = 25, pady = 5, row = 8, column = 0) 
	# Create Back button photoimage object img2 
	imagem2="C:\\_DATA\\Bitmaps\\backArrow.png"
	img2 = PhotoImage(file = imagem2) 
	btnBack = Button(borRetWin, text = "Back", width = 10, image = img2, command = lambda : showAndDestroy(root, borRetWin)) 
	btnBack.grid(pady = 5, row = 8, column = 1) 
	x = datetime.now() 
	thisYear = x.strftime("%Y") 
	cal = Calendar(borRetWin, selectmode = "day", year = int(thisYear), month = x.month, day = x.day)
	cal.grid(padx = 25, pady = 5, row = 9, columnspan = 3, sticky = W)
	
	# Display untill closed manually. 
	
	hide (root) 
	borRetWin.takefocus = True 

	#myDb = askstring("Enter Database Name", "Enter Database Name") 
	#user = askstring("Input Database User", "Enter Database User" , show = '*')        
	#passW = askstring("Input Password", "Enter Database Password" , show = '*') 
	borRetWin.mainloop()

if __name__ =='__main__':
	myDb="Monster"; user='root';  passW='green'
	root=Tk()
	borrowRetWin(root)
	root.mainloop()


