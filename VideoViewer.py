import cv2 as cv

video_file = "rtsp://210.99.70.120:1935/live/cctv001.stream"

video = cv.VideoCapture(video_file)
blur_ksize = (3, 3)
blur_sigma = 3
video_rmode = 0
video_cmode = 0
recording = False
out = None

fourcc = cv.VideoWriter_fourcc(*'MP4V')

if video.isOpened():
    fps = video.get(cv.CAP_PROP_FPS)
    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    

    while True:
        valid, img = video.read()
        if not valid:
            break
        
        if video_cmode == 1:
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img_blur = cv.GaussianBlur(img_gray, blur_ksize, blur_sigma)
            img = cv.Canny(img_blur, 0, 200)
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        if video_rmode == 1:
            if not recording:
                recording = True
                out = cv.VideoWriter('output.mp4', fourcc, 60, (frame_width, frame_height))
            cv.circle(img, (10,10), radius=10, color=(0,0,255), thickness=-1)
        else:
            if recording:
                out.release()
                recording = False 
             
        cv.imshow('Video Player', img)
        if recording:
            out.write(img)
        
        key = cv.waitKey(1)
        if key == 27: # 종료
            break
        elif key == ord(' '): # 모드
            video_rmode = (video_rmode+1)%2
            
        elif key == ord('/') or key == ord('?'): # 추가 기능
            video_cmode = (video_cmode+1)%2
        
    cv.destroyAllWindows()