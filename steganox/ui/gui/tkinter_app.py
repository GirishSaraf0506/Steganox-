"""
Steganox Tkinter GUI Application.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from steganox.core.steganography import SteganoxEngine
from steganox.core.validation import validate_image, validate_password_strength


class SteganoxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Steganox - Steganography Tool")
        self.geometry("600x500")
        self.resizable(False, False)
        self.engine = SteganoxEngine()
        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        embed_frame = ttk.Frame(notebook)
        extract_frame = ttk.Frame(notebook)
        notebook.add(embed_frame, text="  Embed Message  ")
        notebook.add(extract_frame, text="  Extract Message  ")

        self._build_embed_tab(embed_frame)
        self._build_extract_tab(extract_frame)

    def _build_embed_tab(self, parent):
        ttk.Label(parent, text="Carrier Image:").grid(
            row=0, column=0, sticky="w", padx=10, pady=8
        )
        self.embed_image_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.embed_image_var, width=45).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(parent, text="Browse", command=self._browse_embed_image).grid(
            row=0, column=2, padx=5
        )

        ttk.Label(parent, text="Secret Message:").grid(
            row=1, column=0, sticky="nw", padx=10, pady=8
        )
        self.embed_message = tk.Text(parent, height=6, width=45)
        self.embed_message.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(parent, text="Password:").grid(
            row=2, column=0, sticky="w", padx=10, pady=8
        )
        self.embed_password_var = tk.StringVar()
        ttk.Entry(
            parent, textvariable=self.embed_password_var, show="*", width=45
        ).grid(row=2, column=1, padx=5)

        ttk.Label(parent, text="Output Path:").grid(
            row=3, column=0, sticky="w", padx=10, pady=8
        )
        self.embed_output_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.embed_output_var, width=45).grid(
            row=3, column=1, padx=5
        )
        ttk.Button(parent, text="Browse", command=self._browse_output).grid(
            row=3, column=2, padx=5
        )

        ttk.Button(parent, text="Embed Message", command=self._do_embed).grid(
            row=4, column=1, pady=15
        )

        self.embed_status = ttk.Label(parent, text="", foreground="green")
        self.embed_status.grid(row=5, column=0, columnspan=3, padx=10)

    def _build_extract_tab(self, parent):
        ttk.Label(parent, text="Stego Image:").grid(
            row=0, column=0, sticky="w", padx=10, pady=8
        )
        self.extract_image_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.extract_image_var, width=45).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(parent, text="Browse", command=self._browse_extract_image).grid(
            row=0, column=2, padx=5
        )

        ttk.Label(parent, text="Password:").grid(
            row=1, column=0, sticky="w", padx=10, pady=8
        )
        self.extract_password_var = tk.StringVar()
        ttk.Entry(
            parent, textvariable=self.extract_password_var, show="*", width=45
        ).grid(row=1, column=1, padx=5)

        ttk.Button(parent, text="Extract Message", command=self._do_extract).grid(
            row=2, column=1, pady=15
        )

        ttk.Label(parent, text="Extracted Message:").grid(
            row=3, column=0, sticky="nw", padx=10, pady=8
        )
        self.extract_result = tk.Text(parent, height=8, width=45, state="disabled")
        self.extract_result.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    def _browse_embed_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.bmp *.jpg *.jpeg")]
        )
        if path:
            self.embed_image_var.set(path)

    def _browse_extract_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.bmp *.jpg *.jpeg")]
        )
        if path:
            self.extract_image_var.set(path)

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")]
        )
        if path:
            self.embed_output_var.set(path)

    def _do_embed(self):
        image_path = self.embed_image_var.get()
        message = self.embed_message.get("1.0", tk.END).strip()
        password = self.embed_password_var.get()
        output_path = self.embed_output_var.get()

        if not all([image_path, message, password, output_path]):
            messagebox.showerror("Error", "All fields are required.")
            return

        valid_img, img_msg = validate_image(image_path)
        if not valid_img:
            messagebox.showerror("Invalid Image", img_msg)
            return

        valid_pwd, pwd_info = validate_password_strength(password)
        if not valid_pwd:
            messagebox.showwarning("Weak Password", "\n".join(pwd_info["issues"]))

        try:
            result = self.engine.embed(image_path, message, password)
            result.save(output_path)
            self.embed_status.config(
                text=f"✅ Saved to {os.path.basename(output_path)}", foreground="green"
            )
        except Exception as e:
            messagebox.showerror("Embed Failed", str(e))

    def _do_extract(self):
        image_path = self.extract_image_var.get()
        password = self.extract_password_var.get()

        if not all([image_path, password]):
            messagebox.showerror("Error", "Image and password are required.")
            return

        try:
            message = self.engine.extract(image_path, password)
            self.extract_result.config(state="normal")
            self.extract_result.delete("1.0", tk.END)
            self.extract_result.insert("1.0", message)
            self.extract_result.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Extract Failed", str(e))


def run():
    app = SteganoxApp()
    app.mainloop()


if __name__ == "__main__":
    run()
