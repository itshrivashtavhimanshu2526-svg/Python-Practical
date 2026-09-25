import tkinter as tk
from tkinter import filedialog, messagebox
import re
from pypdf import PdfReader

STOP = {"is", "am", "are", "the", "and", "to", "in", "for", "with", "a", "an", "of", "on", "at", "as", "by"}
files = {"res": "", "jd": ""}

def read_file(path):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_words(key, label):
    path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.txt")])
    if path:
        text = read_file(path)
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        files[key] = {w for w in words if w not in STOP}
        label.config(text=path.split("/")[-1], fg="green")

def check():
    if not files["res"] or not files["jd"]:
        messagebox.showwarning("Warning", "Dono files (PDF/TXT) select karein!")
        return
    matched = files["jd"] & files["res"]
    missing = files["jd"] - files["res"]
    score = (len(matched) / len(files["jd"])) * 100
    lbl_res.config(text=f"Score: {score:.1f}%\n\nMatched: {', '.join(matched) or 'None'}\n\nMissing: {', '.join(missing) or 'None'}")

root = tk.Tk()
root.title("ATS PDF Matcher")
root.geometry("420x400")

lbl1 = tk.Label(root, text="Resume: No file", fg="gray")
lbl2 = tk.Label(root, text="JD: No file", fg="gray")

tk.Button(root, text="Upload Resume (PDF/TXT)", command=lambda: load_words("res", lbl1)).pack(pady=8)
lbl1.pack()

tk.Button(root, text="Upload JD (PDF/TXT)", command=lambda: load_words("jd", lbl2)).pack(pady=8)
lbl2.pack()

tk.Button(root, text="Match Score", command=check, bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
lbl_res = tk.Label(root, text="Score: 0%", justify=tk.LEFT, wraplength=380)
lbl_res.pack(pady=10)

root.mainloop()
