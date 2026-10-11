<h1 align="center">Андрей Голованов</h1>
<p align="center"><strong>Data Science / Machine Learning · Python</strong></p>

<p align="center">
  <a href="https://t.me/andr3ikaG">Telegram</a> ·
  <a href="mailto:mrmaderator42@gmail.com">Email</a> ·
  <a href="https://www.kaggle.com/mrmoderator">Kaggle</a> ·
  <a href="https://vk.com/agol0vanov">VK</a>
</p>

Развиваюсь в Data Science и машинном обучении. Работаю с табличными и текстовыми данными: исследую данные, готовлю признаки, обучаю модели и разбираю ошибки. Для демонстрации результатов создаю небольшие веб-интерфейсы.

Ниже — проекты с кодом, сохранёнными результатами и описанием ограничений. Рассматриваю возможности работы в Data Science / ML.

## Проекты

### [Reviews — тональность и темы отзывов](https://github.com/golovanov-andrei/Reviews)

**Задача:** определить тональность англоязычных отзывов и исследовать их основные темы.

- Подготовка текстов, TF-IDF с униграммами и биграммами, логистическая регрессия.
- Матрица ошибок, разбор ложных положительных и отрицательных ответов, анализ весов слов.
- Тематическое моделирование: 5 тем LDA и интерактивная визуализация pyLDAvis.

В сохранённом запуске: **accuracy 0.9375, ROC-AUC 0.9823**. Метки получены из рейтингов; условия оценки описаны в README.

**Стек:** Python, pandas, scikit-learn, Matplotlib, Seaborn, pyLDAvis.

### [MoscowPrices — стоимость квартир в Москве](https://github.com/golovanov-andrei/MoscowPrices)

**Задача:** исследовать связь характеристик квартиры с ценой и создать прототип сервиса оценки.

- Исследование данных, фильтрация выбросов, признаки расположения и характеристик квартиры.
- CatBoost с логарифмированием целевой переменной; анализ ошибок и важности признаков.
- Flask API, форма на HTML/CSS/JavaScript и карта станций метро на Folium.

В README указаны недостающие данные и модель, а также ограничение текущей оценки из-за расчёта признака цены станции до разделения выборки.

**Стек:** Python, pandas, CatBoost, Flask, Folium, JavaScript.

### [Credit-risk — демонстрационный скоринг](https://github.com/golovanov-andrei/Credit-risk)

**Задача:** пройти путь от подготовки табличных признаков до классификатора и Streamlit-прототипа.

- Кодирование категорий, обработка пропусков, Pipeline со StandardScaler и Logistic Regression.
- Работа с дисбалансом классов, порогом классификации и метриками precision/recall/F1.
- Сохранение модели через joblib, категории A/B/C и прототип визуализации SHAP.

Целевая метка задана искусственным правилом; проект демонстрирует технический процесс, а не валидированную оценку дефолта.

**Стек:** Python, pandas, scikit-learn, Streamlit, SHAP.

### [Spring_2026 — учебные работы](https://github.com/golovanov-andrei/Spring_2026)

Алгоритмы и блок-схемы, веб-разработка, Git. В репозитории — Python-программа, отчёты и материалы курса.

## Инструменты

| Направление | Технологии |
| --- | --- |
| Данные | Python, pandas, NumPy, SQL |
| Машинное обучение | scikit-learn, CatBoost |
| Обработка текстов | TF-IDF, CountVectorizer, LDA |
| Визуализация | Matplotlib, Seaborn, Folium, pyLDAvis |
| Прототипы | Flask, Streamlit, HTML, CSS, JavaScript |
| Разработка | Git, Jupyter Notebook, Google Colab |

## Развитие портфолио

Следующий этап — воспроизводимый запуск проектов, единая предобработка обучения и инференса, независимая оценка качества и проверка API. Текущий статус каждого проекта описан в его README.

## Связаться со мной

[Telegram](https://t.me/andr3ikaG) · [Email](mailto:mrmaderator42@gmail.com) · [Kaggle](https://www.kaggle.com/mrmoderator)
