"""Generate Models for Case Management Types"""
# standard library
import os
from enum import Enum
from pathlib import Path
from typing import Any

# third-party
import typer

# first-party
from tcex.tc_api._gen_model_abc import GenerateModelABC
from tcex.tc_api._gen_doc_abc import GenerateDocABC


class GenerateModel(GenerateModelABC):
    """Generate Models for Case Management Types"""

    def __init__(self, type_: str) -> None:
        """Initialize class properties."""
        super().__init__(type_)

        # properties
        _type_map = {
            'user': 'users',
            'user_group': 'userGroups',
        }
        _api_endpoint = f'/v3/security/{_type_map.get(type_)}'
        self.api_url = f'{self._api_server}{_api_endpoint}'

    def _configure_type(self, type_: str, field: str) -> str:
        """Return hint type."""
        _types = self._prop_type_common()
        _types.update(self._prop_type_user(type_, field))

        # handle types
        type_data = _types.get(type_, {})
        requirement_data = type_data.get('requirement')
        validator = type_data.get('validator')
        # TODO: [med] find a better way to handle this.
        _class_name_plural = self.inflect.plural(self.class_name)
        if requirement_data is not None and not type_ == _class_name_plural:
            from_ = requirement_data.get('from')
            import_ = requirement_data.get('import')
            if import_ not in self.requirements.get(from_):
                self.requirements[from_].append(import_)
        if validator is not None:
            self.validators[type_] = '\n'.join(validator)
        return type_data.get('type', type_)


class GenerateDoc(GenerateDocABC):
    """Generate Models for TC API Types"""

    def _import_model(self) -> Any:
        """Import the appropriate model."""
        if self.type_ == 'user':
            # first-party
            from tcex.api.tc.v3.security.models.user_model import UserModel as Model
        elif self.type_ == 'user_group':
            # first-party
            from tcex.security.models.user_group_model import UserGroupModel as Model

        return Model


# Update this !!!
class ObjectTypes(str, Enum):
    """Object Types"""

    user = 'user'
    user_group = 'user_group'


app = typer.Typer()


@app.command()
def doc(
    type_: ObjectTypes = typer.Option(
        ..., '--type', help='The ThreatConnect Case Management Type.'
    ),
):
    """Generate the model"""
    gm = GenerateDoc(type_)

    # run model code first so that requirements can be determined
    gm.gen_docs()


@app.command()
def model(
    type_: ObjectTypes = typer.Option(..., '--type', help='The ThreatConnect Object Type.'),
):
    """Generate the model"""
    # Update this !!!
    out_file = Path(os.path.join('tcex', 'security', 'models', f'{type_}_model.py'))

    # get instance of model generator
    gm = GenerateModel(type_)

    # run model code first so that requirements can be determined
    model_container_code = gm.gen_model_container_code()
    model_data_code = gm.gen_model_data_code()
    model_code = gm.gen_model_code()

    if not out_file.is_file():
        typer.secho(f'\nCould not find file {out_file}.', fg=typer.colors.RED)
        typer.Exit(code=1)

    with out_file.open(mode='w') as fh:
        fh.write(gm.gen_doc_string_code())
        fh.write(gm.gen_requirements_code())
        fh.write(model_container_code)
        fh.write(model_data_code)
        fh.write(model_code)
        fh.write(gm.gen_model_validators())
        # fh.write(gm.gen_model_config_code())
        fh.write(gm.gen_requirements_forward_reference_code())
        fh.write('')  # newline at the end of the file

    typer.secho(f'Successfully wrote {out_file}.', fg=typer.colors.GREEN)


if __name__ == '__main__':
    app()
