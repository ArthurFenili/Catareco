import cv2
import numpy as np
import urllib.request

url = 'http://192.168.1.2/cam-hi.jpg'

whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = 'coco.names'
classNames = []

with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObject(outputs, im):
    hT, wT, cT = im.shape
    bbox = []
    classIds = []
    confs = []
    found_bottle = 0  # Initialize a variable to count bottles
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    print(indices)

    for i in indices:
        i = 0  # Ensure you access the correct index from indices
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        if classNames[classIds[i]] == 'bottle':
            found_bottle += 1  # Increment the bottle count

        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

    # Print the number of bottles found
    print(f'Total Bottles: {found_bottle}')

    # Salvar a imagem em um arquivo
    cv2.imwrite('detected_objects.jpg', im)

img_resp = urllib.request.urlopen(url)
imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
im = cv2.imdecode(imgnp, -1)
blob = cv2.dnn.blobFromImage(im, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
net.setInput(blob)
layer_names = net.getLayerNames()

outputNames = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

outputs = net.forward(outputNames)

findObject(outputs, im)

cv2.imshow('Image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
