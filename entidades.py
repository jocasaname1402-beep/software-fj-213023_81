# -*- coding: utf-8 -*-
"""
Modulo con la clase abstracta que representa cualquier entidad del sistema.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from itertools import count


class EntidadBase(ABC):
    """
    Clase abstracta general del sistema.

    Toda entidad (cliente, servicio, reserva) tiene un identificador unico y
    una fecha de creacion, y debe saber describirse y validarse.
    """

    # Un contador por tipo de entidad (CLI, SRV, RES) para numerar en orden
    _contadores = {}

    def __init__(self, prefijo):
        # Identificador unico con un prefijo segun el tipo de entidad
        contador = EntidadBase._contadores.setdefault(prefijo, count(1))
        self._id = f"{prefijo}-{next(contador):03d}"
        # Momento en que se creo la entidad
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        """Identificador de solo lectura (encapsulado)."""
        return self._id

    @property
    def fecha_creacion(self):
        """Fecha de creacion de solo lectura."""
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Cada entidad debe devolver una descripcion legible."""

    @abstractmethod
    def validar(self):
        """Cada entidad debe validar sus propios datos."""

    def __str__(self):
        # Al imprimir una entidad se muestra su descripcion
        return self.describir()
