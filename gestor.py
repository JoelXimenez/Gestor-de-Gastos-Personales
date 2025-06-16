import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class GestorGastosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Gastos Personales")
        self.geometry("870x500")
        self.configure(fg_color="white")
        self.resizable(False, False)

        self.gastos = []
        self.archivo_json = "gastos.json"
        self.cargar_gastos()

        self.linea_a_indice = {}
        self.linea_seleccionada = None
        self.linea_visual_seleccionada = None

        ctk.CTkLabel(self, text="💰 Registro de Gastos", font=("Arial Rounded MT Bold", 24), text_color="#333333").pack(pady=10)

        # ----------------------------- INPUTS -----------------------------
        ctk.CTkLabel(self, text="Categoría", anchor="w").pack()
        self.categorias = ["Universidad", "Personal", "Otros"]
        self.combo_categoria = ctk.CTkOptionMenu(self, values=self.categorias, width=300)
        self.combo_categoria.set("Universidad")
        self.combo_categoria.pack(pady=3)

        ctk.CTkLabel(self, text="Razón del gasto", anchor="w").pack()
        self.entry_subcategoria = ctk.CTkEntry(self, placeholder_text="Ej: Comida, Transporte...", width=300)
        self.entry_subcategoria.pack(pady=3)

        ctk.CTkLabel(self, text="Monto en USD", anchor="w").pack()
        self.entry_monto = ctk.CTkEntry(self, placeholder_text="Ej: 12.50", width=300)
        self.entry_monto.pack(pady=5)

        # ----------------------------- BOTONES -----------------------------
        frame_botones = ctk.CTkFrame(self, fg_color="#f2f2f2")
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="Registrar Gasto", command=self.registrar_gasto, width=160).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="Eliminar Seleccionado", command=self.eliminar_gasto, fg_color="#ff4d4d", width=200).grid(row=0, column=1, padx=10)

        # ----------------------------- FILTROS -----------------------------
        filtro_frame = ctk.CTkFrame(self, fg_color="white")
        filtro_frame.pack(pady=10)

        ctk.CTkLabel(filtro_frame, text="Categoría", anchor="w").grid(row=0, column=0, padx=5)
        self.combo_filtro = ctk.CTkOptionMenu(filtro_frame, values=["Todas"] + self.categorias, command=self.filtrar_gastos, width=160)
        self.combo_filtro.set("Todas")
        self.combo_filtro.grid(row=1, column=0, padx=5)

        ctk.CTkLabel(filtro_frame, text="Razón contiene", anchor="w").grid(row=0, column=1, padx=5)
        self.entry_buscar = ctk.CTkEntry(filtro_frame, placeholder_text="Buscar", width=180)
        self.entry_buscar.grid(row=1, column=1, padx=5)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.filtrar_gastos())

        ctk.CTkLabel(filtro_frame, text="Fecha (mes-año)", anchor="w").grid(row=0, column=2, padx=5)
        self.meses = self.generar_lista_meses()
        self.combo_mes = ctk.CTkOptionMenu(filtro_frame, values=["Todas"] + self.meses, command=self.filtrar_gastos, width=140)
        self.combo_mes.set("Todas")
        self.combo_mes.grid(row=1, column=2, padx=5)

        # ----------------------------- LISTA GASTOS -----------------------------
        self.texto_gastos = ctk.CTkTextbox(self, width=800, height=320, font=("Consolas", 13), text_color="#222222")
        self.texto_gastos.pack(pady=10)
        self.texto_gastos.bind("<Button-1>", self.guardar_linea_seleccionada)

        self.mostrar_gastos()

    def generar_lista_meses(self):
        desde = datetime(2025, 1, 1)
        hoy = datetime.now()
        meses = []

        while desde <= hoy:
            meses.append(desde.strftime("%m-%Y"))
            if desde.month == 12:
                desde = datetime(desde.year + 1, 1, 1)
            else:
                desde = datetime(desde.year, desde.month + 1, 1)

        return meses

    def registrar_gasto(self):
        categoria = self.combo_categoria.get()
        subcategoria = self.entry_subcategoria.get().strip()
        monto_str = self.entry_monto.get().strip()

        if not subcategoria or not monto_str:
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
            return

        try:
            monto = float(monto_str)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        gasto = {
            "categoria": categoria,
            "subcategoria": subcategoria,
            "monto": monto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.gastos.append(gasto)
        self.guardar_gastos()
        self.mostrar_gastos()

        self.entry_subcategoria.delete(0, 'end')
        self.entry_monto.delete(0, 'end')

    def mostrar_gastos(self, gastos_filtrados=None):
        self.texto_gastos.delete("1.0", "end")
        self.linea_a_indice.clear()
        self.linea_visual_seleccionada = None

        total = 0
        gastos = gastos_filtrados if gastos_filtrados is not None else self.gastos

        for i, gasto in enumerate(gastos):
            fecha = gasto.get('fecha', 'Sin fecha')
            linea = f"{fecha} | {gasto['categoria']} > {gasto['subcategoria']}: ${gasto['monto']:.2f}\n"
            index_inicio = self.texto_gastos.index("end-1c")
            self.texto_gastos.insert("end", linea)
            index_linea = int(float(index_inicio))
            self.linea_a_indice[index_linea] = self.gastos.index(gasto)
            total += gasto['monto']

        self.texto_gastos.insert("end", f"\n🔸 Total gastado: ${total:.2f}")

    def guardar_gastos(self):
        with open(self.archivo_json, 'w') as f:
            json.dump(self.gastos, f, indent=4)

    def cargar_gastos(self):
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, 'r') as f:
                    contenido = f.read().strip()
                    self.gastos = json.loads(contenido) if contenido else []
                    for gasto in self.gastos:
                        if 'fecha' not in gasto:
                            gasto['fecha'] = 'Sin fecha'
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo de gastos está corrupto. Se reiniciará.")
                self.gastos = []
        else:
            self.gastos = []

    def filtrar_gastos(self, *_):
        categoria = self.combo_filtro.get()
        busqueda = self.entry_buscar.get().lower()
        mes_anio = self.combo_mes.get()

        filtrados = []
        for g in self.gastos:
            cumple_categoria = (categoria == "Todas" or g["categoria"] == categoria)
            cumple_razon = busqueda in g["subcategoria"].lower()

            if mes_anio != "Todas":
                try:
                    fecha_gasto = datetime.strptime(g["fecha"], "%Y-%m-%d %H:%M:%S")
                    cumple_fecha = fecha_gasto.strftime("%m-%Y") == mes_anio
                except:
                    cumple_fecha = False
            else:
                cumple_fecha = True

            if cumple_categoria and cumple_razon and cumple_fecha:
                filtrados.append(g)

        self.mostrar_gastos(filtrados)

    def guardar_linea_seleccionada(self, event):
        index = self.texto_gastos.index(f"@{event.x},{event.y}")
        linea = int(float(index))
        self.linea_seleccionada = self.linea_a_indice.get(linea)

        # Resalta visualmente la línea
        self.texto_gastos.tag_remove("seleccionado", "1.0", "end")
        self.texto_gastos.tag_config("seleccionado", background="#cceeff")
        self.texto_gastos.tag_add("seleccionado", f"{linea}.0", f"{linea}.end")

    def eliminar_gasto(self):
        idx = self.linea_seleccionada
        if idx is None or idx >= len(self.gastos):
            messagebox.showinfo("Selecciona un gasto", "Haz clic sobre la línea del gasto que quieras eliminar.")
            return

        gasto = self.gastos[idx]
        texto = f"{gasto['fecha']} | {gasto['categoria']} > {gasto['subcategoria']}: ${gasto['monto']:.2f}"
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar este gasto?\n\n{texto}")
        if confirm:
            del self.gastos[idx]
            self.linea_seleccionada = None
            self.guardar_gastos()
            self.mostrar_gastos()


if __name__ == "__main__":
    app = GestorGastosApp()
    app.mainloop()
