# 🚀 SUMO-AI

🎉 Sumo dataset > Sumo data analyses > Sumo AI

---

## 🧐 About

We're a couple nerd students with a vision to create an AI to predict SUMO matches.

Show us some love with a ⭐ if you like what we’re building—this is our passion project!

---

## ✨ Features

- 🥷 **View SUMO information in a nice clear way.**
- 🎮 **Try and win against our AI in the predictions.**
- 📱 **Mobile-friendly.**
- 🔒 **Secure authentication**
- 🐳 **Dockerized for easy deployment.**

---

## 🛠️ How to Run SUMO-AI

Follow these steps to set up SUMO-AI locally. 🚀  

1. **Generate Certificates**  
  Use this command (requires GIT installed):  
  *Used in a Bash terminal.*
  ```bash
  "C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout nginx/certs/nginx.key -out nginx/certs/nginx.crt -days 365 -nodes  
  ```
  
2. **Start the Application**  
  Spin it up using Docker:  
  ```cmd
  .\run.bat  
  ```

### **Local Backend Setup**  

First, make sure to setup the environment variables:

1. Create a `.env` file in the `backend` folder.
2. Copy over all values from `env.example`.
3. Change them however you see fit.

4. Create a virtual environment:  
  *Use python 3.12+.*
  ```cmd
  cd .\backend\

  py -m venv venv

  .\venv\Scripts\activate
  ```

5. Install requirements:
  ```cmd
  pip install -r .\requirements.txt
  ```

6. Run the Backend:
  ```cmd
  python .\main.py
  ```

---

### **Local Frontend Setup**  

1. Create a `.env` file in the `frontend` folder.
2. Copy over all values from `env.example`.

1. Navigate to the `frontend` folder:  
  ```cmd
  cd .\frontend\  
  ```

2. Install dependencies:
  ```cmd
  npm i  
  ```

3. Start the development server:
  ```cmd
  npm run dev
  ``` 

---

## 🎯 Usage  

- **Backend API Docs**: [https://localhost/api/latest/docs](https://localhost/api/latest/docs)  
- **Frontend App**: [http://localhost/](http://localhost/)  
<!-- - **phpMyAdmin**: [http://localhost:8080/](http://localhost:8080/)   -->

Locally:
- **Backend API Docs**: [http://localhost:8000/api/latest/docs](https://localhost:8000/api/latest/docs)  
- **Frontend App**: [http://localhost:5173/](http://localhost:5173/)  

---

## ⚙️ Technologies  

### 🖥️ **Backend**  
- 🐍 **Python (FastAPI)**: Robust and modern backend framework.  
- ⚡ **WebSockets**: For real-time updates.  
- 🧩 **nginx**: HTTPS reverse proxy.  
- 🐋 **Docker**: Containerization for easy deployment.  
- 🛢️ **MySQL / SQLite**: Reliable database solution.  
- 🛠️ **phpMyAdmin**: Manage the database effortlessly.  

### 🌐 **Frontend**  
- 🟢 **Node.js**: JavaScript runtime.  
- 🚀 **Vite**: Lightning-fast development tool.  
- 🎨 **Vue 3**: Reactive frontend framework.  

---

<!-- ## 🤝 Contribute  

Want to make Quizzap even better? Awesome! Here's how you can help:  

1. Fork the repository.  
2. Create a feature branch:  
  ```cmd
  git checkout -b feature-name
  ```

3. Commit your changes:  
  ```cmd
  git commit -m "Add your message here" 
  ``` 

4. Push the branch:  
  ```cmd
  git push origin feature-name
  ```

5. Open a Pull Request.

--- -->

<!-- ## 📜 License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

🚀 **Ready to start quizzing? Let's go!** -->

