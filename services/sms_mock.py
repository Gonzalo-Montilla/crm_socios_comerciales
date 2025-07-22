"""
Simulador de Servicios SMS
Simula las respuestas de proveedores como Twilio, AWS SNS, etc.
"""
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum


class SMSStatus(Enum):
    """Estados posibles de un SMS"""
    QUEUED = "QUEUED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    UNDELIVERED = "UNDELIVERED"


class SMSProvider(Enum):
    """Proveedores de SMS disponibles"""
    TWILIO = "TWILIO"
    AWS_SNS = "AWS_SNS"
    MESSAGEMEDIA = "MESSAGEMEDIA"
    NEXMO = "NEXMO"


@dataclass
class SMSRequest:
    """Estructura de una solicitud de SMS"""
    to_number: str
    message: str
    from_number: Optional[str] = None
    callback_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SMSResponse:
    """Respuesta de un envío de SMS"""
    message_id: str
    to_number: str
    from_number: str
    message: str
    status: SMSStatus
    created_at: datetime
    updated_at: datetime
    cost: float
    error_message: Optional[str] = None
    provider_response_code: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['status'] = self.status.value
        return data


class SMSMockService:
    """
    Servicio simulado para envío de SMS
    Simula comportamientos de Twilio, AWS SNS, etc.
    """
    
    def __init__(self, provider: SMSProvider = SMSProvider.TWILIO):
        self.provider = provider
        self.api_key = "mock_api_key"
        self.account_sid = "mock_account_sid"
        self.auth_token = "mock_auth_token"
        self.base_url = f"https://api.{provider.value.lower()}-mock.com"
        self.from_number = "+57320123456"  # Número colombiano simulado
        
        # Configurar probabilidades de éxito
        self.delivery_rates = {
            "mobile": 0.95,  # Móviles tienen alta tasa de entrega
            "fixed": 0.0     # Fijos no reciben SMS
        }
        
        # Almacenamiento en memoria de mensajes
        self.messages = {}
        
        # Costos simulados por mensaje (en COP)
        self.cost_per_message = {
            SMSProvider.TWILIO: 80,
            SMSProvider.AWS_SNS: 60,
            SMSProvider.MESSAGEMEDIA: 70,
            SMSProvider.NEXMO: 75
        }
    
    def send_sms(self, sms_request: SMSRequest) -> Dict[str, Any]:
        """
        Envía un SMS
        
        Args:
            sms_request: Datos de la solicitud de SMS
            
        Returns:
            Dict con la respuesta del envío
        """
        # Simular latencia de red
        time.sleep(random.uniform(0.3, 1.5))
        
        message_id = str(uuid.uuid4())
        
        # Validar número de teléfono
        if not self._is_valid_phone_number(sms_request.to_number):
            return {
                "success": False,
                "error": "Número de teléfono inválido",
                "code": "INVALID_PHONE_NUMBER"
            }
        
        # Determinar si es móvil o fijo
        phone_type = self._get_phone_type(sms_request.to_number)
        
        # Determinar el resultado basado en el tipo de teléfono
        delivery_rate = self.delivery_rates.get(phone_type, 0.8)
        will_deliver = random.random() < delivery_rate
        
        if phone_type == "fixed":
            status = SMSStatus.FAILED
            error_message = "No se pueden enviar SMS a números fijos"
            provider_code = "LANDLINE_NOT_SUPPORTED"
        elif will_deliver:
            status = SMSStatus.QUEUED  # Inicialmente en cola
            error_message = None
            provider_code = "QUEUED_FOR_DELIVERY"
        else:
            status = SMSStatus.FAILED
            error_message = self._get_failure_reason()
            provider_code = "DELIVERY_FAILED"
        
        # Calcular costo
        cost = self.cost_per_message.get(self.provider, 70)
        if status == SMSStatus.FAILED:
            cost = 0  # No cobrar por mensajes fallidos
        
        # Crear respuesta de SMS
        sms_response = SMSResponse(
            message_id=message_id,
            to_number=sms_request.to_number,
            from_number=sms_request.from_number or self.from_number,
            message=sms_request.message,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            cost=cost,
            error_message=error_message,
            provider_response_code=provider_code
        )
        
        # Guardar mensaje
        self.messages[message_id] = sms_response
        
        # Simular progresión de estados para mensajes exitosos
        if status == SMSStatus.QUEUED:
            self._simulate_async_delivery(message_id)
        
        return {
            "success": status != SMSStatus.FAILED,
            "message": sms_response.to_dict(),
            "message_id": message_id,
            "status": status.value,
            "cost": cost
        }
    
    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Consulta el estado de un mensaje SMS
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Dict con el estado actual del mensaje
        """
        # Simular latencia
        time.sleep(random.uniform(0.1, 0.5))
        
        if message_id not in self.messages:
            return {
                "success": False,
                "error": "Mensaje no encontrado",
                "code": "MESSAGE_NOT_FOUND"
            }
        
        message = self.messages[message_id]
        
        return {
            "success": True,
            "message": message.to_dict(),
            "status": message.status.value
        }
    
    def send_bulk_sms(self, to_numbers: List[str], message: str, 
                     from_number: Optional[str] = None) -> Dict[str, Any]:
        """
        Envía SMS masivos
        
        Args:
            to_numbers: Lista de números de teléfono
            message: Mensaje a enviar
            from_number: Número remitente opcional
            
        Returns:
            Dict con el resultado del envío masivo
        """
        # Simular latencia adicional para envíos masivos
        time.sleep(random.uniform(1.0, 3.0))
        
        results = []
        total_cost = 0
        successful_sends = 0
        failed_sends = 0
        
        for number in to_numbers:
            sms_request = SMSRequest(
                to_number=number,
                message=message,
                from_number=from_number
            )
            
            result = self.send_sms(sms_request)
            results.append({
                "number": number,
                "success": result["success"],
                "message_id": result.get("message_id"),
                "error": result.get("error")
            })
            
            if result["success"]:
                successful_sends += 1
                total_cost += result["cost"]
            else:
                failed_sends += 1
        
        return {
            "success": True,
            "batch_id": str(uuid.uuid4()),
            "total_messages": len(to_numbers),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "total_cost": total_cost,
            "results": results
        }
    
    def get_delivery_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Genera un reporte de entregas
        
        Args:
            start_date: Fecha inicial
            end_date: Fecha final
            
        Returns:
            Dict con el reporte de entregas
        """
        # Simular latencia
        time.sleep(random.uniform(0.5, 2.0))
        
        # Filtrar mensajes por fecha
        filtered_messages = [
            msg for msg in self.messages.values()
            if start_date <= msg.created_at <= end_date
        ]
        
        # Calcular estadísticas
        total_messages = len(filtered_messages)
        delivered = sum(1 for msg in filtered_messages if msg.status == SMSStatus.DELIVERED)
        failed = sum(1 for msg in filtered_messages if msg.status == SMSStatus.FAILED)
        pending = sum(1 for msg in filtered_messages if msg.status in [SMSStatus.QUEUED, SMSStatus.SENT])
        total_cost = sum(msg.cost for msg in filtered_messages)
        
        return {
            "success": True,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "statistics": {
                "total_messages": total_messages,
                "delivered": delivered,
                "failed": failed,
                "pending": pending,
                "delivery_rate": (delivered / total_messages * 100) if total_messages > 0 else 0,
                "total_cost": total_cost
            },
            "messages": [msg.to_dict() for msg in filtered_messages[-100:]]  # Últimos 100
        }
    
    def _is_valid_phone_number(self, number: str) -> bool:
        """Valida si el número de teléfono es válido"""
        # Remover espacios y caracteres especiales
        clean_number = number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Verificar formato colombiano
        if clean_number.startswith("+57"):
            clean_number = clean_number[3:]
        elif clean_number.startswith("57"):
            clean_number = clean_number[2:]
        
        # Debe tener 10 dígitos
        if not clean_number.isdigit() or len(clean_number) != 10:
            return False
        
        # Verificar que sea un número válido (móvil o fijo)
        first_digit = clean_number[0]
        return first_digit in ['3', '1', '2', '4', '5', '6', '7', '8']
    
    def _get_phone_type(self, number: str) -> str:
        """Determina si es móvil o fijo"""
        clean_number = number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if clean_number.startswith("+57"):
            clean_number = clean_number[3:]
        elif clean_number.startswith("57"):
            clean_number = clean_number[2:]
        
        # En Colombia, móviles empiezan con 3
        if clean_number.startswith('3'):
            return "mobile"
        else:
            return "fixed"
    
    def _get_failure_reason(self) -> str:
        """Genera razones de falla realistas"""
        reasons = [
            "Número fuera de servicio",
            "Buzón de mensajes lleno",
            "Error de red del operador",
            "Número bloqueado",
            "Contenido rechazado por filtros de spam"
        ]
        return random.choice(reasons)
    
    def _simulate_async_delivery(self, message_id: str):
        """
        Simula la progresión asíncrona de estados del mensaje
        En un caso real, esto se haría mediante webhooks del proveedor
        """
        # Por ahora, solo progresamos inmediatamente a SENT
        # En implementación real, esto vendría por webhooks
        if message_id in self.messages:
            message = self.messages[message_id]
            
            # Simular progresión: QUEUED -> SENT -> DELIVERED
            message.status = SMSStatus.SENT
            message.updated_at = datetime.now()
            
            # Simular entrega después de un tiempo aleatorio
            if random.random() < 0.9:  # 90% llegan a DELIVERED
                # En implementación real, esto sería un job diferido
                message.status = SMSStatus.DELIVERED
                message.updated_at = datetime.now() + timedelta(seconds=random.randint(10, 300))


# Instancias de diferentes proveedores
twilio_service = SMSMockService(SMSProvider.TWILIO)
aws_sns_service = SMSMockService(SMSProvider.AWS_SNS)
messagemedia_service = SMSMockService(SMSProvider.MESSAGEMEDIA)
