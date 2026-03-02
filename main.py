import tkinter as tk
from tkinter import messagebox
import requests

def dish_fetch(num):
    """Función lógica solicitada por el ejercicio"""
    url = f"https://api-colombia.com/api/v1/TypicalDish/{num}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": "Plato no encontrado"}
    except:
        return {"error": "Error de conexión"}

def mostrar_plato():
    """Lógica de la interfaz para obtener datos y mostrarlos"""
    id_plato = entry_id.get()
    
    if not id_plato.isdigit():
        messagebox.showwarning("Error", "Por favor ingresa un número válido")
        return

    datos = dish_fetch(id_plato)
    
    if "name" in datos:
        label_nombre.config(text=f"Nombre: {datos['name']}", fg="#2E7D32")
        # Usamos text.delete y insert para la descripción (que puede ser larga)
        text_desc.config(state="normal")
        text_desc.delete("1.0", tk.END)
        text_desc.insert(tk.END, datos.get('description', 'Sin descripción'))
        text_desc.config(state="disabled")
    else:
        messagebox.showerror("Error", datos.get("error", "No se encontró el plato"))

def main():
    # --- Configuración de la Ventana Principal ---
    root = tk.Tk()
    root.title("Menú Típico de Colombia 🇨🇴")
    root.geometry("400x450")
    root.configure(bg="#f0f0f0")

    # Título
    tk.Label(root, text="Buscador de Platos", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Campo de entrada
    tk.Label(root, text="Ingresa el ID del plato:", bg="#f0f0f0").pack()
    global entry_id
    entry_id = tk.Entry(root, font=("Arial", 12), justify="center")
    entry_id.pack(pady=5)

    # Botón de búsqueda
    btn_buscar = tk.Button(root, text="Consultar Menú", command=mostrar_plato, 
                           bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=10)
    btn_buscar.pack(pady=10)

    # Área de resultados
    global label_nombre, text_desc
    label_nombre = tk.Label(root, text="Nombre: ", font=("Arial", 11, "bold"), bg="#f0f0f0", wraplength=350)
    label_nombre.pack(pady=5)

    tk.Label(root, text="Descripción:", bg="#f0f0f0").pack()
    text_desc = tk.Text(root, height=8, width=40, font=("Arial", 10), state="disabled", wrap="word")
    text_desc.pack(pady=5, padx=20)

    # Pie de página
    tk.Label(root, text="API de Colombia v1", font=("Arial", 8), fg="gray", bg="#f0f0f0").pack(side="bottom", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()