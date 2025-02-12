# AI-Powered-Cybersecurity-Threat-Detection-System-in-Automotive-Systems
AI-Powered Cybersecurity Threat Detection System in Automotive Systems( malicious CAN  detection)

 Project Overview
This project focuses on developing an **AI-powered cybersecurity threat detection system** for automotive systems. The system analyzes **Controller Area Network (CAN) data** in real time to detect **malicious activities**, such as **Denial-of-Service (DoS), Fuzzy, and Impersonation attacks**. When a potential threat is detected, the system triggers an alarm or takes preventive action.

## 🔍 Features
- 📡 **CAN Data Analysis** – Monitors real-time CAN data for cybersecurity threats.
- 🤖 **Machine Learning Model** – Trained on datasets containing normal and attack scenarios.
- 🚀 **Real-Time Detection** – Identifies malicious activities as they occur.
- ⚠️ **Threat Response** – Triggers alerts or initiates protective measures.
- 📊 **Data Visualization** – Displays attack trends and anomaly detection results.

## 📂 Datasets Used
The project uses four datasets:
1. **Attack-Free Dataset** – Normal automotive CAN data.
2. **DoS Attack Dataset** – Data with simulated Denial-of-Service attacks.
3. **Fuzzy Attack Dataset** – Data with unpredictable, random attack patterns.
4. **Impersonation Attack Dataset** – Data simulating unauthorized access attempts.

## 🏗️ Tech Stack
- **Programming Language**: Python 🐍
- **Machine Learning Frameworks**: TensorFlow / Scikit-learn
- **Database**: MySQL (if needed for logging detected threats)
- **Visualization**: Matplotlib, Seaborn
- **Deployment**: Flask / FastAPI (for real-time detection API)

## 🚀 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-cybersecurity-threat-detection.git
   cd ai-cybersecurity-threat-detection
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the model training script:
   ```bash
   python train_model.py
   ```
4. Start the real-time detection system:
   ```bash
   python app.py
   ```

## 📜 Usage
- Feed the system with **CAN bus data**.
- The model will classify data as **normal or malicious**.
- If a threat is detected, the system triggers an **alert** or initiates a **defensive response**.

## 📌 Future Enhancements
- **Integration with automotive security frameworks**
- **Deployment on embedded automotive systems**
- **Extended support for more attack types**

## 🤝 Contributing
Feel free to **fork** the repository, create a **pull request**, or report issues via **GitHub Issues**.

## 📜 License
This project is licensed under the **MIT License**.

---
✨ *Designed to enhance automotive cybersecurity with AI-powered threat detection!* 🚗💡
