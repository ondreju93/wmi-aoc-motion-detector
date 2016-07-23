# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
 
# argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=200, help="minimum area size")
args = vars(ap.parse_args())
 
camera = cv2.VideoCapture(0)
time.sleep(0.25)
 

# inicjalizacja - klatka pusta
firstFrame = None

# petla po klatkach nagrania
while True:
	# Pobierz obraz z kamery
	(grabbed, frame) = camera.read()
	text = "Pusty"
 
        # jezeli obraz nie moze byc przechwycony, zakoncz
        if not grabbed:
                break
 
	# rozmiar, skala szarosci, blur
	frame = imutils.resize(frame, width=700)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (11, 11), 0)
 
        # inicjalizacja
	if firstFrame is None:
		firstFrame = gray
		continue

        # roznica miedzy aktualna klatka a pierwsza	
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# poszerzenie i szukanie konturow na tresh'u
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	# petla po konturach
	for c in cnts:
		# jezeli kontur jest za maly, ignoruj
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# oblicz wspolrzedne dla ramki - prostokata
		# aktualizuj tekst
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Pelny"

        # umiesc na ekranie tekst i date
        cv2.putText(frame, "Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# pokaz klatke
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)

        
        key = cv2.waitKey(1) & 0xFF
 
	# na nacisniecie q, wyjdz
	if key == ord("q"):
		break
 
# czyszczenie
camera.release()
cv2.destroyAllWindows()
                
