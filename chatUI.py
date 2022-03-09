from cProfile import label
from cgitb import text
from tkinter import *
from tkinter import messagebox
from tkinter import _setit
import json
import client
import datetime
import time

WIDTH = 375
HEIGHT = 625


root = Tk()
root.title("pyChat")
root.resizable(width=False, height=False)
# center screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (WIDTH / 2))
y_cordinate = int((screen_height / 2) - (HEIGHT / 2))
DIMS = "{}x{}+{}+{}".format(WIDTH, HEIGHT, x_cordinate, y_cordinate)
root.geometry(DIMS)

# locally stored main info----------
chats = ["Chat1", "Chat2"]  # list of chats
chatIDs = ["cID1", "cID2"]  # list of chat Ids
global mainusername  # username of current user

# ----------------------------------
# MAIN SCREEN######################################
def funclogin():
    global mainusername
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
    global mainusername
    action, body = client.reqCREATE_ACC(uname.get(), psword.get())
    mainusername = uname.get()
    client.send(action, body)  # send message to server

    if client.receive():
        # messagebox.showinfo("showinfo", "Account created!")
        root.withdraw()
        chatscreen()
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


def populateChatLabels():
    for i in range(0, len(chats)):
        l = Label(
            chatLabels,
            text=chats[i],
            font=("Calibri", 18),
            width=10,
            borderwidth=2,
            relief="solid",
        )
        l.grid(row=i, column=0, ipadx=50, ipady=10, pady=(0, 10))
        l.bind("<Button-1>", lambda ev: openchat(chats[i]))


def chatscreen():
    global chatscr
    chatscr = Toplevel()
    chatscr.geometry(DIMS)
    chatscr.resizable(width=False, height=False)
    title = Label(
        chatscr,
        text="Chats",
        font=("Calibri", 30),
    ).grid(row=0, column=0, padx=(140, 140), pady=(10, 20))
    global chat
    chat = StringVar()
    global chatLabels
    chatLabels = Frame(chatscr)
    chatLabels.grid(row=1, column=0)
    populateChatLabels()

    chatscr.grid_rowconfigure(len(chats), weight=1)
    btncreategrp = Button(
        chatscr,
        text="Start new chat",
        command=newchatscreen,
    ).grid(row=len(chats) + 1, column=0, pady=(10, 20))


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
        chats.append(grpname.get())
        populateChatLabels()
        newchatscr.destroy()


def newchatscreen():
    global newchatscr
    newchatscr = Toplevel()
    newchatscr.geometry(DIMS)
    newchatscr.resizable(False, False)
    global grpname
    global participants

    grpname = StringVar()
    participants = StringVar()

    title = Label(
        newchatscr,
        text="Start new chat",
        font=("Calibri", 30),
    ).grid(row=0, column=0, pady=(10, 20), padx=(95, 95))

    lblname = Label(newchatscr, text="Enter name of group:").grid(
        row=1, column=0, pady=(180, 0)
    )
    etryname = Entry(newchatscr, textvariable=grpname).grid(
        row=2,
        column=0,
    )
    lblparticipants = Label(
        newchatscr, text="Enter a list of usernames\nseparated by a comma:"
    ).grid(row=3, column=0, pady=(20, 0))
    etryparticipants = Entry(newchatscr, textvariable=participants).grid(
        row=4, column=0
    )
    btncreatechat = Button(newchatscr, text="Create Chat", command=funccreatechat).grid(
        row=5, column=0, pady=(10, 0)
    )


# CHAT SCREEN#############################################
def sendmsg():
    global currentChatId
    global mainusername
    global chatbox
    global etrymsg
    global msg

    action, body = client.reqSEND_MSG(currentChatId, mainusername, msg.get())
    client.send(action, body)

    # still need to clear entry box
    chatbox.insert(
        "end",
        mainusername
        + " at "
        + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + " : "
        + msg.get()
        + "\n",
    )
    chatbox.pack(expand=1, fill=BOTH)
    etrymsg.delete(0, END)


def openchat(chatname):

    global currentChatId
    global mainusername
    global chatbox
    global etrymsg
    global msg
    msg = StringVar()

    # loop to find current chat ID from chatID list
    for i in range(len(chats)):
        if chatname == chats[i]:
            currentChatId = chatIDs[i]

    # initialize chat screen----------
    openchatscr = Toplevel()
    openchatscr.resizable(False, False)
    openchatscr.geometry(DIMS)
    # --------------------------------

    # send request for update of all messages
    # send current date and time
    action, body = client.reqUPDATE_MSGS(
        mainusername, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    client.send(action, body)  # sending message to server
    # ---------------------------------------

    # receive response
    recievedmessage = client.receive()
    while recievedmessage == "":
        start_time = time.time()
        client.send(action, body)
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > 10:
                break
        recievedmessage = client.receive()

    # ------------------

    msglist = [
        {
            "groupId": "grup1",
            "groupName": "coolgroup",
            "content": "you guys are cool",
            "sender": "niv",
            "sentTime": "2022-03-09 20:03:00",
        },
        {
            "groupId": "grup1",
            "groupName": "coolgroup",
            "content": "you guys are not cool at all lorem ipsum dolar sit amet",
            "sender": "niv",
            "sentTime": "2022-03-09 20:03:00",
        },
        {
            "groupId": "grup1",
            "groupName": "coolgroup",
            "content": "inshallah... hehehe siuuuu",
            "sender": "david00",
            "sentTime": "2022-03-09 20:03:00",
        },
    ]  # json.loads(recievedmessage)

    mainframe = LabelFrame(openchatscr)
    mainframe.grid(row=0, column=0, columnspan=2)
    chatbox = Text(mainframe, width=51, height=40, wrap="word")
    chatbox.tag_config("time", foreground="yellow")
    chatbox.config(spacing2=5)
    # adds all messages to chatbox----------------------
    for i in msglist:
        index = chatbox.index("end")
        chatbox.insert(
            index,
            i["sender"] + " at " + i["sentTime"] + ":\t" + i["content"] + "\n\n",
        )
        index = str((int)(index[: index.index(".")]) - 1) + "."
        lengthOfInfo = len(i["sender"] + " at " + i["sentTime"] + " :")
        chatbox.tag_add("time", index + "0", index + str(lengthOfInfo))
        chatbox.pack(expand=1, fill=BOTH)

    # --------------------------------------------------
    global etrymsg
    etrymsg = Entry(openchatscr, width=30, textvariable=msg)
    etrymsg.grid(row=1, column=0, pady=(10, 0))
    btnsend = Button(openchatscr, text="SEND", command=lambda: sendmsg()).grid(
        row=1, column=1, pady=(10, 0)
    )


root.mainloop()
