from pathlib import Path
import cv2
from datetime import datetime
import json
import time



##### configuration values
CAMERA_ID = 0
CAPTURE_INTERVAL_SECONDS = 10
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_IMAGE_FOLDER = BASE_DIR / "data" / "raw"
METADATA_FOLDER = BASE_DIR / "data" / "metadata"
METADATA_FILE = METADATA_FOLDER / "captures.jsonl"  # JSONL = JSON Lines format
IMAGE_PREFIX = "frame"
MAX_CAPTURES = 5 # for testing

def create_directories():
    """
    Create the folders we need if they do not already exist.
    """
    RAW_IMAGE_FOLDER.mkdir( parents = True, exist_ok = True)
    METADATA_FOLDER.mkdir( parents = True, exist_ok = True)
    

def open_camera( camera_id: int ):
    """
    Open the webcam and return the camera object.
    Raise an error if the camera cannot be opened.
    """
    camera = cv2.VideoCapture( camera_id )

    if not camera.isOpened():
        raise RuntimeError(f"Could not open camera with CAMERA_ID = {camera_id}")
    
    return camera

def generate_timestamps():
    """
    Return two timestamp formats:
    1. A filename-safe timestamp for image names
    2. An ISO timestamp for metadata logging
    """
    now = datetime.now()
    filename_timestamp = now.strftime("%Y%m%d_%H%M%S")
    iso_timestamp = now.isoformat()

    return filename_timestamp, iso_timestamp

def save_frame( frame, filename_timestamp ):
    """
    Save the captured frame to disk and return the file path.
    Raise an error if saving fails.
    """
    filename = f"{IMAGE_PREFIX}_{filename_timestamp}.jpg"
    image_path = RAW_IMAGE_FOLDER / filename

    success = cv2.imwrite( str(image_path), frame )

    if not success:
        raise RuntimeError(f"Failed to save image to {image_path}")

    return image_path
    
def append_metadata( image_path, iso_timestamp ):
    """
    Append one metadata record to a JSONL file.
    Each line is a separate JSON object.
    """
    record = {
        "timestamp": iso_timestamp,
        "image_path": str(image_path),
        "file_name": image_path.name,
        "status": "captured",
    }

    with open( METADATA_FILE, "a", encoding = "utf-8" ) as file:
        file.write( json.dumps( record ) + "\n" )


def capture_loop( camera, interval_seconds, camera_id ):
    """
    Repeatedly capture frames from the camera at the specified interval.
    """

    while True:
        success, frame = camera.read()

        if not success:
            print("Warning: Failed to capture frame. Retrying in 2 seconds...")
            time.sleep(2)
            continue
        
        filename_timestamp, iso_timestamp = generate_timestamps()

        try:
            image_path = save_frame( frame, filename_timestamp )
            append_metadata( image_path, iso_timestamp )
            print(f"\nSaved image: {image_path} at {iso_timestamp}")

        except Exception as error:
            print(f"Warning: {error}")

        time.sleep( interval_seconds )
        

def main():

    create_directories()
    camera = open_camera( CAMERA_ID )

    try:
        for _ in range( MAX_CAPTURES ):
            capture_loop( camera, CAPTURE_INTERVAL_SECONDS, CAMERA_ID )

    except KeyboardInterrupt:
        print("\nCapture stopped by user.")

    finally:
        camera.release()
        print("\nCamera released. Exiting.")

if __name__ == "__main__":
    main()