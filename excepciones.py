# -*- coding: utf-8 -*-
"""
Modulo de excepciones personalizadas del sistema Software FJ.

Todas las excepciones del sistema heredan de SoftwareFJError, de modo que
el programa principal puede capturar cualquier error propio con un solo
bloque except, sin detenerse.
"""


class SoftwareFJError(Exception):
    """Excepcion base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Se guarda un codigo para identificar el tipo de error en el log
        super().__init__(mensaje)
        self.codigo = codigo

    def __str__(self):
        # El mensaje se muestra siempre acompanado de su codigo
        return f"[{self.codigo}] {self.args[0]}"


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no superan las validaciones."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-101")


class ParametroInvalidoError(SoftwareFJError):
    """Se lanza cuando falta un parametro o tiene un valor no permitido."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-201")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no esta disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-301")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-401")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una accion no valida para el estado actual."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-402")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un calculo de costos produce un resultado incoherente."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-501")
