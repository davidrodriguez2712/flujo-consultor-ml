# Video del flujo ACOS

`acos-flujo.mp4` (82 s, 1280×720, 24 fps, sin audio, con subtítulos en pantalla) muestra el flujo completo siguiendo **un mismo proyecto** (`demo-fraude`) desde que se describe hasta que se entrega: perfil → `acos init` → workspace y estado central → `status`/`next` → trabajo con el agente → gate (BLOCKED → revisión humana → PASS) → las 7 etapas → entregables finales.

Las salidas de terminal de las escenas 2 a 7 son versiones condensadas de las salidas reales del ejemplo de [`examples/quickstart/`](../../examples/quickstart/). La conversación con el agente (escena 5) es ilustrativa y está marcada así en pantalla. La escena de entregables usa los nombres del piloto sintético `pilots/churn-retencion-sintetico/`.

## Regenerar

El video es una página HTML con un reloj determinista (`render(t)`); se renderiza fotograma a fotograma con Chrome y se codifica con ffmpeg.

```bash
cd docs/video
npm install                      # puppeteer-core
node render.mjs                  # genera acos-flujo.mp4  (requiere Google Chrome y ffmpeg)
node render.mjs --stills 4,22,56 # solo capturas en stills/ para revisar escenas
```

Abre `acos-flujo.html` en el navegador para verlo en bucle; con `?t=22.5` se queda fijo en ese segundo. Los textos, tiempos y subtítulos (`CAPS`) están en el propio HTML. Variable `CHROME` para indicar otra ruta del navegador.
