# viajes_aventura

## Contexto del caso

La agencia **Viajes Aventura** necesita ordenar y conectar tres hitos funcionales en una solución integrada para sus operaciones y clientes:

* **Destinos:** Mantener información válida y reutilizable, permitiendo a la agencia registrar, consultar, modificar y eliminar o retirar destinos conservando el historial de viajes anteriores y validando qué paquetes usan un destino que deja de ofrecerse.
* **Paquetes:** Combinar destinos en un orden definido (indicando en qué orden se visitan), establecer fechas, calcular costos y consultar cupos disponibles (incluyendo cupos independientes para distintas fechas y cómo se calculan antes de confirmar).
* **Reservas y acceso:** Permitir que los clientes se registren e inicien sesión, reserven paquetes indicando quién realizó la reserva y qué personas viajarán, consulten su historial y que la agencia pueda seguir el avance por etapas (cuántos pasajeros están pendientes, viajando o con viaje finalizado, qué etapas completó una persona y cuál está cursando, y recuperar precio e itinerario de reservas anteriores).

En el diseño y entrega del proyecto se trabaja con estructura por capas, convención de código en inglés y mensajes al usuario en español, base de datos relacional con datos de ejemplo y validación de preguntas de negocio, además de gestión mediante ramas, Pull Requests revisados y trazabilidad en Jira.

## Cómo iniciar el proyecto

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd viajes-aventura
