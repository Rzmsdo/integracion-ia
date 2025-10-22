"""
Servicio para integración con Supabase.
Gestiona el almacenamiento de análisis y consultas a la base de datos.
"""

from typing import List, Dict, Optional
from datetime import datetime
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()


class SupabaseService:
    """
    Servicio centralizado para interactuar con Supabase.
    Maneja todas las operaciones de base de datos.
    """
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.table_name = "analyses"
    
    async def save_analysis(
        self, 
        user_id: str, 
        document_name: str, 
        analysis: Dict,
        file_size: Optional[int] = None,
        file_type: Optional[str] = None,
        original_text: Optional[str] = None
    ) -> Dict:
        """
        Guarda el resultado de un análisis en Supabase.
        Primero crea el documento, luego el análisis.
        
        Args:
            user_id: ID del usuario que realizó el análisis
            document_name: Nombre del documento analizado
            analysis: Diccionario con los resultados del análisis
            file_size: Tamaño del archivo en bytes (opcional)
            file_type: Tipo/extensión del archivo (opcional)
            original_text: Texto original del documento (opcional)
        
        Returns:
            Diccionario con los datos guardados
        """
        try:
            # 1. Asegurar que el usuario existe
            user_result = self.client.table("users").select("user_id").eq("user_id", user_id).execute()
            if not user_result.data:
                # Crear usuario si no existe
                self.client.table("users").insert({
                    "user_id": user_id,
                    "name": user_id,
                    "email": f"{user_id}@example.com"
                }).execute()
            
            # 2. Crear documento
            metadata = analysis.get("metadata", {})
            doc_data = {
                "user_id": user_id,
                "filename": document_name,
                "file_type": file_type or "",
                "file_size": file_size or 0,
                "original_text": original_text,
                "text_length": metadata.get("text_length", 0),
                "word_count": metadata.get("word_count", 0)
            }
            
            doc_result = self.client.table("documents").insert(doc_data).execute()
            
            if not doc_result.data:
                raise Exception("No data returned from documents insert")
            
            document_id = doc_result.data[0]["id"]
            
            # 3. Crear análisis
            analysis_data = {
                "document_id": document_id,
                "user_id": user_id,
                "analysis_type": analysis.get("type", "general"),
                "summary": analysis.get("summary"),
                "key_points": analysis.get("key_points"),
                "sentiment": analysis.get("sentiment"),
                "entities": analysis.get("entities"),
                "questions": analysis.get("questions"),
                "model_used": metadata.get("model_used"),
                "metadata": {
                    "file_size": file_size,
                    "file_type": file_type,
                    "analyzed_at": datetime.utcnow().isoformat()
                }
            }
            
            analysis_result = self.client.table("analyses").insert(analysis_data).execute()
            
            if analysis_result.data:
                return {
                    **analysis_result.data[0],
                    "document_id": document_id
                }
            else:
                raise Exception("No data returned from analyses insert")
        
        except Exception as e:
            raise Exception(f"Error saving to Supabase: {str(e)}")
    
    async def get_analysis_by_id(self, analysis_id: str, user_id: str) -> Optional[Dict]:
        """
        Obtiene un análisis específico por ID.
        
        Args:
            analysis_id: ID del análisis
            user_id: ID del usuario (para verificar permisos)
        
        Returns:
            Diccionario con el análisis o None si no existe
        """
        try:
            result = self.client.table(self.table_name) \
                .select("*") \
                .eq("id", analysis_id) \
                .eq("user_id", user_id) \
                .single() \
                .execute()
            
            return result.data if result.data else None
        
        except Exception as e:
            # Si no se encuentra, retornar None en lugar de error
            if "PGRST116" in str(e):  # Error de Supabase para "no rows"
                return None
            raise Exception(f"Error fetching analysis from Supabase: {str(e)}")
    
    async def get_user_analyses(
        self, 
        user_id: str, 
        limit: int = 10,
        offset: int = 0,
        order_by: str = "analyzed_at"
    ) -> List[Dict]:
        """
        Obtiene todos los análisis de un usuario usando la vista document_analyses_view.
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de resultados
            offset: Offset para paginación
            order_by: Campo por el que ordenar
        
        Returns:
            Lista de análisis con información del documento
        """
        try:
            result = self.client.table("document_analyses_view") \
                .select("*") \
                .eq("user_id", user_id) \
                .order(order_by, desc=True) \
                .range(offset, offset + limit - 1) \
                .execute()
            
            # Mapear campos de la vista al formato esperado
            analyses = []
            for item in (result.data or []):
                analyses.append({
                    "id": item.get("analysis_id"),
                    "user_id": item.get("user_id"),
                    "document_name": item.get("filename"),
                    "analysis_type": item.get("analysis_type"),
                    "summary": item.get("summary"),
                    "key_points": item.get("key_points"),
                    "sentiment": item.get("sentiment"),
                    "created_at": item.get("analyzed_at"),
                    "metadata": {
                        "model_used": item.get("model_used"),
                        "file_size": item.get("file_size"),
                        "file_type": item.get("file_type"),
                        "word_count": item.get("word_count")
                    }
                })
            
            return analyses
        
        except Exception as e:
            raise Exception(f"Error fetching analyses from Supabase: {str(e)}")
    
    async def get_analyses_by_document_name(
        self, 
        user_id: str, 
        document_name: str
    ) -> List[Dict]:
        """
        Obtiene todos los análisis de un documento específico.
        
        Args:
            user_id: ID del usuario
            document_name: Nombre del documento
        
        Returns:
            Lista de análisis del documento
        """
        try:
            result = self.client.table(self.table_name) \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("document_name", document_name) \
                .order("created_at", desc=True) \
                .execute()
            
            return result.data if result.data else []
        
        except Exception as e:
            raise Exception(f"Error fetching document analyses from Supabase: {str(e)}")
    
    async def search_analyses(
        self, 
        user_id: str, 
        search_term: str,
        limit: int = 20
    ) -> List[Dict]:
        """
        Busca análisis por término de búsqueda.
        Busca en document_name, summary y key_points.
        
        Args:
            user_id: ID del usuario
            search_term: Término a buscar
            limit: Número máximo de resultados
        
        Returns:
            Lista de análisis que coinciden
        """
        try:
            # Supabase Full Text Search (requiere configuración en la BD)
            result = self.client.table(self.table_name) \
                .select("*") \
                .eq("user_id", user_id) \
                .or_(
                    f"document_name.ilike.%{search_term}%,"
                    f"summary.ilike.%{search_term}%,"
                    f"key_points.ilike.%{search_term}%"
                ) \
                .limit(limit) \
                .execute()
            
            return result.data if result.data else []
        
        except Exception as e:
            raise Exception(f"Error searching analyses in Supabase: {str(e)}")
    
    async def update_analysis(
        self, 
        analysis_id: str, 
        user_id: str, 
        updates: Dict
    ) -> Dict:
        """
        Actualiza un análisis existente.
        
        Args:
            analysis_id: ID del análisis
            user_id: ID del usuario (para verificar permisos)
            updates: Diccionario con los campos a actualizar
        
        Returns:
            Análisis actualizado
        """
        try:
            # Añadir timestamp de actualización
            updates["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.client.table(self.table_name) \
                .update(updates) \
                .eq("id", analysis_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("No data returned from Supabase update")
        
        except Exception as e:
            raise Exception(f"Error updating analysis in Supabase: {str(e)}")
    
    async def delete_analysis(self, analysis_id: str, user_id: str) -> bool:
        """
        Elimina un análisis.
        
        Args:
            analysis_id: ID del análisis a eliminar
            user_id: ID del usuario (para verificar permisos)
        
        Returns:
            True si se eliminó correctamente
        """
        try:
            result = self.client.table(self.table_name) \
                .delete() \
                .eq("id", analysis_id) \
                .eq("user_id", user_id) \
                .execute()
            
            return True
        
        except Exception as e:
            raise Exception(f"Error deleting analysis from Supabase: {str(e)}")
    
    async def get_user_statistics(self, user_id: str) -> Dict:
        """
        Obtiene estadísticas de análisis del usuario.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            # Total de análisis
            total_result = self.client.table(self.table_name) \
                .select("id", count="exact") \
                .eq("user_id", user_id) \
                .execute()
            
            total_analyses = total_result.count if hasattr(total_result, 'count') else 0
            
            # Análisis por tipo
            analyses = await self.get_user_analyses(user_id, limit=1000)
            
            types_count = {}
            for analysis in analyses:
                analysis_type = analysis.get("analysis_type", "general")
                types_count[analysis_type] = types_count.get(analysis_type, 0) + 1
            
            return {
                "total_analyses": total_analyses,
                "analyses_by_type": types_count,
                "total_documents": len(set(a.get("document_name") for a in analyses))
            }
        
        except Exception as e:
            raise Exception(f"Error fetching statistics from Supabase: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Verifica la conexión con Supabase.
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            # Intentar una consulta simple
            result = self.client.table(self.table_name).select("id").limit(1).execute()
            return True
        except Exception as e:
            print(f"Supabase connection test failed: {str(e)}")
            return False


# Instancia global del servicio
supabase_service = SupabaseService()
