# Versión final del programa con tipos de producto predefinidos y comentarios explicativos

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import csv
import os

# ---------------------------
# Nodo de la lista enlazada
# ---------------------------
class NodoCaja:
    def __init__(self, id_caja, tiene_codigo, tipo, estado):
        self.id_caja = id_caja
        self.tiene_codigo = tiene_codigo
        self.tipo = tipo
        self.estado = estado
        self.siguiente = None

# ---------------------------
# Lista enlazada por categoría
# ---------------------------
class ListaCajas:
    def __init__(self):
        self.inicio = None

    def agregar_caja(self, id_caja, tiene_codigo, tipo, estado):
        nueva = NodoCaja(id_caja, tiene_codigo, tipo, estado)
        if not self.inicio:
            self.inicio = nueva
        else:
            temp = self.inicio
            while temp.siguiente:
                temp = temp.siguiente
            temp.siguiente = nueva
        return True

    def eliminar_caja(self, id_caja):
        temp = self.inicio
        anterior = None
        while temp:
            if temp.id_caja == id_caja:
                if anterior:
                    anterior.siguiente = temp.siguiente
                else:
                    self.inicio = temp.siguiente
                return True
            anterior = temp
            temp = temp.siguiente
        return False

    def buscar_caja(self, id_caja):
        temp = self.inicio
        while temp:
            if temp.id_caja == id_caja:
                return temp
            temp = temp.siguiente
        return None

    def obtener_todas(self):
        cajas = []
        temp = self.inicio
        while temp:
            cajas.append(temp)
            temp = temp.siguiente
        return cajas

    def mostrar_cajas(self):
        return [f"[{caja.estado}] {caja.tipo} | ID: {caja.id_caja} | Código: {'Sí' if caja.tiene_codigo else 'No'}" for caja in self.obtener_todas()]

# ---------------------------
# Variables globales
# ---------------------------
almacen = {}
ids_usados = set()
tipos_permitidos = ["Desktop", "Laptop", "Impresora", "Celular", "Televisor"]
estados = ["Nuevo", "Usado"]

def generar_clave(tipo, estado):
    return f"{estado.lower()}_{tipo.lower()}"

def guardar_ids_en_archivo():
    with open("ids_usados.txt", "w") as f:
        for id_ in sorted(ids_usados):
            f.write(id_ + "\n")

def cargar_ids_desde_archivo():
    if os.path.exists("ids_usados.txt"):
        with open("ids_usados.txt", "r") as f:
            for line in f:
                ids_usados.add(line.strip())

def inicializar_almacen():
    for tipo in tipos_permitidos:
        for estado in estados:
            clave = generar_clave(tipo, estado)
            almacen[clave] = ListaCajas()

# ---------------------------
# Interfaz gráfica
# ---------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Gestión de Cajas Tecnológicas")
        root.configure(bg="#f0f0f0")
        root.geometry("700x600")

        # Título
        tk.Label(root, text="GESTIÓN DE CAJAS", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=10)

        # Campo ID
        self.crear_campo("ID Caja:", "entry_id")

        # Menú desplegable para tipo de producto
        tk.Label(root, text="Tipo de Producto:", bg="#f0f0f0").pack()
        self.tipo_var = tk.StringVar(value=tipos_permitidos[0])
        tk.OptionMenu(root, self.tipo_var, *tipos_permitidos).pack(pady=3)

        # Estado (Nuevo o Usado)
        tk.Label(root, text="Estado:", bg="#f0f0f0").pack()
        self.estado_var = tk.StringVar(value="Nuevo")
        tk.OptionMenu(root, self.estado_var, *estados).pack(pady=3)

        # Checkbox para código
        self.codigo_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Tiene código de barras/QR?", variable=self.codigo_var, bg="#f0f0f0").pack(pady=3)

        # Botones principales
        self.boton("Agregar Caja", self.agregar, "#2ecc71")
        self.boton("Eliminar Caja", self.eliminar, "#e74c3c")
        self.boton("Mostrar Almacén", self.mostrar, "#3498db")
        self.boton("Buscar por ID", self.buscar, "#9b59b6")
        self.boton("Reporte por Estado", self.reporte_estado, "#f39c12")
        self.boton("Exportar a CSV", self.exportar_csv, "#16a085")

        # Lista de visualización
        self.lista_box = tk.Listbox(root, width=90, height=15, bg="white", bd=2)
        self.lista_box.pack(pady=10)

    def crear_campo(self, texto, attr):
        tk.Label(self.root, text=texto, bg="#f0f0f0").pack()
        entry = tk.Entry(self.root)
        entry.pack(pady=2)
        setattr(self, attr, entry)

    def boton(self, texto, comando, color):
        tk.Button(self.root, text=texto, command=comando, bg=color, fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=3)

    def agregar(self):
        id_caja = self.entry_id.get().strip()
        tipo = self.tipo_var.get()
        estado = self.estado_var.get()
        tiene_codigo = self.codigo_var.get() == 1

        if not id_caja:
            messagebox.showwarning("Campos incompletos", "Ingresa un ID.")
            return

        if id_caja in ids_usados:
            messagebox.showerror("ID Duplicado", f"El ID '{id_caja}' ya está registrado.")
            return

        clave = generar_clave(tipo, estado)

        if almacen[clave].agregar_caja(id_caja, tiene_codigo, tipo, estado):
            ids_usados.add(id_caja)
            guardar_ids_en_archivo()
            messagebox.showinfo("Éxito", f"Caja '{id_caja}' agregada en '{clave}'")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", f"No se pudo agregar la caja.")

    def eliminar(self):
        id_caja = self.entry_id.get().strip()
        tipo = self.tipo_var.get()
        estado = self.estado_var.get()
        clave = generar_clave(tipo, estado)

        if almacen[clave].eliminar_caja(id_caja):
            ids_usados.discard(id_caja)
            guardar_ids_en_archivo()
            messagebox.showinfo("Eliminado", f"Caja '{id_caja}' eliminada.")
        else:
            messagebox.showerror("Error", "ID no encontrado.")
        self.limpiar_campos()

    def mostrar(self):
        self.lista_box.delete(0, tk.END)
        for clave, lista in almacen.items():
            self.lista_box.insert(tk.END, f"\n--- {clave.upper()} ---")
            for caja in lista.mostrar_cajas():
                self.lista_box.insert(tk.END, caja)

    def buscar(self):
        id_buscado = simpledialog.askstring("Buscar Caja", "Ingrese ID a buscar:")
        if not id_buscado:
            return
        for clave, lista in almacen.items():
            nodo = lista.buscar_caja(id_buscado)
            if nodo:
                self.lista_box.delete(0, tk.END)
                self.lista_box.insert(tk.END, f"Ubicación: {clave.upper()}")
                self.lista_box.insert(tk.END, f"ID: {nodo.id_caja}")
                self.lista_box.insert(tk.END, f"Tipo: {nodo.tipo}")
                self.lista_box.insert(tk.END, f"Estado: {nodo.estado}")
                self.lista_box.insert(tk.END, f"Código: {'Sí' if nodo.tiene_codigo else 'No'}")
                return
        messagebox.showinfo("No encontrado", "ID no registrado.")

    def reporte_estado(self):
        estado = simpledialog.askstring("Reporte", "Ingrese estado a filtrar (Nuevo o Usado):")
        if not estado:
            return
        self.lista_box.delete(0, tk.END)
        for clave, lista in almacen.items():
            if clave.startswith(estado.lower()):
                self.lista_box.insert(tk.END, f"\n--- {clave.upper()} ---")
                for caja in lista.mostrar_cajas():
                    self.lista_box.insert(tk.END, caja)

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not ruta:
            return
        with open(ruta, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Ubicación", "ID", "Tipo", "Estado", "Código"])
            for clave, lista in almacen.items():
                for caja in lista.obtener_todas():
                    writer.writerow([clave.upper(), caja.id_caja, caja.tipo, caja.estado, "Sí" if caja.tiene_codigo else "No"])
        messagebox.showinfo("Exportado", f"Datos guardados en {ruta}")

    def limpiar_campos(self):
        self.entry_id.delete(0, tk.END)
        self.codigo_var.set(0)

# ---------------------------
# Ejecutar la aplicación
# ---------------------------
if __name__ == "__main__":
    cargar_ids_desde_archivo()
    inicializar_almacen()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
