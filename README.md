# Self-Healing Cybersecurity System 🏰️🖥️

## Overview 🌐
The **Self-Healing Cybersecurity System** is an advanced, AI-powered solution designed to detect, mitigate, and respond to network-based cyber threats in real-time. By leveraging **machine learning (ML)-based anomaly detection**, the system identifies potential threats and automatically applies security countermeasures such as **IP blocking and logging** to enhance cybersecurity.

### Key Features ✨
- **AI-Powered Anomaly Detection**: Uses **Isolation Forest** for detecting anomalies in network traffic. 🔍
- **Automated Countermeasures**: Blocks malicious IP addresses and logs threat activity automatically. ⛔️
- **Real-Time Threat Mitigation**: Continuously monitors network traffic and applies security actions as needed. ⚡
- **Modular & Scalable Architecture**: Designed for flexibility, allowing easy integration into different network environments. ⚙️

---

## Repository Updates 🔄
This project is actively maintained and improved with regular updates. Stay tuned for:
- Enhancements to the **anomaly detection model** 🧠
- Expansion of **network traffic datasets** 📊
- Strengthened **security countermeasures** ⚖️
- Ongoing **performance optimizations and bug fixes** 🛠️

---

## Project Structure 🗂️

```bash  
Self-Healing-Cybersecurity-System/
│── main.py               # Entry point for the system
│── detector.py           # Machine learning anomaly detection logic
│── response.py           # Automated security countermeasures
│── firewall.py           # Integrates firewall rules (iptables)
│── logs/                 # Stores detected threat logs
│── data/                 # Contains network traffic datasets
│   ├── model.pkl         # Trained model file
│   ├── scaler.pkl        # Scaler file for normalization
│   ├── quick_check.py    # Script for quick data analysis
│   ├── sample1.csv       # Sample dataset
│   ├── test_data.csv     # Test dataset
```

### Note:
- **Ensure the `data/` folder contains valid datasets (.csv format).**
- **The `logs/` folder will be created automatically if it does not exist.**
- **You can download real-world datasets from [Kaggle](https://www.kaggle.com/) and place them in `data/`.**

---

# 🚀 Getting Started

## 💽 1. Clone the Repository  
```bash
git clone https://github.com/kunal-masurkar/Self-Healing-Cybersecurity-System.git
cd Self-Healing-Cybersecurity-System
```

---

## 📂 2. Install Dependencies  
Ensure you have **Python 3.8+** installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## 📁 3. Prepare Network Traffic Data  
- Place your dataset files (`.csv` format) inside the `data/` folder.  
- Ensure that the data includes features relevant to network traffic analysis.  
- Example valid files:

```
Self-Healing-Cybersecurity-System/
│── data/
│   ├── dataset-main1.csv
│   ├── test_dataset.csv
│   ├── model.pkl
```

---

## 🎯 4. Train the Anomaly Detection Model  
Run the training script to build the machine learning model:
```bash
python detector.py
```
✅ This will train the model and save it as **`model.pkl`** in the `data/` folder.

---

## 🔥 5. Start the Detection & Response System  
Run the system to monitor traffic and respond to threats:
```bash
python main.py
```
📌 **System Functions:**  
✔ Detects anomalies in real-time  
✔ Blocks malicious IPs  
✔ Logs detected threats  

### 📈 Example Output:  
```
[SYSTEM] Threat detected & mitigated.
[ALERT] Blocking malicious IP: 192.168.1.50
```

---

## 📑 6. Check Logs for Detected Threats  
Threat activity is logged in `logs/threats.log`. View logs using:
```bash
cat logs/threats.log
```

---

## 🔒 7. Firewall Rules (Linux Only)  
To check blocked IPs in the firewall:
```bash
sudo iptables -L -v -n
```
To manually unblock an IP:
```bash
sudo iptables -D INPUT -s 192.168.1.100 -j DROP
```

---

## 🔄 8. Updating the Project  
Since this project is **actively maintained**, always pull the latest updates:
```bash
git pull origin main
```

---



# Contributing 🤝

We welcome contributions to enhance the system's functionality. Follow these steps to contribute:

1. **Fork the repository** 
2. **Create a new branch** (`git checkout -b feature-name`) 
3. **Commit your changes** (`git commit -m 'Added new feature'`) 
4. **Push to the branch** (`git push origin feature-name`) 
5. **Open a pull request** 📩

---

# License 📜
This project is licensed under the **Apache 2.0 License**. See the LICENSE file for details.

---

# Acknowledgements 🙏
- **Isolation Forest**: The anomaly detection algorithm used in this project. 🧠
- **Scikit-learn**: The Python library powering the ML model. 📚
- **iptables**: For enforcing firewall rules. 🔥

---

# 💡 Authors
👨‍💻 Developed by **Kunal Masurkar** & **Ayush Gorlawar**  
🌐 [GitHub - Kunal](https://github.com/kunal-masurkar) | 👉 [LinkedIn - Kunal](https://linkedin.com/in/kunal-masurkar-8494a123a)  
🌐 [GitHub - Ayush](https://github.com/AyushGorlawar) | 👉 [LinkedIn - Ayush](https://www.linkedin.com/in/ayush-gorlawar)  

---

## Note: This project is continuously evolving! Feel free to **report issues, submit pull requests, or start discussions**. ✨

