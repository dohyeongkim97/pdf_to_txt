import pdfplumber
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

exe_path = os.path.dirname(os.path.abspath(sys.argv[0])) 

os.chdir(exe_path)


# PDF를 텍스트로 변환하는 함수
def pdf_to_txt(pdf_path, txt_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
    except Exception as e:
        messagebox.showerror("오류", f"파일 처리 중 오류가 발생했습니다: {e}")

# 진행 상황을 업데이트하는 함수
def process_pdfs():
    try:
        # 현재 작업 디렉토리에서 PDF 파일 목록 가져오기
        pdf_files = [file for file in os.listdir() if file.lower().endswith('.pdf')]
        total_files = len(pdf_files)
        
        if total_files == 0:
            messagebox.showinfo("정보", "변환할 PDF 파일이 없습니다.")
            return

        # 진행 표시줄 초기화
        progress_bar["maximum"] = total_files
        progress_bar["value"] = 0
        status_label.config(text="파일 처리 준비 중...")
        root.update_idletasks()

        # 각 PDF 파일에 대해 처리 진행
        for idx, pdf in enumerate(pdf_files, start=1):
            pdf_path = os.path.join(os.getcwd(), pdf)  # 현재 작업 디렉토리에서 PDF 파일 경로 생성
            txt_path = os.path.join(os.getcwd(), f"{os.path.splitext(pdf)[0]}.txt")  # 출력할 텍스트 파일 경로
            
            # PDF 파일을 텍스트로 변환
            pdf_to_txt(pdf_path, txt_path)
            
            # 진행 바 업데이트 및 현재 파일명 표시
            progress_bar["value"] = idx
            status_label.config(text=f"처리 중: {pdf}")
            root.update_idletasks()  # GUI 업데이트

        status_label.config(text="모든 파일 처리 완료!")
        messagebox.showinfo("완료", "모든 파일이 성공적으로 처리되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"파일 목록을 가져오는 중 오류가 발생했습니다: {e}")

# GUI 설정
root = tk.Tk()
root.title("PDF to TXT Converter")

# 파일 처리 상태 표시
status_label = tk.Label(root, text="파일을 처리 중입니다...")
status_label.pack(pady=10)

# 진행 표시줄
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

# 시작 버튼
start_button = tk.Button(root, text="PDF 변환 시작", command=process_pdfs)
start_button.pack(pady=20)

# GUI 창 실행
root.mainloop()