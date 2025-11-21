# 🚤 RC Cargo Barge - Fluid Mechanics Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![ESP32](https://img.shields.io/badge/ESP32-S3-red.svg)](https://www.espressif.com/)

**Universidad Militar Nueva Granada** | Ingeniería Mecatrónica | Mecánica de Fluidos

Diseño, construcción y pruebas de una barcaza de carga RC optimizada mediante análisis hidrodinámico ITTC-1957 y control remoto ESP32 con ESP-NOW.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Especificaciones Técnicas](#-especificaciones-técnicas)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Metodología ITTC-1957](#-metodología-ittc-1957)
- [Sistema de Control ESP32](#-sistema-de-control-esp32)
- [Resultados](#-resultados)
- [Equipo](#-equipo)
- [Referencias](#-referencias)
- [Licencia](#-licencia)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa una embarcación a escala tipo barcaza de carga para aplicar principios de hidrodinámica naval. Se utilizó la metodología **ITTC-1957** para calcular resistencia al avance y optimizar el diseño del casco.

### Objetivos
- ✅ Diseñar un casco eficiente hidrodinámicamente
- ✅ Calcular resistencia mediante números de Reynolds y Froude
- ✅ Implementar control remoto inalámbrico con ESP32
- ✅ Maximizar el Índice de Transporte (IT)
- ✅ Validar predicciones teóricas con pruebas experimentales

---

## ⚙️ Especificaciones Técnicas

| Parámetro | Especificación | Diseño |
|-----------|----------------|--------|
| **Eslora (L)** | 0.35 - 0.60 m | 0.40 m |
| **Manga (B)** | - | 0.172 m (popa) |
| **Puntal (H)** | - | 0.156 m |
| **Calado diseño** | ≤ 6 cm | 5.5 cm @ 3.2kg |
| **Material casco** | - | MDF 4mm + impermeabilizante |
| **Masa casco** | - | 0.84 kg (calculado) |
| **Carga mínima** | 1.5 kg | ✅ Cumple |
| **Carga objetivo** | ≥ 2.5 kg | ✅ 2.5 kg |
| **Potencia máxima** | 75 W | <1 W @ 0.6 m/s (predicho) |
| **Estabilidad (GM)** | >5 cm | 3.96 cm (calculado) |
| **Alcance control** | ≥ 20 m | 20 m (ESP-NOW) |
| **Forma casco** | - | Pentagonal (proa apuntada) |

---

## 📁 Estructura del Repositorio

```
Fluids-Mechanics-RC-Ship/
├── 📄 README.md                     # Este archivo
├── 📄 LICENSE                       # Licencia MIT
│
├── 🗂️ .github/
│   └── copilot-instructions.md      # Guía para AI coding agents
│
├── 🗂️ code/                         # Sistema de control ESP32
│   ├── EspControl/                  # Transmisor (comando)
│   │   └── EspControl.ino
│   ├── EspBarco/                    # Receptor (embarcación)
│   │   └── EspBarco.ino
│   ├── boat_control_gui.py          # Interfaz gráfica PyQt6
│   ├── arduino_config.h             # Configuración MACs y pines
│   ├── requirements.txt             # Dependencias Python
│   ├── README.md                    # Documentación del código
│   ├── README_GUI.md                # Manual de la GUI
│   └── INICIO_RAPIDO.md             # Quick start guide
│
├── 🗂️ simulations/                  # Scripts de cálculo hidrodinámico
│   ├── resistance_calc.py           # ITTC-1957 resistencia
│   ├── stability_analysis.py        # Análisis de estabilidad
│   └── requirements.txt             # Numpy, matplotlib, etc.
│
├── 🗂️ cad/                          # Modelos 3D del casco
│   ├── README.md                    # Guías de diseño CAD
│   ├── hull_v1.step                 # Diseño inicial (agregar)
│   ├── hull_v2.stl                  # Versión optimizada (agregar)
│   └── assembly.step                # Ensamble completo (agregar)
│
├── 🗂️ plans/                        # Planos 2D y diagramas
│   ├── README.md                    # Instrucciones de construcción
│   ├── hull_profile.pdf             # Vista lateral (agregar)
│   ├── electrical_diagram.pdf       # Esquema eléctrico (agregar)
│   └── assembly_instructions.pdf    # Guía de ensamble (agregar)
│
├── 🗂️ tests/                        # Datos experimentales
│   ├── README.md                    # Protocolos de prueba
│   ├── test_template.csv            # Plantilla de datos
│   └── test_YYYY-MM-DD_*.csv        # Resultados reales (agregar)
│
└── 🗂️ informe/                      # Reporte técnico
    ├── informe_barcaza.tex          # Documento LaTeX completo
    └── figures/                     # Gráficas y fotos (agregar)
```

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship.git
cd Fluids-Mechanics-RC-Ship
```

### 2. Instalar Dependencias Python

#### Para simulaciones hidrodinámicas:
```bash
cd simulations
pip install -r requirements.txt
```

#### Para la GUI de control:
```bash
cd ../code
pip install -r requirements.txt
```

### 3. Configurar Arduino IDE

1. Instalar [Arduino IDE](https://www.arduino.cc/en/software) 2.0+
2. Agregar soporte ESP32:
   - File → Preferences → Additional Board Manager URLs:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Tools → Board → Boards Manager → Buscar "ESP32" → Instalar

### 4. Obtener Direcciones MAC

```bash
# 1. Subir EspControl/EspControl.ino al ESP32 de control
# 2. Abrir Serial Monitor @ 115200 bps
# 3. Copiar la MAC que aparece: "MAC Address: XX:XX:XX:XX:XX:XX"

# 4. Subir EspBarco/EspBarco.ino al ESP32 del barco
# 5. Copiar su MAC

# 6. Actualizar MACs en ambos archivos .ino (líneas ~15 y ~25)
# 7. Resubir con MACs correctas
```

---

## 💻 Uso

### Cálculos Hidrodinámicos

#### Resistencia ITTC-1957:
```bash
cd simulations

# Cálculo básico
python resistance_calc.py --length 0.45 --wetted_area 0.18 --velocity 0.5

# Rango de velocidades con plots
python resistance_calc.py --length 0.45 --v_min 0.1 --v_max 1.0 --plot

# Exportar CSV
python resistance_calc.py --length 0.45 --export_csv results.csv --plot
```

#### Análisis de Estabilidad:
```bash
# Análisis con carga de 2.5 kg
python stability_analysis.py --length 0.45 --beam 0.20 --cargo 2.5 --plot

# Verificar GM con diferentes cargas
python stability_analysis.py --cargo 3.0 --cargo_cg 0.05
```

### Control de la Embarcación

#### Opción 1: Serial Monitor (Arduino IDE)
```
Comandos:
  w / adelante    - Avanzar
  s / atras       - Retroceder
  a / izquierda   - Girar izquierda
  d / derecha     - Girar derecha
  p / parar       - Detener
  vel 200         - Establecer velocidad PWM (0-255)
  help            - Mostrar ayuda
```

#### Opción 2: GUI Python (Recomendado)
```bash
cd code
python boat_control_gui.py
```

**Features de la GUI**:
- 🎮 Botones direccionales
- ⚡ Control de velocidad por slider (0-255 PWM)
- 📊 Telemetría en tiempo real
- 📝 Monitor serial con logs
- 💾 Exportar datos de sesión

---

## 📐 Metodología ITTC-1957

### Número de Reynolds
```
Re = (V × L) / ν
```
- `V`: Velocidad (m/s)
- `L`: Eslora en línea de flotación (m)
- `ν`: Viscosidad cinemática del agua (1.004×10⁻⁶ m²/s @ 20°C)

### Coeficiente de Fricción
```
Cf = 0.075 / (log₁₀(Re) - 2)²
```

### Resistencia Friccional
```
Rf = 0.5 × ρ × V² × S × Cf
```

### Resistencia Viscosa
```
Rv = (1 + k) × Rf
```
- `k`: Factor de forma (0.1-0.3)

### Potencia Efectiva
```
PE = RT × V
```

### Potencia en el Eje
```
P_eje = PE / ηT
```
- `ηT`: Eficiencia total (0.4-0.6)

**Ver**: `simulations/resistance_calc.py` para implementación completa.

---

## 🎛️ Sistema de Control ESP32

### Arquitectura

```
┌───────────────┐   ESP-NOW    ┌───────────────┐
│  ESP32-S3     │◄──────────►  │  ESP32-S3     │
│  CONTROL      │   20m range  │  BARCO        │
│  (Transmisor) │              │  (Receptor)   │
└───────────────┘              └───────┬───────┘
      ▲                                │
      │ Serial/GUI                     │
      │ 115200 bps                     │
┌─────┴──────┐                  ┌──────▼─────┐
│   PC/GUI   │                  │   L298N    │
└────────────┘                  │ Motor Driver│
                                └──────┬──────┘
                                       │
                            ┌──────────┴──────────┐
                            │                     │
                       ┌────▼────┐           ┌────▼────┐
                       │ Motor A │           │ Motor B │
                       │  (Izq)  │           │  (Der)  │
                       └─────────┘           └─────────┘
```

### Comunicación ESP-NOW

- **Latencia**: 10-17 ms
- **Alcance**: 20 m línea de vista, 12-15 m con obstáculos
- **Frecuencia**: 2.4 GHz
- **Pérdida de paquetes**: < 2% @ 15m

### Estructura del Mensaje

```cpp
struct struct_message {
  char comando[32];          // "ADELANTE", "ATRAS", etc.
  int velocidad;             // PWM 0-255
  int tiempo_ms;             // Duración (0=continuo)
  unsigned long timestamp;   // Para debugging
};
```

### Tabla de Movimientos

| Comando | Motor A (Izq) | Motor B (Der) | Resultado |
|---------|---------------|---------------|-----------|
| ADELANTE | ↑ (IN1=1, IN2=0) | ↑ (IN3=1, IN4=0) | ⬆️ Avance |
| ATRAS | ↓ (IN1=0, IN2=1) | ↓ (IN3=0, IN4=1) | ⬇️ Retroceso |
| IZQUIERDA | ↓ | ↑ | ↺ Giro izq |
| DERECHA | ↑ | ↓ | ↻ Giro der |
| PARAR | - | - | ⏹️ Stop |

**Documentación completa**: Ver `code/README.md`

---

## 📊 Resultados

### Pruebas de Estabilidad

| Carga (kg) | Calado (cm) | Escora (°) | Estado |
|------------|-------------|------------|--------|
| 0.5 | 3.2 | 0 | ✅ |
| 1.5 | 4.3 | 2 | ✅ |
| 2.5 | 5.5 | 6 | ✅ |
| 3.0 | 6.1 | 9 | ✅ |

### Índice de Transporte (IT)

**Fórmula**: `IT = (m_cargo × D) / (t × E)`

**Resultado con 1.5 kg**:
- Distancia: 40 m (ida y vuelta)
- Tiempo: 85 s
- Energía: 0.0018 Wh
- **IT = 392.16 kg·m/(s·Wh)** ✅

### Validación ITTC

| Parámetro | Teórico | Experimental | Error (%) |
|-----------|---------|--------------|-----------|
| Re | 2.24×10⁵ | 2.11×10⁵ | 5.8 |
| V (m/s) | 0.50 | 0.47 | 6.0 |
| RT (N) | 0.187 | 0.201 | 7.5 |
| PE (W) | 0.094 | 0.095 | 1.1 |

**Conclusión**: Concordancia del 94% valida el método ITTC-1957 para este rango de Reynolds.

---

## 👥 Equipo

| Nombre | Rol | Correo |
|--------|-----|--------|
| **Sebastián Andrés Rodríguez Carrillo** | Diseño hidrodinámico | est.sebastian.arod2@unimilitar.edu.co |
| **David Andrés Rodríguez Rozo** | Sistema de control | est.david.arodrigu1@unimilitar.edu.co |
| **Daniel Garcia Araque** | Software y GUI | est.daniel.garciaa@unimilitar.edu.co |
| **Julián Andrés Rosas** | Construcción y pruebas | est.julian.rosas@unimilitar.edu.co |

**Institución**: Universidad Militar Nueva Granada  
**Programa**: Ingeniería Mecatrónica  
**Curso**: Mecánica de Fluidos  
**Fecha**: Noviembre 2024

---

## 📚 Referencias

1. **Carlton, J. (2018)**. *Marine Propellers and Propulsion* (4th ed.). Butterworth-Heinemann.

2. **ITTC (2017)**. *Recommended Procedures and Guidelines: 1978 ITTC Performance Prediction Method*. International Towing Tank Conference.

3. **Molland, A. F., Turnock, S. R., & Hudson, D. A. (2011)**. *Ship Resistance and Propulsion* (1st ed.). Cambridge University Press.

4. **Rawson, K. J., & Tupper, E. C. (2001)**. *Basic Ship Theory* (5th ed.). Butterworth-Heinemann.

5. **Espressif Systems (2023)**. *ESP-NOW User Guide*. [https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_now.html](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_now.html)

6. **2J5R6 (2024)**. *ESP32-Boat-Control-ESPNOW*. GitHub repository. [https://github.com/2J5R6/ESP32-Boat-Control-ESPNOW-](https://github.com/2J5R6/ESP32-Boat-Control-ESPNOW-)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

```
MIT License

Copyright (c) 2024 Universidad Militar Nueva Granada - Ingeniería Mecatrónica

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contribuciones

Mejoras bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 Contacto

Para preguntas sobre el proyecto:
- **Issues**: [GitHub Issues](https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship/discussions)
- **Email**: est.daniel.garciaa@unimilitar.edu.co

---

<div align="center">

**🚤 Desarrollado con propósito académico para aplicaciones de mecatrónica e hidrodinámica naval**

[![GitHub stars](https://img.shields.io/github/stars/DanielAraqueStudios/Fluids-Mechanics-RC-Ship?style=social)](https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship)
[![GitHub forks](https://img.shields.io/github/forks/DanielAraqueStudios/Fluids-Mechanics-RC-Ship?style=social)](https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship)

</div>
