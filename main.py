import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Application")
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

        # Category Label
        category_label = tk.Label(control_frame, text="Select Object Category:", bg="#d9d9d9", font=("Arial", 12, "bold"))
        category_label.pack(pady=(30, 5))

        # Combobox for categories
        self.category_var = tk.StringVar()
        self.categories = ["Person", "Car", "Dog", "Cat", "Bird"]
        self.category_combo = ttk.Combobox(control_frame, textvariable=self.category_var, values=self.categories, width=18, state="readonly")
        self.category_combo.pack(pady=5)
        self.category_combo.current(0)  # Chọn mặc định mục đầu tiên

        # Open File Button
        self.open_button = tk.Button(control_frame, text="Open Image", font=("Arial", 11, "bold"), fg="white", bg="#007BFF",
                                     activebackground="#0056b3", relief=tk.RAISED, width=18, command=self.open_file)
        self.open_button.pack(pady=(40, 10))

        # Detect Button
        self.detect_button = tk.Button(control_frame, text="Detect Object", font=("Arial", 11, "bold"), fg="white", bg="#28a745",
                                       activebackground="#1e7e34", relief=tk.RAISED, width=18, command=self.detect_objects)
        self.detect_button.pack(pady=(10, 50))

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
            self.root.title(f"Object Detection - {filename}")

        except Exception as e:
            self.image_label.config(text=f"Error loading image: {e}", image="")

    def detect_objects(self):
        if not self.current_image_path:
            messagebox.showinfo("Info", "Please open an image file first.")
            return

        selected_category = self.category_var.get()
        if not selected_category:
            messagebox.showinfo("Info", "Please select an object category.")
            return

        # Hiển thị thông báo giả lập
        messagebox.showinfo("Detection", f"Detecting {selected_category} in the image...")

def main():
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
