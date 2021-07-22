import socket
import threading
from tkinter import *

port=50000
server="192.168.56.1"
address=(server,port)
format="utf-8"

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(address)

class chatbox:
    def __init__(self):
        #chat window which is currently hidden
        self.window=Tk()
        self.window.withdraw()
        #login window for user to add names and connect with server
        self.login=Toplevel()
        #set the title for login window
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        #create a label
        self.label=Label(self.login,text="Please login to continue",justify=CENTER,font="Arial 14 bold")
        self.label.place(relheight=0.15,relx=0.2,rely=0.07)
        self.labelname=Label(self.login,text="Name :  ",font="arial 12")
        self.labelname.place(relheight=0.2,relx=0.1,rely=0.2)
        #entry
        self.entryname=Entry(self.login,font="arial 14")
        self.entryname.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.23)
        #set the focus of the curser
        self.entryname.focus()
        #button
        self.b1=Button(self.login,text="Continue",font="arial 14 bold",command=lambda:self.tochatwindow(self.entryname.get()))
        self.b1.place(relx=0.4,rely=0.55)
        self.window.mainloop()

    def tochatwindow(self,name):
        self.login.destroy()
        self.layout(name)
        #thread created to receive msges
        rcv=threading.Thread(target=self.receive)
        rcv.start()

    #main layout of the chat
    def layout(self,name):
        self.name=name

        # to show chat window
        self.window.deiconify()
        self.window.title("CHAT_ROOM")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=470,height=550,bg="#17282A")
        
        self.labelhead=Label(self.window,bg="#17282A",fg="#EAECEE",text=self.name,font="Helvetica 13 bold",pady=5)
        self.labelhead.place(relwidth=1)
        
        self.line=Label(self.window,width=450,bg="#ABB2B9")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)
        
        self.textcons=Text(self.window,width=20,height=2,bg="#17282A",fg="#EAECEE",font="Helvetica 14",padx=5,pady=5)
        self.textcons.place(relheight=0.745,relwidth=1,rely=0.08)
        
        self.labelbottom=Label(self.window,bg="#ABB2B9",height=80)
        self.labelbottom.place(relwidth=1,rely=0.825)
        
        self.entrymsg=Entry(self.labelbottom,bg="#2C3E58",fg="#EAECEE",font="helvetica 13")
        #place the given window ino thee chat window
        self.entrymsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entrymsg.focus()

        #creating a send button
        self.buttonmsg=Button(self.labelbottom,text="SEND",font="Helvetica 10 bold",bg="#ABB2B9",width=20,command=lambda:self.sendbutton(self.entrymsg.get()))
        self.buttonmsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textcons.config(cursor="arrow")

        #creating scroll bar
        sc=Scrollbar(self.textcons)
        sc.place(relheight=1,relx=0.974)
        sc.config(command=self.textcons.yview)
        self.textcons.config(state=DISABLED)

    def sendbutton(self,msg):
        self.textcons.config(state=DISABLED)
        self.msg=msg
        self.entrymsg.delete(0,END)
        snd=threading.Thread(target=self.sendmessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message=client.recv(1024).decode(format)

                #if the messages from the server is NAME send the clients name
                if message=='NAME':
                    client.send(self.name.encode(format))
                else:
                    #insert messages to text box
                    self.textcons.config(state=NORMAL)
                    self.textcons.insert(END,message+"\n\n")
                    self.textcons.config(state=DISABLED)
                    self.textcons.see(END)

            except:
                #an error will be printed on the comand line or console if there is an error
                print("An error occured !")
                client.close()
                break

    #fuction to send messages
    def sendmessage(self):
        self.textcons.config(state=DISABLED)
        while True:
            message=(f" {self.name} : {self.msg} ")
            client.send(message.encode(format))
            break

#create chatwindow class object
g=chatbox()
