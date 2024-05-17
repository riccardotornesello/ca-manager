import typer
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from prompt_toolkit.validation import ValidationError, Validator

from ca_ez_manager.utils.crypto import generate_certificate
from ca_ez_manager.utils.storage import get_ca_list, store_ca, delete_ca


app = typer.Typer()


@app.command(name="create")
def create(name: str = None):
    ca_list = get_ca_list()

    if name:
        if name in ca_list:
            print("CA already exists")
            raise typer.Exit(code=1)

    else:

        class CANameValidator(Validator):
            def validate(self, document):
                if document.text in ca_list:
                    raise ValidationError(
                        message="CA already exists.",
                        cursor_position=document.cursor_position,
                    )
                if not document.text.isalnum():
                    raise ValidationError(
                        message="The name must contain only lowercase letters and numbers.",
                        cursor_position=document.cursor_position,
                    )

        answers = prompt(
            [
                {
                    "name": "name",
                    "type": "input",
                    "message": "Enter the name of the CA:",
                    "validate": CANameValidator(),
                }
            ]
        )

        name = answers["name"]

    ca_private_key, ca_cert = generate_certificate()

    store_ca(name, ca_private_key, ca_cert)

    print("CA created successfully")


@app.command(name="delete")
def delete(name: str = None):
    ca_list = get_ca_list()

    if name:
        if name not in ca_list:
            print("CA not found")
            raise typer.Exit(code=1)

    else:
        choices = [Choice(value=ca, name=ca) for ca in ca_list]
        questions = [
            {
                "name": "name",
                "type": "list",
                "message": "Select the CA to delete:",
                "choices": choices,
            }
        ]
        answers = prompt(questions)

        name = answers["name"]

    delete_ca(name)

    print("CA deleted successfully")
