import flet as ft
import subprocess


def main(page: ft.Page):
    page.title = "Terminal Executor"
    page.window.width = 900
    page.window.height = 700

    command_field = ft.TextField(
        label="Command",
        hint_text="مثال: ipconfig یا ls -la",
        expand=True,
    )

    output_field = ft.TextField(
        label="Output",
        multiline=True,
        min_lines=20,
        max_lines=20,
        read_only=True,
        expand=True,
    )

    def run_command(e):
        cmd = command_field.value.strip()

        if not cmd:
            output_field.value = "لطفاً یک دستور وارد کنید."
            page.update()
            return

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
            )

            output_field.value = (
                f"Exit Code: {result.returncode}\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        except subprocess.TimeoutExpired:
            output_field.value = "Command timed out."

        except Exception as ex:
            output_field.value = f"Error:\n{ex}"

        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Terminal Command Runner",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[
                        command_field,
                        ft.ElevatedButton(
                            "Run",
                            on_click=run_command,
                        ),
                    ]
                ),
                output_field,
            ],
            expand=True,
        )
    )


ft.run(main)
