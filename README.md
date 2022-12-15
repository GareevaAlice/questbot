# questbot
Телеграм-бот для создания и прохождения текстовых квестов
[https://t.me/quest_chest_bot](https://t.me/quest_chest_bot)

Туториал: [https://gareevaalice.github.io/questbot/tutorial.html](https://gareevaalice.github.io/questbot/tutorial.html)


## Настройка
Нужно положить в файл `.env`:
```
BOT_TOKEN = <BOT_TOKEN>
```

## Запуск
```
docker build . -t questbot
docker run questbot
```
