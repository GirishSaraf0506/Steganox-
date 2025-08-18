from tkinter import filedialog, simpledialog, messagebox, Tk, Label, PhotoImage, Frame, GROOVE, Text, WORD, Scrollbar, Button, END, Toplevel
from PIL import Image, ImageTk
import os
from stegano import lsb 
import hashlib
import numpy as np
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Initialize the main window
root = Tk()
root.title("Steganography Tool - Hide Secret Messages in Images")
root.geometry("900x600+250+100")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# Global variables
filename = None
secret = None


def showimage():
    """Open an image file and display it in the GUI."""
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                          filetypes=(("All image files", "*.png *.jpg *.bmp *.gif"), ("All files", "*.*")))
    if filename:
        try:
            img = Image.open(filename)
            img.thumbnail((250, 250))
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
        except (OSError, IOError) as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

def hide_message():
    """Hide the secret message or link in the selected image."""
    global secret
    if filename:
        password = simpledialog.askstring("Password", "Set a password (min 8 characters):", show='*')
        if password and len(password) >= 8:
            message = text1.get(1.0, END).strip()
            if message:
                try:
                    hash_object = hashlib.sha256(password.encode())
                    hex_dig = hash_object.hexdigest()
                    message_with_hash = f"{hex_dig}:{message}"
                    secret = lsb.hide(filename, message_with_hash)
                    messagebox.showinfo("Success", "The message has been hidden in the image.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to hide message: {e}")
            else:
                messagebox.showwarning("Warning", "Please enter a message to hide.")
        else:
            messagebox.showwarning("Warning", "Please set a password with at least 8 characters.")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")

def reveal():
    """Reveal the hidden message or image from the encoded image."""
    global filename
    if filename:
        entered_password = simpledialog.askstring("Password", "Enter the password:", show='*')
        if entered_password:
            try:
                clear_message = lsb.reveal(filename)
                if clear_message:
                    stored_hash, message = clear_message.split(':', 1)
                    hash_object = hashlib.sha256(entered_password.encode())
                    hex_dig = hash_object.hexdigest()
                    if stored_hash == hex_dig:
                        text1.delete(1.0, END)
                        text1.insert(END, message)
                        if message.startswith("http"):
                            link_button = Button(text1, text=message, fg="blue", cursor="hand2")
                            link_button.pack()
                            link_button.bind("<Button-1>", lambda e: webbrowser.open(message))
                    else:
                        messagebox.showerror("Error", "Incorrect password!")
                else:
                    try:
                        encoded_image = Image.open(filename).convert('RGB')
                        encoded_data = np.array(encoded_image)
                        
                        rows, cols, _ = encoded_data.shape
                        revealed_data = np.zeros((rows, cols, 3), dtype=np.uint8)
                        
                        revealed_data[:, :, 0] = (encoded_data[:, :, 0] & 0x01) << 7
                        revealed_data[:, :, 1] = (encoded_data[:, :, 1] & 0x01) << 7
                        revealed_data[:, :, 2] = (encoded_data[:, :, 2] & 0x01) << 7
                        
                        revealed_image = Image.fromarray(revealed_data)
                        revealed_image.show()
                    except (OSError, IOError) as e:
                        messagebox.showerror("Error", f"Failed to reveal the image: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reveal message: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a password.")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")

def hide_image():
    """Hide an image within another image."""
    global secret
    if filename:
        secret_image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select secret image file",
                                                       filetypes=(("PNG file", "*.png"), ("All files", "*.*")))
        if secret_image_path:
            password = simpledialog.askstring("Password", "Set a password (min 8 characters):", show='*')
            if password and len(password) >= 8:
                try:
                    base_image = Image.open(filename)
                    secret_image = Image.open(secret_image_path).convert('RGB')
                    base_image = base_image.convert('RGB')
                    
                    base_data = np.array(base_image)
                    secret_data = np.array(secret_image)
                    
                    rows, cols, _ = secret_data.shape
                    base_data[:rows, :cols, 0] = (base_data[:rows, :cols, 0] & 0xFE) | (secret_data[:, :, 0] >> 7)
                    base_data[:rows, :cols, 1] = (base_data[:rows, :cols, 1] & 0xFE) | (secret_data[:, :, 1] >> 7)
                    base_data[:rows, :cols, 2] = (base_data[:rows, :cols, 2] & 0xFE) | (secret_data[:, :, 2] >> 7)
                    
                    encoded_image = Image.fromarray(base_data)
                    secret = encoded_image
                    
                    messagebox.showinfo("Success", "The secret image has been hidden in the base image.")
                except (OSError, IOError) as e:
                    messagebox.showerror("Error", f"Failed to hide the image: {e}")
            else:
                messagebox.showwarning("Warning", "Please set a password with at least 8 characters.")
        else:
            messagebox.showwarning("Warning", "Please select a secret image first.")
    else:
        messagebox.showwarning("Warning", "Please select a base image first.")

def save_image():
    """Save the image with the hidden message or hidden image."""
    global secret
    if secret:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG file", "*.png"), ("All files", "*.*")))
        if save_path:
            try:
                secret.save(save_path)
                messagebox.showinfo("Success", f"The image has been saved as {save_path}.")
                text1.delete(1.0, END)
            except (OSError, IOError) as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "Save operation was cancelled.")
    else:
        messagebox.showwarning("Warning", "No secret message or image to save.")

def clear_text():
    """Clear the text area and reset the application state."""
    text1.delete(1.0, END)
    global filename, secret
    filename = None
    secret = None
    lbl.configure(image='', width=250, height=250)

def show_help():
    """Display a help window with guidance on using the application."""
    help_window = Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x300")
    help_window.configure(bg="#2c3e50")
    help_text = Text(help_window, wrap=WORD, bg="#2c3e50", fg="white", font="Arial 12")
    help_text.insert(END, "Welcome to the Steganography Tool!\n\n"
                        "1. Open Image: Select an image file to hide a message.\n"
                        "2. Hide Data: Enter a message and set a password to hide it in the image.\n"
                        "3. Reveal Data: Enter the correct password to reveal the hidden message or image.\n"
                        "4. Hide Image: Select a secret image to hide within the base image.\n"
                        "5. Save Image: Save the modified image with the hidden message or hidden image.\n"
                        "6. Clear: Reset the application.\n")
    help_text.configure(state='disabled')
    help_text.pack(expand=True, fill='both')

def send_email():
    """Send the encoded image via email."""
    if filename:
        recipient = simpledialog.askstring("Recipient Email", "Enter the recipient's email address:")
        if recipient:
            try:
                sender_email = "your_email@example.com"
                sender_password = "your_password"
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = "Encoded Image"
                
                attachment = open(filename, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
                msg.attach(part)
                
                server = smtplib.SMTP('smtp.example.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, msg.as_string())
                server.quit()
                
                messagebox.showinfo("Success", "Email sent successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a recipient email address.")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")

# Load and display the logo
image_icon = PhotoImage(file="C:/Users/admin/OneDrive/Desktop/vs/g/logo.jpg")
root.iconphoto(False, image_icon)

logo = PhotoImage(file="C:/Users/admin/OneDrive/Desktop/vs/g/logo.png")
Label(root, image=logo, bg="#2c3e50").place(x=10, y=0)

# Title Label
Label(root, text="CYBER STEGANO", bg="#2c3e50", fg="yellow", font="Arial 25 bold").place(x=100, y=20)

# Frame for displaying image
frame1 = Frame(root, bd=3, bg="black", width=420, height=280, relief=GROOVE)
frame1.place(x=10, y=80)
lbl = Label(frame1, bg="black")
lbl.place(x=70, y=10)

# Frame for text area
frame2 = Frame(root, bd=3, bg="#dcdcdc", width=420, height=280, relief=GROOVE)
frame2.place(x=470, y=80)
text1 = Text(frame2, font="Arial 16", bg="#dcdcdc", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=490, height=295)

# Scrollbar for text area
scrollbar = Scrollbar(frame2)
scrollbar.place(x=490, y=0, height=295)
scrollbar.config(command=text1.yview)
text1.config(yscrollcommand=scrollbar.set)

# Buttons
Button(root, text="Open Image", width=15, height=2, command=showimage).place(x=30, y=400)
Button(root, text="Hide Message", width=15, height=2, command=hide_message).place(x=200, y=400)
Button(root, text="Reveal Data", width=15, height=2, command=reveal).place(x=370, y=400)
Button(root, text="Hide Image", width=15, height=2, command=hide_image).place(x=540, y=400)
Button(root, text="Save Image", width=15, height=2, command=save_image).place(x=30, y=450)
Button(root, text="Clear", width=15, height=2, command=clear_text).place(x=200, y=450)
Button(root, text="Help", width=15, height=2, command=show_help).place(x=370, y=450)
Button(root, text="Send Email", width=15, height=2, command=send_email).place(x=540, y=450)

# Start the main event loop
root.mainloop()