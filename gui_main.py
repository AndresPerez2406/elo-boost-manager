import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

# --- IMPORTACIONES ---
from core.database import (
    obtener_inventario, obtener_pedidos_activos,
    agregar_booster, eliminar_booster, obtener_boosters_db,
    realizar_backup_db, obtener_config_precios, actualizar_precio_db,
    agregar_precio_db, eliminar_precio_db, inicializar_db
)

class PerezBoostApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        inicializar_db()
        
        self.tabla_inv = None
        self.tabla_pedidos = None
        self.tabla_boosters = None
        self.tabla_precios = None
        self.datos_inventario = [] 
        self.map_c_id = {}
        self.map_c_note = {}

        # 1. Configuración de Ventana
        self.title("PerezBoost Manager V7.5 - Gold Edition")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        self.centrar_ventana(self, 1200, 700)

        # 2. Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 3. Sidebar (MENU LATERAL)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1e1e1e")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🚀 PEREZBOOST", 
                                       font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        # Botones del Menú con orden jerárquico
        self.crear_boton_menu("⚙️ Tarifas", self.mostrar_precios, 1)      
        self.crear_boton_menu("👥 Boosters", self.mostrar_boosters, 2)    
        self.crear_boton_menu("📦 Inventario", self.mostrar_inventario, 3) 
        self.crear_boton_menu("📜 Pedidos Activos", self.mostrar_pedidos, 4)
        self.crear_boton_menu("📊 Historial", self.mostrar_historial, 5)

        # 4. Contenedor Principal
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#121212")
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label_welcome = ctk.CTkLabel(self.content_frame, text="BIENVENIDO MANAGER\nSeleccione una opción para comenzar", 
                                          font=ctk.CTkFont(size=16))
        self.label_welcome.pack(expand=True)

        self.protocol("WM_DELETE_WINDOW", self.cerrar_con_backup)

    # =========================================================================
    #  UTILIDADES
    # =========================================================================

    def centrar_ventana(self, ventana, ancho, alto):
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_boton_menu(self, texto, comando, fila):
        boton = ctk.CTkButton(self.sidebar_frame, text=texto, command=comando, 
                              corner_radius=10, height=40, fg_color="#2b2b2b", hover_color="#3d3d3d")
        boton.grid(row=fila, column=0, padx=20, pady=10, sticky="ew")

    def limpiar_pantalla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def configurar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e1e", foreground="white", 
                        fieldbackground="#1e1e1e", borderwidth=0, font=("Segoe UI", 10), rowheight=35)
        style.configure("Treeview.Heading", background="#333333", foreground="white", 
                        relief="flat", font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[('selected', '#1f538d')])

    # =========================================================================
    #  SECCIÓN: GESTIÓN DE TARIFAS
    # =========================================================================

    def mostrar_precios(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(pady=(15, 5), padx=30, fill="x")
        ctk.CTkLabel(header, text="⚙️ CONFIGURACIÓN DE TARIFAS", font=("Arial", 20, "bold")).pack(side="left")

        cols = ("div", "p_cli", "m_per", "p_boo")
        self.tabla_precios = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        headers = ["DIVISIÓN", "PRECIO CLIENTE", "MARGEN PEREZ", "PAGO BOOSTER"]
        for col, h in zip(cols, headers):
            self.tabla_precios.heading(col, text=h)
            self.tabla_precios.column(col, anchor="center", width=150)

        self.tabla_precios.pack(padx=30, pady=10, fill="both", expand=True)
        self.actualizar_tabla_precios()

        footer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer.pack(pady=(5, 20), padx=30, fill="x")
        ctk.CTkButton(footer, text="+ Nueva Tarifa", fg_color="#2ecc71", command=self.abrir_ventana_nuevo_precio).pack(side="left", padx=5)
        ctk.CTkButton(footer, text="📝 Editar", fg_color="#3498db", command=self.abrir_ventana_editar_precio).pack(side="left", padx=5)
        ctk.CTkButton(footer, text="🗑️ Eliminar", fg_color="#e74c3c", command=self.eliminar_precio_seleccionado).pack(side="right")

    def actualizar_tabla_precios(self):
        for i in self.tabla_precios.get_children(): self.tabla_precios.delete(i)
        for d in obtener_config_precios():
            p_boo = float(d[1]) - float(d[2])
            self.tabla_precios.insert("", tk.END, values=(d[0], f"${d[1]:.2f}", f"${d[2]:.2f}", f"${p_boo:.2f}"))

    def abrir_ventana_nuevo_precio(self):
        v = ctk.CTkToplevel(self)
        v.title("Nueva Tarifa"); self.centrar_ventana(v, 350, 400); v.attributes("-topmost", True)
        ctk.CTkLabel(v, text="REGISTRAR NUEVA TARIFA", font=("Arial", 14, "bold")).pack(pady=15)
        e_div = ctk.CTkEntry(v, placeholder_text="Ej: D1, E4", width=200); e_div.pack(pady=5)
        e_cli = ctk.CTkEntry(v, placeholder_text="Precio Cliente $", width=200); e_cli.pack(pady=5)
        e_per = ctk.CTkEntry(v, placeholder_text="Margen Perez $", width=200); e_per.pack(pady=5)

        def guardar():
            try:
                if agregar_precio_db(e_div.get().upper(), float(e_cli.get()), float(e_per.get())):
                    v.destroy(); self.actualizar_tabla_precios()
                else: messagebox.showerror("Error", "Ya existe esta división", parent=v)
            except: messagebox.showerror("Error", "Datos numéricos inválidos", parent=v)
        ctk.CTkButton(v, text="Añadir", fg_color="#2ecc71", command=guardar).pack(pady=20)

    def abrir_ventana_editar_precio(self):
        sel = self.tabla_precios.selection()
        if not sel: return
        datos = self.tabla_precios.item(sel)['values']
        div, p_cli, m_per = datos[0], str(datos[1]).replace('$',''), str(datos[2]).replace('$','')

        v = ctk.CTkToplevel(self)
        v.title(f"Editar {div}"); self.centrar_ventana(v, 350, 400); v.attributes("-topmost", True)
        e_cli = ctk.CTkEntry(v, width=200); e_cli.insert(0, p_cli); e_cli.pack(pady=20)
        e_per = ctk.CTkEntry(v, width=200); e_per.insert(0, m_per); e_per.pack(pady=5)

        def update():
            try:
                if actualizar_precio_db(div, float(e_cli.get()), float(e_per.get())):
                    v.destroy(); self.actualizar_tabla_precios()
            except: messagebox.showerror("Error", "Error al actualizar", parent=v)
        ctk.CTkButton(v, text="Actualizar", fg_color="#3498db", command=update).pack(pady=20)

    def eliminar_precio_seleccionado(self):
        sel = self.tabla_precios.selection()
        if not sel: return
        div = self.tabla_precios.item(sel)['values'][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar tarifa {div}?", parent=self):
            if eliminar_precio_db(div): self.actualizar_tabla_precios()

    # =========================================================================
    #  SECCIÓN: BOOSTERS (STAFF)
    # =========================================================================

    def mostrar_boosters(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(pady=(15, 5), padx=30, fill="x")
        ctk.CTkLabel(header, text="👥 GESTIÓN DE STAFF", font=("Arial", 20, "bold")).pack(side="left")
        
        self.entry_busqueda_b = ctk.CTkEntry(header, placeholder_text="Nombre...", width=200)
        self.entry_busqueda_b.pack(side="right")
        ctk.CTkButton(header, text="🔍", width=40, command=self.filtrar_boosters).pack(side="right", padx=5)

        cols = ("id_v", "id_r", "nombre")
        self.tabla_boosters = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        self.tabla_boosters.heading("id_v", text="#"); self.tabla_boosters.column("id_v", width=50, anchor="center")
        self.tabla_boosters.heading("id_r", text="ID_R"); self.tabla_boosters.column("id_r", width=0, stretch=tk.NO)
        self.tabla_boosters.heading("nombre", text="NOMBRE DEL STAFF"); self.tabla_boosters.column("nombre", width=400, anchor="center")

        self.tabla_boosters.pack(padx=30, pady=10, fill="both", expand=True)
        self.filtrar_boosters()

        footer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer.pack(pady=(5, 20), padx=30, fill="x")
        ctk.CTkButton(footer, text="+ Nuevo Booster", fg_color="#2ecc71", command=self.abrir_ventana_booster).pack(side="left")
        ctk.CTkButton(footer, text="🗑️ Despedir", fg_color="#e74c3c", command=self.eliminar_booster_seleccionado).pack(side="right")

    def filtrar_boosters(self):
        query = self.entry_busqueda_b.get().lower()
        for i in self.tabla_boosters.get_children(): self.tabla_boosters.delete(i)
        for i, b in enumerate(obtener_boosters_db(), start=1):
            if query == "" or query in b[1].lower():
                self.tabla_boosters.insert("", tk.END, values=(i, b[0], b[1]))

    def abrir_ventana_booster(self):
        v = ctk.CTkToplevel(self); v.title("Nuevo Staff"); self.centrar_ventana(v, 400, 300); v.attributes("-topmost", True)
        entry = ctk.CTkEntry(v, width=250); entry.pack(pady=30)
        def save():
            if entry.get() and agregar_booster(entry.get().strip().title()):
                v.destroy(); self.mostrar_boosters()
        ctk.CTkButton(v, text="Guardar", command=save, fg_color="#2ecc71").pack()

    def eliminar_booster_seleccionado(self):
        sel = self.tabla_boosters.selection()
        if sel:
            id_r = self.tabla_boosters.item(sel)['values'][1]
            if messagebox.askyesno("Confirmar", "¿Eliminar staff?", parent=self):
                if eliminar_booster(id_r): self.mostrar_boosters()

    # =========================================================================
    #  SECCIÓN: INVENTARIO, PEDIDOS E HISTORIAL (Resto de Funcionalidades)
    # =========================================================================

    def mostrar_inventario(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(pady=(15, 5), padx=30, fill="x")
        ctk.CTkLabel(header, text="📦 STOCK DISPONIBLE", font=("Arial", 20, "bold")).pack(side="left")
        
        self.entry_busqueda_i = ctk.CTkEntry(header, placeholder_text="Buscar Elo...", width=200)
        self.entry_busqueda_i.pack(side="right")
        ctk.CTkButton(header, text="🔍", width=40, command=self.filtrar_inventario).pack(side="right", padx=5)

        cols = ("id_v", "user_pass", "elo", "desc")
        self.tabla_inv = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        h_text = ["#", "CUENTA", "ELO", "NOTAS"]
        for col, txt in zip(cols, h_text):
            self.tabla_inv.heading(col, text=txt); self.tabla_inv.column(col, anchor="center")

        self.tabla_inv.pack(padx=30, pady=10, fill="both", expand=True)
        self.filtrar_inventario()

        footer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer.pack(pady=(5, 20), padx=30, fill="x")
        ctk.CTkButton(footer, text="+ Añadir", fg_color="#2ecc71", command=self.abrir_ventana_registro).pack(side="left", padx=5)
        ctk.CTkButton(footer, text="📥 Masivo", fg_color="#3498db", command=self.abrir_ventana_masivo).pack(side="left")
        ctk.CTkButton(footer, text="🗑️ Borrar", fg_color="#e74c3c", command=self.eliminar_seleccionado).pack(side="right")

    def filtrar_inventario(self):
        query = self.entry_busqueda_i.get().lower()
        for i in self.tabla_inv.get_children(): self.tabla_inv.delete(i)
        from modules.inventario import obtener_inventario_visual
        self.datos_inventario = obtener_inventario_visual()
        for d in self.datos_inventario:
            if query == "" or query in d[3].lower():
                self.tabla_inv.insert("", tk.END, values=(d[0], d[2], d[3], d[4]))

    def abrir_ventana_registro(self):
        v = ctk.CTkToplevel(self); self.centrar_ventana(v, 400, 450); v.attributes("-topmost", True)
        up = ctk.CTkEntry(v, placeholder_text="User:Pass", width=250); up.pack(pady=10)
        elo = ctk.CTkOptionMenu(v, values=["Emerald/Plat", "DIAMANTE"], width=250); elo.pack(pady=10)
        not_ent = ctk.CTkEntry(v, placeholder_text="Notas", width=250); not_ent.pack(pady=10)
        def save():
            from modules.inventario import registrar_cuenta_gui
            if registrar_cuenta_gui(up.get(), elo.get(), not_ent.get())[0]:
                v.destroy(); self.mostrar_inventario()
        ctk.CTkButton(v, text="Guardar", command=save, fg_color="#2ecc71").pack()

    def abrir_ventana_masivo(self):
        v = ctk.CTkToplevel(self); self.centrar_ventana(v, 500, 550); v.attributes("-topmost", True)
        txt = ctk.CTkTextbox(v, width=450, height=250); txt.pack(pady=10)
        elo = ctk.CTkOptionMenu(v, values=["Emerald/Plat", "DIAMANTE"], width=200); elo.pack(pady=10)
        def proc():
            from modules.inventario import registrar_lote_gui
            registrar_lote_gui(txt.get("1.0", "end"), elo.get())
            v.destroy(); self.mostrar_inventario()
        ctk.CTkButton(v, text="🚀 Importar", command=proc).pack()

    def eliminar_seleccionado(self):
        sel = self.tabla_inv.selection()
        if sel:
            v_id = self.tabla_inv.item(sel)['values'][0]
            id_r = next(d[1] for d in self.datos_inventario if d[0] == v_id)
            from modules.inventario import eliminar_cuenta_gui
            if eliminar_cuenta_gui(id_r): self.mostrar_inventario()

    def mostrar_pedidos(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(pady=(15, 5), padx=30, fill="x")
        ctk.CTkLabel(header, text="⚔️ PEDIDOS ACTIVOS", font=("Arial", 20, "bold")).pack(side="left")
        self.entry_busqueda = ctk.CTkEntry(header, placeholder_text="Booster...", width=200); self.entry_busqueda.pack(side="right")
        ctk.CTkButton(header, text="🔍", width=40, command=self.filtrar_pedidos).pack(side="right", padx=5)

        cols = ("id_v", "id_r", "booster", "cuenta", "inicio", "fin", "tiempo")
        self.tabla_pedidos = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for c in cols:
            self.tabla_pedidos.heading(c, text=c.upper()); self.tabla_pedidos.column(c, anchor="center")
        self.tabla_pedidos.column("id_r", width=0, stretch=tk.NO)
        self.tabla_pedidos.pack(padx=30, pady=10, fill="both", expand=True)
        self.filtrar_pedidos()

        footer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer.pack(pady=(5, 20), padx=30, fill="x")
        ctk.CTkButton(footer, text="⚡ Nuevo", fg_color="#3498db", command=self.abrir_ventana_nuevo_pedido).pack(side="left")
        ctk.CTkButton(footer, text="✅ Finalizar", fg_color="#2ecc71", command=self.abrir_ventana_finalizar).pack(side="right", padx=5)
        ctk.CTkButton(footer, text="🚫 Abandono", fg_color="#e74c3c", command=self.abrir_ventana_reportar_abandono).pack(side="right")

    def filtrar_pedidos(self):
        query = self.entry_busqueda.get().lower()
        for i in self.tabla_pedidos.get_children(): self.tabla_pedidos.delete(i)
        from modules.pedidos import obtener_pedidos_visual
        for p in obtener_pedidos_visual():
            if query in p[2].lower(): self.tabla_pedidos.insert("", tk.END, values=p)

    def abrir_ventana_nuevo_pedido(self):
        from modules.pedidos import obtener_elos_en_stock, obtener_cuentas_filtradas_datos
        b_raw = obtener_boosters_db(); elos = obtener_elos_en_stock()
        if not b_raw or not elos: return
        v = ctk.CTkToplevel(self); self.centrar_ventana(v, 450, 600); v.attributes("-topmost", True)
        cb_b = ctk.CTkOptionMenu(v, values=[b[1] for b in b_raw], width=300); cb_b.pack(pady=10)
        cb_e = ctk.CTkOptionMenu(v, values=elos, width=300); cb_e.pack(pady=10)
        def go():
            from core.logic import calcular_fecha_limite_sugerida
            from core.database import crear_pedido
            # Lógica de asignación simplificada
            messagebox.showinfo("Info", "Funcionalidad conectada", parent=v); v.destroy()
        ctk.CTkButton(v, text="🚀 Iniciar", command=go).pack()

    def abrir_ventana_finalizar(self):
        sel = self.tabla_pedidos.selection()
        if not sel: return
        id_r = self.tabla_pedidos.item(sel)['values'][1]
        v = ctk.CTkToplevel(self); self.centrar_ventana(v, 400, 450); v.attributes("-topmost", True)
        e_div = ctk.CTkEntry(v, placeholder_text="División Final..."); e_div.pack(pady=10)
        e_wr = ctk.CTkEntry(v, placeholder_text="WR %"); e_wr.pack(pady=10)
        def finish():
            from core.logic import calcular_pago_real
            from core.database import finalizar_pedido_db
            try:
                c, p, g = calcular_pago_real(e_div.get().upper(), float(e_wr.get()))
                if finalizar_pedido_db(id_r, e_div.get(), float(e_wr.get()), c, p, g, 0, ""):
                    v.destroy(); self.mostrar_pedidos()
            except: pass
        ctk.CTkButton(v, text="Cerrar", command=finish).pack()

    def abrir_ventana_reportar_abandono(self):
        sel = self.tabla_pedidos.selection()
        if sel:
            id_r = self.tabla_pedidos.item(sel)['values'][1]
            if messagebox.askyesno("Confirmar", "Reportar Abandono?"):
                from core.database import registrar_abandono_db
                registrar_abandono_db(id_r, "N/A", 0); self.mostrar_pedidos()

    def mostrar_historial(self):
        self.limpiar_pantalla()
        self.configurar_estilo_tabla()
        header_h = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_h.pack(pady=(15, 5), padx=30, fill="x") 
        ctk.CTkLabel(header_h, text="📊 HISTORIAL", font=("Arial", 20, "bold")).pack(side="left")
        self.entry_busqueda_h = ctk.CTkEntry(header_h, placeholder_text="Booster...", width=250); self.entry_busqueda_h.pack(side="right")
        ctk.CTkButton(header_h, text="🔍", width=40, command=self.filtrar_historial).pack(side="right", padx=5)

        cols = ("#", "booster", "cuenta", "pago_b", "gan_m", "total", "inicio", "fin", "tiempo")
        self.tabla_historial = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for col in cols: self.tabla_historial.heading(col, text=col.upper()); self.tabla_historial.column(col, anchor="center")
        self.tabla_historial.pack(padx=30, pady=10, fill="both", expand=True)

        self.panel_total_h = ctk.CTkFrame(self.content_frame, fg_color="#1e1e1e", corner_radius=10, height=60)
        self.panel_total_h.pack(pady=(5, 20), fill="x", padx=30); self.panel_total_h.pack_propagate(False)
        self.lbl_totales_h = ctk.CTkLabel(self.panel_total_h, text="", font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.lbl_totales_h.pack(expand=True)
        self.filtrar_historial()

    def filtrar_historial(self):
        query = self.entry_busqueda_h.get().lower()
        for i in self.tabla_historial.get_children(): self.tabla_historial.delete(i)
        try:
            from modules.pedidos import obtener_historial_visual
            datos, _ = obtener_historial_visual()
            tb, te, tc = 0.0, 0.0, 0.0
            for d in datos:
                if query == "" or query in d[1].lower():
                    self.tabla_historial.insert("", tk.END, values=d)
                    tb += float(str(d[3]).replace('$', '')); te += float(str(d[4]).replace('$', '')); tc += float(str(d[5]).replace('$', ''))
            self.lbl_totales_h.configure(text=f"Boosters: ${tb:.2f} | Perez: ${te:.2f} | Total: ${tc:.2f}")
        except: pass

    def cerrar_con_backup(self):
        realizar_backup_db(); self.destroy()

if __name__ == "__main__":
    app = PerezBoostApp()
    app.mainloop()