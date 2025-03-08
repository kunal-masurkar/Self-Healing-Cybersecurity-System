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
  Self-Healing-Cybersecurity/
  │── main.py
  │── detector.py
  │── response.py
  │── firewall.py
  │── logs/
  │── data/
  │   └── synthetic_network_traffic.csv  # Your data file (CSV format)
  │── requirements.txt
 ```

---

## requirements.txt 
# Dependencies

- **`main.py`**: The entry point of the system that runs the detection and response mechanism. 🎯
- **`detector.py`**: Contains the logic for training and predicting anomalies using machine learning. 🤖
- **`response.py`**: Automates countermeasures such as blocking malicious IPs and logging detected threats. 📝
- **`firewall.py`**: Integrates with system firewall to block malicious IP addresses. 🔒
- **`logs/`**: Directory to store threat logs. 📂
- **`data/`**: Contains datasets used for training and testing the anomaly detection model. 📁

---

## Installation ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/kunal-masurkar/Self-Healing-Cybersecurity.git
   ```
2. Navigate to the project directory:
  ```bash
  cd Self-Healing-Cybersecurity
  ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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
