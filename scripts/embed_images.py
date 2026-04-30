import json
from pathlib import Path
import cv2

from PIL import Image

def read_jsonl( file ):
    """
    Read a JSONL file and return the data as a Python object.
    Raise an error if reading fails.
    """
    records = []

    try:
        with open( file, "r", encoding = "utf-8" ) as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                record = json.loads( line )
                records.append( record )

    except Exception as error:
        raise RuntimeError(f"Failed to read JSON file {file}: {error}")

    return records

    
def load_images( metadata_file ):
    """
    Load images based on metadata records in a JSONL file.
    Return a list of dictionaries with image data and metadata.
    Raise an error if loading fails.
    """
    images = []

    try:
        records = read_jsonl( metadata_file )

        for record in records:
            image_path = record.get("image_path")

            if image_path is None:
                print("Warning: record is missing 'image_path'. Skipping.")
                continue

            image_path = Path( image_path)
            if not image_path.exists():
                print(f"Warning: image file does not exist: {image_path}")
                continue
            
            image = cv2.imread( str(image_path) )

            if image is None:
                print(f"Warning: failed to load image: {image_path}")
                continue

            images.append( {
                "image": image,
                "image_path": str(image_path),
                "timestamp": record.get("timestamp")
                "file_name": record.get("file_name")
            })

    except Exception as error:
        raise RuntimeError(f"Failed to load images from metadata file {metadata_file}: {error}")

    return images

def preprocess_images( images ):
    """
    Preprocess the loaded images as needed (e.g., resizing, normalization).
    This is a placeholder function and can be customized based on requirements.
    """
    preprocessed_images = []

    for image_record in images:
        # Placeholder for actual preprocessing steps
        bgr_image = image_record["image"]

        rgb_image = cv2.cvtColor( bgr_image, cv2.COLOR_BGR2RGB )
        pil_image = Image.fromarray( rgb_image )

        preprocessed_images.append( {
            "image": pil_image,
            "image_path": image_record["image_path"],
            "timestamp": image_record["timestamp"],
            "file_name": image_record["file_name"]
        })

    return preprocessed_images

def load_clip_model():
    pass

def generate_embeddings( preprocessed_images, processor, model ):
    pass

def save_embeddings( base_dir, embeddings_array, mapping ):
    pass

def main():
    base_dir = Path(__file__).resolve().parent.parent
    metadata_file = base_dir / "data" / "metadata" / "captures.jsonl"

    images = load_images( metadata_file )
    preprocessed_images = preprocess_images( images )

    print(f"Loaded and preprocessed {len(preprocessed_images)} images based on metadata from {metadata_file}")

if __name__ == "__main__":
    main()