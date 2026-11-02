import tkinter as tk
from tkinter import ttk, messagebox
import time


class UniversalTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Timer")
        self.root.geometry("500x500")

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 20, "bold"))
        style.configure("Big.TLabel", font=("Courier New", 30, "bold"))

        self.container = ttk.Frame(root)
        self.container.pack(expand=True, fill='both')

        self.create_main_menu()
        self.create_timer_view()
        self.create_stopwatch_view()
        self.create_pomodoro_view()

        self.show_main_menu()


    def show_main_menu(self):

        self.frame_timer.pack_forget()
        self.frame_stopwatch.pack_forget()
        self.frame_pomodoro.pack_forget()


        self.frame_menu.pack(expand=True, fill='both')

    def show_tool(self, tool_frame):

        self.frame_menu.pack_forget()
        tool_frame.pack(expand=True, fill='both')

    def create_main_menu(self):
        self.frame_menu = ttk.Frame(self.container)

        lbl_title = ttk.Label(self.frame_menu, text="MAIN MENU", style="Header.TLabel")
        lbl_title.pack(pady=(80, 40))

        btn_timer = ttk.Button(self.frame_menu, text="1. Timer", command=lambda: self.show_tool(self.frame_timer))
        btn_timer.pack(pady=10, ipadx=20, ipady=5)

        btn_stopwatch = ttk.Button(self.frame_menu, text="2. Stopwatch",
                                   command=lambda: self.show_tool(self.frame_stopwatch))
        btn_stopwatch.pack(pady=10, ipadx=20, ipady=5)

        btn_pomo = ttk.Button(self.frame_menu, text="3. Pomodoro", command=lambda: self.show_tool(self.frame_pomodoro))
        btn_pomo.pack(pady=10, ipadx=20, ipady=5)

        btn_exit = ttk.Button(self.frame_menu, text="4. Exit", command=self.root.quit)
        btn_exit.pack(pady=10, ipadx=20, ipady=5)

    def create_timer_view(self):
        self.frame_timer = ttk.Frame(self.container)

        ttk.Button(self.frame_timer, text="← Main Menu", command=self.show_main_menu).pack(anchor='nw', padx=10,
                                                                                           pady=10)
        self.timer_running = False
        self.timer_paused = False
        self.timer_seconds = 0
        self.timer_speed_delay = 1000
        self.timer_start_val = 0

        ttk.Label(self.frame_timer, text="-- TIMER --", style="Header.TLabel").pack(pady=10)

        frame_input = ttk.Frame(self.frame_timer)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Seconds:").grid(row=0, column=0, padx=5)
        self.entry_timer = ttk.Entry(frame_input, width=10)
        self.entry_timer.grid(row=0, column=1, padx=5)

        frame_speed = ttk.LabelFrame(self.frame_timer, text="Speed")
        frame_speed.pack(pady=5)
        self.speed_var = tk.IntVar(value=1)
        ttk.Radiobutton(frame_speed, text="Normal", variable=self.speed_var, value=1, command=self.set_speed).pack(
            side='left', padx=10)
        ttk.Radiobutton(frame_speed, text="Fast", variable=self.speed_var, value=2, command=self.set_speed).pack(
            side='left', padx=10)
        ttk.Radiobutton(frame_speed, text="V. Fast", variable=self.speed_var, value=3, command=self.set_speed).pack(
            side='left', padx=10)

        self.lbl_timer_display = ttk.Label(self.frame_timer, text="00:00:00", style="Big.TLabel")
        self.lbl_timer_display.pack(pady=20)

        frame_btns = ttk.Frame(self.frame_timer)
        frame_btns.pack(pady=5)
        ttk.Button(frame_btns, text="Start", command=self.start_timer).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Pause", command=self.pause_timer).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Resume", command=self.resume_timer).grid(row=0, column=2, padx=5)
        ttk.Button(frame_btns, text="Stop", command=self.stop_timer).grid(row=0, column=3, padx=5)

        ttk.Label(self.frame_timer, text="History:").pack(pady=(10, 0))
        self.txt_timer_history = tk.Text(self.frame_timer, height=4, width=40, state='disabled')
        self.txt_timer_history.pack(pady=5)

    def set_speed(self):
        choice = self.speed_var.get()
        if choice == 1:
            self.timer_speed_delay = 1000
        elif choice == 2:
            self.timer_speed_delay = 500
        elif choice == 3:
            self.timer_speed_delay = 100

    def format_time(self, total_seconds):
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"

    def update_timer(self):
        if self.timer_running and not self.timer_paused and self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.lbl_timer_display.config(text=self.format_time(self.timer_seconds))
            if self.timer_seconds == 0:
                self.timer_running = False
                messagebox.showinfo("Timer", "Time's Up!")
                self.log_timer_history()
            else:
                self.root.after(self.timer_speed_delay, self.update_timer)

    def start_timer(self):
        if self.timer_running: return
        try:
            t = int(self.entry_timer.get())
            if t <= 0: raise ValueError
            self.timer_seconds = t
            self.timer_start_val = t
            self.timer_running = True
            self.timer_paused = False
            self.lbl_timer_display.config(text=self.format_time(self.timer_seconds))
            self.update_timer()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of seconds > 0")

    def pause_timer(self):
        if self.timer_running: self.timer_paused = True

    def resume_timer(self):
        if self.timer_running and self.timer_paused:
            self.timer_paused = False
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.lbl_timer_display.config(text="00:00:00")

    def log_timer_history(self):
        self.txt_timer_history.config(state='normal')
        self.txt_timer_history.insert('end', f"Completed: {self.timer_start_val} sec\n")
        self.txt_timer_history.see('end')
        self.txt_timer_history.config(state='disabled')

    def create_stopwatch_view(self):
        self.frame_stopwatch = ttk.Frame(self.container)

        ttk.Button(self.frame_stopwatch, text="← Main Menu", command=self.show_main_menu).pack(anchor='nw', padx=10,
                                                                                               pady=10)

        ttk.Label(self.frame_stopwatch, text="-- STOPWATCH --", style="Header.TLabel").pack(pady=10)

        self.sw_running = False
        self.sw_start_time = None
        self.sw_elapsed = 0.0
        self.sw_laps = []

        self.lbl_sw_display = ttk.Label(self.frame_stopwatch, text="00:00:00.00", style="Big.TLabel")
        self.lbl_sw_display.pack(pady=20)

        frame_btns = ttk.Frame(self.frame_stopwatch)
        frame_btns.pack(pady=10)
        ttk.Button(frame_btns, text="Start", command=self.sw_start).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btns, text="Stop", command=self.sw_stop).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btns, text="Lap", command=self.sw_lap).grid(row=0, column=2, padx=5)
        ttk.Button(frame_btns, text="Reset", command=self.sw_reset).grid(row=0, column=3, padx=5)

        ttk.Label(self.frame_stopwatch, text="Laps:").pack(pady=(10, 0))
        self.txt_sw_laps = tk.Text(self.frame_stopwatch, height=6, width=40, state='disabled')
        self.txt_sw_laps.pack(pady=5)

    def sw_update(self):
        if self.sw_running:
            now = time.time()
            total_time = self.sw_elapsed + (now - self.sw_start_time)

            minutes = int(total_time // 60)
            seconds = int(total_time % 60)
            centiseconds = int((total_time * 100) % 100)
            self.lbl_sw_display.config(text=f"{minutes:02}:{seconds:02}.{centiseconds:02}")

            self.root.after(50, self.sw_update)

    def sw_start(self):
        if not self.sw_running:
            self.sw_start_time = time.time()
            self.sw_running = True
            self.sw_update()

    def sw_stop(self):
        if self.sw_running:
            self.sw_elapsed += time.time() - self.sw_start_time
            self.sw_running = False

    def sw_reset(self):
        self.sw_running = False
        self.sw_start_time = None
        self.sw_elapsed = 0.0
        self.sw_laps = []
        self.lbl_sw_display.config(text="00:00:00.00")
        self.txt_sw_laps.config(state='normal')
        self.txt_sw_laps.delete('1.0', 'end')
        self.txt_sw_laps.config(state='disabled')

    def sw_lap(self):
        if self.sw_running:
            now = time.time()
            current_total = self.sw_elapsed + (now - self.sw_start_time)

            if not self.sw_laps:
                lap_delta = current_total
            else:
                lap_delta = current_total - self.sw_laps[-1]

            self.sw_laps.append(current_total)

            self.txt_sw_laps.config(state='normal')
            self.txt_sw_laps.insert('end', f"Lap {len(self.sw_laps)}: {round(lap_delta, 2)}s\n")
            self.txt_sw_laps.see('end')
            self.txt_sw_laps.config(state='disabled')

    def create_pomodoro_view(self):
        self.frame_pomodoro = ttk.Frame(self.container)

        ttk.Button(self.frame_pomodoro, text="← Main Menu", command=self.show_main_menu).pack(anchor='nw', padx=10,
                                                                                              pady=10)

        ttk.Label(self.frame_pomodoro, text="-- POMODORO --", style="Header.TLabel").pack(pady=10)

        self.pomo_running = False
        self.pomo_seconds = 0
        self.pomo_mode = 1
        self.pomo_phase = "Work"
        self.pomo_laps_target = 0
        self.pomo_laps_done = 0
        self.pomo_total_minutes_studied = 0

        frame_opts = ttk.LabelFrame(self.frame_pomodoro, text="Settings")
        frame_opts.pack(pady=10)

        self.pomo_mode_var = tk.IntVar(value=1)
        ttk.Radiobutton(frame_opts, text="25min Work / 5min Break", variable=self.pomo_mode_var, value=1).pack(
            anchor='w', padx=10)
        ttk.Radiobutton(frame_opts, text="45min Work / 15min Break", variable=self.pomo_mode_var, value=2).pack(
            anchor='w', padx=10)

        frame_laps = ttk.Frame(frame_opts)
        frame_laps.pack(pady=5)
        ttk.Label(frame_laps, text="Laps:").pack(side='left')
        self.entry_pomo_laps = ttk.Entry(frame_laps, width=5)
        self.entry_pomo_laps.insert(0, "1")
        self.entry_pomo_laps.pack(side='left', padx=5)

        self.lbl_pomo_status = ttk.Label(self.frame_pomodoro, text="Ready", font=("Helvetica", 14, "bold"),
                                         foreground="blue")
        self.lbl_pomo_status.pack(pady=(10, 0))

        self.lbl_pomo_time = ttk.Label(self.frame_pomodoro, text="00:00", style="Big.TLabel")
        self.lbl_pomo_time.pack(pady=5)

        frame_p_btns = ttk.Frame(self.frame_pomodoro)
        frame_p_btns.pack(pady=10)
        ttk.Button(frame_p_btns, text="Start Session", command=self.pomo_start).grid(row=0, column=0, padx=5)
        ttk.Button(frame_p_btns, text="Stop", command=self.pomo_stop).grid(row=0, column=1, padx=5)

        self.lbl_pomo_stats = ttk.Label(self.frame_pomodoro, text="Total Studied: 0 mins")
        self.lbl_pomo_stats.pack(pady=20)

    def pomo_update(self):
        if self.pomo_running and self.pomo_seconds >= 0:
            mins, secs = divmod(self.pomo_seconds, 60)
            self.lbl_pomo_time.config(text=f"{mins:02}:{secs:02}")

            if self.pomo_seconds == 0:
                self.pomo_handle_phase_end()
            else:
                self.pomo_seconds -= 1
                self.root.after(1000, self.pomo_update)

    def pomo_handle_phase_end(self):
        if self.pomo_phase == "Work":
            work_mins = 25 if self.pomo_mode_var.get() == 1 else 45
            self.pomo_total_minutes_studied += work_mins
            self.lbl_pomo_stats.config(text=f"Total Studied: {self.pomo_total_minutes_studied} mins")

            self.pomo_laps_done += 1
            if self.pomo_laps_done >= self.pomo_laps_target:
                self.pomo_running = False
                messagebox.showinfo("Pomodoro", "Session Complete!")
                self.lbl_pomo_status.config(text="Session Done", foreground="green")
                return

            self.pomo_phase = "Break"
            break_mins = 5 if self.pomo_mode_var.get() == 1 else 15
            self.pomo_seconds = break_mins * 60
            self.lbl_pomo_status.config(text="Take a Break!", foreground="green")
            self.pomo_update()

        elif self.pomo_phase == "Break":
            self.pomo_phase = "Work"
            work_mins = 25 if self.pomo_mode_var.get() == 1 else 45
            self.pomo_seconds = work_mins * 60
            self.lbl_pomo_status.config(text=f"Work (Lap {self.pomo_laps_done + 1})", foreground="red")
            self.pomo_update()

    def pomo_start(self):
        if self.pomo_running: return
        try:
            self.pomo_laps_target = int(self.entry_pomo_laps.get())
            if self.pomo_laps_target <= 0: raise ValueError

            self.pomo_laps_done = 0
            self.pomo_running = True
            self.pomo_phase = "Work"

            work_mins = 25 if self.pomo_mode_var.get() == 1 else 45
            self.pomo_seconds = work_mins * 60

            self.lbl_pomo_status.config(text="Work Time!", foreground="red")
            self.pomo_update()

        except ValueError:
            messagebox.showerror("Error", "Invalid number of laps")

    def pomo_stop(self):
        self.pomo_running = False
        self.lbl_pomo_status.config(text="Stopped", foreground="pink")
        self.lbl_pomo_time.config(text="00:00")
if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalTimerApp(root)
    root.mainloop()