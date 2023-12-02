import cv2
import numpy as np
import urllib.request
import subprocess

class CamYolo:
    def __init__(self, url, whT=320, confThreshold=0.5, nmsThreshold=0.3, classesfile='coco.names',
                 modelConfig='yolov3.cfg', modelWeights='yolov3.weights'):
        self.url = url
        self.whT = whT
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.classesfile = classesfile
        self.classNames = []

        with open(self.classesfile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        self.net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def find_objects(self, outputs, im):
        hT, wT, cT = im.shape
        bbox = []
        classIds = []
        confs = []
        found_bottle = 0

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)

        for i in indices:
            i = 0
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            if self.classNames[classIds[i]] == 'bottle':
                found_bottle += 1

            # cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
            # cv2.putText(im, f'{self.classNames[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        print(f'Total Bottles: {found_bottle}')
        cv2.imwrite('detected_objects.jpg', im)

        return found_bottle

    def process_image(self):
        img_resp = urllib.request.urlopen(self.url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        blob = cv2.dnn.blobFromImage(im, 1 / 255, (self.whT, self.whT), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()
        output_names = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(output_names)
        bottles = self.find_objects(outputs, im)
        print("AFTER FIND")
        # cv2.imshow('Image', im)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return bottles

    def call_detect(self):
        #self.process_image()
        command = "python trash_recognition/yolov5/detect.py --weights trash_recognition/yolov5/weights/best.pt --save-txt --source detected_objects.jpg"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print(process.returncode)
        # Open the file in read mode ('r')
        with open('return.txt', 'r') as file:
            # Read the entire content of the file
            content = file.read()
        content = content.split(',')
        return content
        


# # Example of how to use the class
# url = 'http://192.168.1.2/cam-hi.jpg'
# cam_yolo_instance = CamYolo(url)
# cam_yolo_instance.process_image()
