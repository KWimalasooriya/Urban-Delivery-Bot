# 🚚📸🔐 Urban Delivery Bot – An Industrial IoT Innovation

A **fully functional autonomous and manually controlled delivery robot** designed for secure, contactless deliveries in urban environments.  

Built as part of our **final-year Industrial IoT coursework** at the **Department of Physics, University of Colombo**, this project demonstrates how advanced sensing, automation, and communication can solve real-world challenges in **urban logistics** and **secure delivery**.

---

## 🧩 Key Features

### ✅ Automatic Mode
- Set the destination → Robot navigates autonomously using **GPS**.  
- Avoids obstacles in **real time** using ultrasonic sensors.  
- On arrival:  
  - Scans the **customer’s QR code** via front-facing camera.  
  - If scanning fails → fallback with secure code entry on keypad.  
- **Dual security**: QR verification + keypad authentication.  
- **Electromagnetic lock** opens only for authorized recipients.  
- Robot **returns automatically** to central hub after delivery.  

### 🎮 Manual Mode
- Remote control from **any IP address globally**.  
- Navigate safely using **real-time video stream** from the robot’s camera.  

---

## 🔧 Technologies Used

- **Raspberry Pi** – Camera integration, video streaming, QR recognition, remote control  
- **Arduino** – Motor control, ultrasonic sensors, electromagnetic lock  
- **GPS + HTML Map Interface** – Real-time tracking and routing  
- **Ultrasonic Sensors** – Intelligent obstacle avoidance  
- **Electromagnetic Lock + Keypad** – Secure, dual-authentication package access  
- **Python GUI + HTML Dashboard** – Local and remote control interfaces  

---

## ⚙️ System Architecture

1. **Autonomous Navigation**
   - GPS coordinates define route  
   - Raspberry Pi + HERE/Map API for mapping (or similar)  
   - Ultrasonic sensors prevent collisions  

2. **Secure Delivery**
   - Camera scans customer QR code  
   - Backup authentication via keypad  
   - Electromagnetic lock ensures only valid recipients can open  

3. **Remote Access**
   - Live video feed streamed from Pi camera  
   - Robot can be manually driven from a web interface anywhere in the world  

---
## Demo
![bot1](https://github.com/user-attachments/assets/6bb6c53a-928c-4792-be60-c5f035c003a4)




## 🛠️ Hardware Setup

- Raspberry Pi 4 Model B  
- Arduino (for low-level motor + sensor control)  
- GPS Module (Neo-6M)  
- Ultrasonic Sensors (front + sides for obstacle detection)  
- Camera Module (for QR scanning + video streaming)  
- Electromagnetic Lock + Keypad  
- Motor driver + DC motors with wheels  
- Power supply with dual-rail support  

---

## 💻 Software Stack

- **Languages**: Python, C/C++ (Arduino)  
- **Frameworks**: OpenCV (QR scanning), Flask/Django (dashboard)  
- **Tools**: HTML/JS (remote map + interface), AVR/Arduino IDE  
- **Protocols**: Bluetooth/Wi-Fi for comms, Serial for Pi–Arduino  

---

## 🚀 Getting Started

### Clone Repository
```bash
git clone https://github.com/<your-username>/urban-delivery-bot.git
cd urban-delivery-bot
