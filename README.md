
# 🌟 **TaskManager** 🌟

TaskManager — это современное приложение для управления задачами, разработанное с акцентом на **безопасную авторизацию** с использованием **JWT (JSON Web Tokens)**. Проект создан для изучения и реализации интересующих меня методологий в области авторизации и управления токенами, с упором на безопасность и производительность.

---

## 🚀 **Особенности**

### 🔒 **JWT Авторизация**
- Поддержка **безопасной авторизации** через JWT.
- Используется **сложный секрет** для подписи токенов, что делает их устойчивыми к атаке перебором.
- Синхронное шифрование, обеспечивающее простоту реализации и безопасность.
- Реализована система обновления токенов с сохранением каждого рефреш токена в базе данных.
- При каждом обновлении старый рефреш токен становится недействительным, даже если его срок действия не истек. Это предотвращает повторное использование и улучшает безопасность.

### ⚡ **Асинхронность**
- Весь стек приложения поддерживает асинхронность, что позволяет обрабатывать большое количество запросов одновременно, без блокировки потоков.
- Используется асинхронная версия SQLAlchemy для работы с базой данных.
- Реализованы асинхронные маршруты FastAPI, обеспечивающие высокую производительность и отзывчивость приложения.

### 🧰 **Кеширование сессий с помощью Redis**
- Сессии пользователей кешируются в **Redis**, что обеспечивает быстрый доступ к данным авторизации.
- В кеше хранятся JWT токены для быстрого чтения и проверки.
- **Время жизни кеша** для токенов контролируется, что гарантирует своевременную их ротацию.

### 🔄 **Фоновые задачи с Celery**
- В качесте брокера для передачи задач между приложением и воркерами используется Redis.
- Воркеры Celery обрабатывают задачи, забирая их из очереди.
- Результаты выполнения задач также сохраняются в Redis.
- Также для мониторинга используется удобный инструмент Flower, который позволяет отслеживать статусы задач, количество задач в очереди, статистику воркеров, логи ошибок задач.
- Реализовано логирование.

### 🔑 **Система ролей и ограничение доступа**
- Реализована система ролей ('guest', 'user', 'admin').
- Ограничение доступа к различным ресурсам и действиям на основе ролей.
- Простая интеграция с JWT для проверки прав доступа.

### 💾 **База данных**
- Хранение данных реализовано с помощью **SQLite**, что обеспечивает легкость развертывания и использования.
- Управление базой данных осуществляется через **SQLAlchemy ORM** для удобной работы с запросами.

---

## 🛠 **Технические детали**

- **Язык разработки:** Python.
- **Фреймворк:** FastAPI
- **База данных:** SQLite с использованием SQLAlchemy ORM.
- **Кеш:** Redis для быстрого доступа к данным сессий и токенов.
- **Алгоритм подписи токенов:** HMAC (синхронный) с планами перехода на **асинхронное шифрование** (RSA).
- **Фоновые задачи:** Celery.
- **Брокер сообщений:** Redis.
- **Основные зависимости:**
  - `FastAPI` для написания API.
  - `pydantic` для валидации данных.
  - `PyJWT` для работы с токенами.
  - `SQLAlchemy` для ORM.
  - `aioredis` для асинхронного кеширования.
  - `celery` для выполнения фоновых задач.
  - `redis` как брокер сообщений и БД для хранения задач.
  - `Jinja2` для рендеринга шаблонов.
---

## 💡 **Цели проекта**

Главная цель проекта — **отработка и реализация интересующих методологий**, в частности:

1. Разработка **безопасной системы авторизации** с использованием JWT.
2. Углубленное изучение работы с рефреш токенами, обеспечивающими ротацию и контроль доступа.
3. Реализация **системы ролей** для ограничения доступа.
4. Практика работы с базой данных и ORM-инструментами, такими как SQLAlchemy.
5. Реализация кеширования данных с использованием Redis для повышения производительности и масштабируемости.

---

## 🔮 **Планы на будущее**

- 🚧 Переход с синхронного шифрования на **асинхронное шифрование** (например, RSA или ECDSA).
- 🛠 Расширение функционала TaskManager для поддержки:
  - Масштабируемых баз данных.
  - Интеграции с внешними API.
  - Присоединение к микросервисному приложению
  - Создание удобного пользовательского интерфейса.
- 🌐 Расширение функционала кеширования:
  - Кеширование задач для быстрого доступа.
  - Хранение временных данных для аналитики.

---

## 📦 **Установка и запуск**

### 📥 **Шаг 1: Клонируйте репозиторий**
```bash
git clone https://github.com/Pup0chek/TaskManager.git
cd TaskManager
```

### 🛠 **Шаг 2: Установите зависимости**
Рекомендуется использовать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```

### ▶️ **Шаг 3: Запустите приложение**
```bash
python app.py
```

Приложение будет доступно по адресу: `http://127.0.0.1:5000`.

---

### 🖥 Развертывание на сервере
Приложение развернуто на виртуальном хостинге TimeWeb и доступно по следующему адресу: http://194.87.133.31:8000/docs

### 🐳 Docker-развертывание
Приложение развернуто в контейнере Docker с использованием docker-compose, что обеспечивает лёгкость и унифицированность развертывания.

Для развертывания приложения в Docker:

Соберите контейнер:

```bash
docker-compose up --build -d
```
Приложение будет доступно на порту 8000.

---

## 🛡 **Безопасность**

- Используется сложный секрет для подписи токенов, который генерируется автоматически.
- Каждый рефреш токен сохраняется в базе данных и перезаписывается при обновлении, исключая возможность повторного использования.
- Все токены ограничены по времени действия.
- **Сессии кешируются в Redis**, что сокращает время проверки токенов.
- Система ролей обеспечивает ограничение доступа к действиям и данным на основе привилегий.

---

## 📚 **Документация API**

| Метод   | Путь                | Описание                                                         |
|---------|---------------------|------------------------------------------------------------------|
| `POST`  | `/login`            | Авторизация и выдача JWT токена.                                 |
| `POST`  | `/refresh`          | Обновление токена через рефреш.                                  |
| `GET`   | `/tasks`            | Получение списка задач.                                          |
| `POST`  | `/tasks`            | Создание новой задачи.                                           |
| `GET`   | `/tasks/{id}`       | Обновление существующей задачи.                                  |
| `DELETE`| `/tasks/{id}`       | Удаление задачи.                                                 |
| `GET`   | `/admin`            | Доступ к административным функциям (только для администраторов). |



