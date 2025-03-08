# Self-Healing-Cybersecurity-System 🛡️💻

## Overview 🌐

The **Self-Healing Cybersecurity System** is an intelligent system designed to detect and mitigate network-based attacks automatically. The system utilizes machine learning (AI-based anomaly detection) to identify potential threats in real-time and applies countermeasures such as IP blocking and logging.

### Features ✨:
- **Anomaly Detection**: Uses **Isolation Forest** from scikit-learn for AI-based anomaly detection in network traffic. 🔍
- **Automated Countermeasures**: Automatically blocks malicious IP addresses using the system's firewall (iptables) and logs the threats. 🚫
- **Real-Time Detection**: The system is capable of detecting and mitigating attacks in real-time as network traffic is analyzed. ⚡

---

## Repository Updates 🔄

This repository is actively maintained, and changes are made on a regular basis. New features, enhancements, and bug fixes are continuously being implemented. Keep an eye on the repository for updates, including:

- Enhancements to the **anomaly detection model**. 🧠
- Addition of more **network traffic datasets**. 📊
- Improved **countermeasures** and system response mechanisms. 🔧
- Ongoing **performance optimizations** and testing. ⚙️

---

## Project Structure 🗂️

The project follows a modular structure for ease of use and maintainability:
```bash  
  Self-Healing-Cybersecurity-System/
  │── main.py
  │── detector.py
  │── response.py
  │── firewall.py
  │── logs/
  │── data/
  │   └── synthetic_network_traffic.csv  # Your data file (CSV format)
 ```
- **`main.py`**: The entry point of the system that runs the detection and response mechanism. 🎯
- **`detector.py`**: Contains the logic for training and predicting anomalies using machine learning. 🤖
- **`response.py`**: Automates countermeasures such as blocking malicious IPs and logging detected threats. 📝
- **`firewall.py`**: Integrates with system firewall to block malicious IP addresses. 🔒
- **`logs/`**: Directory to store threat logs. 📂
- **`data/`**: Contains datasets used for training and testing the anomaly detection model. 📁
### Note:
The data and logs folder is not present in the upload create them manually, <br>
Ensure that your data/ folder contains valid dataset files (.csv format). You can download real-world datasets from Kaggle and place them inside the data/ folder.

---

# 🚀 How to Run the Self-Healing Cybersecurity System  

This guide provides step-by-step instructions to set up and run the **Self-Healing Cybersecurity System**, which detects network attacks and applies countermeasures automatically.  

## 📥 1. Clone the Repository  
```bash
git clone https://github.com/kunal-masurkar/Self-Healing-Cybersecurity-System.git
cd Self-Healing-Cybersecurity-System
```

---

## 📦 2. Install Dependencies  
Ensure you have **Python 3.8+** installed. Then, install the required dependencies:  
```bash
pip install numpy pandas scikit-learn joblib
```

---

## 📂 3. Prepare Network Traffic Data  
- Place your dataset files (`.csv` format) inside the `data/` folder.  
- You can download real-world datasets from **[Kaggle](https://www.kaggle.com/)**.  
- Ensure the `data/` folder contains valid files like:  

```
Self-Healing-Cybersecurity-System/
│── data/
│   ├── network_traffic1.csv
│   ├── network_traffic2.csv
│   ├── attack_data.csv
```

---

## 🎯 4. Train the Anomaly Detection Model  
Run the training script to train the AI-based model:  
```bash
python detector.py
```
✅ This will train the model using data inside `data/` and save it as **`model.pkl`**.

---

## 🔥 5. Run the Detection & Response System  
Start the **Self-Healing Security System** by running:  
```bash
python main.py
```
📌 The system will:  
✔ Detect anomalies in real-time  
✔ Block malicious IPs  
✔ Log threats automatically  

🔹 **Example Output:**  
```
[SYSTEM] Threat detected & mitigated.
[ALERT] Blocking malicious IP: 
```

---

## 📜 6. Check Logs for Detected Threats  
The system logs detected threats in `logs/threats.log`. View logs using:  
```bash
cat logs/threats.log
```

---

## 🛡️ 7. (Optional) Firewall Rules (Linux)  
To check blocked IPs in the firewall (Linux only):  
```bash
sudo iptables -L -v -n
```
To manually unblock an IP:  
```bash
sudo iptables -D INPUT -s 192.168.1.100 -j DROP
```

---

## 🔄 8. Updating the Project  
Since this project is **regularly updated**, pull the latest changes using:  
```bash
git pull origin main
```

---

## 🎉 Done!  
Your **Self-Healing Cybersecurity System** is now running, automatically detecting and mitigating cyber threats in real time! 🚀🔐

---

# Contributing 🤝
## We welcome contributions to enhance the functionality and improve the system. To contribute:

1. Fork the repository. 🍴
2. Create a new branch (git checkout -b feature-name). 🌱
3. Commit your changes (git commit -m 'Add new feature'). ✍️
4. Push to the branch (git push origin feature-name). 🚀
5. Open a pull request. 📨

---

# License 📜
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

---

# Acknowledgements 🙏
  Isolation Forest: The anomaly detection algorithm used in this project. 🧠 <br>
  Scikit-learn: The Python library used for machine learning. 📚 <br>
  Iptables: For blocking IP addresses in the system firewall. 🔥 

---

## 💡 Author
👨‍💻 Developed by **Kunal Masurkar**  
🌐 [GitHub](https://github.com/kunal-masurkar) | 🔗 [LinkedIn](https://linkedin.com/in/kunal-masurkar-8494a123a)

---
## Note: This project is continuously updated, and contributions are welcome! Feel free to create issues, submit pull requests, or open discussions. 💬
