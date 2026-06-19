from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import IntVar
import fetchSongsFromList as ff
from threading import Thread

root = Tk()
root.geometry('320x180')
root.title('Download AniSongs')

def onSelectDirectoryChangeButtonText(directoryButton):
    directory = filedialog.askdirectory()
    if directory:
        directoryButton.config(text=directory)
        toggleDownloadButtonState()

def toggleDownloadButtonState( ):
    if op.get() == 1 or ed.get() == 1 or ins.get() == 1:
        if (RomajRadio.instate(['selected']) or EnglishRadio.instate(['selected'])):
            if filedialogButton.cget("text") != "Browse":
                downloadButton.config(state = "normal")
    else:
        downloadButton.config(state = "disabled")

def onDownloadButtonClick( ):
    downloadStatusLabel.config(text="Download in progress...")
    thread = Thread(target=onDownloadButtonClickThread)
    thread.start()

def onDownloadButtonClickThread( ):
    username = usernameEntry.get()
    listName = listEntry.get()
    songTypes = []
    if OPCheckButton.instate(['selected']):
        songTypes.append("Opening")
    if EDCheckButton.instate(['selected']):
        songTypes.append("Ending")
    if INCheckButton.instate(['selected']):
        songTypes.append("Insert")
    language = "Romaji" if RomajRadio.instate(['selected']) else "English"
    filepath = filedialogButton.cget("text")

    if not username or not listName:
        messagebox.showerror("Error", "Please enter both username and list name.")
        return

    ff.downloadMp3FromUsername_List_SongType_Language(username, listName, songTypes, language, filepath)
    print("Download completed!")
    downloadStatusLabel.config(text="Download completed!")

ttk.Label(root, text = "AniList username:").grid(column = 0, row = 0)
usernameEntry = ttk.Entry(root, width = 30)
usernameEntry.grid(column = 1, row = 0)
ttk.Label(root, text = "List name:").grid(column = 0, row = 1)
listEntry = ttk.Entry(root, width = 30)
listEntry.grid(column = 1, row = 1)
ttk.Label(root, text = "Song type:").grid(column = 0, row = 2)
songTypeFrame = ttk.Frame(root)
songTypeFrame.grid(column = 1, row = 2)
op = IntVar(value=0)
ed = IntVar(value=0)
ins = IntVar(value=0)
OPCheckButton = ttk.Checkbutton(songTypeFrame, text = "OP", command=toggleDownloadButtonState, variable=op)
EDCheckButton = ttk.Checkbutton(songTypeFrame, text = "ED", command=toggleDownloadButtonState, variable=ed)
INCheckButton = ttk.Checkbutton(songTypeFrame, text = "IN", command=toggleDownloadButtonState, variable=ins)
OPCheckButton.grid(column = 0, row = 0, sticky="w")
EDCheckButton.grid(column = 1, row = 0)
INCheckButton.grid(column = 2, row = 0, sticky="e")
ttk.Label(root, text = "Language for filename:").grid(column = 0, row = 3)
languageFrame = ttk.Frame(root)
languageFrame.grid(column = 1, row = 3)
RomajRadio = ttk.Radiobutton(languageFrame, text = "Romaji", value = "Romaji", command=toggleDownloadButtonState)
RomajRadio.grid(column = 0, row = 0)
EnglishRadio = ttk.Radiobutton(languageFrame, text = "English", value = "English", command= toggleDownloadButtonState)
EnglishRadio.grid(column = 1, row = 0)
ttk.Label(root, text = "File path to save songs:").grid(column = 0, row = 4)
filedialogButton = ttk.Button(root, text = "Browse", command = lambda: onSelectDirectoryChangeButtonText(filedialogButton))
filedialogButton.grid(column = 1, row = 4)
downloadButton = ttk.Button(root, text = "Download", command = onDownloadButtonClick, state = "disabled")
downloadButton.grid(column = 0, row = 5)
downloadStatusLabel = ttk.Label(root, text = "")
downloadStatusLabel.grid(column = 1, row = 5)


root.mainloop()   
