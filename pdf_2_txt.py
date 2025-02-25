import pdfplumber
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

exe_path = os.path.dirname(os.path.abspath(sys.argv[0])) 

os.chdir(exe_path)


def pdf_to_txt(pdf_path, txt_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
    except Exception as e:
        messagebox.showerror("Error", f"An Error Occured While Processing: {e}")

def process_pdfs():
    try:
        pdf_files = [file for file in os.listdir() if file.lower().endswith('.pdf')]
        total_files = len(pdf_files)
        
        if total_files == 0:
            messagebox.showinfo("Info", "No PDF File to Process.")
            return

        progress_bar["maximum"] = total_files
        progress_bar["value"] = 0
        status_label.config(text="Processing")
        root.update_idletasks()

        for idx, pdf in enumerate(pdf_files, start=1):
            pdf_path = os.path.join(os.getcwd(), pdf) 
            txt_path = os.path.join(os.getcwd(), f"{os.path.splitext(pdf)[0]}.txt") 
            
            pdf_to_txt(pdf_path, txt_path)
            
            progress_bar["value"] = idx
            status_label.config(text=f"Processing: {pdf}")
            root.update_idletasks() 

        status_label.config(text="Done")
        messagebox.showinfo("Done", "Succesfully Processed.")
    except Exception as e:
        messagebox.showerror("Error", f"An Error Occured: {e}")

root = tk.Tk()
root.title("PDF to TXT Converter")

status_label = tk.Label(root, text="Processing")
status_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

start_button = tk.Button(root, text="Start", command=process_pdfs)
start_button.pack(pady=20)

root.mainloop()