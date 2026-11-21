# -*- coding: utf-8 -*-
"""
Modulo con la clase Cliente y sus validaciones.
"""

import re

from entidades import EntidadBase
from excepciones import ClienteInvalidoError

# Expresion regular sencilla para validar correos electronicos
_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")


class Cliente(EntidadBase):
    """
    Representa a un cliente de Software FJ.

    Los datos personales son privados (encapsulacion) y solo se modifican a
    traves de propiedades que validan cada valor.
    """

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__("CLI")
        # Cada asignacion pasa por su propiedad, que valida el dato
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------------- nombre ----------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre es obligatorio y solo admite letras y espacios
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre del cliente es obligatorio.")
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(f"El nombre '{valor}' contiene caracteres no validos.")
        self.__nombre = valor.strip().title()

    # ---------------- documento ----------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # El documento debe tener entre 6 y 10 digitos
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"El documento '{valor}' debe tener entre 6 y 10 digitos.")
        self.__documento = valor

    # ---------------- correo ----------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # El correo debe tener el formato usuario@dominio.ext
        if not isinstance(valor, str) or not _PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato valido.")
        self.__correo = valor.strip().lower()

    # ---------------- telefono ----------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # El telefono debe tener exactamente 10 digitos
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError(f"El telefono '{valor}' debe tener 10 digitos.")
        self.__telefono = valor

    def validar(self):
        """Vuelve a comprobar todos los datos (util antes de reservar)."""
        self.nombre = self.nombre
        self.documento = self.documento
        self.correo = self.correo
        self.telefono = self.telefono
        return True

    def describir(self):
        """Descripcion del cliente; el documento se muestra parcialmente oculto."""
        oculto = "*" * (len(self.documento) - 4) + self.documento[-4:]
        return f"{self.id} | {self.nombre} | Doc. {oculto} | {self.correo}"
