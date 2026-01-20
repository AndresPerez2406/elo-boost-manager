# PerezBoost Manager V6 (SQL Edition) ⚔️

**A professional, SQL-driven management system specifically designed to streamline digital service operations (Elo Boosting), automate complex order tracking, and ensure financial integrity.**

> *"Moving from manual text files to a robust relational architecture."*

---

---

## 🖼️ Preview (V7 GUI Prototype Coming Soon)

**`<div align="center">`**
  **`<img src="preview_v7.png" alt="Prototipo GUI V7" width="800">`**
  **`<p>`**`<em>`Imagen representativa del concepto de interfaz gráfica moderna (Dark Mode) planeada para la versión V7.**`</em>`**`</p>`
**`</div>`**

---

## 🚀 Business Problem Solved

Running a high-volume boosting service manually via spreadsheets or chats leads to operational bottlenecks, lost accounts, and financial tracking errors. **PerezBoost Manager v6** centralizes the core business logic into a robust environment:

- **Automated Order Lifecycle:** Tracking from assignment to final closure with time stamping.
- **Smart Inventory Control:** Categorized account management. The system intelligently handles abandoned orders, restoring the account's original category while logging the specific details in the notes.
- **Financial Integrity:** Automatic calculation of client fees, booster payouts, and net profit based on division rules and winrates.

## 🛠️ Technical Stack & Architecture (V6)

The system moved from a legacy script to a professional modular architecture.

- **Language:** Python 3.x
- **Database:** SQLite3 (Relational Database Management) - No more flat text files.
- **Architecture:** **Modular MVC-lite**. Separated into:
  - `core/`: Database engine and reliable business logic (the "Brain").
  - `modules/`: Functional interfaces for Boosters, Inventory, and Orders.

## 📜 Version History & Changelog

### **V6.0: The SQL Migration & Modularity (Current Stable)**

*Major architectural overhaul focused on data integrity and scalability.*

- **[FEAT] SQL Persistence:** Migrated all data persistence from `.txt` files to a structured **SQLite database**.
- **[REFACTOR] Modular Structure:** Split the monolithic `main.py` into dedicated modules (`boosters.py`, `inventario.py`, `pedidos.py`) supported by a robust `core/` engine.
- **[LOGIC] Abandonment Protocol v2:** Implemented smart logic that restores an abandoned account to its original inventory category but logs current rank/WR in the description field.
- **[UX] Robust Inputs:** Standardized all user inputs to prevent crashes due to trailing spaces or incorrect formats.
- **[FEAT] Financial Reporting:** Added detailed breakdown of costs and profits upon order completion.

### **V5.0: Legacy Prototype (Deprecated)**

*Initial proof of concept.*

- Basic CLI menu system.
- Simple CRUD operations using flat text files for storage.
- *Limitations:* Prone to data corruption, no complex business rules, hard to maintain.

---

## 🔮 Roadmap: Towards V7 (In Development)

**The next major milestone focuses on User Experience (UX), transitioning from the terminal to a modern desktop interface.**

| Status                  | Feature                     | Description                                                                                             |
| :---------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------ |
| 🔄**In Progress** | **Modern GUI**        | Implementing a graphical user interface using**CustomTkinter** for a modern, dark-mode aesthetic. |
| 📝 Planned              | **Visual Dashboards** | Replacing text lists with interactive tables for easier sorting and viewing of active orders.           |
| 📝 Planned              | **Automated Backups** | (V7.1) System to automatically rotate `.db` backups on startup for data safety.                       |
| 📝 Planned              | **Visual Analytics**  | (V7.2) Charts showing monthly profits and top performing boosters.                                      |

---

## 📁 Project Structure (V6)

```text
├── main.py              # Entry point / Menu Orchestrator
├── core/                # THE ENGINE
│   ├── database.py      # SQL Connections, Queries & Transactions
│   └── logic.py         # Pure Business Logic (Calculations, Date formatting)
├── modules/             # THE INTERFACES
│   ├── boosters.py      # Staff management menus
│   ├── inventario.py    # Account stock management menus
│   └── pedidos.py       # Order lifecycle menus
└── perezboost.db        # SQLite Database (Auto-generated)
```

## 🔧 Installation & Usage

1. **Clone the repository:**
   **Bash**

   ```
   git clone [https://github.com/AndresPerez2406/elo-boost-manager.git](https://github.com/AndresPerez2406/elo-boost-manager.git)
   cd elo-boost-manager
   ```
2. **Run the application:**
   **Bash**

   ```
   python main.py
   ```

   *(The system will automatically create `perezboost.db` and the necessary tables on the first run.)*

---

*Developed by Andres Perez - 2026*
