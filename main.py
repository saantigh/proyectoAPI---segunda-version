from api.api_module import APIClient
from ui.ui_module import UI
import logging

class MainApp:
    def __init__(self):
        self.api_client = APIClient()
        self.ui = UI()

    def run(self):
        try:
            while True:
                self.ui.mostrar_menu()
                opcion = input("Seleccione la opción que desee: ")

                if opcion == "1":
                    departamento, municipio, cultivo, limit = self.ui.obtener_entrada()
                    resultados = self.api_client.consultar_datos(departamento, municipio, cultivo, limit)
                    
                    if resultados.empty:
                        print("No se encontraron resultados para la consulta realizada.")
                    else:
                        medianas = self.api_client.calcular_mediana(resultados)
                        self.ui.mostrar_resultados(resultados, medianas)
                
                elif opcion == "2":
                    print("Saliendo del programa. ¡Hasta pronto!")
                    break
                else:
                    logging.warning("Opción no válida seleccionada.")
                    print("Opción no válida, por favor intente de nuevo.")
        except Exception as e:
            logging.error(f"Ocurrió un error inesperado: {e}")
            print(f"Error inesperado: {e}. El programa ha terminado.")

if __name__ == "__main__":
    app = MainApp()
    app.run()

