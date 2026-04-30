mkdirimport json
from pathlib import Path
import cv2


def read_jsonl(file_path):
    """
    Read a JSONL file and return a list of Python dictionaries.
    Raise an error if reading fails.
    """
    records = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                record = json.loads(line)
                records.append(record)

    except Exception as error:
        raise RuntimeError(f"Failed to read JSONL file {file_path}: {error}")

    return records


def load_images(metadata_file):
    """
    Load images based on metadata records in a JSONL file.
    Return a list of dictionaries with image data and metadata.
    Raise an error if loading fails.
    """
    images = []

    try:
        records = read_jsonl(metadata_file)

        for record in records:
            image_path = record.get("image_path")

            if image_path is None:
                print("Warning: record is missing 'image_path'. Skipping.")
                continue

            image_path = Path(image_path)

            if not image_path.exists():
                print(f"Warning: image file does not exist: {image_path}")
                continue

            image = cv2.imread(str(image_path))

            if image is None:
                print(f"Warning: failed to load image: {image_path}")
                continue

            images.append({
                "image": image,
                "image_path": str(image_path),
                "timestamp": record.get("timestamp"),
                "file_name": record.get("file_name"),
                "camera_id": record.get("camera_id"),
                "status": record.get("status")
            })

    except Exception as error:
        raise RuntimeError(f"Failed to load images from metadata file {metadata_file}: {error}")

    return images


def preprocess_images(images):
    """
    Preprocess the loaded images as needed.
    For now, this version simply returns the same images unchanged.
    """
    preprocessed_images = []

    for image_record in images:
        image = image_record["image"]

        preprocessed_images.append({
            "image": image,
            "image_path": image_record["image_path"],
            "timestamp": image_record["timestamp"],
            "file_name": image_record["file_name"],
            "camera_id": image_record["camera_id"],
            "status": image_record["status"]
        })

    return preprocessed_images


def main():
    base_dir = Path(__file__).resolve().parent.parent
    metadata_file = base_dir / "data" / "metadata" / "captures.jsonl"

    images = load_images(metadata_file)
    preprocessed_images = preprocess_images(images)

    print(f"Loaded {len(images)} images.")
    print(f"Preprocessed {len(preprocessed_images)} images.")


if __name__ == "__main__":
    main()