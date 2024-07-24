import tkinter as tk
from tkinter import scrolledtext
import json
import random
import time

def center_window(width, height, window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def start_learning_program():
    words_json_path = '/Users/eva/Desktop/M-Agent/data/words/vocab.json'
    with open(words_json_path, 'r', encoding='utf-8') as f:
        vocab_list = json.load(f)
    
    # 创建原始列表的副本
    vocab_list_copy = vocab_list.copy()
    
    # 打乱副本中的单词顺序
    random.shuffle(vocab_list_copy)
    
    words_to_learn = [word for word in vocab_list_copy if word["memory"] == "No"]
    current_index = 0

    def learn_word():
        if current_index < len(words_to_learn):
            word = words_to_learn[current_index]["word"]
            word_label.config(text=word)
            mean_text.delete('1.0', tk.END)  # 清空之前的单词意思
            helping_text_label.pack_forget()  # 隐藏帮助文本
            progress_label.config(text=f"Progress: {current_index + 1}/{len(words_to_learn)}")
            
            window.wait_variable(show_mean)
            word_mean = words_to_learn[current_index]["helping_text"]
            mean_text.insert(tk.END, word_mean)  # 在单词正下方显示意思
            helping_text = words_to_learn[current_index]["mean"]
            helping_text_label.config(text=helping_text)
            helping_text_label.pack(pady=10)  # 显示帮助文本
            
            input_entry.pack(pady=10)
            input_entry.focus_set()
        else:
            word_label.config(text="Congratulations! You've finished learning!")
            mean_text.delete('1.0', tk.END)
            helping_text_label.pack_forget()
            progress_label.config(text="")
            input_entry.pack_forget()
            time.sleep(2)
            on_closing()

    def check_input(event):
        user_input = input_entry.get().strip().upper()
        word = words_to_learn[current_index]["word"]
        for item in vocab_list:
            if item["word"] == word:
                if 'Y' in user_input:
                    item["memory"] = "Yes"
                    with open(words_json_path, 'w', encoding='utf-8') as f:
                        json.dump(vocab_list, f, ensure_ascii=False, indent=4)
                else:
                    item["memory"] = "No"
                break
        next_word()

    def next_word():
        nonlocal current_index
        input_entry.delete(0, tk.END)
        input_entry.pack_forget()
        
        current_index += 1
        learn_word()

    window = tk.Tk()
    window.title("Word Learning Program")
    center_window(900, 400, window)

    word_label = tk.Label(window, text="", font=("Helvetica", 48))
    word_label.pack(pady=20)

    mean_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Helvetica", 24), height=3)
    mean_text.pack(pady=10)

    helping_text_label = tk.Label(window, text="", font=("Helvetica", 14))
    helping_text_label.pack_forget()  # 初始化时隐藏帮助文本

    progress_label = tk.Label(window, text="", font=("Helvetica", 12))
    progress_label.pack(pady=10)

    show_mean = tk.BooleanVar()
    window.bind("<Key-space>", lambda event: show_mean.set(True))

    def on_closing():
        window.quit()
        window.destroy()

    input_entry = tk.Entry(window, font=("Helvetica", 14))
    input_entry.bind('<Return>', check_input)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.bind('<Control-q>', lambda event: on_closing())

    learn_word()
    window.mainloop()

if __name__ == "__main__":
    start_learning_program()
