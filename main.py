import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1
from utils import get_mp3_length

class MP3MetadataEditor:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('MP3 Metadata Editor')

        #Folder selection
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(frame, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=10)
        self.browse_button = tk.Button(frame, text='Browse', command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT)

        #Listbox displaying .mp3 files
        self.file_listbox = tk.Listbox(self.root, width=100, activestyle='none')
        self.file_listbox.pack(pady=10)
        self.file_listbox.bind('<<ListboxSelect>>', self.load_metadata)

        #Metadata fields
        self.title_var = tk.StringVar()
        self.artist_var = tk.StringVar()
        self.filename_var = tk.StringVar()

        self.mp3_files: List[str] = []

        label_texts = ["Title", "Contributing artists", "Filename"]
        string_vars = [self.title_var, self.artist_var, self.filename_var]
        for label_text, string_var in zip(label_texts, string_vars):
            self.add_entry(label_text, string_var)

        self.save_button = tk.Button(self.root, text='Save', command=self.edit_metadata)
        self.save_button.pack(pady=10)

    def add_entry(self, label_text: str, text_variable: tk.StringVar) -> None:
        tk.Label(self.root, text=label_text).pack()
        entry = tk.Entry(self.root, textvariable=text_variable, width=50)
        entry.pack(pady=2)
            
    def browse_folder(self) -> None:
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.list_mp3_files(folder_selected)
        
    def add_mp3_file(self, folder_path: str, file_name: str) -> None:
        file_path = os.path.join(folder_path, file_name)
        self.mp3_files.append(file_path)
        audio = MP3(file_path, ID3=ID3)
        title = audio.get('TIT2', '')
        artist = audio.get('TPE1', '')
        length = get_mp3_length(audio)
        self.file_listbox.insert(tk.END, f'{file_name} | Title: {title} | Artist: {artist} | Length: {length}')
        

    def list_mp3_files(self, folder_path: str) -> None:
        self.file_listbox.delete(0, tk.END)
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.mp3'):
                self.add_mp3_file(folder_path, file_name)       

    def load_metadata(self, event: tk.Event) -> None:
        selected_index = self.file_listbox.curselection()
        if selected_index:
            file_path = self.mp3_files[selected_index[0]]
            audio = MP3(file_path, ID3=ID3)
            title = audio.get('TIT2', '')
            artist = audio.get('TPE1', '')

            self.title_var.set(str(title))
            self.artist_var.set(str(artist))
            self.filename_var.set(os.path.basename(file_path))
            self.file_path = file_path

    def edit_metadata(self) -> None:
        if hasattr(self, 'file_path'):
            title = self.title_var.get()
            artist = self.artist_var.get()
            filename = self.filename_var.get()

            if not filename.lower().endswith('.mp3'):
                messagebox.showerror("Error", "Filename must end with '.mp3'")
                return

            audio = MP3(self.file_path, ID3=ID3)
            audio['TIT2'] = TIT2(encoding=3, text=title)
            audio['TPE1'] = TPE1(encoding=3, text=artist)
            audio.save()

            if filename != os.path.basename(self.file_path):
                file_path = os.path.join(os.path.dirname(self.file_path), filename)
                os.rename(self.file_path, file_path)
                self.file_path = file_path

            messagebox.showinfo('Success', 'Changes saved')
            self.list_mp3_files(self.folder_path.get())
        else:
            messagebox.showwarning('Error', 'No file selected')

if __name__ == '__main__':
    root = tk.Tk()
    app = MP3MetadataEditor(root)
    root.mainloop()
