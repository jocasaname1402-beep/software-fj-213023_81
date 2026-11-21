# -*- coding: utf-8 -*-
"""
Modulo de registro (logs) del sistema Software FJ.

Configura un archivo de logs donde se guardan los eventos importantes y
todos los errores que ocurren durante la ejecucion.
"""

import logging

# Nombre del archivo donde se guardan los eventos y errores
ARCHIVO_LOG = "software_fj.log"

# Se crea un registrador propio para no mezclarlo con otros modulos
_logger = logging.getLogger("software_fj")
_logger.setLevel(logging.INFO)

# Solo se agrega el manejador una vez, aunque el modulo se importe varias veces
if not _logger.handlers:
    _manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
    _formato = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    _manejador.setFormatter(_formato)
    _logger.addHandler(_manejador)


def registrar_evento(mensaje):
    """Guarda en el log un evento normal del sistema (nivel INFO)."""
    _logger.info(mensaje)


def registrar_advertencia(mensaje):
    """Guarda en el log una situacion que no es error pero merece atencion."""
    _logger.warning(mensaje)


def registrar_error(error, contexto=""):
    """
    Guarda un error en el log.

    Si el error fue encadenado (raise ... from ...), tambien se registra la
    causa original para facilitar el diagnostico.
    """
    texto = f"{contexto} -> {error}" if contexto else str(error)
    if error.__cause__ is not None:
        # Encadenamiento de excepciones: se deja constancia de la causa
        texto += f" | causa original: {type(error.__cause__).__name__}: {error.__cause__}"
    _logger.error(texto)
