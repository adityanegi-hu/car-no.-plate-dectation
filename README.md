🚗 Car Number Plate Detection System

This project is a Car Number Plate Detection System built using Python, OpenCV, and OCR techniques to detect and recognize Indian vehicle number plates from images.
It is suitable for college projects, computer vision learning, and basic traffic surveillance applications.

📌 Features

✅ Detects vehicle number plates from images

✅ Supports Indian number plate formats (MH, DL, UK, KA, etc.)

✅ Uses image processing techniques

✅ Simple backend logic with Python

✅ Can be extended to video or live camera input

🛠️ Technologies Used

Python

OpenCV

OCR (EasyOCR / Tesseract)

Flask (for backend, if web-based)

HTML (templates for UI)

📁 Project Structure
car-no.-plate-dectation/
│
├── backend.py          # Main backend logic
├── car.py              # Vehicle / plate processing logic
├── vehicles.csv        # Sample vehicle data
├── templates/          # HTML templates (UI)
├── static/             # Static files (CSS / images if any)
└── README.md           # Project documentation

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/adityanegi-hu/car-no.-plate-dectation.git
cd car-no.-plate-dectation

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

3️⃣ Install Required Libraries
pip install opencv-python
pip install numpy
pip install flask
pip install easyocr


⚠️ If using Tesseract OCR, install it separately and add it to PATH.

▶️ How to Run the Project
python backend.py


If Flask is used, open your browser and go to:

http://127.0.0.1:5000/


Upload a vehicle image and the system will detect and display the number plate.

🧪 Sample Output

Input Image → 🚗
Detected Plate → UK07AB1234

🇮🇳 Supported Number Plate Format

Examples:

MH12AB1234
DL09CG5678
UK07EF9012
KA05MN4321

📌 Use Cases

🚦 Traffic monitoring

🅿️ Parking management systems

🏫 College mini / major projects

🧠 Computer vision learning

🔐 Security & surveillance (basic)

🚀 Future Enhancements

🔹 Live camera detection

🔹 Video file support

🔹 Database integration

🔹 Accuracy improvement using YOLO

🔹 Vehicle owner lookup

👨‍💻 Author

Aditya Negi
GitHub: adityanegi-hu

📜 License

This project is for educational purposes only.
Feel free to modify and improve it.
