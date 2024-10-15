from aiogram import Bot, Dispatcher, executor, types
import requests
import json

openweathermap_API_key = ''
weather_API_key = ''
bot = Bot(token=weather_API_key)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def start(message):
    await bot.send_message(message.from_user.id, "Hi! I'm a weather bot. Write the name of the city, I'll help you with the forecast.")

@dp.message_handler()
async def send_message(message: types.Message):
	code = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(message.text, openweathermap_API_key))

	if code.status_code == 200:
		answer = code.text
		res = json.loads(answer)
		weather = res.get('weather')[0].get('main')
		temp = res.get('main').get('temp')
		pressure = res.get('main').get('pressure')
		humidity = res.get('main').get('humidity')
		wind = res.get('wind').get('speed')
		await message.reply('The weather in {} - {}, temp - {}°C, pressure - {}mm, humidity - {}, wind - {}m/s'.format(message.text, weather, round(temp - 273.15), pressure, humidity, wind))

	else:
		await message.reply('No such city was found. Try again')

executor.start_polling(dp, skip_updates=True)
