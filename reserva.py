# -*- coding: utf-8 -*-
"""
Modulo con la clase Reserva, que une cliente, servicio, duracion y estado.
"""

from entidades import EntidadBase
from excepciones import (OperacionNoPermitidaError, ParametroInvalidoError,
                         ReservaInvalidaError, SoftwareFJError)
from registro import registrar_error, registrar_evento
from servicios import IVA


class Reserva(EntidadBase):
    """
    Reserva de un servicio por parte de un cliente.

    Estados posibles: PENDIENTE -> CONFIRMADA -> PROCESADA, o CANCELADA.
    """

    PENDIENTE, CONFIRMADA, PROCESADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA"

    def __init__(self, cliente, servicio, duracion, descuento=None):
        super().__init__("RES")
        # Se exige que existan el cliente y el servicio
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Una reserva necesita un cliente y un servicio.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = descuento
        self._estado = Reserva.PENDIENTE
        self._total = None

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def validar(self):
        """La reserva es valida si el cliente y la duracion lo son."""
        self._cliente.validar()
        self._servicio.validar_parametros(self._duracion)
        return True

    def confirmar(self):
        """
        Confirma la reserva calculando su costo.

        Usa try/except/else: si el calculo falla se encadena el error; si no
        falla, el bloque else cambia el estado y registra el evento.
        """
        if self._estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar la reserva {self.id} en estado {self._estado}.")
        try:
            self._servicio.verificar_disponibilidad()
            self.validar()
            total = self._servicio.calcular_costo(self._duracion, impuesto=IVA, descuento=self._descuento)
        except ParametroInvalidoError as error:
            # Encadenamiento: el error de parametro se convierte en error de reserva
            raise ReservaInvalidaError(f"La reserva {self.id} tiene parametros incorrectos.") from error
        else:
            # Solo se ejecuta si no hubo ningun error
            self._total = total
            self._estado = Reserva.CONFIRMADA
            registrar_evento(f"Reserva {self.id} confirmada por ${total:,.2f}")

    def cancelar(self):
        """Cancela la reserva si todavia no ha sido procesada."""
        if self._estado in (Reserva.PROCESADA, Reserva.CANCELADA):
            raise OperacionNoPermitidaError(f"La reserva {self.id} ya esta {self._estado} y no se puede cancelar.")
        self._estado = Reserva.CANCELADA
        registrar_evento(f"Reserva {self.id} cancelada")

    def procesar(self):
        """
        Procesa (cobra) la reserva.

        Usa try/except/finally: pase lo que pase, el bloque finally deja
        constancia en el log del intento de procesamiento.
        """
        try:
            if self._estado != Reserva.CONFIRMADA:
                raise OperacionNoPermitidaError(f"Solo se procesan reservas CONFIRMADAS ({self.id} esta {self._estado}).")
            self._estado = Reserva.PROCESADA
            registrar_evento(f"Reserva {self.id} procesada. Cobro: ${self._total:,.2f}")
        except SoftwareFJError as error:
            registrar_error(error, "procesar")
            raise
        finally:
            # Siempre se ejecuta, haya error o no
            registrar_evento(f"Intento de procesamiento de {self.id} finalizado (estado: {self._estado})")

    def describir(self):
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return (f"{self.id} | {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"duracion {self._duracion} | {self._estado} | total {total}")
