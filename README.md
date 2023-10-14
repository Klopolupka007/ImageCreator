<h1 align="center">Image Creator</h1>
<br>
<p align="center">
  <a href="https://github.com/Klopolupka007/Part-Mechanical_Recognition/releases/tag/v1.1.0">
    <img alt="logo" title="Image Creator" src="logo.png" width="300">
  </a>
</p>
<p align="center" href="https://media.tenor.com/jUMex_rdqPwAAAAd/among-us-twerk.gif">Веб-приложение для генерации изображений для загружаемого видео, аватарки пользователя и обложки канала.</p>


## Содержание
- [О проекте](#о-проекте)
- [Руководство пользователя](#technologist-руководство-пользователя)
  - [Установка приложения](#установка)
  - [Использование](#использование)
- [Архитектура системы](#wrench-архитектура-системы)
- [Веб-приложение](#globe_with_meridians-веб-приложение)
  - [Загрузка видео](#загрузка-видео)
  - [Профиль пользователя](#профиль-пользователя)
- [Генерация промпта](#memo-генерация-промпта)
  - [Llama](#llama)
  - [Метрики качества](#метрики-качества)
- [Генерация изображений](#art-генерация-изображений)
  - [Stable Diffussion](#stable-diffusion)
  - [Модификаторы](#модификаторы)
  - [Style Transfer](#style-transfer)
- [Команда](#busts_in_silhouette-команда)
<!-- ABOUT THE PROJECT -->
## О проекте
Проект содержит реализацию веб-приложения и моделей нейронных сетей со следующим функционалом:

**UI/UX:**
- загрузка видео на канал;
- изменение изображение профиля пользователя (аватарки);
- изменение обложки канала;
- автоматическая генерация и ручное изменение промпта для модуля генерации изображений;
- выбор стилей и модификаторов для генерации изображений;
- генерация изображений.

**Модуль генерации промпта**:
- извлечение содержания контента из видео по кадрам (Image captioning);
- генерация промпта по запросу в LLM (Large Language Model).

**Модуль генерации изображений**:
- фильтрация запрещенного контента;
- основная генерация изображений на базе модели Stable Diffusion;
- добавление стилей к изображениям (образам на изображениях) при помощи динамически присоединяемых LoRA моделей;
- перенос стиля одного изображения на другое (Style Transfer);
- генерация изображений на основе позы человека и лица;
- генерация изображений с InPaint модификатором;
- масштабирование изображений (upscale);

## :technologist: Руководство пользователя


<p align="right">(<a href="#image-сreator">Наверх</a>)</p>


## :wrench: Архитектура системы

Ниже перечислены все основные технологии, использованные в проекте:

* [![PyTorch][pytorch]][pytorch-url]
* [![docker][docker]][docker-url]
* [![flask][flask]][flask-url]
* [![python][python]][python-url]

<p align="right">(<a href="#image-сreator">Наверх</a>)</p>

## :globe_with_meridians: Веб-приложение

<p align="right">(<a href="#image-сreator">Наверх</a>)</p>

## :memo: Генерация промпта

<p align="right">(<a href="#image-сreator">Наверх</a>)</p>

## :art: Генерация изображений

<p align="right">(<a href="#image-сreator">Наверх</a>)</p>


<!-- CONTACT -->
## :busts_in_silhouette: Команда
**Project Manager**: Галяутдинов Аскар Тимурович - asckar.ivanov@yandex.ru
* Теймуров Чингизхан Иззетдинович (CV) - https://t.me/ItIsNotLiterallyMe
* Панкрухин Максим Сергеевич (CV/PHP)
* Галяутдинов Аскар Тимурович (NLP) - Project Manager - asckar.ivanov@yandex.ru

<p align="right">(<a href="#image-сreator">Наверх</a>)</p>

[pytorch]: https://img.shields.io/badge/pytorch-0A0A0A?style=for-the-badge&logo=pytorch&logoColor=e44c2c
[pytorch-url]: https://pytorch.org/
[python]: https://img.shields.io/badge/python-F0F0F0.svg?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDMyIDMyIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9IkEiIHgxPSI4MTEuNTI3IiB5MT0iNTc0Ljg5NSIgeDI9IjY2NS4yNTUiIHkyPSI1NzMuNzMyIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMzY2YTk2Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMzY3OWIwIi8+PC9saW5lYXJHcmFkaWVudD48bGluZWFyR3JhZGllbnQgaWQ9IkIiIHgxPSI4NjIuODI0IiB5MT0iNjQyLjE3NiIgeDI9IjU3My4yNzYiIHkyPSI2NDIuMTc2IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjZmZjODM2Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjZmZlODczIi8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PGcgdHJhbnNmb3JtPSJtYXRyaXgoLjE2MTcgMCAwIC4xNTgwODkgLTEwNy41Mzc2NCAtODEuNjYxODcpIj48cGF0aCBkPSJNNzE2LjI1NSA1NDQuNDg3YzAtMTMuNjIzIDMuNjUzLTIxLjAzNCAyMy44MjItMjQuNTYzIDEzLjY5My0yLjQgMzEuMjUtMi43IDQ3LjYyNyAwIDEyLjkzNSAyLjEzNSAyMy44MjIgMTEuNzcgMjMuODIyIDI0LjU2M3Y0NC45NDVjMCAxMy4xODItMTAuNTcgMjMuOTgtMjMuODIyIDIzLjk4aC00Ny42MjdjLTE2LjE2NCAwLTI5Ljc4NyAxMy43ODItMjkuNzg3IDI5LjM2M3YyMS41NjRoLTE2LjM3NmMtMTMuODUyIDAtMjEuOTE3LTkuOTg4LTI1LjMwNS0yMy45NjQtNC41Ny0xOC43NzYtNC4zNzYtMjkuOTYzIDAtNDcuOTQ1IDMuNzk0LTE1LjY4NyAxNS45MTctMjMuOTY0IDI5Ljc3LTIzLjk2NGg2NS41MnYtNmgtNDcuNjQ1di0xNy45OHoiIGZpbGw9InVybCgjQSkiLz48cGF0aCBkPSJNODExLjUyNyA2ODguMzJjMCAxMy42MjMtMTEuODIzIDIwLjUyMy0yMy44MjIgMjMuOTY0LTE4LjA1MiA1LjE4OC0zMi41NCA0LjM5NC00Ny42MjcgMC0xMi42LTMuNjctMjMuODIyLTExLjE3LTIzLjgyMi0yMy45NjR2LTQ0Ljk0NWMwLTEyLjkzNSAxMC43ODItMjMuOTggMjMuODIyLTIzLjk4aDQ3LjYyN2MxNS44NjQgMCAyOS43ODctMTMuNzEgMjkuNzg3LTI5Ljk2M3YtMjAuOTY0aDE3Ljg1OGMxMy44NyAwIDIwLjQgMTAuMzA1IDIzLjgyMiAyMy45NjQgNC43NjQgMTguOTcgNC45NzYgMzMuMTU3IDAgNDcuOTQ1LTQuODE3IDE0LjM2NC05Ljk3IDIzLjk2NC0yMy44MjIgMjMuOTY0SDc2My45djZoNDcuNjI3djE3Ljk4eiIgZmlsbD0idXJsKCNCKSIvPjxwYXRoIGQ9Ik03MjguMTY2IDU0MS41MDVjMC00Ljk3NiAzLjk4OC05IDguOTMtOSA0LjkyMyAwIDguOTMgNC4wMjMgOC45MyA5IDAgNC45Ni00LjAwNiA4Ljk4Mi04LjkzIDguOTgyLTQuOTQgMC04LjkzLTQuMDIzLTguOTMtOC45ODJ6bTUzLjU5IDE0OS43OThjMC00Ljk2IDQuMDA2LTguOTgyIDguOTMtOC45ODIgNC45NCAwIDguOTMgNC4wMjMgOC45MyA4Ljk4MiAwIDQuOTc2LTMuOTg4IDktOC45MyA5LTQuOTIzIDAtOC45My00LjAyMy04LjkzLTl6IiBmaWxsPSIjZmZmIi8+PC9nPjwvc3ZnPg==
[python-url]: https://www.python.org
[docker]: https://img.shields.io/badge/docker-27282C?style=for-the-badge&logo=docker
[docker-url]: https://www.docker.com
