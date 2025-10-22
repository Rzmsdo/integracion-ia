"""
Servicio para integración con Ollama.
Gestiona toda la comunicación con el modelo de IA local.
"""

from typing import Dict, Optional
import httpx
from ollama import generate, GenerateResponse
from app.core.config import get_settings

settings = get_settings()


class OllamaService:
    """
    Servicio centralizado para interactuar con Ollama.
    Proporciona métodos para diferentes tipos de análisis de documentos.
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 300  # 5 minutos para análisis complejos
    
    async def generate_response(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Genera una respuesta usando Ollama (método HTTP).
        
        Args:
            prompt: El prompt a enviar al modelo
            model: Modelo específico a usar (opcional, usa el default si no se especifica)
        
        Returns:
            Respuesta del modelo como string
        """
        target_model = model or self.model
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": target_model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    return response.json()["response"]
                else:
                    raise Exception(f"Ollama error: {response.status_code} - {response.text}")
        
        except httpx.TimeoutException:
            raise Exception(f"Timeout al comunicarse con Ollama después de {self.timeout}s")
        except Exception as e:
            raise Exception(f"Error en Ollama: {str(e)}")
    
    def generate_sync(self, prompt: str) -> str:
        """
        Genera una respuesta usando el cliente sync de Ollama (SDK).
        Útil para scripts o casos donde no necesitas async.
        
        Args:
            prompt: El prompt a enviar al modelo
        
        Returns:
            Respuesta del modelo como string
        """
        try:
            response: GenerateResponse = generate(self.model, prompt)
            return response.response
        except Exception as e:
            raise Exception(f"Error en Ollama sync: {str(e)}")
    
    async def analyze_document(self, text: str, analysis_type: str = "general") -> str:
        """
        Analiza un documento según el tipo especificado.
        
        Args:
            text: Texto del documento a analizar
            analysis_type: Tipo de análisis (general, summary, key_points, sentiment)
        
        Returns:
            Resultado del análisis como string
        """
        prompts = {
            "general": self._get_general_prompt(text),
            "summary": self._get_summary_prompt(text),
            "key_points": self._get_key_points_prompt(text),
            "sentiment": self._get_sentiment_prompt(text),
            "entities": self._get_entities_prompt(text),
            "questions": self._get_questions_prompt(text),
        }
        
        prompt = prompts.get(analysis_type, prompts["general"])
        return await self.generate_response(prompt)
    
    async def analyze_comprehensive(self, text: str) -> Dict[str, any]:
        """
        Realiza un análisis completo del documento.
        Incluye: resumen, puntos clave, sentimiento y metadatos.
        
        Args:
            text: Texto del documento a analizar
        
        Returns:
            Diccionario con todos los resultados del análisis
        """
        # Ejecutar análisis en paralelo (si quieres optimizar, usa asyncio.gather)
        summary = await self.analyze_document(text, "summary")
        key_points = await self.analyze_document(text, "key_points")
        sentiment = await self.analyze_document(text, "sentiment")
        
        return {
            "type": "comprehensive",
            "summary": summary,
            "key_points": key_points,
            "sentiment": sentiment,
            "metadata": {
                "text_length": len(text),
                "word_count": len(text.split()),
                "char_count": len(text),
                "model_used": self.model
            }
        }
    
    # ==================== Prompts Personalizados ====================
    
    def _get_general_prompt(self, text: str) -> str:
        """Prompt para análisis general"""
        return f"""Analiza el siguiente documento de manera general y proporciona:
1. Un resumen breve
2. Los temas principales
3. El tono y estilo del texto

Documento:
{text}

Por favor, proporciona tu análisis de forma estructurada."""
    
    def _get_summary_prompt(self, text: str) -> str:
        """Prompt para resumen"""
        return f"""Resume el siguiente documento de forma concisa y clara, capturando los puntos más importantes:

Documento:
{text}

Resumen:"""
    
    def _get_key_points_prompt(self, text: str) -> str:
        """Prompt para extracción de puntos clave"""
        return f"""Extrae y lista los puntos clave más importantes del siguiente documento. 
Presenta cada punto de forma clara y concisa:

Documento:
{text}

Puntos clave:"""
    
    def _get_sentiment_prompt(self, text: str) -> str:
        """Prompt para análisis de sentimiento"""
        return f"""Analiza el sentimiento y tono del siguiente texto. 
Indica si es positivo, negativo, neutral o mixto, y explica por qué:

Texto:
{text}

Análisis de sentimiento:"""
    
    def _get_entities_prompt(self, text: str) -> str:
        """Prompt para extracción de entidades"""
        return f"""Identifica y lista las entidades principales mencionadas en el texto 
(personas, organizaciones, lugares, fechas, etc.):

Texto:
{text}

Entidades identificadas:"""
    
    def _get_questions_prompt(self, text: str) -> str:
        """Prompt para generar preguntas"""
        return f"""Basándote en el siguiente documento, genera 5 preguntas clave 
que ayuden a comprender mejor el contenido:

Documento:
{text}

Preguntas:"""
    
    async def check_model_availability(self) -> bool:
        """
        Verifica si Ollama está disponible y el modelo está cargado.
        
        Returns:
            True si está disponible, False en caso contrario
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    # Comparación flexible: busca el modelo con o sin :latest
                    return any(
                        model["name"] == self.model or 
                        model["name"] == f"{self.model}:latest" or
                        model["name"].startswith(f"{self.model}:")
                        for model in models
                    )
            return False
        except:
            return False
    
    async def get_available_models(self) -> list:
        """
        Obtiene la lista de modelos disponibles en Ollama.
        
        Returns:
            Lista de nombres de modelos disponibles
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return [model["name"] for model in models]
            return []
        except:
            return []


# Instancia global del servicio
ollama_service = OllamaService()
