import cv2
import dlib
import csv
import pathlib
from datetime import datetime
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600
face_x2,face_y2 = 0,0

def detectAndTrackLargestFace():
    print('start')
    
    capture = cv2.VideoCapture(0)

    #cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

    #cv2.moveWindow("base-image",0,100)
    cv2.moveWindow("result-image",400,50)

    #cv2.startWindowThread()

    tracker = dlib.correlation_tracker()
    counter=0
    move=[]
    
    secs=1
    t1=datetime.now()
   
    trackingFace = 0

    rectangleColor = (0,165,255)




    try:
        while True:
            rc,fullSizeBaseImage = capture.read()

            baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))

            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('q'):
                cv2.destroyAllWindows()
                exit(0)



            resultImage = baseImage.copy()






            if not trackingFace:

                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                print("Detector searching for face")
                t2=datetime.now()
                delta=t2-t1
                sec=delta.seconds
                #print(sec)
                if sec==secs :
                    move.append(counter)
                    move.append(0)
                    csvfile=open('data.csv','a+', newline='')
                    obj=csv.writer(csvfile)
                    obj.writerow(move)
                    csvfile.close()
                    move.clear()
                    counter=counter+1
                    secs=secs+1



                maxArea = 0
                x = 0
                y = 0
                w = 0
                h = 0

                for (_x,_y,_w,_h) in faces:
                    if  _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h

                if maxArea > 0 :

                    tracker.start_track(baseImage,
                                        dlib.rectangle( x-10,
                                                        y-20,
                                                        x+w+10,
                                                        y+h+20))

                    trackingFace = 1

            if trackingFace:

                trackingQuality = tracker.update( baseImage )
               

                if trackingQuality > 5:
                    tracked_position =  tracker.get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(resultImage, (t_x, t_y),
                                                (t_x + t_w , t_y + t_h),
                                                rectangleColor ,2)
                    face_x2,face_y2 = (t_x +(t_x + t_w)) //2 , (t_y +(t_y + t_h)) //2
                    center = cv2.circle(resultImage,(face_x2,face_y2),3,(0, 255, 0), 2)
                    
                    trackmove=int(trackingQuality)
                    t2=datetime.now()
                    delta=t2-t1
                    sec=delta.seconds
                    if sec==secs :
                        move.append(counter)
                        move.append(trackmove)
                        csvfile=open('data.csv','a+', newline='')
                        obj=csv.writer(csvfile)
                        obj.writerow(move)
                        csvfile.close()
                        move.clear()
                        counter=counter+1
                        secs=secs+1
                   
                                                

                else:
                    trackingFace = 0





            largeResult = cv2.resize(resultImage,
                                     (OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))
            #cv2.imshow("base-image", baseImage)
            cv2.imshow("result-image", largeResult)
            
            




    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)



if __name__ == '__main__':
    detectAndTrackLargestFace()
   