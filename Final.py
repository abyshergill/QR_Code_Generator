import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def create_qr_code(data, save_path, remark=None):
    # Generate QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')

    # Create a new image with space for the remark
    width, height = img.size
    new_img = Image.new('RGB', (width, height + 50), 'white')
    new_img.paste(img, (0, 0))

    # Add text to the image
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.load_default()
    
    #For QR code text 
    draw.text((10, height + 5), f'QR Code: {data}', fill='black', font=font)
    
    # This line is for remark text 
    draw.text((10, height + 25), f'Remark: {remark}' if remark else 'No Remark', fill='black', font=font)

    # Save the image
    new_img.save(save_path)
    return save_path

def submit():
    text = entry.get("1.0", tk.END).strip()  # Get multiline text from the first text box
    save_path = save_entry.get().strip()  # Ensure the save path is stripped of extra whitespace
    remarks = remark_entry.get("1.0", tk.END).strip().splitlines()  # Get multiline remarks from the second text box

    if text and save_path:
        lines = text.splitlines()
        remark_count = len(remarks)

        for i, line in enumerate(lines):
            # Generate the QR save path for each line
            qr_save_path = os.path.splitext(save_path)[0] + f"_image{i + 1}.jpg"
            
            # Determine the remark for the current line
            remark = remarks[min(i, remark_count - 1)] if remark_count > 0 else None

            # Create the combined text for the QR code
            qr_text = f"{line}" if remark else line
            
            try:
                create_qr_code(qr_text, qr_save_path, remark)  # Create QR code image
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code for line {i + 1}: {e}")
                return  # Stop processing on error
        
        messagebox.showinfo("Success", f'QR Codes saved at: {os.path.dirname(save_path)}')
        continue_prompt()
    else:
        messagebox.showwarning("Input Error", "Please enter text and select a save location for the QR codes.")



def continue_prompt():
    response = messagebox.askyesno("Continue", "Do you want to generate another set of QR codes?")
    if response:
        entry.delete("1.0", tk.END)  # Clear multiline entry
        remark_entry.delete("1.0", tk.END)  # Clear multiline entry
        save_entry.delete(0, tk.END)  # Clear save path
       # remark_entry.delete(0, tk.END)  # Clear remark entry
    else:
        root.destroy()  # Close the window

def browse_file():
    text = entry.get("1.0", tk.END).strip()
    default_filename = f"{text.splitlines()[0] if text else 'QR_Code'}.jpg"

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                               initialfile=default_filename,
                                               filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        save_entry.delete(0, tk.END)  # Clear current entry
        save_entry.insert(0, file_path)  # Insert the selected file path

# Global variable to track the editor window
editor_window = None

def open_text_editor(target):
    global editor_window

    # Check if the editor window is already open
    if editor_window is not None and editor_window.winfo_exists():
        editor_window.lift()  # Bring the existing window to the front
        return
    # Create a new window for multiline input
    editor_window = tk.Toplevel(root)
    editor_window.title("Enter Text for QR Code")
    editor_window.geometry("400x400")
    editor_window.resizable(False, False)  # Make the window size fixed

    # Set the same color as the main window
    editor_window.configure(bg="#E6F7FF")

    # Optionally set an icon for the editor window
    # editor_window.iconbitmap(r'')  # Uncomment and set the path to your icon

    text_editor = tk.Text(editor_window, width=40, height=10, font=("Arial", 12), bg="#FFFFFF")
    text_editor.pack(pady=10)

    def on_ok():
        # Get the text from the text editor and insert it into the main text box
        text = text_editor.get("1.0", tk.END).strip()
        if text:
            target.delete("1.0", tk.END)
            target.insert(tk.END, text)
        editor_window.destroy()

    def on_cancel():
        editor_window.destroy()

    ok_button = tk.Button(editor_window, text="OK", command=on_ok, width=20, font=("Arial", 12), bg="#A6D6FF")
    ok_button.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button = tk.Button(editor_window, text="Cancel", command=on_cancel, width=20, font=("Arial", 12), bg="#A6D6FF")
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Note: Ensure to set the appropriate icon path if you want to use an icon.


# Create the main window
root = tk.Tk()
root.title("QR Code Generator")  
root.geometry("650x550")  
root.resizable(False, False)

# Set a soft color for the window
root.configure(bg="#E6F7FF")  

# Create a frame for the content
frame = tk.Frame(root, padx=20, pady=20, bg="#E6F7FF")
frame.pack(pady=10)

# Label for multiline input
label1 = tk.Label(frame, text="Enter text for QR Codes:", font=("Arial", 12), bg="#E6F7FF", height=1)
label1.grid(row=0, column=0, sticky="w", padx=(0, 10))

entry = tk.Text(frame, width=40, height=5, font=("Arial", 12))
entry.grid(row=0, column=1)

# Double-click to open the text editor
entry.bind("<Double-1>", lambda e: open_text_editor(entry))

# Label for remark
label2 = tk.Label(frame, text="Remark (optional):", font=("Arial", 12), bg="#E6F7FF")
label2.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10,0))

remark_entry = tk.Text(frame, width=40, height=5, font=("Arial", 12))
remark_entry.grid(row=1, column=1)

remark_entry.bind("<Double-1>", lambda e: open_text_editor(remark_entry))

# Label for setting location
set_location_label = tk.Label(frame, text="Set your location:", font=("Arial", 12), bg="#E6F7FF")
set_location_label.grid(row=2, column=1, sticky="w", padx=(0, 10))

save_entry = tk.Entry(frame, width=40, font=("Arial", 12))
save_entry.grid(row=3, column=1)

# Create the browse button
browse_button = tk.Button(frame, text="Browse", command=browse_file, font=("Arial", 12), height=1, width=15, bg="#A6D6FF", activebackground="#85C6FF")
browse_button.grid(row=3, column=0, padx=(0, 0))

# Create a submit button
submit_button = tk.Button(frame, text="Submit", command=submit, font=("Arial", 16), width=15, bg="#A6D6FF", activebackground="#85C6FF")
submit_button.grid(row=4, column=0, columnspan=3, pady=(20, 0))

# Footer
footer_label = tk.Label(root, text="Program Source Repository at \n https://github.com/abyshergill/QR_Code_Generator/", font=("Arial", 10), bg="#E6F7FF")
footer_label.pack(side=tk.BOTTOM, anchor='e', padx=20, pady=10)

# Set a custom icon if desired
# root.iconbitmap(r'')

# Run the Tkinter event loop
root.mainloop()
