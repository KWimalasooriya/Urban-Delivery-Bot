import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")  # Use "yolov8n.pt" (Nano) for faster performance

# Open the webcam (0 = default laptop camera)
cap = cv2.VideoCapture(0)

# Set camera resolution (optional)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Failed to capture frame")
        break

    # Run YOLO object detection
    results = model(frame)

    # Plot results on the frame
    annotated_frame = results[0].plot()

    # Show the output
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
