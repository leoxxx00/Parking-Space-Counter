import cv2
import pickle
import cvzone
import numpy as np

class ParkingSpaceDetector:
    def __init__(self, video_path, pos_file_path, width, height):
        self.cap = cv2.VideoCapture(video_path)
        self.width, self.height = width, height
        self.pos_list = self.load_positions(pos_file_path)

    def load_positions(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def check_parking_space(self, img, img_pro):
        space_counter = 0

        for pos in self.pos_list:
            x, y = pos

            img_crop = img_pro[y:y + self.height, x:x + self.width]
            count = cv2.countNonZero(img_crop)

            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                space_counter += 1
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.rectangle(img, pos, (pos[0] + self.width, pos[1] + self.height), color, thickness)

        cvzone.putTextRect(img, f'Free Spaces Left: {space_counter}/{len(self.pos_list)}', (100, 50),
                           scale=3, thickness=5, offset=20, colorR=90)

    def process_frame(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, 25, 16)

        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.int8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        self.check_parking_space(img, img_dilate)

    def run(self):
        while True:
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            success, img = self.cap.read()

            self.process_frame(img)

            cv2.imshow("Image", img)
            cv2.waitKey(10)

if __name__ == "__main__":
    video_path = 'carPark.mp4'
    pos_file_path = 'CarParkPos'
    detector = ParkingSpaceDetector(video_path, pos_file_path, 107, 48)
    detector.run()
