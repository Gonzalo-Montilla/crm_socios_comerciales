"""
Simulador de servicios de DataCrédito/Centrales de Riesgo
Este simulador imita las respuestas de las APIs de consulta crediticia
"""
import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CreditScore:
    """Representa el puntaje crediticio de una persona"""
    score: int
    categoria: str
    fecha_consulta: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HistorialCredito:
    """Representa el historial crediticio de una persona"""
    total_obligaciones: int
    valor_total_deuda: float
    obligaciones_al_dia: int
    obligaciones_vencidas: int
    score_comportamiento: str
    ultima_actualizacion: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DataCreditoMockService:
    """
    Servicio simulado para consultas a DataCrédito
    Simula las operaciones más comunes de consulta crediticia
    """
    
    # Datos simulados para diferentes tipos de documentos
    MOCK_DATA = {
        "12345678": {
            "nombres": "JUAN CARLOS",
            "apellidos": "RODRIGUEZ GARCIA",
            "score": 750,
            "categoria": "A",
            "total_obligaciones": 3,
            "valor_total_deuda": 15000000,
            "obligaciones_al_dia": 3,
            "obligaciones_vencidas": 0,
            "score_comportamiento": "EXCELENTE"
        },
        "87654321": {
            "nombres": "MARIA ELENA",
            "apellidos": "LOPEZ MARTINEZ",
            "score": 650,
            "categoria": "B",
            "total_obligaciones": 2,
            "valor_total_deuda": 8500000,
            "obligaciones_al_dia": 1,
            "obligaciones_vencidas": 1,
            "score_comportamiento": "BUENO"
        },
        "11111111": {
            "nombres": "CARLOS ANDRES",
            "apellidos": "PEREZ SILVA",
            "score": 450,
            "categoria": "D",
            "total_obligaciones": 5,
            "valor_total_deuda": 25000000,
            "obligaciones_al_dia": 2,
            "obligaciones_vencidas": 3,
            "score_comportamiento": "DEFICIENTE"
        }
    }
    
    def __init__(self):
        self.api_key = "mock_api_key"
        self.base_url = "https://api.datacredito-mock.com"
        
    def consultar_score_crediticio(self, numero_documento: str, tipo_documento: str = "CC") -> Dict[str, Any]:
        """
        Simula la consulta de score crediticio
        
        Args:
            numero_documento: Número de documento de identidad
            tipo_documento: Tipo de documento (CC, CE, NIT, etc.)
            
        Returns:
            Dict con información del score crediticio
        """
        # Simular latencia de red
        time.sleep(random.uniform(0.5, 2.0))
        
        # Verificar si tenemos datos mock para este documento
        if numero_documento in self.MOCK_DATA:
            mock_data = self.MOCK_DATA[numero_documento]
            
            score = CreditScore(
                score=mock_data["score"],
                categoria=mock_data["categoria"],
                fecha_consulta=datetime.now()
            )
            
            return {
                "success": True,
                "data": {
                    "documento": numero_documento,
                    "tipo_documento": tipo_documento,
                    "score": score.to_dict(),
                    "nombres": mock_data["nombres"],
                    "apellidos": mock_data["apellidos"]
                },
                "message": "Consulta exitosa"
            }
        else:
            # Generar datos aleatorios para documentos no definidos
            score_value = random.randint(300, 850)
            categoria = self._get_categoria_by_score(score_value)
            
            score = CreditScore(
                score=score_value,
                categoria=categoria,
                fecha_consulta=datetime.now()
            )
            
            return {
                "success": True,
                "data": {
                    "documento": numero_documento,
                    "tipo_documento": tipo_documento,
                    "score": score.to_dict(),
                    "nombres": "PERSONA",
                    "apellidos": "GENERADA AUTOMATICAMENTE"
                },
                "message": "Consulta exitosa (datos simulados)"
            }
    
    def consultar_historial_credito(self, numero_documento: str, tipo_documento: str = "CC") -> Dict[str, Any]:
        """
        Simula la consulta del historial crediticio completo
        
        Args:
            numero_documento: Número de documento de identidad
            tipo_documento: Tipo de documento
            
        Returns:
            Dict con el historial crediticio
        """
        # Simular latencia de red
        time.sleep(random.uniform(1.0, 3.0))
        
        if numero_documento in self.MOCK_DATA:
            mock_data = self.MOCK_DATA[numero_documento]
            
            historial = HistorialCredito(
                total_obligaciones=mock_data["total_obligaciones"],
                valor_total_deuda=mock_data["valor_total_deuda"],
                obligaciones_al_dia=mock_data["obligaciones_al_dia"],
                obligaciones_vencidas=mock_data["obligaciones_vencidas"],
                score_comportamiento=mock_data["score_comportamiento"],
                ultima_actualizacion=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            return {
                "success": True,
                "data": {
                    "documento": numero_documento,
                    "tipo_documento": tipo_documento,
                    "historial": historial.to_dict(),
                    "detalles_obligaciones": self._generar_obligaciones_detalle(mock_data)
                },
                "message": "Consulta de historial exitosa"
            }
        else:
            # Generar datos aleatorios
            total_obligaciones = random.randint(0, 8)
            obligaciones_vencidas = random.randint(0, min(total_obligaciones, 3))
            obligaciones_al_dia = total_obligaciones - obligaciones_vencidas
            valor_total_deuda = random.uniform(1000000, 50000000)
            
            historial = HistorialCredito(
                total_obligaciones=total_obligaciones,
                valor_total_deuda=valor_total_deuda,
                obligaciones_al_dia=obligaciones_al_dia,
                obligaciones_vencidas=obligaciones_vencidas,
                score_comportamiento=self._get_comportamiento_by_vencidas(obligaciones_vencidas),
                ultima_actualizacion=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            return {
                "success": True,
                "data": {
                    "documento": numero_documento,
                    "tipo_documento": tipo_documento,
                    "historial": historial.to_dict(),
                    "detalles_obligaciones": []
                },
                "message": "Consulta de historial exitosa (datos simulados)"
            }
    
    def consulta_express(self, numero_documento: str, tipo_documento: str = "CC") -> Dict[str, Any]:
        """
        Consulta rápida que combina score y resumen del historial
        
        Args:
            numero_documento: Número de documento
            tipo_documento: Tipo de documento
            
        Returns:
            Dict con información resumida
        """
        # Simular latencia reducida para consulta express
        time.sleep(random.uniform(0.2, 0.8))
        
        score_result = self.consultar_score_crediticio(numero_documento, tipo_documento)
        
        if score_result["success"]:
            score_data = score_result["data"]["score"]
            recommendation = self._get_recommendation_by_score(score_data["score"])
            
            return {
                "success": True,
                "data": {
                    "documento": numero_documento,
                    "score": score_data["score"],
                    "categoria": score_data["categoria"],
                    "recomendacion": recommendation,
                    "fecha_consulta": score_data["fecha_consulta"]
                },
                "message": "Consulta express exitosa"
            }
        else:
            return score_result
    
    def _get_categoria_by_score(self, score: int) -> str:
        """Determina la categoría basada en el score"""
        if score >= 750:
            return "A"
        elif score >= 650:
            return "B"
        elif score >= 550:
            return "C"
        else:
            return "D"
    
    def _get_comportamiento_by_vencidas(self, vencidas: int) -> str:
        """Determina el comportamiento basado en obligaciones vencidas"""
        if vencidas == 0:
            return "EXCELENTE"
        elif vencidas == 1:
            return "BUENO"
        elif vencidas == 2:
            return "REGULAR"
        else:
            return "DEFICIENTE"
    
    def _get_recommendation_by_score(self, score: int) -> str:
        """Genera recomendación basada en el score"""
        if score >= 750:
            return "APROBACION_DIRECTA"
        elif score >= 650:
            return "EVALUACION_ESTANDAR"
        elif score >= 550:
            return "EVALUACION_DETALLADA"
        else:
            return "REVISION_ESPECIAL"
    
    def _generar_obligaciones_detalle(self, mock_data: Dict) -> list:
        """Genera detalles ficticios de obligaciones"""
        obligaciones = []
        for i in range(mock_data["total_obligaciones"]):
            obligacion = {
                "entidad": random.choice(["BANCO_COLOMBIA", "BANCO_BOGOTA", "BANCOLOMBIA", "DAVIVIENDA", "BBVA"]),
                "tipo_producto": random.choice(["TARJETA_CREDITO", "CREDITO_CONSUMO", "CREDITO_VEHICULO", "HIPOTECARIO"]),
                "valor_inicial": random.uniform(1000000, 10000000),
                "saldo_actual": random.uniform(100000, 5000000),
                "estado": "AL_DIA" if i < mock_data["obligaciones_al_dia"] else "VENCIDA",
                "dias_vencido": 0 if i < mock_data["obligaciones_al_dia"] else random.randint(30, 180)
            }
            obligaciones.append(obligacion)
        return obligaciones


# Instancia global del servicio mock
datacredito_service = DataCreditoMockService()
