<a name="readme-top"></a>
![Maintained][Maintained-shield]
![Forks][Forks-shield]
![Pull Request][PullRequest-shield]
![Pull Request Closed][PullRequestclosed-shield]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/NicoZela23/CV-Robotic-Claw">
    <img src="repo_assets/Title.jpg" alt="Logo" width="185" height="218">
  </a>

<h3 align="center">Omni Robot</h3>

  <p align="center">
    Motoron powered Robotic
    <br />
    <a href="https://github.com/NicoZela23/Omni-Motoron-Robot/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/NicoZela23/Omni-Motoron-Robot/issues">Report Bug</a>
    ·
    <a href="https://github.com/NicoZela23/Omni-Motoron-Robot/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Tabla de contenido</summary>
  <ol>
    <li>
      <a href="#acerca-del-proyeto">Acerca Del Proyeto</a>
    </li>
    <li><a href="#hardware-necesario">Hardware Necesario</a></li>
    <li><a href="#configuracion-de-entorno">Configuracion de entorno</a></li>
    <li>
      <a href="#descarga">Descarga</a>
    </li>
    <li><a href="#instalacion">Instalacion</a></li>
    <li><a href="#configuracion-del-robot">Configuracion del robot</li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#uso">Uso</a></li>
  </ol>
</details>

## Acerca Del Proyeto

`Omni Robot` es un proyecto Open Source hecho para probar los conceptos de robotica especializada relacionado con controladores avanzados, motores driver y control asincrono basado en `SSH`

- El raspberry pi 4 se encarga del control y orquestracion de movimientos del robot a travez de un script de Python
- Se ejecuta la secuancia de configuracion de los motores los cuales podran acceder a las difentes acciones de movimiento (1-5)

## Hardware Necesario

> [!IMPORTANT]
> Este proyecto requiere de `Hardware` especifico tanto para ser construido como para ser usado, ademas de una estructura para sostener los motores.

- Raspberry Pi 4 Model B
- Pololu M3H550 Triple Motor Driver
- 3 x JGB37-520 motor dc
- 3 x JGB37-520
- Fuente de alimentación 
- Protoboard
- Cables jumper y terminales

Considerando la correcta implementacion, se debe consultar al manual y descripcion en [Omni Robot Docs](https://drive.google.com/file/d/1AXFSMzN8EUFieELDR_ty4NCXF2URdGLX/view?usp=sharing)

**Siendo este una construccion especifica esperando un resultado final como este:**

<img src="repo_assets/construccion_final.jpeg" alt="video-demo" width="600" height="450"/>


## Configuracion de entorno previa

Considerando que el proyecto hace uso de la libreria `motoron` es importante instalar la misma, considerando que no esta disponible directamente desde `pip` esta debe ser integrada de la siguiente manera desde el raspberry pi

```
$ mkdir project_library
$ cd project_library
$ git pull https://github.com/pololu/motoron-python.git
```

Con esto tendremos disponible toda la libreria junto con ejemplos de uso para los casos de us `motoron`

## Descarga

> [!IMPORTANT]
> Ya que esta libreria es especifica del fabricante `Pololu` para poder hacer uso de la libreria `motoron` debemos clonar este proyecto y extraer el script `robot.py` dentro de los archivos de la carpeta `motoron-python` donde se encuentran disponibles los archivos core

```
$ cd project_library
$ cd motoron-python
$ git clone https://github.com/NicoZela23/Omni-Motoron-Robot.git
$ mv Omni-Motoron-Robot/* .
```

## Instalacion

El proyecto no requiere de una instalacion mas alla de la ejecucion del script de Python `robot.py`

```
$ sudo python robot.py
```

## Configuracion del robot

La configuracion mas crucial del proyecto recaera en el uso del mismo siendo las opciones base del menu, todo ejecutado desde la shell con comandos simples ingresados por consola

<img src="repo_assets/Controls.png" alt="video-demo" width="415" height="163"/>

## Tech Stack

[![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)]()
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![Debian](https://img.shields.io/badge/Debian-A81D33?logo=debian&logoColor=fff)]()

## Uso

La ejecucion del proyecto se hara mediante el script mismo que accionara movimientos de calibracion en los motores para despues abrir la terminal para poder realizar las acciones pre configuradas

[Maintained-shield]: https://img.shields.io/badge/Maintained%3F-yes-green.svg
[Forks-shield]: https://img.shields.io/github/forks/NicoZela23/Omni-Motoron-Robot.svg
[PullRequest-shield]: https://img.shields.io/github/issues-pr/NicoZela23/Omni-Motoron-Robot.svg
[PullRequestclosed-shield]: https://img.shields.io/github/issues-pr-closed/NicoZela23/Omni-Motoron-Robot.svg
