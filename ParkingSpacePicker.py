import cv2
import pickle

class CarParkImageEditor:
    def __init__(self, image_path, pos_file_path, width, height):
        self.img = cv2.imread(image_path)
        self.width, self.height = width, height
        self.pos_list = self.load_positions(pos_file_path)

    def load_positions(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def save_positions(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.pos_list, f)

    def handle_mouse_click(self, events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            self.pos_list.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(self.pos_list):
                x1, y1 = pos
                if x1 < x < x1 + self.width and y1 < y < y1 + self.height:
                    self.pos_list.pop(i)
        self.save_positions('CarParkPos')

    def process_image(self):
        img_copy = self.img.copy()
        for pos in self.pos_list:
            cv2.rectangle(img_copy, pos, (pos[0] + self.width, pos[1] + self.height), (255, 0, 255), 2)
        return img_copy

    def run(self):
        while True:
            img_to_display = self.process_image()

            cv2.imshow("Image", img_to_display)
            cv2.setMouseCallback("Image", self.handle_mouse_click)
            key = cv2.waitKey(1)

            if key == 27:  # 27 is the ASCII code for the Esc key
                break

if __name__ == "__main__":
    image_path = 'carParkImg.png'
    pos_file_path = 'CarParkPos'
    editor = CarParkImageEditor(image_path, pos_file_path, 107, 48)
    editor.run()

    cv2.destroyAllWindows()
