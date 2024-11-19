import torch
import cv2
import os
import logging

# Initialize logging
logging.basicConfig(filename='object_detection.log', level=logging.INFO)

# Load the YOLOv5 model (pre-trained on COCO dataset)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s' is the small model

# Directory to store processed images
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

def detect_objects_in_image(image_path):
    # Read image
    img = cv2.imread(image_path)
    
    # Perform inference with YOLO
    results = model(img)
    
    # Get the detection results
    results_data = results.pandas().xywh[0]  # Get pandas dataframe of results
    return results_data

def process_images_from_directory(image_dir):
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        
        if image_path.endswith('.jpg') or image_path.endswith('.png'):
            logging.info(f"Processing image: {image_name}")
            
            # Run object detection
            results_data = detect_objects_in_image(image_path)
            
            # Save results to database
            save_detection_results_to_db(results_data, image_name)
            
            # Save annotated image
            results = model(image_path)
            results.save()  # Saves annotated image in 'runs/detect/exp'

            logging.info(f"Processed image: {image_name}")

def save_detection_results_to_db(results_data, image_name):
    try:
        # Connect to your database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()

        # Insert detection results into a database table (customize as needed)
        for index, row in results_data.iterrows():
            cursor.execute(f'''
                INSERT INTO object_detection_results (image_name, class, confidence, x_center, y_center, width, height)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (image_name, row['name'], row['confidence'], row['x_center'], row['y_center'], row['width'], row['height']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info(f"Saved detection results for {image_name} to the database.")
    
    except Exception as e:
        logging.error(f"Error saving detection results for {image_name}: {e}")

# Process images from a directory (e.g., 'images/Chemed')
process_images_from_directory('photos/@lobelia4cosmetics')
