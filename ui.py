import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from error_reporter import report_error
from lector import capturar_huella, identificar_huella
from database import (
    registrar_socio,
    buscar_por_huella,
    registrar_asistencia,
    obtener_socios,
    buscar_socio_nombre
)
from datetime import datetime
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Vikingo Gym")
        self.geometry("900x520")
        self.resizable(False, False)

        # ---------------- TOP BAR ----------------
        topbar = ctk.CTkFrame(self, height=60)
        topbar.pack(fill="x", side="top")

        titulo = ctk.CTkLabel(topbar, text="Vikingo Gym Control", font=("Arial", 22, "bold"))
        titulo.pack(pady=15)

        # ---------------- MAIN CONTAINER ----------------
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # ---------------- MENU ----------------
        menu = ctk.CTkFrame(container, width=200)
        menu.pack(fill="y", side="left")

        # ---------------- WORK AREA ----------------
        self.workspace = ctk.CTkFrame(container)
        self.workspace.pack(fill="both", expand=True, side="right")

        # ---------------- MARCA DE AGUA ----------------
        try:

            img = Image.open("vkg2.png")

            self.bg_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(350, 350)
            )

            self.bg_label = ctk.CTkLabel(
                self.workspace,
                image=self.bg_img,
                text=""
            )

            # Siempre centrada
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as e:
            print("Error cargando imagen:", e)

        # ---------------- CAPA DE PANTALLAS ----------------
        self.layer_pantallas = ctk.CTkFrame(
            self.workspace,
            fg_color="transparent"
        )

        # Esta capa cubre todo pero es transparente
        self.layer_pantallas.place(relwidth=1, relheight=1)

        # SCREENS
        self.pantallas = {}

        self.crear_inicio()
        self.crear_socios()
        self.crear_accesos()
        self.crear_lista_socios()
        self.crear_panel_socios()

        # MENU
        ctk.CTkButton(menu, text="Inicio",
                    command=lambda: self.mostrar("inicio")).pack(pady=10, padx=10)

        ctk.CTkButton(menu, text="Socios",
                    command=lambda: self.mostrar("socios")).pack(pady=10, padx=10)

        ctk.CTkButton(menu, text="Accesos",
                    command=lambda: self.mostrar("accesos")).pack(pady=10, padx=10)

        ctk.CTkButton(menu, text="Ver Socios",
                    command=lambda: self.mostrar("lista_socios")).pack(pady=10, padx=10)
        
        ctk.CTkButton(
                    menu,
                    text="Panel Socios",
                    command=lambda: self.mostrar("panel_socios")
                ).pack(pady=10,padx=10)

    # ---------------- CAMBIAR PANTALLA ----------------
    def mostrar(self, nombre):

        for p in self.pantallas.values():
            p.place_forget()

        self.pantallas[nombre].place(relwidth=1, relheight=1)

    # ---------------- INICIO ----------------
    def crear_inicio(self):

        inicio = ctk.CTkFrame(self.layer_pantallas, fg_color="transparent")

        lbl = ctk.CTkLabel(
            inicio,
            text="Bienvenido al sistema",
            font=("Arial", 24)
        )

        lbl.pack(expand=True)

        self.pantallas["inicio"] = inicio

    # ---------------- SOCIOS ----------------
    def crear_socios(self):

        socios = ctk.CTkFrame(self.layer_pantallas, fg_color="transparent")

        titulo = ctk.CTkLabel(socios, text="Registro de Socio", font=("Arial", 22))
        titulo.pack(pady=20)

        self.nombre = ctk.CTkEntry(socios, placeholder_text="Nombre completo", width=300)
        self.nombre.pack(pady=5)

        self.telefono = ctk.CTkEntry(socios, placeholder_text="Teléfono", width=300)
        self.telefono.pack(pady=5)

        self.vencimiento = ctk.CTkEntry(
            socios,
            placeholder_text="Fecha vencimiento (YYYY-MM-DD)",
            width=300
        )
        self.vencimiento.pack(pady=5)

        self.estado = ctk.CTkLabel(socios, text="")
        self.estado.pack(pady=10)

        btn_guardar = ctk.CTkButton(
            socios,
            text="Registrar socio",
            command=self.registrar_click
        )
        btn_guardar.pack(pady=20)

        self.pantallas["socios"] = socios

    # ---------------- REGISTRAR SOCIO ----------------
    def registrar_click(self):

        try:

            nombre = self.nombre.get()
            telefono = self.telefono.get()
            venc = self.vencimiento.get()

            if not nombre or not venc:
                self.estado.configure(text="Faltan datos", text_color="red")
                return

            self.estado.configure(text="Coloque la huella...")
            self.update()

            huella = capturar_huella()

            registrar_socio(nombre, telefono, venc, huella)

            self.estado.configure(
                text=f"Socio registrado | ID {huella[:8]}",
                text_color="green"
            )

            self.nombre.delete(0, "end")
            self.telefono.delete(0, "end")
            self.vencimiento.delete(0, "end")

        except Exception as e:
            report_error(e, "ui.py")

    # ---------------- ACCESOS ----------------
    def crear_accesos(self):

        accesos = ctk.CTkFrame(self.layer_pantallas, fg_color="transparent")

        titulo = ctk.CTkLabel(accesos, text="Control de Acceso", font=("Arial", 22))
        titulo.pack(pady=20)

        self.mensaje = ctk.CTkLabel(
            accesos,
            text="Coloque su dedo en el lector",
            font=("Arial", 18)
        )
        self.mensaje.pack(pady=20)

        btn_scan = ctk.CTkButton(
            accesos,
            text="Escanear huella",
            command=self.scan_click,
            height=50,
            width=200
        )
        btn_scan.pack(pady=40)

        self.pantallas["accesos"] = accesos

    # ---------------- ESCANEAR HUELLA ----------------
    def scan_click(self):

        try:

            self.mensaje.configure(text="Escaneando...")
            self.update()

            huella = identificar_huella()

            socio = buscar_por_huella(huella)

            if not socio:
                self.mensaje.configure(text="No registrado", text_color="red")
                return

            venc = datetime.strptime(socio[2], "%Y-%m-%d")

            if venc < datetime.now():
                self.mensaje.configure(
                    text=f"{socio[1]} | Membresía vencida",
                    text_color="orange"
                )
                return

            registrar_asistencia(
                socio[0],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            self.mensaje.configure(
                text=f"Bienvenido {socio[1]}",
                text_color="green"
            )

        except Exception as e:
            report_error(e, "ui.py")

    # ---------------- ERRORES ----------------
    def report_callback_exception(self, exc, val, tb):

        report_error(val, "ui.py")

        print("Error en interfaz:", val)



    def crear_lista_socios(self):

        lista = ctk.CTkFrame(self.layer_pantallas, fg_color="transparent")

        titulo = ctk.CTkLabel(lista, text="Socios Registrados", font=("Arial", 22))
        titulo.pack(pady=10)

        # BUSCADOR
        self.buscar_entry = ctk.CTkEntry(lista, placeholder_text="Buscar socio...")
        self.buscar_entry.pack(pady=5)

        btn_buscar = ctk.CTkButton(
            lista,
            text="Buscar",
            command=self.buscar_socios
        )
        btn_buscar.pack(pady=5)

        btn_actualizar = ctk.CTkButton(
            lista,
            text="Actualizar lista",
            command=self.cargar_socios
        )
        btn_actualizar.pack(pady=5)

        # TABLA
        self.tabla_socios = ctk.CTkTextbox(lista, width=650, height=300)
        self.tabla_socios.pack(pady=15)

        self.pantallas["lista_socios"] = lista

    def cargar_socios(self):

        self.tabla_socios.delete("1.0", "end")

        socios = obtener_socios()

        for s in socios:

            linea = f"""
            ID: {s[0]}
            Nombre: {s[1]}
            Telefono: {s[2]}
            Vence: {s[3]}
            ------------------------------
            """

            self.tabla_socios.insert("end", linea)

    def buscar_socios(self):

        nombre = self.buscar_entry.get()

        self.tabla_socios.delete("1.0", "end")

        socios = buscar_socio_nombre(nombre)

        for s in socios:

            linea = f"""
            ID: {s[0]}
            Nombre: {s[1]}
            Telefono: {s[2]}
            Vence: {s[3]}
            ------------------------------
            """

            self.tabla_socios.insert("end", linea)

    
    def crear_panel_socios(self):

        frame = ctk.CTkFrame(self.layer_pantallas, fg_color="transparent")

        titulo = ctk.CTkLabel(frame, text="Panel de Socios", font=("Arial",22))
        titulo.pack(pady=10)

        # BUSCADOR
        buscador_frame = ctk.CTkFrame(frame)
        buscador_frame.pack(pady=5)

        self.buscar_var = tk.StringVar()

        buscador = ctk.CTkEntry(
            buscador_frame,
            textvariable=self.buscar_var,
            placeholder_text="Buscar socio..."
        )
        buscador.pack(side="left", padx=5)

        ctk.CTkButton(
            buscador_frame,
            text="Buscar",
            command=self.buscar_tabla
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buscador_frame,
            text="Actualizar",
            command=self.cargar_tabla
        ).pack(side="left", padx=5)

        # TABLA
        columnas = ("ID","Nombre","Telefono","Vencimiento")

        self.tree = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(pady=10, fill="x")

        # COLORES
        self.tree.tag_configure("activo", background="#d4edda")
        self.tree.tag_configure("vencido", background="#f8d7da")

        # BOTONES
        botones = ctk.CTkFrame(frame)
        botones.pack(pady=10)

        ctk.CTkButton(
            botones,
            text="Editar",
            command=self.editar_socio
        ).grid(row=0,column=0,padx=5)

        ctk.CTkButton(
            botones,
            text="Eliminar",
            command=self.eliminar_socio
        ).grid(row=0,column=1,padx=5)

        ctk.CTkButton(
            botones,
            text="Socios activos",
            command=self.ver_activos
        ).grid(row=0,column=2,padx=5)

        ctk.CTkButton(
            botones,
            text="Socios vencidos",
            command=self.ver_vencidos
        ).grid(row=0,column=3,padx=5)

        self.contador = ctk.CTkLabel(frame,text="")
        self.contador.pack(pady=5)

        self.pantallas["panel_socios"] = frame


    def cargar_tabla(self):

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        socios = obtener_socios()

        hoy = datetime.now()

        for s in socios:

            venc = datetime.strptime(s[3], "%Y-%m-%d")

            tag = "activo"

            if venc < hoy:
                tag = "vencido"

            self.tree.insert(
                "",
                "end",
                values=s,
                tags=(tag,)
            )

        self.contador.configure(text=f"Total socios: {len(socios)}")

    def buscar_tabla(self):

        texto = self.buscar_var.get().lower()

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        socios = obtener_socios()

        for s in socios:

            if texto in s[1].lower():

                self.tree.insert("", "end", values=s)

    def eliminar_socio(self):

        seleccionado = self.tree.focus()

        if not seleccionado:
            return

        datos = self.tree.item(seleccionado)["values"]

        eliminar_socio(datos[0])

        self.cargar_tabla()

    def editar_socio(self):

        seleccionado = self.tree.focus()

        if not seleccionado:
            return

        datos = self.tree.item(seleccionado)["values"]

        ventana = ctk.CTkToplevel(self)
        ventana.title("Editar socio")
        ventana.geometry("300x250")

        nombre = ctk.CTkEntry(ventana)
        nombre.insert(0,datos[1])
        nombre.pack(pady=5)

        telefono = ctk.CTkEntry(ventana)
        telefono.insert(0,datos[2])
        telefono.pack(pady=5)

        venc = ctk.CTkEntry(ventana)
        venc.insert(0,datos[3])
        venc.pack(pady=5)

        def guardar():

            actualizar_socio(
                datos[0],
                nombre.get(),
                telefono.get(),
                venc.get()
            )

            ventana.destroy()
            self.cargar_tabla()

        ctk.CTkButton(ventana,text="Guardar",command=guardar).pack(pady=10)

    def ver_activos(self):

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        socios = obtener_socios()

        hoy = datetime.now()

        for s in socios:

            venc = datetime.strptime(s[3], "%Y-%m-%d")

            if venc >= hoy:
                self.tree.insert("", "end", values=s, tags=("activo",))

    def ver_vencidos(self):

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        socios = obtener_socios()

        hoy = datetime.now()

        for s in socios:

            venc = datetime.strptime(s[3], "%Y-%m-%d")

            if venc < hoy:
                self.tree.insert("", "end", values=s, tags=("vencido",))