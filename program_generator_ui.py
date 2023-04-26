"""
@author: Lakshmi Dinesh
All GUI operations of the application are done in this class.
Input data are the user inputs
"""

import subprocess
import tkinter as t
from tkinter import filedialog
from tkinter import ttk
from program_generator_constants import LVL_QUESTIONS, TOPICS, PREFIX, POSTFIX, DEBUG_CONSOLE_LOG
from program_generator_utils import *


class ProgramGeneratorGUI:
    def __init__(self, parent, engine):
        self.num_q = 0
        self.dir_path = None
        self.topic = None
        self.prompt = None
        self.u_name = None

        self.GPT_engine = engine
        self.level = list(LVL_QUESTIONS)[0]
        self.lang = list(TOPICS)[0]

        root = parent
        root.title("Programming questions generator")
        root.geometry("500x450")
        frame = t.Frame(root, bg="white")
        frame.pack()

        info_frame = t.LabelFrame(frame, text="User Details", padx=5, pady=10)
        info_frame.grid(row=0, column=0, sticky='news')

        f_name_label = t.Label(info_frame, text='First name', padx=5, pady=10)
        f_name_label.grid(row=0, column=0)
        self.f_name = t.Entry(info_frame)
        self.f_name.grid(row=0, column=1)

        l_name_label = t.Label(info_frame, text="Last name", padx=5, pady=10)
        l_name_label.grid(row=0, column=2)
        self.l_name = t.Entry(info_frame)
        self.l_name.grid(row=0, column=3)

        course_frame = t.LabelFrame(frame, text="Course details", padx=5, pady=10)
        course_frame.grid(row=1, column=0, sticky='news')

        lang_label = t.Label(course_frame, text="Language", padx=5, pady=10)
        lang_label.grid(row=0, column=0)

        lang_cbox = ttk.Combobox(course_frame, values=list(TOPICS))
        lang_cbox.current(0)
        lang_cbox.grid(row=0, column=1)
        lang_cbox.bind("<<ComboboxSelected>>", self.callback_lang_cbox)

        level_label = t.Label(course_frame, text="Level", padx=5, pady=10)
        level_label.grid(row=0, column=2)

        self.level_cbox = ttk.Combobox(course_frame, values=list(LVL_QUESTIONS))
        self.level_cbox.current(0)
        self.level_cbox.grid(row=0, column=3)
        self.level_cbox.bind("<<ComboboxSelected>>", self.callback_level_cbox)

        q_label = t.Label(course_frame, text="Questions", padx=5, pady=10)
        q_label.grid(row=1, column=0)

        self.q_num_spinbox = t.Spinbox(course_frame, from_=1, to=10)
        self.q_num_spinbox.grid(row=1, column=1)

        topic_label = t.Label(course_frame, text="Topics", padx=5, pady=10)
        topic_label.grid(row=1, column=2)

        self.course_list = t.Listbox(course_frame)
        self.course_list.grid(row=1, column=3)
        self.course_list.configure(width=25, height=9)
        self.populate_listbox()

        self.generate_btn = t.Button(frame, text="Generate questions",
                                     command=self.callback_generate_btn,
                                     bg="#FCE5CA", activebackground="blue")
        self.generate_btn.grid(row=2, column=0, sticky='news', pady=5)

        progress_frame = t.LabelFrame(frame, text="Progress", padx=5, pady=10)
        progress_frame.grid(row=3, column=0, sticky='news')

        style = t.ttk.Style()
        style.theme_use('default')
        style.configure('blue.Horizontal.TProgressbar', background='blue', troughcolor='white')
        self.p_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode='determinate', length=300,
                                     style='blue.Horizontal.TProgressbar')
        self.p_bar.grid(row=0, column=0, sticky='news', pady=5, padx=10)

        self.folder_browse_btn = t.Button(progress_frame, text="Browse",
                                          command=self.callback_browse_btn,
                                          bg="#FCE5CA", activebackground="blue")
        self.folder_browse_btn.grid(row=0, column=1, sticky='news', pady=5, padx=10)
        self.folder_browse_btn.configure(state="disabled")

    def populate_listbox(self):
        for item in TOPICS[self.lang][self.level]:
            self.course_list.insert('end', item)

    def callback_lang_cbox(self, event):
        self.lang = event.widget.get()
        if self.course_list.size() > 0:
            self.course_list.delete(0, 'end')
        self.populate_listbox()

    def callback_level_cbox(self, event):
        self.level = event.widget.get()
        if self.course_list.size() > 0:
            self.course_list.delete(0, 'end')
        self.populate_listbox()
        self.update_q_nums()

    def update_q_nums(self):
        self.q_num_spinbox.configure(values=LVL_QUESTIONS[self.level])

    def callback_generate_btn(self):
        fn = self.f_name.get()
        ln = self.l_name.get()

        if validate_name(fn, ln) and self.validate_topic():
            self.p_bar['value'] += 10
            self.folder_browse_btn.config(state='disabled')
            self.u_name = "{}_{}".format(fn.title(), ln.title())
            self.form_gpt_prompt()
            self.generate_btn.config(state='disabled')
            self.dir_path = create_dir_path(self.lang, self.level, self.topic)
            file_name = create_file_name()
            file_path = create_file_path(self.dir_path, file_name)

            self.GPT_engine.set_gpt_params(file_path, self.num_q, self.format_log())
            self.p_bar['value'] += 20
            response = self.GPT_engine.generate_questions(self.prompt)

            if response:
                self.p_bar['value'] += 70
                if DEBUG_CONSOLE_LOG:
                    print("GPT response received, file created")
                mb.showinfo("File created", "File created at\n" + file_path)
                self.p_bar['value'] = 0
                self.generate_btn.config(state='normal')
                self.folder_browse_btn.config(state='normal')
            else:
                mb.showerror("Error", "GPT response error!\nCheck your connection and try again later!")
                self.p_bar['value'] = 0
                self.generate_btn.config(state='normal')

    def validate_topic(self):
        try:
            topic_index = self.course_list.curselection()
            if not topic_index:
                show_message('Error', 'Please select a Topic!')
                return False
            self.topic = TOPICS[self.lang][self.level][topic_index[0]]
        except IndexError:
            mb.showerror("Error", "Topic list empty\nRestart application!")
            return False
        except t.TclError:
            mb.showerror("Error", "Issue with Tcl interpreter")
            return False
        return True

    def form_gpt_prompt(self):
        self.num_q = int(self.q_num_spinbox.get())
        lvl_list = list(LVL_QUESTIONS)
        if self.level == lvl_list[3]:
            q = self.num_q // 3
            basic = "{} {}".format(str(q), lvl_list[0])
            intermediate = "{} {}".format(str(q), lvl_list[1])
            advanced = "{} {}".format(str(q), lvl_list[2])
            q_lvl = "{}, {} and {}".format(basic, intermediate, advanced)
        else:
            q_lvl = "{} {}".format(str(self.num_q), self.level)
        self.prompt = "{}{}{}{} {}".format(PREFIX, q_lvl, POSTFIX, self.lang, self.topic)

    def format_log(self):
        log_str = "{} : {}".format(self.u_name, self.prompt)
        if DEBUG_CONSOLE_LOG:
            print(log_str)
        return log_str

    def callback_browse_btn(self):
        file = filedialog.askopenfilename(initialdir=self.dir_path, title="Browse")
        if file:
            try:
                subprocess.Popen("notepad " + file)
            except OSError:
                mb.showerror("Error", "Operating system error opening file")
            except Exception as e:
                mb.showwarning("Error", "Error trying to open file in notepad")
                print(f"Error trying to open file in notepad: {e}")
                traceback.print_exc()
