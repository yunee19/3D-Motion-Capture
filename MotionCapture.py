import cv2
from cvzone.PoseModule import PoseDetector

# Initialize video capture and pose detector
cap = cv2.VideoCapture('Video.mp4')
detector = PoseDetector()
posList = []

while True:
    success, img = cap.read()

    # Exit loop if video frame is not read successfully
    if not success:
        break

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    # Check if lmList is empty
    if not lmList:
        print("No landmarks detected!")

    if bboxInfo:
        frame_pos_list = []
        for lm in lmList:
            # Ensure lm has at least 3 elements (x, y, z)
            if len(lm) >= 3:
                # Extract x, y, and z coordinates
                x, y, z = lm[:3]
                # Append to frame_pos_list
                frame_pos_list.extend([x, y, z])

        # Convert frame_pos_list to comma-separated string
        frame_pos_str = ','.join(map(str, frame_pos_list))

        # Append frame_pos_str to posList
        posList.append(frame_pos_str)

        print(len(posList))

    cv2.imshow("Image", img)

    # Capture key press
    key = cv2.waitKey(1)

    # Break loop on 'q' key press
    if key & 0xFF == ord('q'):
        break
    # Save data on 's' key press
    elif key & 0xFF == ord('s'):
        with open("AnimationFile.txt", 'w') as f:
            f.writelines("%s\n" % item for item in posList)
        print("Data saved to AnimationFile.txt")

# Release video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
