import tkinter as tk
from tkinter import ttk, filedialog
import qrcode
import os
from PIL import Image, ImageTk

def generate_qr_code(data, file_name):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

def upload_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        photo_path_entry.delete(0, tk.END)
        photo_path_entry.insert(0, file_path)
        display_selected_photo(file_path)

def display_selected_photo(photo_path):
    image = Image.open(photo_path)
    
    # Resize image to fit within the photo_label widget without cropping
    width, height = image.size
    max_size = min(photo_label.winfo_width(), photo_label.winfo_height())
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        image = image.resize((new_width, new_height), Image.BILINEAR)
    
    photo = ImageTk.PhotoImage(image)
    photo_label.config(image=photo)
    photo_label.image = photo
    
    # Ensure that the photo frame does not shrink
    photo_frame.pack_propagate(False)
    photo_frame.pack(fill=tk.BOTH, expand=True)
    photo_frame.config(width=400, height=400)  # Set a fixed size for the photo frame







def generate_qr_from_gui():
    # Retrieve data from entry fields
    dl_number = entry_fields["DL Number"].get()
    first_name = entry_fields["First Name"].get()
    last_name = entry_fields["Last Name"].get()
    middle_name = entry_fields["Middle Name"].get()
    address = entry_fields["Address"].get()
    city = entry_fields["City"].get()
    zip_code = entry_fields["Zip code"].get()
    dl_class = entry_fields["DL Class"].get()
    sex = entry_fields["Sex"].get()
    donor = entry_fields["Donor"].get()
    birth_date = entry_fields["Birth Date"].get()
    issue_date = entry_fields["Issue Date"].get()
    dd = entry_fields["DD"].get()
    icn = entry_fields["ICN"].get()
    
    # Combine data into a single string
    data = f"DL Number: {dl_number}\nFirst Name: {first_name}\nLast Name: {last_name}\nMiddle Name: {middle_name}\nAddress: {address}\nCity: {city}\nZip code: {zip_code}\nDL Class: {dl_class}\nSex: {sex}\nDonor: {donor}\nBirth Date: {birth_date}\nIssue Date: {issue_date}\nDD: {dd}\nICN: {icn}"
    
    # Get the photo path from the entry field
    photo_path = photo_path_entry.get()
    
    # Check if photo path is provided
    if not photo_path:
        status_label.config(text="Please upload a photo.")
        return
    
    # Check if file exists
    if not os.path.isfile(photo_path):
        status_label.config(text="Invalid photo file.")
        return
    
    # Add photo path to the data string
    data += f"\nPhoto Path: {photo_path}"
    
    # Get the file name for saving the QR code
    file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    
    # Generate QR code if file name is provided
    if file_name:
        generate_qr_code(data, file_name)
        status_label.config(text="QR code generated successfully!")
    else:
        status_label.config(text="Please select a file name.")

# Create the main application window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("800x400")  # Set initial window size

# Create frame for input fields
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Create and layout input widgets
fields = ["DL Number", "First Name", "Last Name", "Middle Name", "Address", "City", "Zip code", "DL Class", "Sex", "Donor", "Birth Date", "Issue Date", "DD", "ICN"]
entry_fields = {}

for field in fields:
    label = tk.Label(input_frame, text=field)
    label.grid(sticky="w", pady=(5, 0))
    if field == "Sex":
        sex_var = tk.StringVar()
        sex_combobox = ttk.Combobox(input_frame, textvariable=sex_var, values=["Male", "Female"])
        sex_combobox.grid(row=fields.index(field), column=1, padx=(10, 0), pady=(5, 0), sticky="w")
        entry_fields[field] = sex_var
    elif field == "Donor":
        donor_var = tk.StringVar()
        donor_combobox = ttk.Combobox(input_frame, textvariable=donor_var, values=["Yes", "No"])
        donor_combobox.grid(row=fields.index(field), column=1, padx=(10, 0), pady=(5, 0), sticky="w")
        entry_fields[field] = donor_var
    else:
        entry = tk.Entry(input_frame, width=30)
        entry.grid(row=fields.index(field), column=1, padx=(10, 0), pady=(5, 0), sticky="w")
        entry = tk.Entry(input_frame, width=30)
        entry.grid(row=fields.index(field), column=1, padx=(10, 0), pady=(5, 0), sticky="w")
        entry_fields[field] = entry

# Create frame for photo upload and display
photo_frame = tk.Frame(root)
photo_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create and layout photo upload widgets
photo_path_label = tk.Label(photo_frame, text="Photo Path:")
photo_path_label.grid(row=0, column=0, sticky="w")

photo_path_entry = tk.Entry(photo_frame, width=30)
photo_path_entry.grid(row=0, column=1, padx=(10, 0), sticky="w")

upload_button = tk.Button(photo_frame, text="Upload Photo", command=upload_photo)
upload_button.grid(row=0, column=2, padx=(10, 0), pady=10)

# Create and layout photo display label
photo_label = tk.Label(photo_frame, width=20, height=10, borderwidth=2, relief="groove")
photo_label.grid(row=1, columnspan=3, padx=10, pady=10)

# Create generate button
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_from_gui)
generate_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create status label
status_label = tk.Label(root, text="")
status_label.pack(side=tk.BOTTOM, padx=10, pady=(0, 10))

# Start the Tkinter event loop
root.mainloop()
