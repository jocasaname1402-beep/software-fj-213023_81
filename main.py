# -*- coding: utf-8 -*-
"""
Programa principal: simulacion de operaciones del sistema Software FJ.

Curso: Programacion (213023) - UNAD - Fase 4
Grupo: 213023_81

Se ejecutan operaciones validas e invalidas para demostrar que el sistema
maneja los errores, los registra en el log y sigue funcionando.
"""

from registro import ARCHIVO_LOG, registrar_error, registrar_evento
from servicios import AlquilerEquipo, Asesoria, ReservaSala
from sistema import SistemaSoftwareFJ


def titulo(numero, texto):
    """Imprime el encabezado de cada operacion simulada."""
    print(f"\n[Operacion {numero:02d}] {texto}")


def main():
    # Se crea el sistema con sus listas vacias
    sistema = SistemaSoftwareFJ()
    print("=" * 70)
    print(" SOFTWARE FJ - Simulacion de clientes, servicios y reservas")
    print("=" * 70)

    titulo(1, "Registro de cliente valido")
    ana = sistema.registrar_cliente("ana maria torres", "1065432198", "ana.torres@correo.com", "3001234567")

    titulo(2, "Registro de cliente con correo invalido")
    sistema.registrar_cliente("Luis Perez", "1098765", "luis-correo.com", "3109876543")

    titulo(3, "Registro de cliente con documento invalido")
    sistema.registrar_cliente("Marta Gomez", "12AB", "marta@correo.com", "3201112233")

    titulo(4, "Registro de segundo cliente valido y de un documento repetido")
    jorge = sistema.registrar_cliente("Jorge Diaz", "77012345", "jorge.diaz@correo.co", "3157778899")
    sistema.registrar_cliente("Jorge Duplicado", "77012345", "otro@correo.co", "3157778800")

    titulo(5, "Creacion de los tres servicios validos")
    sala = sistema.agregar_servicio(ReservaSala, "Sala Innovacion", 50000, capacidad=12)
    equipo = sistema.agregar_servicio(AlquilerEquipo, "Portatil i7", 40000, cantidad=3)
    asesoria = sistema.agregar_servicio(Asesoria, "Ciberseguridad", 120000, nivel="experto")

    titulo(6, "Creacion de servicio con tarifa negativa (invalido)")
    sistema.agregar_servicio(ReservaSala, "Sala Fantasma", -10000, capacidad=5)

    titulo(7, "Creacion de asesoria con nivel inexistente (invalido)")
    sistema.agregar_servicio(Asesoria, "Redes", 90000, nivel="maestro")

    titulo(8, "Reserva valida de sala con 10 % de descuento")
    r1 = sistema.crear_reserva(ana, sala, 3, descuento=0.10)

    titulo(9, "Reserva de sala por 12 horas (excede el maximo de 8)")
    sistema.crear_reserva(jorge, sala, 12)

    titulo(10, "Reserva de equipo por 2.5 dias (debe ser un numero entero)")
    sistema.crear_reserva(ana, equipo, 2.5)

    titulo(11, "Reserva de un servicio no disponible")
    # Se desactiva temporalmente la asesoria para provocar el error
    asesoria.cambiar_disponibilidad(False)
    sistema.crear_reserva(jorge, asesoria, 2)
    asesoria.cambiar_disponibilidad(True)

    titulo(12, "Reserva sin cliente (cliente rechazado = None)")
    sistema.crear_reserva(None, equipo, 2)

    titulo(13, "Reserva valida de asesoria y de equipo")
    r2 = sistema.crear_reserva(jorge, asesoria, 2)
    r3 = sistema.crear_reserva(jorge, equipo, 5)

    titulo(14, "Procesar reserva confirmada")
    sistema.procesar_reserva(r1)

    titulo(15, "Cancelar reserva ya procesada (operacion no permitida)")
    sistema.cancelar_reserva(r1)

    titulo(16, "Cancelar reserva confirmada y luego intentar procesarla")
    sistema.cancelar_reserva(r3)
    sistema.procesar_reserva(r3)

    titulo(17, "Descuento fuera de rango (60 %)")
    sistema.crear_reserva(ana, sala, 2, descuento=0.6)

    titulo(18, "Calculo de costos con 'sobrecarga' (variantes del mismo metodo)")
    print(f"   Costo base 2 h de asesoria:         ${asesoria.calcular_costo(2):,.2f}")
    print(f"   Con IVA 19 %:                       ${asesoria.calcular_costo(2, impuesto=0.19):,.2f}")
    print(f"   Con descuento 10 %:                 ${asesoria.calcular_costo(2, descuento=0.10):,.2f}")
    print(f"   Con IVA y descuento:                ${asesoria.calcular_costo(2, 0.19, 0.10):,.2f}")

    # Al final se muestra lo que quedo guardado en las listas
    sistema.resumen()
    print(f"\nTodos los eventos y errores quedaron registrados en '{ARCHIVO_LOG}'.")
    registrar_evento("Simulacion finalizada correctamente")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # Ultima red de seguridad: nada detiene el programa sin registro
        registrar_error(error, "error inesperado en main")
        print(f"Error inesperado registrado en el log: {error}")
