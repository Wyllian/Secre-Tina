import flet as ft
import os
from datetime import datetime
import asyncio

# Importar lógica da Secre-Tina (será refinado na integração)
from secre_tina import record_audio, transcribe_audio, generate_summary

class Message(ft.Column):
    def __init__(self, text, is_user=True):
        super().__init__()
        self.text = text
        self.is_user = is_user
        
        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Você" if is_user else "Secre-Tina",
                        size=12,
                        weight="bold",
                        color=ft.Colors.BLUE_200 if is_user else ft.Colors.GREEN_200
                    ),
                    ft.Markdown(
                        text,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    )
                ], tight=True),
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.GREY_900 if is_user else ft.Colors.GREY_800,
                width=600,
            )
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.START

async def main(page: ft.Page):
    page.title = "Secre-Tina - Assistente Virtual"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1100
    page.window_height = 800
    
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True
    )
    
    # Simulação de histórico na Sidebar
    history_list = ft.ListView(
        expand=True,
        spacing=5,
        padding=10,
    )
    
    async def add_history_item(name):
        history_list.controls.append(
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHAT, size=16),
                    ft.Text(name, size=13, overflow=ft.TextOverflow.ELLIPSIS)
                ], width=200),
                on_click=lambda _: print(f"Carregar {name}")
            )
        )
    
    # Adicionar itens fake ao histórico
    for i in range(5):
        await add_history_item(f"Reunião de Alinhamento {i+1}")

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Button(
                    "Nova Sessão",
                    icon=ft.Icons.ADD,
                    width=230,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
                padding=20
            ),
            ft.Divider(height=1, color=ft.Colors.GREY_800),
            history_list,
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS),
                    title=ft.Text("Configurações"),
                    on_click=lambda _: print("Abrir Configs")
                ),
                padding=10
            )
        ]),
        width=250,
        bgcolor=ft.Colors.BLACK,
        height=page.window_height
    )

    message_input = ft.TextField(
        hint_text="Comece a falar ou digite aqui...",
        expand=True,
        border_radius=15,
        border_color=ft.Colors.GREY_700,
        bgcolor=ft.Colors.GREY_900,
        content_padding=15,
        multiline=True,
        min_lines=1,
        max_lines=5
    )

    is_recording = False

    async def toggle_recording(e):
        nonlocal is_recording
        is_recording = not is_recording
        rec_button.icon = ft.Icons.STOP if is_recording else ft.Icons.MIC
        rec_button.icon_color = ft.Colors.RED if is_recording else ft.Colors.WHITE
        rec_button.update()
        
        if not is_recording:
            # Simular processamento
            chat_list.controls.append(Message("Simulação de áudio gravado: 'Precisamos terminar o projeto Secre-Tina até amanhã.'", is_user=True))
            page.update()
            
            # Simular IA
            await asyncio.sleep(1)
            chat_list.controls.append(Message("### Resumo da Reunião\n- **Ação**: Finalizar o projeto Secre-Tina.\n- **Prazo**: Amanhã.", is_user=False))
            page.update()

    rec_button = ft.IconButton(
        icon=ft.Icons.MIC,
        icon_size=24,
        on_click=toggle_recording,
        tooltip="Gravar Áudio"
    )

    input_container = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Row([
                    message_input,
                    rec_button,
                    ft.IconButton(ft.Icons.SEND, icon_size=24, tooltip="Enviar")
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=800,
                padding=10,
                bgcolor=ft.Colors.GREY_900,
                border_radius=20,
                border=ft.Border.all(1, ft.Colors.GREY_800)
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor=ft.Colors.TRANSPARENT
    )

    main_view = ft.Column([
        chat_list,
        input_container
    ], expand=True)

    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_800),
            main_view
        ], expand=True)
    )

if __name__ == "__main__":
    ft.run(main)
