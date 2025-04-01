import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from recognize import recognize_objects

if getattr(sys, 'frozen', False):
    # Nếu đang chạy từ tệp .exe
    base_path = sys._MEIPASS
else:
    # Nếu đang phát triển (không phải .exe)
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'icon.ico')

class ObjectRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Recognition Application")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")  # Nền xám nhạt

        # Main Frame
        main_frame = tk.Frame(root, bg="#d9d9d9", bd=2, relief=tk.RIDGE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame (Image display)
        self.image_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.SOLID, width=600, height=500)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame, text="No Image", bg="#ffffff", fg="gray", font=("Arial", 14))
        self.image_label.pack(expand=True)

        # Right frame (Controls)
        control_frame = tk.Frame(main_frame, bg="#d9d9d9", bd=2, relief=tk.RIDGE, width=250)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Results Label
        results_label = tk.Label(control_frame, text="Recognition Results:", bg="#d9d9d9", font=("Arial", 12, "bold"))
        results_label.pack(pady=(30, 5))

        # Textbox for results
        self.results_text = tk.Text(control_frame, height=10, width=30, wrap=tk.WORD, state="disabled", font=("Arial", 10))
        self.results_text.pack(pady=5)

        # Open File Button
        self.open_button = tk.Button(control_frame, text="Open Image", font=("Arial", 11, "bold"), fg="white", bg="#007BFF",
                                     activebackground="#0056b3", relief=tk.RAISED, width=18, command=self.open_file)
        self.open_button.pack(pady=(40, 10))

        # Recognize Button
        self.recognize_button = tk.Button(control_frame, text="Recognize Object", font=("Arial", 11, "bold"), fg="white", bg="#28a745",
                                          activebackground="#1e7e34", relief=tk.RAISED, width=18, command=self.recognize_objects)
        self.recognize_button.pack(pady=(10, 50))

        # Initialize variables
        self.current_image_path = None
        self.photo_image = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )

        if file_path:
            self.current_image_path = file_path
            self.load_image(file_path)

    def load_image(self, image_path):
        try:
            # Open and resize image
            image = Image.open(image_path)

            # Calculate aspect ratio
            frame_width = self.image_frame.winfo_width() - 10
            frame_height = self.image_frame.winfo_height() - 10
            img_width, img_height = image.size

            ratio = min(frame_width / img_width, frame_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            image = image.resize((new_width, new_height), Image.LANCZOS)

            # Convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo_image, text="")

            # Update window title with filename
            filename = os.path.basename(image_path)
            self.root.title(f"Object Recognition - {filename}")

        except Exception as e:
            self.image_label.config(text=f"Error loading image: {e}", image="")

    def recognize_objects(self):
        if not self.current_image_path:
            messagebox.showinfo("Info", "Please open an image file first.")
            return

        try:
            # Call the function from recognize.py
            results = recognize_objects(self.current_image_path)
            self.results_text.config(state="normal")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)
            self.results_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to recognize objects: {e}")

def main():
    root = tk.Tk()
    app = ObjectRecognitionApp(root)
    root.iconbitmap(icon_path)
    root.mainloop()

if __name__ == "__main__":
    main()
