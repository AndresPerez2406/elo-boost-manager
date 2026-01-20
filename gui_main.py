import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
# Importamos tu lógica
from core.database import obtener_inventario, obtener_pedidos_activos

class PerezBoostApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de Ventana
        self.title("PerezBoost Manager V7 - Pro Edition")
        self.geometry("1150x650") # Un poco más ancho para el historial financiero
        ctk.set_appearance_mode("dark")

        # 2. Layout (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 3. Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1e1e1e")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🚀 PEREZBOOST", 
                                       font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        # BOTONES DEL MENÚ
        self.btn_stock = self.crear_boton_menu("📦 Inventario", self.mostrar_inventario, 1)
        self.btn_activos = self.crear_boton_menu("📜 Pedidos Activos", self.mostrar_pedidos, 2)
        # Agregado correctamente dentro del __init__
        self.btn_historial = self.crear_boton_menu("📊 Historial", self.mostrar_historial, 3)

        # 4. Contenedor de Contenido Principal
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#121212")
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Mensaje de Bienvenida inicial
        self.label_welcome = ctk.CTkLabel(self.content_frame, text="BIENVENIDO MANAGER\nSeleccione una opción para comenzar", 
                                          font=ctk.CTkFont(size=16))
        self.label_welcome.pack(expand=True)

    # --- UTILIDADES DE INTERFAZ ---
    def crear_boton_menu(self, texto, comando, fila):
        boton = ctk.CTkButton(self.sidebar_frame, text=texto, command=comando, 
                              corner_radius=10, height=40, fg_color="#2b2b2b", hover_color="#3d3d3d")
        boton.grid(row=fila, column=0, padx=20, pady=10, sticky="ew")
        return boton

    def limpiar_pantalla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def configurar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#1e1e1e", 
                        foreground="white", 
                        fieldbackground="#1e1e1e", 
                        borderwidth=0, 
                        font=("Segoe UI", 10),
                        rowheight=35) # Filas un poco más altas para legibilidad
        style.configure("Treeview.Heading", 
                        background="#333333", 
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[('selected', '#1f538d')])

    # --- VISTAS (MÉTODOS) ---

    def mostrar_inventario(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        
        titulo = ctk.CTkLabel(self.content_frame, text="📦 STOCK DE CUENTAS", 
                              font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=20)

        cols = ("id_visual", "user_pass", "elo_tipo", "descripcion")
        tabla = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        
        tabla.heading("id_visual", text="#") 
        tabla.heading("user_pass", text="CUENTA")
        tabla.heading("elo_tipo", text="CATEGORÍA")
        tabla.heading("descripcion", text="NOTAS")

        tabla.column("id_visual", width=50, anchor="center")
        tabla.column("user_pass", width=200)
        tabla.column("elo_tipo", width=150)
        tabla.column("descripcion", width=400)

        try:
            from modules.inventario import obtener_inventario_visual
            cuentas = obtener_inventario_visual()
            for v_id, r_id, user, elo, desc in cuentas:
                tabla.insert("", tk.END, values=(v_id, user, elo, desc))
        except Exception as e:
            print(f"Error al cargar inventario: {e}")

        tabla.pack(padx=30, pady=10, fill="both", expand=True)

    def mostrar_pedidos(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        
        titulo = ctk.CTkLabel(self.content_frame, text="📜 PEDIDOS ACTIVOS ACTUALMENTE", 
                              font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=20)

        cols = ("id_visual", "booster", "cuenta", "inicio", "fin", "tiempo")
        tabla = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        
        tabla.heading("id_visual", text="#")
        tabla.heading("booster", text="BOOSTER")
        tabla.heading("cuenta", text="CUENTA")
        tabla.heading("inicio", text="INICIO")
        tabla.heading("fin", text="DEADLINE")
        tabla.heading("tiempo", text="TIEMPO ACTIVO")

        tabla.column("id_visual", width=40, anchor="center")
        tabla.column("booster", width=120, anchor="center")
        tabla.column("cuenta", width=180, anchor="w")
        tabla.column("inicio", width=140, anchor="center")
        tabla.column("fin", width=140, anchor="center")
        tabla.column("tiempo", width=120, anchor="center")

        try:
            from modules.pedidos import obtener_pedidos_visual
            pedidos_gui = obtener_pedidos_visual()
            for v_id, r_id, b, c, ini, fin, t in pedidos_gui:
                tabla.insert("", tk.END, values=(v_id, b, c, ini, fin, t))
        except Exception as e:
            print(f"Error al cargar pedidos: {e}")

        tabla.pack(padx=30, pady=10, fill="both", expand=True)

    def mostrar_historial(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        
        titulo = ctk.CTkLabel(self.content_frame, text="💰 BALANCE FINANCIERO Y RENDIMIENTO", 
                              font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=20)

        cols = ("#", "booster", "cuenta", "pago_b", "gan_m", "total", "inicio", "fin", "tiempo")
        tabla = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        
        headers = ["#", "BOOSTER", "CUENTA/ELO", "PAGO B.", "MI GAN.", "CLIENTE", "INICIO", "ENTREGA", "TIEMPO"]
        for col, head in zip(cols, headers):
            tabla.heading(col, text=head)
            tabla.column(col, anchor="center", width=100)
        
        tabla.column("#", width=40)
        tabla.column("booster", width=120)

        try:
            from modules.pedidos import obtener_historial_visual
            datos, totales = obtener_historial_visual()
            
            for d in datos:
                tabla.insert("", tk.END, values=d)
            
            # --- PANEL DE TOTALES (EL BOX DE ABAJO) ---
            panel_resumen = ctk.CTkFrame(self.content_frame, fg_color="#1e1e1e", corner_radius=10)
            panel_resumen.pack(pady=20, padx=20, fill="x")
            
            texto_totales = (f"PAGADO A BOOSTERS: ${totales['booster']:.2f}    |    "
                             f"MI GANANCIA NETA: ${totales['empresa']:.2f}    |    "
                             f"TOTAL GENERADO: ${totales['cliente']:.2f}")
            
            lbl_resumen = ctk.CTkLabel(panel_resumen, text=texto_totales, 
                                       font=ctk.CTkFont(size=14, weight="bold"), 
                                       text_color="#2ecc71")
            lbl_resumen.pack(pady=10)

        except Exception as e:
            print(f"Error al cargar historial en GUI: {e}")

        tabla.pack(padx=20, pady=10, fill="both", expand=True)

if __name__ == "__main__":
    app = PerezBoostApp()
    app.mainloop()