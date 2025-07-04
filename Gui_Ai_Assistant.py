# GUI AI Assistant
# Modified on 4/7/25
# Created By HK (Harshk Khandal) Hacker


#Import
from ollama import chat
from ollama import ChatResponse
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import subprocess
import webbrowser

#Initial Variables
flag=False

#Ollama Install
try :
    result = subprocess.run("ollama", capture_output=True, text=True, check=True)
except :
    def downloadollama():
        webbrowser.open("https://ollama.com/download")


    notollama = Tk()
    notollama.geometry("300x150")
    notollama.resizable(0,0)
    
    try:    
        icon=PhotoImage(file='img.png')
        notollama.iconphoto(True, icon)
    except Exception as e:
        pass
    
    notollama.config(background="lightyellow")
    notollama.title("Download Ollama!!")

    Label(notollama, text="Warning : Ollama Not Found", background="lightyellow", font=("",12,"bold")).place(x=150,y=35,anchor=CENTER)
    download=Button(text="Download Now!", command=downloadollama, height=2, width=15,background="Green", font=("",11,"bold"), foreground="white")
    download.place(x=150,y=100,anchor=CENTER)

    notollama.mainloop()
    exit()


#Prompt
history=[{
    "role":"system",
    "content":"You are a precise, thoughtful AI assistant. Give short responses."
}]

#defs
def start():                                       #Run after select button
    MSG.config(state=NORMAL, background="White")
    Submit.config(state=NORMAL)
    Add.config(state=NORMAL)

def file():                                        #To open File after + Button
    global filelocation
    global content
    
    def fileread(fileloc):
        global flag

        flag=True

        if fileloc.endswith(('.txt')):
            with open(fileloc, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            messagebox.showwarning("No Supported File Format", "Selected file format is NOT Supported by our program!!")


    filetype = [("Text", "*.txt")]

    filelocation = filedialog.askopenfilename(filetypes=filetype)
    content = fileread(filelocation)



def choosemodel():                                 #Choose Model Among the available ones
    global model

    chatbox.config(state=NORMAL)
    chatbox.delete("1.0",END)
    chatbox.insert("1.0","\n")
    chatbox.config(state=DISABLED)
    preinstalled=subprocess.check_output(["ollama","list"],text=True)
    if dropdown.get() == "gemma3:1b (Smallest)":
        if not 'gemma3:1b' in preinstalled.lower():
            yes_no = messagebox.askyesno("Download gemma3:1b Ollama Model","Gemma3:1b Not found. Would you like to install?")
            if yes_no:
                subprocess.run("ollama pull gemma3:1b")
            else:
                exit()
        startollamainbg = subprocess.Popen("ollama run gemma3:1b", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        model = 'gemma3:1b'
        start()

    elif dropdown.get() == "gemma3 (Recommended)":
        if not 'gemma3:latest' in preinstalled.lower():
            yes_no = messagebox.askyesno("Download gemma3 Ollama Model","Gemma3 Not found. Would you like to install?")
            if yes_no:
                subprocess.run("ollama pull gemma3")
            else:
                exit()
        startollamainbg = subprocess.Popen("ollama run gemma3", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        model = 'gemma3'
        start()

    elif dropdown.get() == "deepseek-r1":
        if not 'deepseek-r1' in preinstalled.lower():
            yes_no = messagebox.askyesno("Download deepseek-r1 Ollama Model","Deepseek-r1 Not found. Would you like to install?")
            if yes_no:
                subprocess.run("ollama pull deepseek-r1")
            else:
                exit()
        startollamainbg = subprocess.Popen("ollama run deepseek-r1", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        model = 'deepseek-r1'
        start()

    else:
        messagebox.showwarning("No Option Selected","Please Select an Option.")

def ai():                                              #Main Part (Request & Response)
    global flag

    if len(MSG.get(1.0,END)) > 1:
        inp=MSG.get(1.0,END)
        inp=inp.strip()
        MSG.delete(1.0, END)

        if not flag : 
            chatbox.config(state=NORMAL)
            chatbox.insert(END, " You : " + inp)

            message={"role":"user", "content":inp}
            history.append(message)

            response: ChatResponse = chat(model='gemma3', messages=history)

            history.append({"role": "assistant", "content": response['message']['content']})

            out = "\n AI : " + response['message']['content']

            chatbox.insert(END, out + "\n\n")
            chatbox.config(state=DISABLED)

        if flag : 
            chatbox.config(state=NORMAL)
            chatbox.insert(END, " You : " + inp + " " +filelocation)

            prompt = f"The user uploaded this file:\n\n{content}\n\nNow the user says:\n{inp}"

            message = {"role": "user", "content": prompt}       
            history.append(message)

            response: ChatResponse = chat(model=model, messages=history)

            history.append({"role": "assistant", "content": response['message']['content']})

            out = "\n AI : " + response['message']['content']

            chatbox.insert(END, out + "\n\n")
            chatbox.config(state=DISABLED)

            flag = False

#Main Window
win=Tk()

win.config(background="lightblue")

win.geometry('750x450')
win.resizable(0,0)

try:
    icon=PhotoImage(file='img.png')
    win.iconphoto(True, icon)
except Exception as e:
    pass

win.title("AI Assistant")

Heading=Label(text="Personal AI Assistant", background="lightblue", font=("",20,"bold","italic"))

Heading.place(x=375, y=25, anchor=CENTER)

chatbox=Text(win, state=NORMAL, height=18, width=90, background="LightGrey")
chatbox.place(x=375, y=100, anchor=N)

#banner
chatbox.insert("1.0",
r'''
     ___  ___  ___  __       
    |\  \|\  \|\  \|\  \     
    \ \  \\\  \ \  \/  /|_   
     \ \   __  \ \   ___  \  
      \ \  \ \  \ \  \\ \  \ 
       \ \__\ \__\ \__\\ \__\
        \|__|\|__|\|__| \|__|
                         
''')

chatbox.config(state=DISABLED)

MSG=Text(win, state=DISABLED, height=2, width=70, background="LightGrey")
MSG.place(x=14, y=400, anchor=NW)

Submit=Button(win, text="Submit", command=ai , background="Green", foreground="White", font=("",13,'bold'), state=DISABLED)

Submit.place(x=736, y=400, anchor=NE, height=35, width=110)

Add=Button(win, text="+", command=file , background="grey", foreground="White", font=("",13,'bold'), state=DISABLED)
Add.place(x=582, y=400, anchor=NW, height=35, width=40)

dropdown=ttk.Combobox(win,values=["gemma3:1b (Smallest)","gemma3 (Recommended)","deepseek-r1"], width=25, state="readonly")
dropdown.set("Select Option")
dropdown.place(x=370,y=60, anchor=E)

choose=Button(win, text="Select Model", command=choosemodel, background="Green", width=25, foreground="White")
choose.place(x= 380, y=60, anchor=W)

win.mainloop()

# GUI AI Assistant
# Modified on 4/7/2025
# Created By HK (Harshk Khandal) Hacker