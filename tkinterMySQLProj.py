#tkinterMySQLProj.py
#from Elgobary "GUI Window App using Python Tkinter Mysql"

from tkinter import *
from datetime import *
from tkinter.ttk import *
import sys
sys.path.append('C:\_DATA\_ListsAndDBs\_SOFTWARE\Tkinter')
sys.path.append('C:\_DATA\_ListsAndDBs\_SOFTWARE\Tkinter\Documentation\Elgobary')
from tkinterDbWin import *
from tkinterDbTblWin import *
from tkinterBookTblInputWin import *
from tkinterUserSearchWin import *
from tkinterBorrowRetWin import *
from tkinterBookSearchWin import *
from tkinterReportsWin import *
from PIL import ImageTk, Image
from tkinterMyProjUtilities import *


def moveText(): #unpag tuple of textItem bounding box
    xULCorner,yULCorner,xBRCorner,yBRCorner=myCanv.bbox(textItem)
    w=myCanv.winfo_width()
    if(xULCorner>w):
        xULCorner=0
        yULCorner=myCanv.winfo_height()//2
        myCanv.coords(textItem, xULCorner, yULCorner)
    else:
        myCanv.move(textItem, 1,0)
    myCanv.after(10,moveText)

def myTime():
    currTime=datetime.now()
    currTime=currTime.strftime("%H:%M%S")
    timeStrVar.set(currTime)
    lblTime.after(1000,myTime)

def myDate(dateStrVar):
    myDay=datetime.now()
    #myDay=myDay.strftime("Y-%m-%d")
    dateStrVar.set(myDay)


#main gui window
root=Tk()
root.title("Root Window")
#this next method is placed in the utilities file tkinterMyProjUtilities
winSizeAndPos(root, 450, 550) #can be used for any window
#root background
root["bg"]='#BDBDBD' 
btnConfig()
myCanv = Canvas(root, bg = 'black', width = 435, height = 35)
myCanv.place(x=5,y=5)
myPhoto = ImageTk.PhotoImage(file= 'C:\_DATA\Bitmaps\Donald-duck.png')
photoOnMyCanv=myCanv.create_image(27, 19, image = myPhoto, tag = 'photo')
myText = " Public Library Application"
h = (myCanv.winfo_height() * 30 // 2)
textItem = myCanv.create_text(2, h,text=myText,font=('Times New Roman',15,'bold'),anchor='w')
myColor='white'
myCanv.itemconfig(textItem, fill = myColor)
moveText()

#time label
timeStrVar=StringVar()
fontTuple=('TimesNewRoman',15,'bold')
lblTime=Label(root,background='black',font=fontTuple, textvariable=timeStrVar, width=10,foreground='green')
lblTime.place(x=335,y=50)

#date label
dateStrVar=StringVar()
lblDate=Label(root, textvariable=dateStrVar, width=10,foreground='green',background='black',font=fontTuple)
lblDate.place(x=0,y=50)

#BUTTONS - 

#1.btnDispDbWin to invoke crDbaseWin(root) method
btnDispDbWin=Button(root, text="Open Create Database Window", width=30,
                    command=lambda:crDbaseWin(root))
btnDispDbWin.place(x=80,y=100)

#2.btnDispDbTblWin to invoke databaseTblWin(root) method
btnDispDbTblWin=Button(root,text="Open Create Table Window", width=30,
                       command=lambda:databaseTblWin(root))
btnDispDbTblWin.place(x=80,y=150)

#3. btnDispBookTblWin to invoke bookTblEntryWin(root) method
btnDispBookTblWin=Button(root,text='Book Data Entry Window',width=30, 
                         command=lambda: bookTblEntryWin(root))
btnDispBookTblWin.place(x=80, y=200)

#4. btnDispUserTblWin to invoke userTblEntryWin(root) method
btnDispUserTblWin=Button(root,text="User Data Entry Window", width=30,
                         command=lambda:userTblEntryWin(root))
btnDispUserTblWin.place(x=80,y=250)

#5. btnDispBorrowTblWin to invoke borrowRetWin(root) method
btnDispBorrowTblWin=Button(root, text="Borrow/Return Data Entry Window", w=30,
                           command=lambda:borrowRetWin(root))
btnDispBorrowTblWin.place(x=80, y=300)

#6. btnDispBookSearchWin to invoke bkSearchWin(root) method
btnDispBookSearchWin=Button(root,text="Book Search Window", w=30,
                            command=lambda:bkSearchWin(root))
btnDispBookSearchWin.place(x=80, y=350)

#7. btnDispUserSearchWin to invoke uSearchWin(root) method
btnDispUserSearchWin=Button(root,text="User Search Window", w=30,
                            command=lambda:uSearchWin(root))
btnDispUserSearchWin.place(x=80, y=400)

#8 btnDispReportsWin to invoke myReportsWin(root) method
btnDispReportsWin=Button(root, text="Reports Window", w=30,
                         command=lambda:myReportsWin(root))
btnDispReportsWin.place(x=80, y=450)

#9 btnExit 
btnExit=Button(root, text="Exit", w=30,
               command=root.destroy)
btnExit.place(x=80,y=500)

#databaseTblWin(root)
#moveText()
myTime()
myDate(dateStrVar)

root.mainloop()