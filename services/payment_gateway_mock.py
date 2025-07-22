"""
Simulador de Pasarelas de Pago
Simula las respuestas de PayU, Wompi, Mercado Pago, etc.
"""
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class PaymentStatus(Enum):
    """Estados posibles de un pago"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentMethod(Enum):
    """Métodos de pago disponibles"""
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PSE = "PSE"
    NEQUI = "NEQUI"
    DAVIPLATA = "DAVIPLATA"
    EFECTY = "EFECTY"
    BALOTO = "BALOTO"


@dataclass
class PaymentRequest:
    """Estructura de una solicitud de pago"""
    amount: float
    currency: str
    description: str
    customer_email: str
    customer_name: str
    customer_phone: str
    customer_document: str
    payment_method: PaymentMethod
    reference: str
    return_url: str
    confirmation_url: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PaymentResponse:
    """Respuesta de una transacción de pago"""
    transaction_id: str
    reference: str
    status: PaymentStatus
    amount: float
    currency: str
    payment_method: PaymentMethod
    created_at: datetime
    updated_at: datetime
    authorization_code: Optional[str] = None
    error_message: Optional[str] = None
    gateway_response_code: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['status'] = self.status.value
        data['payment_method'] = self.payment_method.value
        return data


class PaymentGatewayMockService:
    """
    Servicio simulado para pasarelas de pago
    Simula comportamientos de PayU, Wompi, Mercado Pago, etc.
    """
    
    def __init__(self, gateway_name: str = "PayU"):
        self.gateway_name = gateway_name
        self.api_key = "mock_api_key"
        self.merchant_id = "mock_merchant_123"
        self.base_url = f"https://api.{gateway_name.lower()}-mock.com"
        
        # Configurar probabilidades de éxito por método de pago
        self.success_rates = {
            PaymentMethod.CREDIT_CARD: 0.85,
            PaymentMethod.DEBIT_CARD: 0.80,
            PaymentMethod.PSE: 0.90,
            PaymentMethod.NEQUI: 0.95,
            PaymentMethod.DAVIPLATA: 0.95,
            PaymentMethod.EFECTY: 0.98,
            PaymentMethod.BALOTO: 0.98
        }
        
        # Almacenamiento en memoria de transacciones
        self.transactions = {}
    
    def create_payment(self, payment_request: PaymentRequest) -> Dict[str, Any]:
        """
        Crea una nueva transacción de pago
        
        Args:
            payment_request: Datos de la solicitud de pago
            
        Returns:
            Dict con la respuesta de la transacción
        """
        # Simular latencia de red
        time.sleep(random.uniform(0.5, 2.0))
        
        transaction_id = str(uuid.uuid4())
        
        # Determinar el resultado basado en las probabilidades
        success_rate = self.success_rates.get(payment_request.payment_method, 0.85)
        is_successful = random.random() < success_rate
        
        if is_successful:
            status = PaymentStatus.APPROVED
            auth_code = f"AUTH_{random.randint(100000, 999999)}"
            error_message = None
            response_code = "00"  # Código de éxito estándar
        else:
            status = self._get_random_failure_status()
            auth_code = None
            error_message = self._get_error_message(status, payment_request.payment_method)
            response_code = self._get_error_code(status)
        
        # Crear respuesta de pago
        payment_response = PaymentResponse(
            transaction_id=transaction_id,
            reference=payment_request.reference,
            status=status,
            amount=payment_request.amount,
            currency=payment_request.currency,
            payment_method=payment_request.payment_method,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            authorization_code=auth_code,
            error_message=error_message,
            gateway_response_code=response_code
        )
        
        # Guardar transacción
        self.transactions[transaction_id] = payment_response
        
        # Simular webhook asíncrono para algunos casos
        if status == PaymentStatus.PENDING:
            # En un caso real, esto se haría asíncronamente
            self._simulate_async_confirmation(transaction_id)
        
        return {
            "success": status in [PaymentStatus.APPROVED, PaymentStatus.PENDING],
            "transaction": payment_response.to_dict(),
            "payment_url": f"{self.base_url}/checkout/{transaction_id}" if status == PaymentStatus.PENDING else None,
            "message": f"Transacción {status.value.lower()}"
        }
    
    def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Consulta el estado de una transacción
        
        Args:
            transaction_id: ID de la transacción
            
        Returns:
            Dict con el estado actual de la transacción
        """
        # Simular latencia
        time.sleep(random.uniform(0.2, 0.8))
        
        if transaction_id not in self.transactions:
            return {
                "success": False,
                "error": "Transacción no encontrada",
                "code": "TRANSACTION_NOT_FOUND"
            }
        
        transaction = self.transactions[transaction_id]
        
        return {
            "success": True,
            "transaction": transaction.to_dict(),
            "message": "Consulta exitosa"
        }
    
    def refund_payment(self, transaction_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Procesa un reembolso
        
        Args:
            transaction_id: ID de la transacción original
            amount: Monto a reembolsar (None para reembolso total)
            
        Returns:
            Dict con el resultado del reembolso
        """
        # Simular latencia
        time.sleep(random.uniform(1.0, 3.0))
        
        if transaction_id not in self.transactions:
            return {
                "success": False,
                "error": "Transacción no encontrada",
                "code": "TRANSACTION_NOT_FOUND"
            }
        
        original_transaction = self.transactions[transaction_id]
        
        if original_transaction.status != PaymentStatus.APPROVED:
            return {
                "success": False,
                "error": "Solo se pueden reembolsar transacciones aprobadas",
                "code": "INVALID_TRANSACTION_STATUS"
            }
        
        refund_amount = amount or original_transaction.amount
        
        if refund_amount > original_transaction.amount:
            return {
                "success": False,
                "error": "El monto del reembolso no puede ser mayor al monto original",
                "code": "INVALID_REFUND_AMOUNT"
            }
        
        # Simular probabilidad de éxito del reembolso
        if random.random() < 0.95:  # 95% de éxito en reembolsos
            refund_id = str(uuid.uuid4())
            
            # Actualizar transacción original
            if refund_amount == original_transaction.amount:
                original_transaction.status = PaymentStatus.REFUNDED
            
            original_transaction.updated_at = datetime.now()
            
            return {
                "success": True,
                "refund_id": refund_id,
                "refund_amount": refund_amount,
                "original_transaction_id": transaction_id,
                "status": "REFUND_APPROVED",
                "message": "Reembolso procesado exitosamente"
            }
        else:
            return {
                "success": False,
                "error": "Error procesando el reembolso",
                "code": "REFUND_PROCESSING_ERROR"
            }
    
    def cancel_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Cancela una transacción pendiente
        
        Args:
            transaction_id: ID de la transacción
            
        Returns:
            Dict con el resultado de la cancelación
        """
        time.sleep(random.uniform(0.5, 1.5))
        
        if transaction_id not in self.transactions:
            return {
                "success": False,
                "error": "Transacción no encontrada",
                "code": "TRANSACTION_NOT_FOUND"
            }
        
        transaction = self.transactions[transaction_id]
        
        if transaction.status != PaymentStatus.PENDING:
            return {
                "success": False,
                "error": "Solo se pueden cancelar transacciones pendientes",
                "code": "INVALID_TRANSACTION_STATUS"
            }
        
        transaction.status = PaymentStatus.CANCELLED
        transaction.updated_at = datetime.now()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "status": "CANCELLED",
            "message": "Transacción cancelada exitosamente"
        }
    
    def _get_random_failure_status(self) -> PaymentStatus:
        """Retorna un estado de falla aleatorio"""
        failure_statuses = [PaymentStatus.REJECTED, PaymentStatus.ERROR]
        weights = [0.7, 0.3]  # Más rechazos que errores
        return random.choices(failure_statuses, weights=weights)[0]
    
    def _get_error_message(self, status: PaymentStatus, payment_method: PaymentMethod) -> str:
        """Genera mensajes de error realistas"""
        if status == PaymentStatus.REJECTED:
            messages = [
                "Transacción rechazada por el banco emisor",
                "Fondos insuficientes",
                "Tarjeta vencida",
                "Tarjeta bloqueada",
                "Límite de transacciones excedido"
            ]
        else:  # ERROR
            messages = [
                "Error de comunicación con el banco",
                "Timeout en la transacción",
                "Error interno del sistema",
                "Servicio temporalmente no disponible"
            ]
        
        return random.choice(messages)
    
    def _get_error_code(self, status: PaymentStatus) -> str:
        """Genera códigos de error realistas"""
        if status == PaymentStatus.REJECTED:
            codes = ["51", "14", "54", "62", "65"]  # Códigos ISO 8583 comunes
        else:  # ERROR
            codes = ["96", "91", "99", "30"]
        
        return random.choice(codes)
    
    def _simulate_async_confirmation(self, transaction_id: str):
        """
        Simula la confirmación asíncrona de una transacción pendiente
        En un caso real, esto se haría mediante un job en background
        """
        # Por ahora, solo marcamos que se procesará asíncronamente
        # En implementación real, usarías Celery o similar
        pass


# Instancias de diferentes gateways
payu_service = PaymentGatewayMockService("PayU")
wompi_service = PaymentGatewayMockService("Wompi")
mercadopago_service = PaymentGatewayMockService("MercadoPago")
