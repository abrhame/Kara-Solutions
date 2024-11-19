# **Ethiopian Medical Business Data Warehouse**

## **Overview**
This project builds a **data warehouse** to store and analyze data related to Ethiopian medical businesses scraped from public Telegram channels. It includes pipelines for **data scraping**, **cleaning**, **object detection** using YOLO, and exposing the collected data via **FastAPI**. The system is designed to be scalable, reliable, and insightful.

---

## **Features**
### 1. **Data Scraping Pipeline**
- Extract data from Telegram channels using `telethon` and custom Python scripts.
- Target channels include:
  - [DoctorsET](https://t.me/DoctorsET)  
  - [Chemed Telegram Channel](https://t.me/lobelia4cosmetics)  
  - [Yetena Weg](https://t.me/yetenaweg)  
  - [EAHCI](https://t.me/EAHCI)  
  - Additional channels from [Telegram Stats](https://et.tgstat.com/medicine).
- Collect and store images for object detection.

### 2. **Data Cleaning and Transformation**
- Perform cleaning operations:
  - Remove duplicates.
  - Handle missing values.
  - Standardize formats.
- Transform data using **DBT (Data Build Tool)** for SQL-based processing.

### 3. **Object Detection Using YOLO**
- Detect objects in images from Telegram channels using YOLO.
- Process detection results for bounding boxes, confidence scores, and class labels.
- Store extracted insights in the database.

### 4. **Data Warehouse Design**
- Centralized storage for cleaned and enriched data.
- Facilitate advanced analytics to identify trends, patterns, and insights.

### 5. **Exposing Data via FastAPI**
- RESTful API endpoints for CRUD operations.
- Integrate with SQLAlchemy for database management.

---

## **Technologies Used**
- **Languages**: Python
- **Libraries and Frameworks**:
  - Data Scraping: `telethon`
  - Data Transformation: `DBT`, `SQLAlchemy`
  - Object Detection: YOLO (`PyTorch`, `OpenCV`)
  - API Development: `FastAPI`, `Uvicorn`
- **Database**: PostgreSQL (or similar relational database)
- **Logging & Monitoring**: Custom logging for pipeline tracking.

---

## **Use Case**
This solution provides actionable intelligence about Ethiopian medical businesses by:
- Centralizing fragmented data scraped from Telegram channels.
- Enhancing analysis with object detection.
- Supporting fast, reliable decision-making through structured and queryable data.

---

## **Setup Instructions**

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-repo-name.git
cd Kara-Solutions-main
```

### 2. **Set Up the Environment**
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Configure database settings in `database.py`.

### 3. **Run Data Pipelines**
- Execute scripts for data scraping, cleaning, and transformation.

### 4. **Set Up YOLO**
- Clone the YOLO repository:
  ```bash
  git clone https://github.com/ultralytics/yolov5.git
  cd yolov5
  pip install -r requirements.txt
  ```

### 5. **Run FastAPI Server**
- Start the server:
  ```bash
  uvicorn scripts.main:app --reload
  ```

---

## **Deliverables**
- Data scraping and transformation pipelines.
- Object detection insights from Telegram images.
- Scalable data warehouse with ETL/ELT processes.
- RESTful API for data access and management.

---

## **Contributions**
Contributions are welcome! Please fork the repository and submit a pull request for feature suggestions or bug fixes.

