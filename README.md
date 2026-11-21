# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

**Curso:** Programación (213023) – UNAD
**Actividad:** Fase 4 – Componente práctico – Prácticas simuladas
**Grupo:** 213023_81

Sistema orientado a objetos en Python, **sin base de datos**, que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y reservas para la empresa
Software FJ. Su objetivo principal es demostrar un **manejo robusto de excepciones**: el programa
registra todos los errores en un archivo de logs y **nunca se detiene** ante datos inválidos.

## Cómo ejecutarlo

Requiere Python 3.8 o superior (no usa librerías externas).

```bash
python main.py
```

Al terminar se crea el archivo `software_fj.log` con todos los eventos y errores.

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y 6 excepciones hijas con código de error) |
| `registro.py` | Configuración del archivo de logs y funciones para registrar eventos y errores |
| `entidades.py` | Clase abstracta `EntidadBase` (identificador, fecha, `describir()` y `validar()`) |
| `cliente.py` | Clase `Cliente` con datos encapsulados y validaciones (nombre, documento, correo, teléfono) |
| `servicios.py` | Clase abstracta `Servicio` y los servicios `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reserva.py` | Clase `Reserva` con estados y los métodos `confirmar()`, `cancelar()` y `procesar()` |
| `sistema.py` | Clase `SistemaSoftwareFJ`, que guarda todo en listas y atrapa los errores |
| `main.py` | Simulación de 18 operaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `EntidadBase`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `costo_base()`, `validar_parametros()` y `describir()`.
- **Encapsulación:** los datos del cliente son privados y se validan con propiedades (`@property`).
- **Sobrecarga simulada:** `calcular_costo(duracion, impuesto=None, descuento=None)` admite cuatro variantes.
- **Manejo de excepciones:**
  - Excepciones personalizadas con código (FJ-101, FJ-201, FJ-301, FJ-401, FJ-402, FJ-501).
  - `try/except` en todas las operaciones del sistema.
  - `try/except/else` en `Reserva.confirmar()` y en los métodos de `SistemaSoftwareFJ`.
  - `try/except/finally` en `Reserva.procesar()`.
  - **Encadenamiento** (`raise ReservaInvalidaError(...) from error`) cuando falla un parámetro de la reserva.
- **Logs:** todos los eventos y errores se guardan en `software_fj.log`, incluida la causa de los errores encadenados.

## Operaciones simuladas

1. Cliente válido
2. Cliente con correo inválido
3. Cliente con documento inválido
4. Segundo cliente válido y documento repetido
5. Creación de los tres servicios
6. Servicio con tarifa negativa
7. Asesoría con nivel inexistente
8. Reserva válida con descuento
9. Reserva que excede las horas permitidas
10. Alquiler con días no enteros
11. Servicio no disponible
12. Reserva sin cliente
13. Reservas válidas de asesoría y equipo
14. Procesamiento de una reserva
15. Cancelación de una reserva ya procesada (no permitida)
16. Cancelación y luego intento de procesamiento
17. Descuento fuera de rango
18. Cálculo de costos con las variantes de "sobrecarga"

## Integrantes

| Integrante | Usuario de GitHub | Aporte |
|---|---|---|
| Carlos Alberto Ospino Castilla | jocasaname1402-beep | Estructura del proyecto, excepciones, logs, clases y simulación |
