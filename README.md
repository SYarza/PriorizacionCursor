echo "# Sistema de Priorización de Transporte

Este proyecto implementa un sistema de optimización para la distribución de carga en diferentes tipos de transporte, considerando restricciones específicas de peso y capacidad.

## Descripción

El sistema genera planes de distribución de carga optimizados para dos tipos de transporte:
- **Trailer 40**: Capacidad entre 29 y 36 toneladas
- **Doble Remolque**: Capacidad entre 50 y 56 toneladas

### Características principales

- Procesamiento de órdenes desde archivo JSON
- Generación de tres tipos de planes:
  1. Solo usando trailers 40
  2. Solo usando dobles remolques
  3. Plan mixto optimizado
- Respeto de restricciones de peso por tipo de transporte
- Priorización de carga completa por producto

## Requisitos

- Python 3.9 o superior
- Docker (opcional)

## Instalación

1. Clonar el repositorio:
\`\`\`bash
git clone https://github.com/SYarza/PriorizacionCursor.git
cd PriorizacionCursor
\`\`\`

### Ejecución directa con Python

\`\`\`bash
python solucion_distribucion.py
\`\`\`

### Ejecución con Docker

1. Construir la imagen:
\`\`\`bash
docker build -t distribucion-app .
\`\`\`

2. Ejecutar el contenedor:
\`\`\`bash
docker run distribucion-app
\`\`\`

## Estructura del proyecto

\`\`\`
├── solucion_distribucion.py   # Código principal
├── dataO2D.json              # Archivo de datos de entrada
├── requirements.txt          # Dependencias del proyecto
├── Dockerfile               # Configuración de Docker
└── README.md               # Este archivo
\`\`\`

## Reglas de negocio

1. Los camiones deben respetar los límites de peso:
   - Trailer 40: 29-36 toneladas
   - Doble remolque: 50-56 toneladas

2. Las cargas deben ser múltiplos del peso teórico de cada producto

3. Se prioriza la carga de productos completos en cada transporte

4. Los productos se ordenan por tonelaje de mayor a menor

## Contribución

Si deseas contribuir al proyecto:

1. Haz un Fork del repositorio
2. Crea una rama para tu característica (\`git checkout -b feature/AmazingFeature\`)
3. Haz commit de tus cambios (\`git commit -m 'Add some AmazingFeature'\`)
4. Push a la rama (\`git push origin feature/AmazingFeature\`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles." > README.md
