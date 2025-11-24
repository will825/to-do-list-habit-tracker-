import tkinter as tk
from tkinter import messagebox, filedialog


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do & Habit Tracker")
        self.root.geometry("520x420")

        # --- Menu bar ---
        menu_bar = tk.Menu(root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Tasks", command=self.save_tasks)
        file_menu.add_command(label="Load Tasks", command=self.load_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menu_bar)

        # --- Title ---
        title_label = tk.Label(
            root,
            text="To-Do & Habit Tracker",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=8)

        # --- Frame for task input ---
        input_container = tk.Frame(root)
        input_container.pack(fill=tk.X, padx=10)

        # label + entry stacked vertically
        entry_label = tk.Label(input_container, text="Task:")
        entry_label.pack(anchor="w")

        entry_frame = tk.Frame(input_container)
        entry_frame.pack(fill=tk.X, pady=(0, 5))

        self.task_entry = tk.Entry(entry_frame, width=45)
        self.task_entry.pack(side=tk.LEFT, padx=(0, 6), fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", self.add_task_event)

        add_button = tk.Button(
            entry_frame,
            text="Add",
            width=10,
            command=self.add_task
        )
        add_button.pack(side=tk.RIGHT)

        # --- Listbox and scrollbar ---
        list_frame = tk.Frame(root)
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            width=60,
            height=10
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Allow double-click to mark complete / incomplete
        self.task_listbox.bind("<Double-Button-1>", self.toggle_completed_event)
        # Allow Delete key to remove selected task
        self.task_listbox.bind("<Delete>", self.delete_task_event)

        # --- Action buttons ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=8)

        complete_button = tk.Button(
            button_frame,
            text="Mark Completed",
            width=14,
            command=self.mark_completed
        )
        complete_button.grid(row=0, column=0, padx=5)

        uncomplete_button = tk.Button(
            button_frame,
            text="Mark Active",
            width=14,
            command=self.mark_active
        )
        uncomplete_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Delete Task",
            width=14,
            command=self.delete_task
        )
        delete_button.grid(row=0, column=2, padx=5)

        # --- Status bar ---
        self.status_label = tk.Label(
            root,
            text="0 tasks | 0 completed",
            anchor="w"
        )
        self.status_label.pack(fill=tk.X, padx=8, pady=(0, 6))

        self.update_status()

    # ---------------- Helper methods ---------------- #

    def is_completed(self, text: str) -> bool:
        """Check if a task line is marked as done."""
        return text.startswith("[Done] ")

    def strip_done_marker(self, text: str) -> str:
        """Remove [Done] marker if present."""
        if self.is_completed(text):
            return text[len("[Done] "):]
        return text

    def update_status(self):
        total = self.task_listbox.size()
        completed = 0
        for i in range(total):
            if self.is_completed(self.task_listbox.get(i)):
                completed += 1
        self.status_label.config(
            text=f"{total} task(s) | {completed} completed"
        )

    # --- Event wrappers for bindings --- #

    def add_task_event(self, event):
        self.add_task()

    def delete_task_event(self, event):
        self.delete_task()

    def toggle_completed_event(self, event):
        self.toggle_completed()

    # --- Core actions --- #

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please type a task before adding.")
            return
        self.task_listbox.insert(tk.END, task_text)
        self.task_entry.delete(0, tk.END)
        self.update_status()

    def mark_completed(self):
        try:
            index = self.task_listbox.curselection()[0]
        except IndexError:
            messagebox.showinfo("No Selection", "Select a task to mark as completed.")
            return

        current_text = self.task_listbox.get(index)
        if self.is_completed(current_text):
            messagebox.showinfo("Already Completed", "This task is already completed.")
            return

        new_text = "[Done] " + current_text
        self.task_listbox.delete(index)
        self.task_listbox.insert(index, new_text)
        # Optional: gray out completed items
        self.task_listbox.itemconfig(index, fg="gray")
        self.update_status()

    def mark_active(self):
        """Remove completed marker and make task active again."""
        try:
            index = self.task_listbox.curselection()[0]
        except IndexError:
            messagebox.showinfo("No Selection", "Select a task to mark as active.")
            return

        current_text = self.task_listbox.get(index)
        base_text = self.strip_done_marker(current_text)
        self.task_listbox.delete(index)
        self.task_listbox.insert(index, base_text)
        # reset color
        self.task_listbox.itemconfig(index, fg="black")
        self.update_status()

    def toggle_completed(self):
        """Double-click toggles between completed and active."""
        try:
            index = self.task_listbox.curselection()[0]
        except IndexError:
            return

        current_text = self.task_listbox.get(index)
        if self.is_completed(current_text):
            # make active
            base_text = self.strip_done_marker(current_text)
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, base_text)
            self.task_listbox.itemconfig(index, fg="black")
        else:
            # make completed
            new_text = "[Done] " + current_text
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, new_text)
            self.task_listbox.itemconfig(index, fg="gray")

        self.update_status()

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
        except IndexError:
            messagebox.showinfo("No Selection", "Select a task to delete.")
            return

        task_text = self.task_listbox.get(index)
        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete:\n\n{task_text}"
        )
        if not confirm:
            return

        self.task_listbox.delete(index)
        self.update_status()

    # --- File operations --- #

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for i in range(self.task_listbox.size()):
                    f.write(self.task_listbox.get(i) + "\n")
            messagebox.showinfo("Saved", f"Tasks saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error Saving", f"Could not save file:\n{e}")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()

            self.task_listbox.delete(0, tk.END)
            for line in lines:
                if line.strip():
                    self.task_listbox.insert(tk.END, line.strip())

            # re-apply gray color to completed tasks
            for i in range(self.task_listbox.size()):
                text = self.task_listbox.get(i)
                if self.is_completed(text):
                    self.task_listbox.itemconfig(i, fg="gray")

            self.update_status()
            messagebox.showinfo("Loaded", f"Tasks loaded from:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error Loading", f"Could not load file:\n{e}")

    # --- Misc --- #

    def show_about(self):
        messagebox.showinfo(
            "About",
            "To-Do & Habit Tracker\n\n"
            "Double-click a task to toggle completed.\n"
            "Press Delete to remove a task."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
