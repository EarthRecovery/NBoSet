import time
import cv2
from picamera2 import Picamera2

# Initialize the Picamera2 object
picam2 = Picamera2()

# Configure the camera
camera_config = picam2.create_preview_configuration(main={"size": (1080, 720)})
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Allow the camera to warm up
time.sleep(2)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

frame_num=0
store_rects = None

try:
    while True:
        # Capture a frame
        frame = picam2.capture_array()

        # Convert the frame to BGR (OpenCV uses BGR by default)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if (frame_num % 5 )== 0:
            (rects, weights) = hog.detectMultiScale(frame_bgr, winStride=(8, 8), padding=(8, 8), scale=1.10)
            store_rects = rects
        else:
            rects = store_rects
        
        for (x, y, w, h) in rects:
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Camera Feed", frame_bgr)

        frame_num += 1

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    pass

finally:
    # Stop the camera and close the window
    picam2.stop()
    cv2.destroyAllWindows()
