# Document Analyzer - Frontend

Interfaz web moderna para el análisis inteligente de documentos con IA.

## 🚀 Stack Tecnológico

- **Next.js 14** - App Router con SSR/SSG
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **React Hooks** - State management

## 📦 Componentes

### `FileUpload`
- Drag & drop de archivos
- Validación de extensiones (.pdf, .docx, .txt, .md)
- Límite de tamaño (10MB)
- 5 tipos de análisis: general, summary, key_points, sentiment, comprehensive

### `AnalysisResults`
- Visualización de resultados con estadísticas
- Secciones para resumen, puntos clave, sentimiento
- Display de entidades y preguntas (cuando aplican)
- Tarjetas de métricas: palabras, caracteres, oraciones, párrafos, etc.

### `AnalysisHistory`
- Listado de análisis guardados desde Supabase
- Filtro por usuario
- Formato de fechas en español
- Badges con colores por tipo de análisis
- Botón de refresh manual

### `SystemStatus`
- Monitoreo en tiempo real del sistema
- Auto-refresh cada 30 segundos
- Estado de Backend, Ollama, Supabase
- Indicadores visuales (verde=ok, amarillo=warning, rojo=error)

## 🛠️ Instalación

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.local.example .env.local
# Editar .env.local y configurar NEXT_PUBLIC_API_URL

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
npm start
```

## 🔧 Configuración

### Variables de Entorno

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### API Backend

El frontend espera que el backend esté corriendo en `http://localhost:8000` con los siguientes endpoints:

- `POST /documents/analyze` - Analizar documento
- `GET /documents/user/{user_id}/analyses` - Obtener historial
- `GET /system/health` - Estado del sistema
- `GET /system/info` - Información del sistema

## 📂 Estructura

```
frontend/
├── app/
│   ├── layout.tsx          # Layout global con metadata
│   ├── page.tsx            # Página principal con composición de componentes
│   └── globals.css         # Estilos globales de Tailwind
├── components/
│   ├── FileUpload.tsx      # Componente de carga de archivos
│   ├── AnalysisResults.tsx # Visualización de resultados
│   ├── AnalysisHistory.tsx # Historial de análisis
│   └── SystemStatus.tsx    # Estado del sistema
├── lib/
│   └── api.ts              # Cliente de API con tipos TypeScript
├── public/                 # Archivos estáticos
├── .env.local              # Variables de entorno (no subir a git)
└── package.json
```

## 🎨 Diseño

- **Responsive**: Grid adaptable (1 columna en móvil, 2 en desktop)
- **Gradientes**: Fondo con degradado azul-morado sutil
- **Sombras**: Cards con elevación visual
- **Animaciones**: Hover effects y transiciones suaves
- **Color-coding**: Secciones con colores distintivos (azul=resumen, verde=puntos, morado=sentimiento)

## 🔄 Estado Global

La página principal (`page.tsx`) maneja:
- `currentResult`: Resultado del análisis actual
- `userId`: ID del usuario para filtrar historial
- `refreshTrigger`: Contador para refrescar historial

## 🧪 Testing

```bash
# Verificar compilación de TypeScript
npm run build

# Linting
npm run lint
```

## 📝 Uso

1. **Iniciar backend**: Asegúrate de que el backend esté corriendo
2. **Cargar archivo**: Arrastra un documento o haz clic para seleccionar
3. **Elegir tipo de análisis**: General, Resumen, Puntos clave, etc.
4. **Analizar**: Haz clic en "Analizar Documento"
5. **Ver resultados**: Los resultados aparecen con estadísticas y secciones
6. **Revisar historial**: Todos los análisis guardados aparecen en el panel derecho

## 🚀 Despliegue

### Vercel (recomendado)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔗 Integración con Backend

El frontend consume la API REST del backend. Asegúrate de:

1. **CORS configurado**: Backend debe permitir `http://localhost:3000`
2. **Backend corriendo**: `cd backend && uvicorn main:app --reload`
3. **Ollama activo**: `ollama serve` con modelo `llama3.2:1b`
4. **Supabase conectado**: Variables de entorno configuradas

## 🐛 Troubleshooting

### Error de conexión con API
- Verifica que `NEXT_PUBLIC_API_URL` esté correcto
- Confirma que el backend esté corriendo
- Revisa la consola del navegador para errores de CORS

### Componente no actualiza
- Verifica que estés usando `'use client'` en el componente
- Asegúrate de pasar `refreshTrigger` correctamente
- Revisa el estado en React DevTools

### Error de tipo TypeScript
- Ejecuta `npm run build` para ver errores de compilación
- Verifica que las interfaces en `lib/api.ts` coincidan con el backend
- Usa `console.log` para inspeccionar la estructura de datos

## 📚 Recursos

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Hooks](https://react.dev/reference/react)

## 🎯 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Búsqueda en historial
- [ ] Exportar resultados a PDF
- [ ] Comparación de análisis
- [ ] Modo oscuro
- [ ] Gráficos interactivos
- [ ] Paginación en historial
- [ ] Filtros avanzados
- [ ] Compartir análisis públicamente

