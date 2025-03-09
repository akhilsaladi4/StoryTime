import cv2
from fer import FER
import time

detector = FER(mtcnn = True)

def process_image(imgurl):
    begin = time.time()
    image = cv2.imread(imgurl)
    print(f"Processing: {imgurl}")
    # Detect emotions in the image
    results = detector.detect_emotions(image)

    
    if len(results) == 0:
        print("No faces found")
        return None
    else:
        if len(results) > 1:
            print(f"Found {len(results)} faces. Using the first one detected. Please only have one user")

        '''
        process the central face
        '''
        face = results[0]
        bounding_box = face["box"]
        emotions = face["emotions"]
        print(f"Bounding Box: {bounding_box}")
        print(emotions)
        print("Emotions:")
        for emotion, score in emotions.items():
            print(f"  {emotion}: {score:.2f}")
        print(f"Time taken: {time.time() - begin:.2f}s")
        print()
        return emotions