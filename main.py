import pyaudio
import winsound
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

def record_voice(file_name):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 7
	WAVE_OUTPUT_FILENAME = "voices/" + file_name + ".wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	
	engine = pyttsx3.init()
	engine.setProperty('rate', 200) 
	engine.say("Этот звонок спецально для тебя!")
	engine.runAndWait()
	engine.say("Эта жизнь только для тебя")
	engine.runAndWait()
	engine.say("Привет на связи паукообразная коза, задай странный вопрос за 7 сек после сигнала  и получи странный ответ  ")
	engine.runAndWait()

	b.beep()
	


	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* done recording")
	b.beep(8)
	stream.stop_stream()
	stream.close()
	p.terminate()

	engine.say("Все внимательно записала, дай-ка подумать")
	engine.runAndWait()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
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
		engine = pyttsx3.init()
		engine.setProperty('rate', 200) 
		engine.say("Хм, какие-то проблемы с распознованием текста. Говори громче!")
		engine.runAndWait()
		raise e
	except sr.RequestError as e:
		print("Ошибка сервиса; {0}".format(e))

		engine = pyttsx3.init()
		engine.setProperty('rate', 200) 
		engine.say("Хм, какие-то проблемы с сервисом распознования")
		engine.runAndWait()
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

ser = serial.Serial('COM3', 9600)

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
				engine = pyttsx3.init()
				engine.setProperty('rate', 200) 

				#Здесь рабочий цикл программы
				record_voice(file_name) # рассказываем что к чему и пишем голос
				# Нужно добавить проверку если звонок сброшен
				text_recognizer(file_name) #распознаем речь
				


				translation = ts.google(text,from_language='ru', to_language='en',sleep_seconds = 5,if_use_cn_host=True)
				print("Перевод = "+ translation)
				engine.say("кажись я поняла тебя")
				engine.runAndWait()


				out = gpt_3(translation)

				predict = ts.google(out,from_language='en', to_language='ru',sleep_seconds = 5,if_use_cn_host=True)

				
				engine.say(predict)
				engine.runAndWait()
				engine.say("Это все что я хотел сказать, понимай как хочешь, пока-пока ")
				engine.runAndWait()
				time.sleep(10)


				#Делаем цикл что бы положили трубку
				while True:
					update_serial()
					if button == 0:
						print("Один цикл завершен")
						break


	except Exception as e:
		print(e)