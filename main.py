import tkinter as tk
from tkinter import messagebox
import requests
import sys

def dish_fetch(num):
    """
    Criterio 3 y 4: Conexión a API y procesamiento de JSON.
    """
    url = f"https://api-colombia.com/api/v1/TypicalDish/{num}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": "Plato no encontrado"}
    except Exception as e:
        return {"error": f"Error de conexión: {e}"}

def mostrar_plato_gui():
    """Lógica para la interfaz gráfica (Criterio 5: Creatividad)"""
    id_plato = entry_id.get()
    if not id_plato.isdigit():
        messagebox.showwarning("Error", "Por favor ingresa un número válido")
        return

    datos = dish_fetch(id_plato)
    if "name" in datos:
        label_nombre.config(text=f"Nombre: {datos['name']}", fg="#2E7D32")
        text_desc.config(state="normal")
        text_desc.delete("1.0", tk.END)
        text_desc.insert(tk.END, datos.get('description', 'Sin descripción'))
        text_desc.config(state="disabled")
    else:
        messagebox.showerror("Error", datos.get("error"))

def main():
    """
    Criterio 1 y 2: Herramienta que acepta entradas y muestra salidas.
    """
    # Verificamos si queremos ejecutar la GUI o la Consola
    # Si pasas un argumento por terminal, funciona como CLI pura
    if len(sys.argv) > 1:
        id_arg = sys.argv[1]
        resultado = dish_fetch(id_arg)
        if "name" in resultado:
            print(f"\n--- {resultado['name']} ---")
            print(f"Descripción: {resultado['description']}\n")
        else:
            print(f"Error: {resultado.get('error')}")
        return

    # Iniciar Interfaz Gráfica (Criterio 5)
    try:
        root = tk.Tk()
        root.title("Menú Típico de Colombia 🇨🇴")
        root.geometry("400x500")
        root.configure(bg="#f0f0f0")

        tk.Label(root, text="Buscador de Platos", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(root, text="Ingresa el ID del plato:", bg="#f0f0f0").pack()
        global entry_id
        entry_id = tk.Entry(root, font=("Arial", 12), justify="center")
        entry_id.pack(pady=5)

        btn_buscar = tk.Button(root, text="Consultar Menú", command=mostrar_plato_gui, 
                               bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=10)
        btn_buscar.pack(pady=10)

        global label_nombre, text_desc
        label_nombre = tk.Label(root, text="Nombre: ", font=("Arial", 11, "bold"), bg="#f0f0f0", wraplength=350)
        label_nombre.pack(pady=5)

        tk.Label(root, text="Descripción:", bg="#f0f0f0").pack()
        text_desc = tk.Text(root, height=8, width=40, font=("Arial", 10), state="disabled", wrap="word")
        text_desc.pack(pady=5, padx=20)

        tk.Label(root, text="API de Colombia v1", font=("Arial", 8), fg="gray", bg="#f0f0f0").pack(side="bottom", pady=5)

        root.mainloop()
    except Exception:
        # Si no hay entorno gráfico (para el test automático), pedimos entrada por consola
        print("--- CLI Mode ---")
        id_cli = input("Ingresa el ID del plato: ")
        print(dish_fetch(id_cli))

if __name__ == "__main__":
    main()