<h1 align="center">Image Creator</h1>
<br>
<a href="https://github.com/Klopolupka007/Part-Mechanical_Recognition/releases/tag/v1.1.0" align="center"></a>
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
- [Генерация изображений](#art-генерация-изображений)
  - [Stable Diffussion](#stable-diffusion)
  - [LoRA](#lora)
  - [ControlNet](#controlnet)
  - [InPaint](#inpaint)
  - [Upscale](#upscale)
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
- извлечение содержания контента из видео по кадрам (***Image captioning***);
- генерация промпта по запросу в LLM (***Large Language Model***).

**Модуль генерации изображений**:
- фильтрация запрещенного контента;
- основная генерация изображений на базе модели ***Stable Diffusion***;
- добавление стилей к изображениям (образам на изображениях) при помощи динамически присоединяемых ***LoRA*** моделей;
- перенос стиля одного изображения на другое (***Style Transfer***);
- генерация изображений на основе позы человека и лица;
- генерация изображений с ***InPaint*** модификатором;
- масштабирование изображений (***upscale***);

<p align="right">(<a href="#image-creator">Наверх</a>)</p>

## :technologist: Руководство пользователя


<p align="right">(<a href="#image-creator">Наверх</a>)</p>


## :wrench: Архитектура системы

Система представляет из себя микросервисную архитектуру, состояющую из трех модулей:

**1. Веб-приложение.**
Модуль предназначен для взаимодействия с пользователем в рамках реализации основного функционала системы.

**2. Брокер сообщений.**
Модуль является связующим звеном между веб-приложением и AI модулем. Необходим для передачи сообщений через API.

**3. AI модуль.**
Основная логика системы и API-компоненты для связи с веб-приложением. Хранит и реализует функционал моделей нейронных сетей.

<div align="center"><img src="https://i.imgur.com/0tHsoAk.png"></div>
<div align="center"><em>Детальный план архитектуры системы</em></div>

Ниже перечислены все основные технологии, использованные в проекте:
* [![python][python]][python-url]
* [![stable-diffusion][stable-diffusion]][stable-diffusion-url]
* [![PyTorch][pytorch]][pytorch-url]
* [![docker][docker]][docker-url]
* [![fastapi][fastapi]][fastapi-url]
* [![GoogleColab][GoogleColab]][GoogleColab-url]
* [![php][php]][php-url]
* [![js][js]][js-url]
<p align="right">(<a href="#image-creator">Наверх</a>)</p>

## :globe_with_meridians: Веб-приложение
### Загрузка видео


### Профиль пользователя

[Stable Diffusion API][Stable-Diffusion-API-url]
[Upscale API][Upscale-API-url]


<p align="right">(<a href="#image-creator">Наверх</a>)</p>

## :memo: Генерация промпта

Генерация промпта составляет одну из основных функциональных частей системы. Она позволяет **автоматически производить написание наиболее подходящего запроса в модель генерации изображения**, отражая при этом суть некоторого текста. 
Сам текст извлекается из описаний, заголовков и **генерируется автоматически на основе контентного описания кадров видеороликов**.

В качестве LLM (Большой языковой модели) была выбрана модель **Llama**, поскольку она имеет ряд преимуществ:
1. Простота разработки и обучения.
2. Высокая скорость и точность обработки запросов.
3. Открытый исходный код.

Поскольку встроенных систем генераций промптов для генераторов изображений на Llama не существует, а обучение модели для этого требует больших трудозатрат несопоставимых с целесообразностью: даже не совсем точные сгенерированные промпты не будут иметь большого влияния на итоговое генерируемое изображение. Таким образом было решено разработать формализованную форму опытным путем для генерации наиболее подходящих промптов.

<p align="right">(<a href="#image-creator">Наверх</a>)</p>

## :art: Генерация изображений

### Stable Diffusion 
Для ядра генерации изображений используется модель нейронной сети [Stable Diffusion][stable-diffusion-url].

**Данный выбор основан на:**
* Высокой производительности модели.
* Точности и красочности генерации изображений, относительно промптов (запросов).
* Большое сообщество разработчиков и технической поддержки.
* Открытый исходный код.
* Большое количество модификаторов, настроек и улучшений для генерации узконаправленных пользовательских запросов.
* Простота развертывания, разработки и работы с моделью.

<div align="center"><img src=""></div>
<div align="center"><em>Пример работы Stable Diffusion (800x800 разрешение)</em></div>

<div align="center"><img src=""></div>
<div align="center"><em>Пример работы Stable Diffusion (2204x864 разрешение)</em></div>

### LoRA
LoRA - это небольшие по размеру файлы, которые можно объединить с моделью Stable Diffusion для введения новых концепций (образов) в модель. В данной системе реализован функционал динамической подгрузки LoRA. Файлы можно получить как на HuggingFace, так и на [Civitai][Civitai-url]


<div align="center"><img src="https://i.imgur.com/3t8v5KO.png"></div>
<div align="center"><em>Пример работы с LoRA</em></div>

<div align="center"><img src="https://i.imgur.com/wOcm02R.png"></div>
<div align="center"><em>Пример работы с LoRA</em></div>

<p align="right">(<a href="#image-creator">Наверх</a>)</p>

### ControlNet
В рамках реализации системы приводится два варианта реализации модификатора ControlNet для Stable Diffusion. ControlNet - это структура нейронной сети для управления моделями диффузии путем добавления дополнительных условий, в данном случае: отслеживание **выражения лица** и **позы человека**.

1. ***Отслеживание позы человека***.
Данная функция генерирует изображение в Stable Diffusion по положению фигуры человека на фотографии. Была использована модель [SDXL-controlnet: OpenPose][OpenPose], которая распознает скелет человека по изображению и накладывает соответствующее условие на диффузионную модель генерации изображений.
<div align="center"><img src="https://i.imgur.com/iHS8jX0.png"></div>
<div align="center"><em>Пример работы с ControlNet pose estimation</em></div>


2. ***Отслеживание выражения лица человека***.
Модель ControlNet с лицевой обработкой позволяет переносить мимику человека по фото на генерируемые изображения. Для данной задачи была использована модель [ControlNetMediaPipeFace][ControlNetMediaPipeFace-url]. 

<div align="center"><img src="https://i.imgur.com/n43f9IM.png"></div>
<div align="center"><em>Пример работы с ControlNet pose estimation</em></div>

### InPaint
InPaint - модификация Stable Diffusion, позволяющая редактировать выделяемые части изображения через маску и текстовый промпт. В качестве модели была выбрана [Stable-Diffusion-Inpainting][Stable-Diffusion-Inpainting-url].

<div align="center"><img src="https://i.imgur.com/gh3nVG4.png"></div>
<div align="center"><em>Пример работы с InPaint</em></div>

### Upscale

Масштабирование изображений является одной из самых необходимых функций, поскольку требуется приводить изображения к строго опредленным размерам. Так как Stable Diffusion стабильно генерирует изображения только низкой размерности (до 700 пикселей на сторону), то существует необходимость расширения изображений до нужных масштабов, что приводит к необратимому значительному ухудшению качества изображений. Для качественного масштабирования была использована модель [Stable Diffusion x4 upscaler][SD-upscale-url], которая генерирует выходное изображение в 4 раза больше исходной. Данная модель обучена на изобажениях 512x512 для 2к, что является абсолютным преимуществом выбора модели для upscale.

<div align="center"><img src="https://i.imgur.com/7UYRlXS.png"></div>
<div align="center"><em>Пример работы с InPaint</em></div>


### Style Transfer
[Style Transfer][ST-url] - это технология для перевода визуального и художественного стиля одного изображения в другое. Для данной технологии была выбрана модель [VGG16][vgg16-url].

Рзаработанный подмодуль находится в [блокноте Google Colab][st-colab-url].

**Примеры использования Style Transfer:**

<div align="center"><img src="https://i.imgur.com/cWOdVCa.png"></div>
<div align="center"><em>Пример работы модели</em></div>

<div align="center"><img src="https://i.imgur.com/a9do1jZ.jpg"></div>
<div align="center"><em>Пример работы модели</em></div>

<div align="center"><img src="https://i.imgur.com/d9bpz2c.png"></div>
<div align="center"><em>Пример работы модели</em></div>

<div align="center"><img src="https://i.imgur.com/TCdDQ5x.png"></div>
<div align="center"><em>Пример работы модели</em></div>

<div align="center"><img src="https://i.imgur.com/wzgKSIi.png"></div>
<div align="center"><em>Пример работы модели</em></div>


## :busts_in_silhouette: Команда
* Теймуров Чингизхан Иззетдинович (CV) - https://t.me/ItIsNotLiterallyMe
* Панкрухин Максим Сергеевич (CV/PHP)
* Галяутдинов Аскар Тимурович (NLP) - Project Manager - asckar.ivanov@yandex.ru

<p align="right">(<a href="#image-creator">Наверх</a>)</p>

[pytorch]: https://img.shields.io/badge/pytorch-0A0A0A?style=for-the-badge&logo=pytorch&logoColor=e44c2c
[pytorch-url]: https://pytorch.org/
[python]: https://img.shields.io/badge/python-F0F0F0.svg?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDMyIDMyIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9IkEiIHgxPSI4MTEuNTI3IiB5MT0iNTc0Ljg5NSIgeDI9IjY2NS4yNTUiIHkyPSI1NzMuNzMyIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMzY2YTk2Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMzY3OWIwIi8+PC9saW5lYXJHcmFkaWVudD48bGluZWFyR3JhZGllbnQgaWQ9IkIiIHgxPSI4NjIuODI0IiB5MT0iNjQyLjE3NiIgeDI9IjU3My4yNzYiIHkyPSI2NDIuMTc2IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjZmZjODM2Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjZmZlODczIi8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PGcgdHJhbnNmb3JtPSJtYXRyaXgoLjE2MTcgMCAwIC4xNTgwODkgLTEwNy41Mzc2NCAtODEuNjYxODcpIj48cGF0aCBkPSJNNzE2LjI1NSA1NDQuNDg3YzAtMTMuNjIzIDMuNjUzLTIxLjAzNCAyMy44MjItMjQuNTYzIDEzLjY5My0yLjQgMzEuMjUtMi43IDQ3LjYyNyAwIDEyLjkzNSAyLjEzNSAyMy44MjIgMTEuNzcgMjMuODIyIDI0LjU2M3Y0NC45NDVjMCAxMy4xODItMTAuNTcgMjMuOTgtMjMuODIyIDIzLjk4aC00Ny42MjdjLTE2LjE2NCAwLTI5Ljc4NyAxMy43ODItMjkuNzg3IDI5LjM2M3YyMS41NjRoLTE2LjM3NmMtMTMuODUyIDAtMjEuOTE3LTkuOTg4LTI1LjMwNS0yMy45NjQtNC41Ny0xOC43NzYtNC4zNzYtMjkuOTYzIDAtNDcuOTQ1IDMuNzk0LTE1LjY4NyAxNS45MTctMjMuOTY0IDI5Ljc3LTIzLjk2NGg2NS41MnYtNmgtNDcuNjQ1di0xNy45OHoiIGZpbGw9InVybCgjQSkiLz48cGF0aCBkPSJNODExLjUyNyA2ODguMzJjMCAxMy42MjMtMTEuODIzIDIwLjUyMy0yMy44MjIgMjMuOTY0LTE4LjA1MiA1LjE4OC0zMi41NCA0LjM5NC00Ny42MjcgMC0xMi42LTMuNjctMjMuODIyLTExLjE3LTIzLjgyMi0yMy45NjR2LTQ0Ljk0NWMwLTEyLjkzNSAxMC43ODItMjMuOTggMjMuODIyLTIzLjk4aDQ3LjYyN2MxNS44NjQgMCAyOS43ODctMTMuNzEgMjkuNzg3LTI5Ljk2M3YtMjAuOTY0aDE3Ljg1OGMxMy44NyAwIDIwLjQgMTAuMzA1IDIzLjgyMiAyMy45NjQgNC43NjQgMTguOTcgNC45NzYgMzMuMTU3IDAgNDcuOTQ1LTQuODE3IDE0LjM2NC05Ljk3IDIzLjk2NC0yMy44MjIgMjMuOTY0SDc2My45djZoNDcuNjI3djE3Ljk4eiIgZmlsbD0idXJsKCNCKSIvPjxwYXRoIGQ9Ik03MjguMTY2IDU0MS41MDVjMC00Ljk3NiAzLjk4OC05IDguOTMtOSA0LjkyMyAwIDguOTMgNC4wMjMgOC45MyA5IDAgNC45Ni00LjAwNiA4Ljk4Mi04LjkzIDguOTgyLTQuOTQgMC04LjkzLTQuMDIzLTguOTMtOC45ODJ6bTUzLjU5IDE0OS43OThjMC00Ljk2IDQuMDA2LTguOTgyIDguOTMtOC45ODIgNC45NCAwIDguOTMgNC4wMjMgOC45MyA4Ljk4MiAwIDQuOTc2LTMuOTg4IDktOC45MyA5LTQuOTIzIDAtOC45My00LjAyMy04LjkzLTl6IiBmaWxsPSIjZmZmIi8+PC9nPjwvc3ZnPg==
[python-url]: https://www.python.org
[docker]: https://img.shields.io/badge/docker-27282C?style=for-the-badge&logo=docker
[docker-url]: https://www.docker.com
[fastapi]: https://img.shields.io/badge/fastapi-27282C?style=for-the-badge&logo=fastapi
[fastapi-url]: https://fastapi.tiangolo.com/
[stable-diffusion-url]: https://stablediffusionweb.com
[stable-diffusion]: https://img.shields.io/badge/stablediffusion-F0F0F0.svg?style=for-the-badge&logo=data:image/png%2bxml;base64,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
[php]: https://img.shields.io/badge/php-27282C?style=for-the-badge&logo=php
[php-url]: https://www.php.net/
[js]: https://img.shields.io/badge/javascript-27282C?style=for-the-badge&logo=javascript
[js-url]: https://www.ecma-international.org/
[GoogleColab]: https://img.shields.io/badge/GoogleColab-27282C?style=for-the-badge&logo=GoogleColab
[GoogleColab-url]: https://colab.research.google.com/
[onnx]: https://img.shields.io/badge/onnx-27282C?style=for-the-badge&logo=onnx
[onnx-url]: https://onnx.ai/
[rabbitmq]: https://img.shields.io/badge/rabbitmq-27282C?style=for-the-badge&logo=rabbitmq
[rabbitmq-url]: https://www.rabbitmq.com/
[ST-url]: https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf
[vgg16-url]: https://pytorch.org/vision/stable/models/generated/torchvision.models.vgg16.html?highlight=vgg
[st-colab-url]: https://colab.research.google.com/drive/1uX6oZP6bERV0ts-wsp6ivmV59iQVi_ji?usp=sharing
[SD-upscale-url]: https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler
[OpenPose]: https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0
[ControlNetMediaPipeFace-url]: https://huggingface.co/CrucibleAI/ControlNetMediaPipeFace
[Stable-Diffusion-Inpainting-url]: https://huggingface.co/runwayml/stable-diffusion-inpainting
[Civitai-url]: https://civitai.com/tag/lora
[Upscale-API-url]: https://colab.research.google.com/drive/1sQ9dIUskv_S-GnpHACibeXoAgb7WHDOq?usp=sharing
[Stable-Diffusion-API-url]: https://colab.research.google.com/drive/1Z-OzonGFlQHL69sAB6mD_PAjzu_IWXtT?usp=sharing
