.import cv2
import numpy as np
from skimage.measure import compare_ssim

def noiseCalibrate(cap,rob,bbLC,bbRC):
    diffPercent=0
    for i in range(30):
        ret,frame=cap.read()
        roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        (score,diff)=compare_ssim(rob,roi,full=True,multichannel=True)
        diffPercent+=score
    diffPercent/=30
    return diffPercent-.03


cap = cv2.VideoCapture(0)
bbLC=(0,0)
bbRC=(300,300)
textOrg=(20,50)
kernel=np.ones((5,5),np.uint8)
dontcare,temp=cap.read()
rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)
fingerCount=0
while True:
    ret,frame=cap.read()
    roi=frame[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
    (score,diff)=compare_ssim(rob,roi,full=True,multichannel=True)
    cv2.rectangle(frame,bbLC,bbRC,(0,255,0),0)
    if(score<diffPercent):
        diff = (diff * 255).astype("uint8")
        diff = cv2.morphologyEx(diff,cv2.MORPH_OPEN,kernel)
        diff = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        diff = cv2.GaussianBlur(diff,(5,5),100)
        th= cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV| cv2.THRESH_OTSU)[1]
        cnt, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(cnt, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(frame, [cnt], -1, (255,255,0), 2)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        if defects is not None:
            count=0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(frame,start,end,[0,255,0],2)
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                if angle <= np.pi/2:  # angle less than 90 degree, treat as fingers
                    count += 1
                    cv2.line(frame,start,far,[255,0,0],2)
                    cv2.line(frame,far,end,[255,0,0],2)
                    cv2.circle(frame, far, 4, [0, 0, 255], -1)
            if count > 0:
              count = count+1
            fingerCount=count
            cv2.putText(frame, str(fingerCount), textOrg,cv2.FONT_HERSHEY_SIMPLEX,1,[255,255,255])
    else:
        mask = np.zeros(roi.shape, dtype='uint8')
        th = np.zeros(roi.shape, dtype='uint8')
    cv2.imshow('diff',diff)
    cv2.imshow('sanitized',th)
    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    if (cv2.waitKey(1) & 0xFF == ord('r')):
        dontcare,temp=cap.read()
        rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
        diffPercent=noiseCalibrate(cap,rob,bbLC,bbRC)
        bkgrem=cv2.bgsegm.createBackgroundSubtractorGSOC(replaceRate=0,propagationRate=0)
cap.release()
cv2.destroyAllWindows()
