# -*- coding: utf-8 -*-
"""
Modulo con la clase abstracta Servicio y los tres servicios especializados.
"""

from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroInvalidoError,
                         ServicioNoDisponibleError)

# IVA por defecto en Colombia
IVA = 0.19


class Servicio(EntidadBase):
    """
    Clase abstracta para todos los servicios de Software FJ.

    Cada servicio hijo debe definir su propio calculo de costo base, su
    descripcion y la validacion de sus parametros (polimorfismo).
    """

    def __init__(self, nombre, tarifa, disponible=True):
        super().__init__("SRV")
        # La tarifa debe ser un numero positivo
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ParametroInvalidoError(f"La tarifa de '{nombre}' debe ser un numero mayor que cero.")
        self._nombre = nombre
        self._tarifa = float(tarifa)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        """Permite activar o desactivar el servicio."""
        self._disponible = bool(disponible)

    def verificar_disponibilidad(self):
        """Lanza un error si el servicio no se puede reservar en este momento."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no esta disponible.")

    # ---------- metodos que cada hijo debe sobrescribir (polimorfismo) ----------
    @abstractmethod
    def costo_base(self, duracion):
        """Costo sin impuestos ni descuentos para una duracion dada."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Comprueba que la duracion solicitada sea valida para el servicio."""

    @abstractmethod
    def describir(self):
        """Descripcion del servicio."""

    def validar(self):
        """Un servicio es valido si tiene tarifa positiva."""
        return self._tarifa > 0

    # ---------- "sobrecarga" del calculo de costos ----------
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        Calcula el costo con distintas variantes (sobrecarga simulada).

        Python no permite varios metodos con el mismo nombre, por eso se
        usan parametros opcionales:
          - calcular_costo(duracion)                    -> costo base
          - calcular_costo(duracion, impuesto=0.19)     -> con impuesto
          - calcular_costo(duracion, descuento=0.10)    -> con descuento
          - calcular_costo(duracion, 0.19, 0.10)        -> con ambos
        """
        self.validar_parametros(duracion)
        costo = self.costo_base(duracion)

        if descuento is not None:
            # El descuento debe estar entre 0 % y 50 %
            if not 0 <= descuento <= 0.5:
                raise ParametroInvalidoError(f"Descuento {descuento:.0%} fuera del rango permitido (0 % a 50 %).")
            costo *= (1 - descuento)

        if impuesto is not None:
            # El impuesto debe estar entre 0 % y 30 %
            if not 0 <= impuesto <= 0.3:
                raise ParametroInvalidoError(f"Impuesto {impuesto:.0%} fuera del rango permitido (0 % a 30 %).")
            costo *= (1 + impuesto)

        # Control de coherencia: un costo nunca puede ser negativo o cero
        if costo <= 0:
            raise CalculoInconsistenteError(f"El costo calculado ({costo}) no es valido.")
        return round(costo, 2)


class ReservaSala(Servicio):
    """Reserva de salas por horas, con capacidad maxima de personas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion):
        # Una sala se reserva entre 1 y 8 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 8:
            raise ParametroInvalidoError(f"Una sala se reserva entre 1 y 8 horas (se pidieron {duracion}).")

    def costo_base(self, duracion):
        # Tarifa por hora
        return self._tarifa * duracion

    def describir(self):
        return f"{self.id} | Sala '{self._nombre}' | {self._capacidad} personas | ${self._tarifa:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por dias, con una cantidad de unidades."""

    def __init__(self, nombre, tarifa_dia, cantidad, disponible=True):
        super().__init__(nombre, tarifa_dia, disponible)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroInvalidoError("La cantidad de equipos debe ser un entero positivo.")
        self._cantidad = cantidad

    def validar_parametros(self, duracion):
        # Un equipo se alquila entre 1 y 30 dias completos
        if not isinstance(duracion, int) or not 1 <= duracion <= 30:
            raise ParametroInvalidoError(f"Un equipo se alquila entre 1 y 30 dias enteros (se pidieron {duracion}).")

    def costo_base(self, duracion):
        # Tarifa por dia por cada unidad alquilada
        return self._tarifa * duracion * self._cantidad

    def describir(self):
        return f"{self.id} | Alquiler '{self._nombre}' x{self._cantidad} | ${self._tarifa:,.0f}/dia"


class Asesoria(Servicio):
    """Asesoria especializada por horas; el nivel experto tiene recargo."""

    NIVELES = {"basico": 1.0, "avanzado": 1.3, "experto": 1.6}

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise ParametroInvalidoError(f"Nivel '{nivel}' no valido. Use: {', '.join(self.NIVELES)}.")
        self._nivel = nivel

    def validar_parametros(self, duracion):
        # Una asesoria dura entre media hora y 4 horas
        if not isinstance(duracion, (int, float)) or not 0.5 <= duracion <= 4:
            raise ParametroInvalidoError(f"Una asesoria dura entre 0.5 y 4 horas (se pidieron {duracion}).")

    def costo_base(self, duracion):
        # Tarifa por hora multiplicada por el factor del nivel
        return self._tarifa * duracion * self.NIVELES[self._nivel]

    def describir(self):
        return f"{self.id} | Asesoria '{self._nombre}' nivel {self._nivel} | ${self._tarifa:,.0f}/hora"
