import flet as ft
import re
from cryptography.fernet import Fernet

# Cifrado simulado del teléfono
clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

# Lista para almacenar amigos
amigos = []

def main(page: ft.Page):
    page.title = "Agenda de Amigos Segura"

    name_input = ft.TextField(label="Nombre completo", width=300)
    email_input = ft.TextField(label="Correo electrónico", width=300)
    phone_input = ft.TextField(label="Celular", width=300)

    name_error = ft.Text("", color="red")
    email_error = ft.Text("", color="red")
    phone_error = ft.Text("", color="red")
    result_text = ft.Text("")

    friend_list = ft.Column()

    def sanitize(text):
        return text.replace("<", "").replace(">", "").replace("&", "").replace('"', "").replace("'", "")

    def es_email_valido(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email)

    def es_telefono_valido(phone):
        return re.match(r"^\d{10}$", phone)

    def ya_existe_correo(correo):
        return any(correo == amigo["email"] for amigo in amigos)

    def add_friend(e):
        name = sanitize(name_input.value.strip())
        email = sanitize(email_input.value.strip())
        phone = sanitize(phone_input.value.strip())

        errores = []

        # Validaciones
        if not name or len(name) > 50:
            name_error.value = "Nombre obligatorio (máx. 50 caracteres)"
            errores.append(True)
        else:
            name_error.value = ""

        if not email or not es_email_valido(email):
            email_error.value = "Correo electrónico inválido"
            errores.append(True)
        elif ya_existe_correo(email):
            email_error.value = "Este correo ya está registrado"
            errores.append(True)
        else:
            email_error.value = ""

        if not phone or not es_telefono_valido(phone):
            phone_error.value = "Celular inválido (solo números de 10 dígitos)"
            errores.append(True)
        else:
            phone_error.value = ""

        if errores:
            result_text.value = ""
            page.update()
            return

        # Cifrado del teléfono
        phone_encrypted = cipher_suite.encrypt(phone.encode())

        amigos.append({
            "name": name,
            "email": email,
            "telefono_cifrado": phone_encrypted
        })

        friend_list.controls.append(ft.Text(f"{name} - {email} - [Teléfono cifrado]"))
        name_input.value = ""
        email_input.value = ""
        phone_input.value = ""
        result_text.value = "Amigo registrado correctamente ✅"

        page.update()

    page.add(
        ft.Column([
            ft.Text("Agenda de Amigos", style="headlineMedium"),
            name_input, name_error,
            email_input, email_error,
            phone_input, phone_error,
            ft.ElevatedButton("Agregar amigo", on_click=add_friend),
            result_text,
            ft.Divider(),
            ft.Text("Lista de amigos:", weight="bold"),
            friend_list
        ])
    )

ft.app(target=main)
