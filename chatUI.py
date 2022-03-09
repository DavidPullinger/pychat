from tkinter import *
from tkinter import messagebox
import json
import client


root = Tk()
root.title("ChatApp")
root.geometry("800x600")
#locally stored main info----------
chats = []    #list of chats
chatIDs = []    #list of chat Ids
global mainusername #username of current user
#----------------------------------
#MAIN SCREEN######################################
def funclogin():
    action, body = client.reqLOGIN(uname.get(), psword.get())
    mainusername = uname.get()
    client.send(action, body)  # sends message to server
    body = client.receive()
    if body == "False":
        messagebox.showerror("showerror", "Incorrect login details")
    else:
        flag = True
        body = json.loads(body)
        for i in body:
            # add chats to global chats list
            for j in chatIDs:
                if i.groupId == j:
                    flag = False
            if flag:
                chatIDs.append(i.groupId)
                chats.append(i.groupName)

        chatscreen()


def funccreateacc():
    action, body = client.reqCREATE_ACC(uname.get(), psword.get())
    mainusername = uname.get()
    client.send(action, body)  # send message to server
    if client.receive():
        chatscreen()
        messagebox.showinfo("showinfo", "Account created!")
    else:
        messagebox.showerror("showerror", "USERNAME ALREADY EXISTS")
    return 0


title = Label(root, text="ChatApp", font=("Calibri", 30)).grid(row=0, column=1)
lbluname = Label(root, text="username:").grid(row=1, column=0)
lblpsword = Label(root, text="password:").grid(row=2, column=0)
uname = StringVar()
psword = StringVar()
etryuname = Entry(root, textvariable=uname).grid(row=1, column=1)
etrypsword = Entry(root, textvariable=psword).grid(row=2, column=1)

btnlogin = Button(root, text="Login", command=funclogin).grid(row=3, column=1)
btncreateacc = Button(root, text="Create Account", command=funccreateacc).grid(
    row=4, column=1
)


#CHAT choose SCREEN######################################
#send UPDATE_MSGS regularly
def updatechatoptions():
    drpchats['menu'].delete(0,'end')
    for i in chats:
        drpchats['menu'].add_command(chatscr,chat, *chats,command=lambda chat: openchat(chat))
    

def chatscreen():
    global chatscr
    chatscr = Toplevel()
    chatscr.geometry("800x600")
    chatscr.title("CHATSCREEN")
    btncreategrp = Button(
        chatscr, text="Create New group", command=newchatscreen
    ).pack()
    global chat
    chat = StringVar()
    global drpchats
    drpchats = OptionMenu(
        chatscr, chat, *chats, command=lambda chat: openchat(chat)
    ).pack()


# NEW CHAT SCREEN##################################################
def funccreatechat():
    stripped = [s.strip() for s in participants.get().split(",")]
    action, body = client.reqCREATE_GROUP(grpname.get(), stripped)
    client.send(action, body)  # send message to server
    bod = client.receive()
    if bod == "False":
        messagebox.showerror("showerror", "PARTICIPANTS NOT VALID")
    else:
        #add group to list bod containts group ID
        chats.append(grpname.get())
        
        messagebox.showinfo("showinfo", "Chat Created!")
        
        
        


def newchatscreen():
    newchatscr = Toplevel()
    newchatscr.title("CREAT NEW CHAT")
    newchatscr.geometry("800x600")
    global grpname
    global participants
    grpname = StringVar()
    participants = StringVar()
    lblname = Label(newchatscr, text="Enter name of group").grid(row=0, column=0)
    etryname = Entry(newchatscr, textvariable=grpname).grid(row=0, column=1)
    lblparticipants = Label(
        newchatscr, text="Enter a list of usernames\nSeparated by a ,"
    ).grid(row=1, column=0)
    etryparticipants = Entry(newchatscr, textvariable=participants).grid(
        row=1, column=1
    )
    btncreatechat = Button(newchatscr, text="Create Chat", command=funccreatechat).grid(
        row=2, column=0
    )


# CHAT SCREEN#############################################
def sendmsg(msg):
    print(msg)


def openchat(chatname):
    openchatscr = Toplevel()
    openchatscr.geometry("800x600")
    openchatscr.title("opened chat")
    print(chatname)
    mainframe = LabelFrame(openchatscr)
    mainframe.grid(row=0, column=0, columnspan=3)
    chatbox = Text(mainframe, width=50, height=30)
    chatbox.insert("1.0", "First message in chat")
    # chatbox.grid(row = 0, colum = 0, columnspan=3)
    chatbox.pack(expand=1, fill=BOTH)
    etrymsg = Entry(openchatscr).grid(row=1, column=0, columnspan=2)
    btnsend = Button(openchatscr, text="SEND", command=lambda msg: sendmsg(msg)).grid(
        row=1, column=1, columnspan=2
    )


########################################
# while True:
#    root.update()
#    loop()


root.mainloop()
