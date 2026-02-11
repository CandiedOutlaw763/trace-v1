# Trace v1 🕵️‍♂️

> **Track Digital Footprints Across the Web**

**Trace** is a username enumeration tool designed for OSINT (Open Source Intelligence) purposes. It allows you to input a single username and instantly scan over **400+ websites** to find matching profiles. Whether you are conducting a security audit, checking username availability, or investigating a digital footprint, Trace automates the search process with speed and precision.

## 🔗 Live Demo

Access the tool online here:
👉 **[https://trace-s4bi.onrender.com/](https://trace-s4bi.onrender.com/)**

## 🚀 Key Features

* **Massive Scope:** Scans 400+ platforms including major social media (Instagram, Twitter), coding platforms (GitHub, Replit), and niche forums.
* **High Speed:** Utilizes asynchronous requests (`aiohttp`) to check hundreds of sites in seconds, not minutes.
* **Real-Time Results:** Live feedback on found profiles with direct links to the accounts.
* **False Positive Reduction:** Smart status checking (HTTP 200 vs 404) to ensure accuracy.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Concurrency:** `aiohttp` / `asyncio` (for parallel requests)
* **Frontend:** HTML, CSS, JavaScript
* **Deployment:** Render

## 💻 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CandiedOutlaw763/trace-v1.git
    cd trace-v1
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    flask run
    ```

4.  **Open in Browser:**
    Navigate to `http://127.0.0.1:5000` to start tracing.

## ⚠️ Disclaimer

**For Educational and Ethical Use Only.**
This tool is intended to help users protect their own privacy or for authorized security assessments. The developer assumes no liability and is not responsible for any misuse or damage caused by this program. Please use responsibly.

## 📄 License

This project is open-source.
