# Pedestal

# English: 
<details>
<summary> <b></b> (<i>click to expand</i>)</summary>

## Stand for things with backlight and rotation

Video on YouTube: https://youtu.be/cd8HgQr4loQ

### Features:
- Different operating modes;<details>
  <summary> <b></b> (<i>click to expand</i>)</summary>

  #### Backlight operation modes:
  - One color;
  <details><summary> <b></b> (<i>click to expand</i>)</summary>
  
  ![один цвет](https://user-images.githubusercontent.com/80697141/227638143-9e3a5081-f24a-4871-b809-0f7fe94cda16.png) 
  </details>
  - Graduation;
  <details><summary> <b></b> (<i>click to expand</i>)</summary>
  
  ![градация](https://user-images.githubusercontent.com/80697141/227640291-9695e472-f2fd-4e54-ad62-7f6b8ba20df6.png)
  </details>
  - Random;
  <details><summary> <b></b> (<i>click to expand</i>)</summary>
  
  ![рандом](https://user-images.githubusercontent.com/80697141/227641280-4c4ee593-9d20-4e6e-aa0d-7509cc02f024.png)
  </details>
  - Manual;
  <details><summary> <b></b> (<i>click to expand</i>)</summary>
  
  ![ручной](https://user-images.githubusercontent.com/80697141/227641600-be39dd3a-42d3-4816-aaf4-b3ddf798cf71.png)
  </details>
  - Train;
  <details><summary> <b></b> (<i>click to expand</i>)</summary>
  
  ![поезд](https://user-images.githubusercontent.com/80697141/227641842-4468060a-e50c-4ac6-98ae-4e1ca0ce065f.png)
  </details>

- Support RGB LEDs;
- Support for table rotation using a stepper motor;
- Remote control via WIFI;

### Component base:
- Controller - ESP 32;
- Ring of address LEDs - WS2812;
- Step-down converter - mini360 [3.3V];
- Boost converter - MT3608 [12V];
- Stepper motor - EM-463;
- Stepper motor driver - DRV8825.

<details>
  <summary> <b>Connecting components</b> (<i>click to expand</i>)</summary>
  
- RGB LEDs:
  Contact name| I/O port
  --- | ---
  DI | 27
  
- DRV8825:
  Contact name| I/O port
  --- | ---
  M0 | 17
  M1 | 5
  M2 | 16
  STEP | 12
  RST | 25
  DIR | 26
  
  <details>
  <summary> <b>Scheme</b> (<i>click to expand</i>)</summary>
  
  soon
  </details>
</details>

### Used libraries:
- Hugo kernel:
  - micropython-nanoweb: https://github.com/hugokernel/micropython-nanoweb

### Notes:
- Development was carried out in Thonny IDE V3.3.13;
- Performance tested on: "MicroPython v 1.19.1 on 2022-06-18; ESP 32 module with ESP 32";
- You can not add a stepper motor to your pedestal, as this will require modification of the model for your engine, as well as create additional costs.

### Creators:
- Author of the idea: Nikita;
- Author of the design and code: Denis.
</details>

</details>

# Русский: 
<details>
<summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>

## Подставка под вещи с подсветкой и вращением.

Ролик на YouTube: https://youtu.be/cd8HgQr4loQ

### Особенности:
- Разные режимы работы;<details>
  <summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>

  #### Режимы работы подсветки:
  - One color - Определённый цвет;
  <details><summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![один цвет](https://user-images.githubusercontent.com/80697141/227638143-9e3a5081-f24a-4871-b809-0f7fe94cda16.png) 
  </details>
  - Graduation - Градация;
  <details><summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![градация](https://user-images.githubusercontent.com/80697141/227640291-9695e472-f2fd-4e54-ad62-7f6b8ba20df6.png)
  </details>
  - Random - Рандомные светодиоды;
  <details><summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![рандом](https://user-images.githubusercontent.com/80697141/227641280-4c4ee593-9d20-4e6e-aa0d-7509cc02f024.png)
  </details>
  - Manual - Ручной;
  <details><summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![ручной](https://user-images.githubusercontent.com/80697141/227641600-be39dd3a-42d3-4816-aaf4-b3ddf798cf71.png)
  </details>
  - Train - Поезд;
  <details><summary> <b></b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  ![поезд](https://user-images.githubusercontent.com/80697141/227641842-4468060a-e50c-4ac6-98ae-4e1ca0ce065f.png)
  </details>
- Поддержка RGB светодиодов;
- Поддержка вращения стола при помощи шагового двигателя;
- Удалённое управление при помощи WIFI;

### Компонентная база:
- Контроллер - ESP32;
- Кольцо адресных светодиодов - WS2812;
- Понижающий преобразователь - mini360 [в 3.3V];
- Повышающий преобразователь - MT3608 [в 12V];
- Шаговый двигатель - EM-463;
- Драйвер для шагового двигателя - DRV8825.
<details>
  <summary> <b>Подключение компонентов</b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
- RGB LEDs:
  Название контакта| I/O порт
  --- | ---
  DI | 27
  
- DRV8825:
  Название контакта| I/O порт
  --- | ---
  M0 | 17
  M1 | 5
  M2 | 16
  STEP | 12
  RST | 25
  DIR | 26
  
  <details>
  <summary> <b>Схема</b> (<i>нажмите, чтобы развернуть</i>)</summary>
  
  soon
  </details>
</details>

### Используемые библиотеки:
- Hugokernel:
  - micropython-nanoweb: https://github.com/hugokernel/micropython-nanoweb

### Примечания:
  - Разработка велась в Thonny IDE V3.3.13;
  - Работоспособность проверена на: "MicroPython v1.19.1 on 2022-06-18; ESP32 module with ESP32";
  - Вы можете не добавлять в свой пьедестал шаговый мотор, поскольку это потребует модификации модели под ваш двигатель, а так же создаст дополнительные расходы.

 ### Создатели:
 - Автор идеи: Никита;
 - Автор дизайна и кода: Денис.
</details>
