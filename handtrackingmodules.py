import cv2
import time
import mediapipe as mp







class handDetector():

    def __init__(self,mode=False,maxhands=6,detectioncon=0.5,trackcon=0.5) :
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.trackcon = trackcon




        self.mpHands = mp.solutions.hands
        self.mpdraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.detectioncon,self.trackcon)



    def findHands(self, img, draw=True ):
        imgrgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        
        return img

    
    def findPosition(self,img,handNo=0,draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c =img.shape
                cx,cy =int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(225,0,225),cv2.FILLED)
        
        return lmList

def main():
    PTIME =0
    CTIME =0

    detector = handDetector()
    cap = cv2.VideoCapture(0)

    while 1:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) !=0:
            print(lmList[4])

        CTIME =time.time()
        fps = 1/(CTIME-PTIME)
        PTIME =CTIME

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(225,0,255),3)
        cv2.imshow('output',img)
        cv2.waitKey(1)

if __name__ == "__main__" :
    main()
