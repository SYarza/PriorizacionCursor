from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from enum import Enum

class TipoCamion(Enum):
    TRAILER_40 = "TRAILER 40"
    DOBLE_REMOLQUE = "DOBLE REMOLQUE"

@dataclass
class Producto:
    clave: int
    peso_teorico: float
    cantidad: int
    toneladas: float

@dataclass
class Camion:
    tipo: TipoCamion
    productos: Dict[int, float]  # clave_producto: toneladas
    toneladas_totales: float = 0.0

class Distribuidor:
    def __init__(self, ruta_json: str):
        self.LIMITE_TRAILER = {"min": 29.0, "max": 36.0}
        self.LIMITE_DOBLE = {"min": 50.0, "max": 56.0}
        self.productos = self._cargar_datos(ruta_json)
        
    def _cargar_datos(self, ruta_json: str) -> List[Producto]:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        productos = []
        order_detail = data["client_information_request"]["OrderDetail"]
        
        for item in order_detail:
            prod = Producto(
                clave=item["ClaArticulo"],
                peso_teorico=item["PesoTeorico"],
                cantidad=item["Cantidad"],
                toneladas=item["Toneladas"]
            )
            productos.append(prod)
            
        return sorted(productos, key=lambda x: x.toneladas, reverse=True)

    def _es_carga_valida(self, toneladas: float, tipo_camion: TipoCamion) -> bool:
        limites = self.LIMITE_TRAILER if tipo_camion == TipoCamion.TRAILER_40 else self.LIMITE_DOBLE
        return limites["min"] <= toneladas <= limites["max"]

    def plan_solo_trailers(self) -> List[Camion]:
        plan = []
        productos_pendientes = self.productos.copy()
        
        while productos_pendientes:
            producto = productos_pendientes[0]
            if self._es_carga_valida(producto.toneladas, TipoCamion.TRAILER_40):
                camion = Camion(
                    tipo=TipoCamion.TRAILER_40,
                    productos={producto.clave: producto.toneladas},
                    toneladas_totales=producto.toneladas
                )
                plan.append(camion)
                productos_pendientes.pop(0)
            else:
                return []  # No es posible hacer el plan solo con trailers
        
        return plan

    def plan_solo_dobles(self) -> List[Camion]:
        plan = []
        toneladas_totales = sum(p.toneladas for p in self.productos)
        
        if not self._es_carga_valida(toneladas_totales, TipoCamion.DOBLE_REMOLQUE):
            return []  # No es posible hacer el plan solo con dobles
            
        camion = Camion(
            tipo=TipoCamion.DOBLE_REMOLQUE,
            productos={p.clave: p.toneladas for p in self.productos},
            toneladas_totales=toneladas_totales
        )
        plan.append(camion)
        return plan

    def plan_mixto(self) -> List[Camion]:
        # Por ahora, usaremos la mejor solución entre solo trailers y solo dobles
        plan_trailers = self.plan_solo_trailers()
        plan_dobles = self.plan_solo_dobles()
        
        if not plan_trailers and not plan_dobles:
            return []
            
        return plan_trailers if len(plan_trailers) <= len(plan_dobles) else plan_dobles

    def generar_planes(self) -> Dict[str, List[Camion]]:
        return {
            "solo_trailers": self.plan_solo_trailers(),
            "solo_dobles": self.plan_solo_dobles(),
            "mixto": self.plan_mixto()
        }

def imprimir_plan(plan: List[Camion], nombre_plan: str):
    print(f"\nPlan {nombre_plan}:")
    if not plan:
        print("No es posible generar un plan válido con estas restricciones")
        return
        
    for i, camion in enumerate(plan, 1):
        print(f"Camión {i} ({camion.tipo.value}): {camion.toneladas_totales:.2f} toneladas")
        for clave, tons in camion.productos.items():
            print(f"  - Producto {clave}: {tons:.2f} toneladas")

def main():
    distribuidor = Distribuidor('dataO2D.json')
    planes = distribuidor.generar_planes()
    
    for nombre_plan, plan in planes.items():
        imprimir_plan(plan, nombre_plan)

if __name__ == "__main__":
    main() 