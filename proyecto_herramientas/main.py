# ejecucion.py

from auth import puede_administrar, puede_residente
from usuarios import crear_usuario, listar_usuarios, buscar_usuario_por_id, actualizar_usuario, eliminar_usuario
from herramientas import (
    crear_herramienta, listar_herramientas, buscar_herramienta_por_id,
    actualizar_herramienta, inactivar_herramienta, eliminar_herramienta
)
from prestamos import crear_prestamo, devolver_prestamo, marcar_vencidos
from reportes import (
    herramientas_stock_bajo, prestamos_activos_y_vencidos,
    historial_prestamos_por_usuario, herramientas_mas_cotizadas,
    usuarios_que_mas_piden
)
from logger import log_info

def input_no_vacio(msg: str) -> str:
    val = input(msg).strip()
    while not val:
        val = input(f"(No vacío) {msg}").strip()
    return val

def menu_admin():
    print("\n--- Menú ADMINISTRADOR ---")
    print("1. Gestionar usuarios")
    print("2. Gestionar herramientas")
    print("3. Gestionar préstamos")
    print("4. Consultas y reportes")
    print("0. Salir")

def menu_residente():
    print("\n--- Menú RESIDENTE ---")
    print("1. Consultar herramientas")
    print("2. Crear solicitud de préstamo")
    print("3. Consultar mis préstamos")
    print("0. Salir")

def gestionar_usuarios():
    print("\n--- Gestión de Usuarios ---")
    print("1. Crear usuario")
    print("2. Listar usuarios")
    print("3. Actualizar usuario")
    print("4. Eliminar usuario")
    print("0. Volver")
    op = input("Opción: ").strip()

    if op == "1":
        data = {
            "id": input_no_vacio("ID: "),
            "primer_nombre": input_no_vacio("Primer nombre: "),
            "primer_apellido": input_no_vacio("Primer apellido: "),
            "telefono": input_no_vacio("Teléfono: "),
            "direccion": input_no_vacio("Dirección: "),
            "tipo_usuario": input_no_vacio("Tipo (ADMINISTRADOR/RESIDENTE): ").upper(),
        }
        print("OK" if crear_usuario(data) else "Error")
    elif op == "2":
        for u in listar_usuarios():
            print(u)
    elif op == "3":
        uid = input_no_vacio("ID usuario a actualizar: ")
        cambios = {}
        print("Deja vacío para no cambiar.")
        pn = input("Nuevo primer nombre: ").strip()
        if pn: cambios["primer_nombre"] = pn
        pa = input("Nuevo primer apellido: ").strip()
        if pa: cambios["primer_apellido"] = pa
        tel = input("Nuevo teléfono: ").strip()
        if tel: cambios["telefono"] = tel
        dirc = input("Nueva dirección: ").strip()
        if dirc: cambios["direccion"] = dirc
        tipo = input("Nuevo tipo (ADMINISTRADOR/RESIDENTE): ").strip().upper()
        if tipo: cambios["tipo_usuario"] = tipo
        print("OK" if actualizar_usuario(uid, cambios) else "Error")
    elif op == "4":
        uid = input_no_vacio("ID usuario a eliminar: ")
        print("OK" if eliminar_usuario(uid) else "Error")

def gestionar_herramientas():
    print("\n--- Gestión de Herramientas ---")
    print("1. Crear herramienta")
    print("2. Listar herramientas")
    print("3. Buscar herramienta")
    print("4. Actualizar herramienta")
    print("5. Inactivar herramienta")
    print("6. Eliminar herramienta")
    print("0. Volver")
    op = input("Opción: ").strip()

    if op == "1":
        data = {
            "id": input_no_vacio("ID: "),
            "nombre": input_no_vacio("Nombre: "),
            "categoria": input_no_vacio("Categoría: "),
            "cantidad_disponible": int(input_no_vacio("Cantidad disponible: ")),
            "estado": input_no_vacio("Estado (ACTIVA/INACTIVA/MANTENIMIENTO): ").upper(),
            "valor_estimado": float(input_no_vacio("Valor estimado: ")),
        }
        print("OK" if crear_herramienta(data) else "Error")
    elif op == "2":
        for h in listar_herramientas():
            print(h)
    elif op == "3":
        hid = input_no_vacio("ID herramienta: ")
        print(buscar_herramienta_por_id(hid) or "No encontrada")
    elif op == "4":
        hid = input_no_vacio("ID herramienta a actualizar: ")
        cambios = {}
        print("Deja vacío para no cambiar.")
        nom = input("Nuevo nombre: ").strip()
        if nom: cambios["nombre"] = nom
        cat = input("Nueva categoría: ").strip()
        if cat: cambios["categoria"] = cat
        cant = input("Nueva cantidad disponible: ").strip()
        if cant: cambios["cantidad_disponible"] = int(cant)
        est = input("Nuevo estado (ACTIVA/INACTIVA/MANTENIMIENTO): ").strip().upper()
        if est: cambios["estado"] = est
        val = input("Nuevo valor estimado: ").strip()
        if val: cambios["valor_estimado"] = float(val)
        print("OK" if actualizar_herramienta(hid, cambios) else "Error")
    elif op == "5":
        hid = input_no_vacio("ID herramienta a inactivar: ")
        print("OK" if inactivar_herramienta(hid) else "Error")
    elif op == "6":
        hid = input_no_vacio("ID herramienta a eliminar: ")
        print("OK" if eliminar_herramienta(hid) else "Error")

def gestionar_prestamos_admin():
    print("\n--- Gestión de Préstamos (Admin) ---")
    print("1. Crear préstamo")
    print("2. Devolver préstamo")
    print("3. Marcar vencidos (ingrese fecha YYYY-MM-DD)")
    print("0. Volver")
    op = input("Opción: ").strip()

    if op == "1":
        data = {
            "id": input_no_vacio("ID préstamo: "),
            "usuario_id": input_no_vacio("ID usuario: "),
            "herramienta_id": input_no_vacio("ID herramienta: "),
            "cantidad": int(input_no_vacio("Cantidad: ")),
            "fecha_inicio": input_no_vacio("Fecha inicio (YYYY-MM-DD): "),
            "fecha_devolucion_estimada": input_no_vacio("Fecha devolución estimada (YYYY-MM-DD): "),
            "estado": "ACTIVO",
            "observaciones": "",
        }
        print("OK" if crear_prestamo(data) else "Error")
    elif op == "2":
        pid = input_no_vacio("ID préstamo a devolver: ")
        obs = input("Observaciones: ").strip()
        print("OK" if devolver_prestamo(pid, obs) else "Error")
    elif op == "3":
        hoy = input_no_vacio("Fecha hoy (YYYY-MM-DD): ")
        cambios = marcar_vencidos(hoy)
        print(f"Vencidos marcados: {cambios}")

def consultas_reportes():
    print("\n--- Consultas y Reportes ---")
    print("1. Herramientas con stock bajo")
    print("2. Préstamos activos y vencidos")
    print("3. Historial de préstamos por usuario")
    print("4. Herramientas más cotizadas")
    print("5. Usuarios que más piden herramientas")
    print("0. Volver")
    op = input("Opción: ").strip()

    if op == "1":
        for h in herramientas_stock_bajo():
            print(h)
    elif op == "2":
        r = prestamos_activos_y_vencidos()
        print("ACTIVOS:")
        for p in r["ACTIVOS"]:
            print(p)
        print("VENCIDOS:")
        for p in r["VENCIDOS"]:
            print(p)
    elif op == "3":
        uid = input_no_vacio("ID usuario: ")
        for p in historial_prestamos_por_usuario(uid):
            print(p)
    elif op == "4":
        top = input("Top (default 5): ").strip()
        topn = int(top) if top else 5
        for item in herramientas_mas_cotizadas(topn):
            print(item)
    elif op == "5":
        top = input("Top (default 5): ").strip()
        topn = int(top) if top else 5
        for item in usuarios_que_mas_piden(topn):
            print(item)

def flujo_admin():
    while True:
        menu_admin()
        op = input("Opción: ").strip()
        if op == "1":
            gestionar_usuarios()
        elif op == "2":
            gestionar_herramientas()
        elif op == "3":
            gestionar_prestamos_admin()
        elif op == "4":
            consultas_reportes()
        elif op == "0":
            break

def flujo_residente(usuario_id: str):
    while True:
        menu_residente()
        op = input("Opción: ").strip()
        if op == "1":
            for h in listar_herramientas():
                print(h)
        elif op == "2":
            # Solicitud de préstamo (queda como creación directa para simplificar flujo)
            data = {
                "id": input_no_vacio("ID préstamo: "),
                "usuario_id": usuario_id,
                "herramienta_id": input_no_vacio("ID herramienta: "),
                "cantidad": int(input_no_vacio("Cantidad: ")),
                "fecha_inicio": input_no_vacio("Fecha inicio (YYYY-MM-DD): "),
                "fecha_devolucion_estimada": input_no_vacio("Fecha devolución estimada (YYYY-MM-DD): "),
                "estado": "ACTIVO",
                "observaciones": "Solicitud creada por residente",
            }
            print("OK" if crear_prestamo(data) else "Error")
        elif op == "3":
            for p in historial_prestamos_por_usuario(usuario_id):
                print(p)
        elif op == "0":
            break

def main():
    print("=== Sistema de Control de Herramientas del Vecindario ===")
    log_info("Aplicación iniciada.")
    tipo = input_no_vacio("¿Eres ADMINISTRADOR o RESIDENTE? ").upper()

    if tipo == "ADMINISTRADOR":
        flujo_admin()
    elif tipo == "RESIDENTE":
        uid = input_no_vacio("Ingresa tu ID de usuario: ")
        u = buscar_usuario_por_id(uid)
        if not u or u["tipo_usuario"] != "RESIDENTE":
            print("Usuario no válido para rol RESIDENTE.")
            return
        flujo_residente(uid)
    else:
        print("Rol no reconocido.")

if __name__ == "__main__":
    main()
