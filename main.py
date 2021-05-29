#_*_ coding: utf-8 _*_
import pyaudio

import speech_recognition as sr
import time
import os
import pyaudio
import wave
import pyttsx3
import translators as ts
import requests
import uuid
import beepy as b 
import serial
from playsound import playsound
from gtts import gTTS
import multiprocessing

def record_voice(file_name):
	
	RECORD_SECONDS = 7
	

	
	playsound("voice_speech/0.mp3")
	playsound("voice_speech/1.mp3")

	b.beep()
	
	print("* recording")
	os.system("arecord --device=hw:0,0 --format S16_LE -c 2  --rate 48000 -d " + str(RECORD_SECONDS)+ " voices/" + file_name + ".wav")

	

	print("* done recording")
	b.beep(8)
	

	playsound("voice_speech/2.mp3")#Поняла тебя дайка подумать минутку
	
	return 0

text =''

def text_recognizer(file_name):
	r = sr.Recognizer()
	with sr.AudioFile("voices/" + file_name + ".wav") as source:
			audio = r.listen(source)
	try:
		global text
		text = r.recognize_google(audio, language = "ru-RU")
		print(text)
	except sr.UnknownValueError as e:
		print("Непоняточка номер")
		playsound("voice_speech/4.mp3")
		raise e
	except sr.RequestError as e:
		print("Ошибка сервиса; {0}".format(e))
		playsound("voice_speech/5.mp3")
	return 0


def gpt_3(translation):
	r = requests.post(
		"https://api.deepai.org/api/text-generator",
		data={
			'text': translation ,
		},
		headers={'api-key': '7e828e96-862b-4ef5-8b1d-6b9cf031a2b9'}
	)
	print (r.json())
	return (r.json())['output'].replace("\n", " ")

ser = serial.Serial('/dev/ttyUSB0', 9600)

def update_serial():
	while ser.in_waiting:  
		line = (ser.readline().decode("utf-8")).split()[0] 
		global button
		global motion 
		if line == 'Motion':
			motion = 1
		if line == "Release":
			button = 1
		if line == "Holded":
			button = 0
	
  #Основной цикл программы  
motion = 0
button = 0
while True:
	try:
		while True:
			

			update_serial()
			if motion == 1 and button == 0  : # Звонилка
				playsound('ring.mp3')
				motion = 0

			#Кто то снял трубку 
			if button == 1 :
				playsound('up.mp3')
				#Генерируем случайное имя файла 
				file_name = str(uuid.uuid4())

				#Здесь рабочий цикл программы
				record_voice(file_name) # рассказываем что к чему и пишем голос

				p = multiprocessing.Process(target=playsound, args=("wait.mp3",))
				p.start()#Запустил музыку для ожидания
				print("Включаю музыкуожидания")




				# Нужно добавить проверку если звонок сброшен
				text_recognizer(file_name) #распознаем речь
				


				translation = ts.google(text,from_language='ru', to_language='en',sleep_seconds = 1,if_use_cn_host=True)
				print("Перевод = "+ translation)
				

				out = gpt_3(translation)
				print("Ответ получен")
				

				predict = ts.google(out,from_language='en', to_language='ru',sleep_seconds = 1,if_use_cn_host=True)
				print("Перевожу ответ")
				



				
				#engine.say(predict)
				#engine.runAndWait()
				tts = gTTS(text = predict, lang ='ru')
				tts.save("out_from_google.mp3")

				p.terminate() # Торможу музыку ожидания


				playsound('out_from_google.mp3')
				playsound('voice_speech/3.mp3')

				time.sleep(10)


				#Делаем цикл что бы положили трубку
				while True:
					update_serial()
					if button == 0:
						print("Один цикл завершен")
						break


	except Exception as e:
		print(e)