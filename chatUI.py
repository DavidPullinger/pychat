from tkinter import *
from tkinter import messagebox
import json
import tkinter
import client


root = Tk()
root.title("pyChat")
root.resizable(width=False, height=False)


global chats  # list of chats
# MAIN SCREEN######################################
def funclogin():
    action, body = client.reqLOGIN(uname.get(), psword.get())
    client.send(action, body)  # sends message to server
    body = client.receive()
    if body == "False":
        messagebox.showerror("showerror", "Incorrect login details")
    else:
        flag = True
        body = json.loads(body)
        for i in body:
            # add chats to global chats list
            for j in chats:
                if i.groupName == j:
                    flag = False
            if flag:
                chats.append(i.groupName)

        chatscreen()
        root.destroy()


def funccreateacc():
    action, body = client.reqCREATE_ACC(uname.get(), psword.get())
    client.send(action, body)  # send message to server
    if client.receive():
        chatscreen()
        messagebox.showinfo("showinfo", "Account created!")
    else:
        messagebox.showerror("showerror", "USERNAME ALREADY EXISTS")
    return 0


title2 = Label(root, text="Chat", font=("Calibri", 30), fg="#306998").grid(
    row=0, column=0, columnspan=2, padx=(50, 0), pady=(10, 0)
)
title1 = Label(root, text="py", font=("Calibri", 30), fg="#FFE873").grid(
    row=0, column=0, columnspan=2, padx=(0, 50), pady=(10, 0)
)
subtitle = Label(root, text="Chatting made easy as pie", font=("Calibri", 20)).grid(
    row=1, column=0, columnspan=2, padx=(50, 50), pady=(10, 200)
)
lbluname = Label(root, text="Username:").grid(row=2, column=0, padx=(50, 0))
lblpsword = Label(root, text="Password:").grid(row=3, column=0, padx=(50, 0))
uname = StringVar()
psword = StringVar()
etryuname = Entry(root, textvariable=uname).grid(row=2, column=1, padx=(0, 50))
etrypsword = Entry(root, textvariable=psword, show="*").grid(
    row=3, column=1, padx=(0, 50)
)

btnlogin = Button(root, text="Login", command=funclogin).grid(
    row=4, column=0, columnspan=2, pady=(20, 0)
)
btncreateacc = Button(root, text="Create Account", command=funccreateacc).grid(
    row=5, column=0, columnspan=2, pady=(10, 200)
)


# CHAT choose SCREEN######################################
# send UPDATE_MSGS regularly
def chatscreen():
    chatscr = Toplevel()
    btncreategrp = Button(
        chatscr, text="Create New group", command=newchatscreen
    ).pack()
    chat = StringVar()
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
        # add group to list bod containts group ID
        messagebox.showinfo("showinfo", "Group Created!")


def newchatscreen():
    newchatscr = Toplevel()
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
