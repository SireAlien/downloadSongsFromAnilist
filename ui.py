from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import fetchSongsFromList as ff
from threading import Thread

root = Tk()
root.geometry('320x180')
root.title('Download AniSongs')

def onSelectDirectoryChangeButtonText(directoryButton):
    directory = filedialog.askdirectory()
    if directory:
        directoryButton.config(text=directory)

def onDownloadButtonClick( ):
    downloadStatusLabel.config(text="Download in progress...")
    thread = Thread(target=onDownloadButtonClickThread)
    thread.start()

def onDownloadButtonClickThread( ):
    username = usernameEntry.get()
    listName = listEntry.get()
    songType = songTypeCombo.get()
    language = languageCombo.get()
    filepath = filedialogButton.cget("text")

    if not username or not listName:
        messagebox.showerror("Error", "Please enter both username and list name.")
        return

    ff.downloadMp3FromUsername_List_SongType_Language(username, listName, songType, language, filepath)
    print("Download completed!")
    downloadStatusLabel.config(text="Download completed!")

ttk.Label(root, text = "AniList username:").grid(column = 0, row = 0)
usernameEntry = ttk.Entry(root, width = 30)
usernameEntry.grid(column = 1, row = 0)
ttk.Label(root, text = "List name:").grid(column = 0, row = 1)
listEntry = ttk.Entry(root, width = 30)
listEntry.grid(column = 1, row = 1)
ttk.Label(root, text = "Song type:").grid(column = 0, row = 2)
songTypeCombo = ttk.Combobox(root, values=["ALL", "OP", "ED", "IN"], state="readonly")
songTypeCombo.current(0)
songTypeCombo.grid(column = 1, row = 2)
ttk.Label(root, text = "Language for filename:").grid(column = 0, row = 3)
languageCombo = ttk.Combobox(root, values=["JP", "EN"], state="readonly")
languageCombo.current(0)    
languageCombo.grid(column = 1, row = 3)
ttk.Label(root, text = "File path to save songs:").grid(column = 0, row = 4)
filedialogButton = ttk.Button(root, text = "Browse", command = lambda: onSelectDirectoryChangeButtonText(filedialogButton))
filedialogButton.grid(column = 1, row = 4)
downloadButton = ttk.Button(root, text = "Download", command = onDownloadButtonClick)
downloadButton.grid(column = 0, row = 5)
downloadStatusLabel = ttk.Label(root, text = "")
downloadStatusLabel.grid(column = 1, row = 5)


root.mainloop()   
