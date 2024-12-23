import tkinter as tk
from tkinter import filedialog, ttk
from ArithFloat import ArithFloat  


class ArithmeticCompressionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Compression Program")
        self.root.geometry("500x500")  
        self.root.resizable(False, False)
        self.arithCoder = ArithFloat()

        # Styling
        self.root.configure(bg="#f4f4f4")
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)
        self.style.configure("TLabel", background="#f4f4f4", font=("Helvetica", 12))

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_frame = tk.Frame(self.root, bg="#003366")
        title_frame.pack(fill="x", pady=(0, 10))
        self.title_label = tk.Label(
            title_frame,
            text="Arithmetic Compression Program",
            font=("Helvetica", 18, "bold"),
            bg="#003366",
            fg="#ffffff",
        )
        self.title_label.pack(pady=10)

        # Main Buttons
        button_frame = tk.Frame(self.root, bg="#f4f4f4")
        button_frame.pack(pady=10)

        self.compress_button = ttk.Button(button_frame, text="Compress a File", command=self.compress_file)
        self.compress_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.decompress_button = ttk.Button(button_frame, text="Decompress a File", command=self.decompress_file)
        self.decompress_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Log Area
        log_frame = tk.Frame(self.root, bg="#f4f4f4")
        log_frame.pack(pady=10, fill="both", expand=True)

        self.log_label = tk.Label(log_frame, text="Logs:", bg="#f4f4f4", fg="#000000", font=("Helvetica", 12, "bold"))
        self.log_label.pack(anchor="w")

        self.log_text = tk.Text(log_frame, wrap="word", height=10, bg="#ffffff", fg="#000000", font=("Helvetica", 10))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", anchor="w", bg="#d9d9d9", fg="#000000", font=("Helvetica", 10))
        self.status_bar.pack(side="bottom", fill="x")

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.append_log(f"STATUS: {message}")

    def append_log(self, message):
        self.log_text.insert("end", message + "\n\n")
        self.log_text.see("end")  # Auto-scroll to the bottom

    def compress_file(self):
        input_file = filedialog.askopenfilename(
            title="Select Input File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if input_file:
            try:
                output_file_path = self.arithCoder.compressToFile(input_file)
                self.update_status("File compressed successfully!")
                self.append_log(f"Compressed file: {output_file_path}")
            except Exception as e:
                self.update_status("Error during file compression.")
                self.append_log(f"Error: {e}")

    def decompress_file(self):
        compressed_file = filedialog.askopenfilename(
            title="Select Compressed File", filetypes=(("Compressed Files", "*.arf"), ("All Files", "*.*"))
        )
        if compressed_file:
            try:
                output_file_path = self.arithCoder.decompressFromFile(compressed_file)
                self.update_status("File decompressed successfully!")
                self.append_log(f"Decompressed file: {output_file_path}")
            except Exception as e:
                self.update_status("Error during file Decompression.")
                self.append_log(f"Error: {e}")


# Create the main window and run the GUI
def run_gui():
    root = tk.Tk()
    app = ArithmeticCompressionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
