#_*_ coding: utf-8 _*_
voices = ["Этот звонок спецально для тебя! Этот праздник только для тебя","Привет, рад видеть тебя, я отвечаю на самые сокровенные вопросы. Подумай что тебя беспокоит и спроси з 7 секунд после сигнала", "Поняла тебя, дай-ка подумать минутку.","Это все что я думаю, понимай как хочешь, пока-пока","Какие-то проблемы с распознованием текста. Говори громче!","Какие-то проблемы с сервисом распознования"]
from gtts import gTTS

number = 0
for i in voices:
	tts = gTTS(text = i, lang ='ru')
	tts.save("voice_speech/"+ str(number)+".mp3")
	print("Done")
	number+=1