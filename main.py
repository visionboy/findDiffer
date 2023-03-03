import os, time
import pyautogui
from PIL import ImageChops
import cv2

width, height = 510, 409
x_pos, y_pos = 91, 353

# 스크린 캡쳐상 첫번째 이미지 가져오기
firstImg = pyautogui.screenshot(region=(x_pos, y_pos, width, height))
firstImg.save('firstImg.jpg')

# 스크린 캡쳐상 두번째 이미지 가져오기
secondImg = pyautogui.screenshot(region=(606, y_pos, width, height))
secondImg.save('secondImg.jpg')

diff = ImageChops.difference(firstImg, secondImg)
diff.save('diff.jpg')

# 파일 생성 대기
while not os.path.exists('diff.jpg'):
    time.sleep(1)

# 첫번째 이미지
firstImg_img = cv2.imread('firstImg.jpg')
# 두번째 이미지
secondImg_img = cv2.imread('secondImg.jpg')
# 첫번째와 두번째 이미지상 다른 부분표기 이미지
diff_img = cv2.imread('diff.jpg')

# 이미지 해상도상 테두리부분 점선들도 차이이미지로 나므로 색상변경
gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
gray = (gray > 25) * gray # 이 줄 추가
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

COLOR = (0, 200, 0)
for cnt in contours:
    if cv2.contourArea(cnt) > 100:
        x, y, width, height = cv2.boundingRect(cnt)
        # cv2.rectangle(firstImg_img, (x, y), (x + width, y + height), COLOR, 2)
        # cv2.rectangle(secondImg_img, (x, y), (x + width, y + height), COLOR, 2)
        cv2.rectangle(diff_img, (x, y), (x + width, y + height), COLOR, 2)

        # 각 그림의 틀린 x,y좌표값 구하기
        to_x = x + (width // 2)
        to_y = y + (height // 2) + y_pos
        
        # 틀린 그림 포지션으로 마우스 이동 및 클릭
        # pyautogui.moveTo(to_x, to_y, duration=0.15)
        # pyautogui.click(to_x, to_y)

# cv2.imshow('src', firstImg_img)
# cv2.imshow('dest', secondImg_img)
cv2.imshow('Image difference', diff_img)
cv2.waitKey(0) # 아무키나 눌러서 프로그램 종료
cv2.destroyAllWindows()

