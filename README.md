
# ⚔️ PerezBoost Manager: Evolution Journey (V1 to V7.5)

**De un prototipo funcional a una infraestructura empresarial para la gestión de servicios digitales (Elo Boosting).**

Este repositorio documenta el proceso de aprendizaje y escalabilidad de un sistema de gestión real, pasando por la migración de archivos planos a SQL, la modularización de lógica de negocio y la implementación de una interfaz gráfica moderna.

---

## 📈 Línea de Tiempo del Proyecto

| **Versión** | **Hito Tecnológico**       | **Descripción**                                                                               |
| ------------------ | --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **V1 - V5**  | **Prototipado Legacy**      | Uso de archivos `.txt` para persistencia. Menús simples en consola.                               |
| **V6.0**     | **Migración SQL**          | Implementación de **SQLite3** . Estructura de carpetas profesional (`core/`,`modules/`). |
| **V7.0**     | **Interfaz Gráfica (GUI)** | Transición a **CustomTkinter **con diseño Dark Mode y ventanas dinámicas.                       |
| **V7.5**     | **Arquitectura Dual**       | Sistema híbrido:**GUI **para gestión masiva y CMD para operaciones rápidas.                    |

---

## 🖼️ Preview: La Cúspide del Proyecto (V7.5)

<div align="center">

<img src="image.png" alt="PerezBoost V7.5 GUI" width="800">

<p><em>Interfaz final implementada con CustomTkinter, integrando tablas dinámicas, filtrado inteligente y gestión de tarifas.</em></p>

</div>

---

## 🚀 Innovaciones Técnicas Destacadas

### 1. Arquitectura Desacoplada (MVC-lite)

El sistema separa estrictamente la **Persistencia** (`core/database.py`), la **Lógica de Negocio** (`core/logic.py`) y la **Interfaz** (`gui_main.py` & `cmd_main.py`). Esto permite que ambos modos (Gráfico y Consola) compartan el mismo "cerebro" sin duplicar código.

### 2. Gestión de Tarifas Dinámica (Data-Driven)

A diferencia de las versiones iniciales, la V7.5 elimina el  *hardcoding* . Los precios de las divisiones y los márgenes de ganancia se gestionan desde una pestaña dedicada que actualiza la base de datos en tiempo real.

### 3. Protocolo de Integridad y Respaldo

* **Backups Automatizados:** Sistema de rotación de 10 copias de seguridad cada vez que se cierra la aplicación.
* **Protocolo de Abandono:** Lógica inteligente que restaura cuentas al inventario manteniendo el historial de rendimiento del booster.

## 📁 Estructura del Repositorio

**Plaintext**

```
├── gui_main.py          # Lanzador de Interfaz Gráfica (V7.5)
├── cmd_main.py          # Lanzador de Consola (V7.5)
├── core/                # EL MOTOR (Logic & DB)
│   ├── database.py      # Queries, Transacciones y Backups
│   └── logic.py         # Cálculos financieros y fechas
├── modules/             # LOS PUENTES (Lógica de Módulos)
│   ├── boosters.py      # Gestión de Staff
│   ├── inventario.py    # Gestión de Stock
│   └── pedidos.py       # Ciclo de vida de órdenes
├── dev_logs/            # Archivos de aprendizaje y versiones previas (V1-V6)
└── perezboost.db        # Base de Datos Relacional
```

---

## 🛠️ Instalación para Desarrolladores

1. **Clonar y preparar entorno:**
   **Bash**

   ```
   git clone https://github.com/AndresPerez2406/elo-boost-manager.git
   cd elo-boost-manager
   python -m venv .venv
   source .venv/scripts/activate  # En Windows: .venv\Scripts\activate
   ```
2. **Instalar dependencias:**
   **Bash**

   ```
   pip install customtkinter
   ```
3. **Ejecutar versión de preferencia:**

   * **Modo Pro (GUI):** `python gui_main.py`
   * **Modo Rápido (CMD):** `python cmd_main.py`

---

## 🧠 Aprendizajes Clave

* **SQL vs Flat Files:** Mejora del 100% en la integridad de datos y capacidad de búsqueda.
* **POO & CustomTkinter:** Creación de componentes reutilizables y manejo de estados en interfaces complejas.
* **Separation of Concerns:** Cómo mantener un proyecto limpio separando la vista de la lógica.

---

*Desarrollado con dedicación por Andres Perez - 2026*
