import cv2
import tkinter as tk
from tkinter import Label, Button, filedialog
from PIL import Image, ImageTk
import glob

# Load Haar cascade for face detection
detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Function to detect faces in an image
def detect_faces(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect.detectMultiScale(gray, 1.1, 10)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 4)
    return img

# Function to detect faces in a video frame and draw bounding boxes
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = detect.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

# GUI application class for face detection
class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection")
        self.root.geometry("800x800")  # Initial window size

        # Create a label to display the original photo
        self.label = Label(root)
        self.label.pack(expand=True, fill='both')

        # Create a label to display the photo with detected faces
        self.label_cv = Label(root)
        self.label_cv.pack(expand=True, fill='both')

        # Create buttons for webcam detection, photo import, and image folder detection
        self.webcam_button = Button(root, text="Use Webcam", command=self.start_webcam)
        self.webcam_button.pack()

        self.photo_button = Button(root, text="Import Photo", command=self.import_photo)
        self.photo_button.pack()

        self.folder_button = Button(root, text="Detect Faces in Folder", command=self.detect_faces_in_folder)
        self.folder_button.pack()

        # Configure window resizing behavior
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    # Function to start webcam detection
    def start_webcam(self):

        video_capture = cv2.VideoCapture(0)
        while True:

            result, video_frame = video_capture.read()  # read frames from the video
            if result is False:
                break  # terminate the loop if the frame is not read successfully

            faces = detect_bounding_box(
                video_frame
            )  # apply the function we created to the video frame

            cv2.imshow(
                "My Face Detection Project", video_frame
            )  # display the processed frame in a window named "My Face Detection Project"

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            ## Wait for a key event for 1 millisecond, mask the key code with 0xFF,
            # and break the loop if the pressed key is equal to the ASCII value of "q"

        video_capture.release()
        cv2.destroyAllWindows()


    def import_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            
            # Calculate scaling factor to maintain aspect ratio
            orig_width, orig_height = img.size
            label_width, label_height = self.label.winfo_width(), self.label.winfo_height()
            scale_factor = min(label_width / orig_width, label_height / orig_height)
            new_width, new_height = int(orig_width * scale_factor), int(orig_height * scale_factor)

            img = img.resize((new_width, new_height))
            imgtk = ImageTk.PhotoImage(image=img)
            ## Create PhotoImage object using the ImageTk 

            # Detect faces in the imported photo
            img_cv = detect_faces(file_path)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            img_cv = Image.fromarray(img_cv)
            img_cv = img_cv.resize((new_width, new_height))
            imgtk_cv = ImageTk.PhotoImage(image=img_cv)

            # Update the label with the imported photo and detection result
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            self.label_cv.imgtk = imgtk_cv
            self.label_cv.configure(image=imgtk_cv)

    # Function to detect faces in images within a folder and display the results
    def detect_faces_in_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            all_images = glob.glob(folder_path + "/*.jpg") + glob.glob(folder_path + "/*.jpeg") + glob.glob(folder_path + "/*.png" )  + glob.glob(folder_path + "/*.JPG") + glob.glob(folder_path + "/*.JPEG")
            for image in all_images:
                img_cv = detect_faces(image)
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                img_cv = Image.fromarray(img_cv)

                # Calculate scaling factor to maintain aspect ratio
                orig_width, orig_height = img_cv.size
                label_width, label_height = self.label_cv.winfo_width(), self.label_cv.winfo_height()
                scale_factor = min(label_width / orig_width, label_height / orig_height)
                new_width, new_height = int(orig_width * scale_factor), int(orig_height * scale_factor)

                img_cv = img_cv.resize((new_width, new_height))
                imgtk_cv = ImageTk.PhotoImage(image=img_cv)

                self.label_cv.imgtk = imgtk_cv
                self.label_cv.configure(image=imgtk_cv)
                self.root.update_idletasks()  # Update the GUI to display the image

                self.root.after(2)  # Wait for 2 seconds before displaying the next image
                self.label_cv.configure(image='')  # Clear the label before displaying the next image
                self.root.update_idletasks()  # Update the GUI to clear the image



if __name__ == "__main__":
    root = tk.Tk()
    FaceDetectionApp(root)
    root.mainloop()




