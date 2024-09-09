import pandas as pd
from tabulate import tabulate

class UI:
    def mostrar_menu(self):
        print("1. Consultar propiedades edáficas")
        print("2. Salir")

    def obtener_entrada(self):
        departamento = input("Ingrese el departamento: ").upper()
        municipio = input("Ingrese el municipio: ").upper()
        
         # Validación del cultivo para asegurar que la primera letra sea mayúscula
        while True:
            cultivo = input("Ingrese el cultivo: ").strip()  # Elimina espacios adicionales
            if cultivo and cultivo[0].isalpha():
                cultivo = cultivo.capitalize()
                break
            else:
                print("Error: El cultivo debe comenzar con una letra y no puede estar vacío.")

        while True:
            try:
                limit = int(input("Ingrese el número de registros a consultar: "))
                if limit <= 0 or limit>=1000:
                    raise ValueError("El número de registros debe ser un número positivo y menor a 1000 registros.")
                break
            except ValueError as e:
                print(f"Entrada inválida: {e}. Intente de nuevo.")
        
        return departamento, municipio, cultivo, limit

    def mostrar_resultados(self, resultados, medianas):
        if isinstance(resultados, pd.DataFrame) and not resultados.empty:
            # Mostrar los resultados de la consulta:
            print("\nResultados de la consulta: ")
            print(tabulate(resultados, headers='keys', tablefmt='grid', showindex=False))

            # Crear la tabla final combinando resultados y medianas
            tabla_final = self.crear_tabla_final(resultados, medianas)

            print("\nTabla con los resultados y las medianas:")
            print(tabulate(tabla_final, headers='keys', tablefmt='grid', showindex=False))

            # Mostrar advertencias si faltan datos para alguna mediana
            self.mostrar_advertencias(medianas)

        else:
            print("No se encontraron resultados o el formato no es válido.")

    def crear_tabla_final(self, resultados, medianas):
        # Crear un DataFrame con las medianas
        medianas_df = pd.DataFrame([medianas], columns=['pH', 'Fósforo', 'Potasio'])

        # Crear un DataFrame para la tabla final
        tabla_final = pd.concat([
            resultados[['departamento', 'municipio', 'cultivo', 'topografia']].head(1),
            medianas_df
        ], axis=1)

        return tabla_final

    def mostrar_advertencias(self, medianas):
        # Mostrar mensajes de advertencia si alguna mediana no pudo ser calculada
        if pd.isna(medianas['pH']):
            print("Advertencia: no se pudo calcular la mediana del pH debido a datos faltantes.")
        if pd.isna(medianas['Fósforo']):
            print("Advertencia: no se pudo calcular la mediana del Fósforo debido a datos faltantes.")
        if pd.isna(medianas['Potasio']):
            print("Advertencia: no se pudo calcular la mediana del Potasio debido a datos faltantes.")

