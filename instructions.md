Guía del Reto Final – Barcaza de Carga
Curso: Mecánica de Fluidos
1. Descripción del reto
Diseñar, construir y probar una embarcación a escala capaz de transportar carga de manera
eficiente y estable, aplicando principios de mecánica de fluidos e hidrodinámica naval. El
objetivo es optimizar el desempeño hidrodinámico y el consumo energético, cumpliendo las
restricciones dadas.
2. Restricciones del diseño
• Eslora (L): 0,35 – 0,60 m.
• Propulsión: eléctrica (máx. 75 W), baterías selladas; sin combustión.
• Carga útil mínima: 1,5 kg; objetivo ≥ 2,5 kg.
• Calado máximo: 6 cm.
• Materiales: libres (impresión 3D, madera, espuma, laminados), con sellado
obligatorio.
• Control: RC o autónomo.
• Equipos: 3 - 4 estudiantes
3. Banco de pruebas
• Recorrido: canal de 20 m.
• Misiones:
1. Capacidad y estabilidad: añadir carga escalonada (0,5 kg) hasta 2,5 kg;
banda ≤ 10°.
2. Eficiencia: con 1,5 kg, recorrer 20 m ida y vuelta; medir tiempo y energía
eléctrica consumida.
4. Guía de cálculo ITTC
Paso 1 – Número de Reynolds y coeficiente de fricción
𝑅𝑒 = 𝑉𝐿/𝜈, 𝐶𝑓 = 0.075(𝑙𝑜𝑔10𝑅𝑒 − 2)
2
• 𝑉: velocidad del barco (m/s)
• 𝐿: eslora en flotación (m)
• 𝜈: viscosidad cinemática del agua (m²/s)
• 𝐶𝑓: coeficiente de fricción (adimensional) según ITTC-1957
• 𝑅𝑒: número de Reynolds
Paso 2 – Resistencia por fricción
𝑅𝑓 =
1
2
𝜌 𝑉
2 𝑆 𝐶𝑓
• 𝑅𝑓: resistencia por fricción (N)
• 𝜌: densidad del agua (kg/m³)
• 𝑆: área mojada del casco (m²)
• 𝑉: velocidad del barco (m/s)
• 𝐶𝑓: coeficiente de fricción calculado
Paso 3 – Resistencia viscosa total
𝑅𝑉 = (1 + 𝑘)𝑅𝑓
• 𝑅𝑉: resistencia viscosa total (N)
• 𝑘: factor de forma (adimensional, entre 0,1 y 0,3 normalmente)
• 𝑅𝑓: resistencia por fricción (N)
Paso 4 – Resistencia por olas y aire
𝑅𝑇 = 𝑅𝑉 + 𝑅𝑊 + 𝑅𝐴
• 𝑅𝑇: resistencia total (N)
• 𝑅𝑊: resistencia debida a la formación de olas (N)
• 𝑅𝐴: resistencia debida al aire/viento (N)
• 𝐹𝑟 =
𝑉
√𝑔𝐿
: número de Froude, usado para estimar 𝑅𝑊
Paso 5 – Potencia
𝑃𝐸 = 𝑅𝑇 ⋅ 𝑉, 𝑃𝑒𝑗𝑒 =
𝑃𝐸
𝜂𝑇
• 𝑃𝐸: potencia efectiva para vencer la resistencia (W)
• 𝑃𝑒𝑗𝑒: potencia que debe entregar el eje del propulsor (W)
• 𝜂𝑇: eficiencia total del sistema (adimensional), entre 0,4 y 0,6
5. Entregables
1. Informe técnico (8–12 págs.) con cálculos, CAD, justificación ITTC y estabilidad.
2. Planos y lista de materiales.
3. Registro de pruebas (video + datos).
4. Código y/o esquema eléctrico (si aplica).
5. Póster y presentación.
7. Guía del informe técnico
Formato: PDF, Arial/Calibri 11 pt, 8–12 págs., figuras y tablas numeradas.
Secciones sugeridas:
1. Portada
2. Resumen ejecutivo
3. Introducción
4. Metodología de diseño
5. Construcción y materiales
6. Pruebas y resultados
7. Análisis y discusión
8. Conclusiones y recomendaciones
9. Referencias
10. Anexos
Los mejores trabajos, seleccionados por su desempeño técnico, estabilidad y presentación
integral, recibirán una calificación de 5.0 en el reto final. Además, estos mecanismos serán
conservados como muestras didácticas representativas del curso y del programa académico.
8. Rúbrica global del reto (100 pts)
Componente Criterio Descripción Pts
Informe técnico
(40 pts) Claridad y organización Redacción clara, formato uniforme 5
Metodología de diseño Justificación de decisiones, uso correcto
de ITTC/Prohaska, Re, Fr 10
Cálculos y exactitud
técnica Correctos y coherentes con resultados 8
Documentación de
construcción Fotos, materiales y costos 4
Resultados y análisis Tablas, gráficos y análisis técnico 8
Conclusiones y
recomendaciones Claras y aplicables 5
Subtotal informe 40
Prueba práctica
(40 pts) Índice de Transporte (IT)
𝐼𝑇 =
𝑚𝑐𝑎𝑟𝑔𝑎⋅𝐷
𝑡⋅𝐸
, donde:
 𝑚𝑐𝑎𝑟𝑔𝑎 = masa de carga (kg)
𝐷= distancia recorrida (m)
𝑡 = tiempo (s)
𝐸 = energía consumida (Wh)
15
Velocidad y control Trayectoria y arranque en estático 5
Estabilidad Banda ≤ 10° con carga máxima 10
Cumplimiento de
restricciones Calado, carga, seguridad 10
Subtotal práctica 40
Presentación oral
y póster (20 pts) Claridad expositiva Lenguaje técnico y secuencia lógica 6
Apoyo visual Póster A2 claro y completo 5
Argumentación técnica Respaldo con datos 6
Tiempo y manejo de
preguntas
Cumple tiempo, responde con precisión 3
Subtotal
presentación 20
TOTAL 100