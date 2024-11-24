
# 🌟 **TaskManager** 🌟

TaskManager — это современное приложение для управления задачами, разработанное с акцентом на **безопасную авторизацию** с использованием **JWT (JSON Web Tokens)**. Проект создан для изучения и реализации интересующих меня методологий в области авторизации и управления токенами, с упором на безопасность и производительность.

---

## 🚀 **Особенности**

### 🔒 **JWT Авторизация**
- Поддержка **безопасной авторизации** через JWT.
- Используется **сложный секрет** для подписи токенов, что делает их устойчивыми к атаке перебором.
- Синхронное шифрование, обеспечивающее простоту реализации и безопасность.

### ⚡ **Асинхронность**
- Весь стек приложения поддерживает асинхронность, что позволяет обрабатывать большое количество запросов одновременно, без блокировки потоков.
- Используется асинхронная версия SQLAlchemy для работы с базой данных.
- Реализованы асинхронные маршруты FastAPI, обеспечивающие высокую производительность и отзывчивость приложения.

### ♻️ **Рефреш токены**
- Реализована система обновления токенов с сохранением каждого рефреш токена в базе данных.
- При каждом обновлении старый рефреш токен становится недействительным, даже если его срок действия не истек. Это предотвращает повторное использование и улучшает безопасность.

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
- **Фреймворк:** FastAPI — укажите подходящий.
- **База данных:** SQLite с использованием SQLAlchemy ORM.
- **Алгоритм подписи токенов:** HMAC (синхронный) с планами перехода на **асинхронное шифрование** (например, RSA).
- **Основные зависимости:**
  - `FastAPI`
  - `PyJWT` для работы с токенами.
  - `SQLAlchemy` для ORM.

---

## 💡 **Цели проекта**

Главная цель проекта — **отработка и реализация интересующих методологий**, в частности:

1. Разработка **безопасной системы авторизации** с использованием JWT.
2. Углубленное изучение работы с рефреш токенами, обеспечивающими ротацию и контроль доступа.
3. Реализация **системы ролей** для ограничения доступа.
4. Практика работы с базой данных и ORM-инструментами, такими как SQLAlchemy.

---

## 🔮 **Планы на будущее**

- 🚧 Переход с синхронного шифрования на **асинхронное шифрование** (например, RSA или ECDSA).
- 🛠 Расширение функционала TaskManager для поддержки:
  - Масштабируемых баз данных.
  - Интеграции с внешними API.
  - Создание удобного пользовательского интерфейса

---

## 📦 **Установка и запуск**

### 📥 **Шаг 1: Клонируйте репозиторий**
```bash
git clone https://github.com/your-username/taskmanager.git
cd taskmanager
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

## 🛡 **Безопасность**

- Используется сложный секрет для подписи токенов, который генерируется автоматически.
- Каждый рефреш токен сохраняется в базе данных и перезаписывается при обновлении, исключая возможность повторного использования.
- Все токены ограничены по времени действия.
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

---

## ❤️ **Благодарности**

Этот проект стал результатом моего интереса к современным методологиям авторизации. Надеюсь, он будет полезен вам и вдохновит на реализацию новых идей! 🙌

---

**Автор:** Pup0chek(https://github.com/Pup0chek)  
**Лицензия:** MIT
