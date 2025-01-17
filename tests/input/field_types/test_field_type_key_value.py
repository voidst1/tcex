"""Testing TcEx Input module field types."""
# standard library
from typing import TYPE_CHECKING, Optional

# third-party
import pytest
from pydantic import BaseModel

# first-party
from tcex.backports import cached_property
from tcex.input.field_types import KeyValue, TCEntity
from tcex.pleb.scoped_property import scoped_property
from tests.input.field_types.utils import InputTest

if TYPE_CHECKING:
    # first-party
    from tests.mock_app import MockApp


# pylint: disable=no-self-argument, no-self-use
class TestInputsFieldTypeKeyValue(InputTest):
    """Test TcEx Inputs Config."""

    def setup_method(self):
        """Configure setup before all tests."""
        scoped_property._reset()
        cached_property._reset()

    @pytest.mark.parametrize(
        ('input_value,expected,optional,fail_test'),
        [
            (
                {'key': 'my_key', 'value': 'my_string', 'type': 'string'},
                {'key': 'my_key', 'value': 'my_string', 'type': 'string'},
                False,
                False,
            ),
            (
                None,
                None,
                True,
                False,
            ),
        ],
    )
    def test_field_type_key_value_simple(
        self,
        input_value: str,
        expected: str,
        optional: bool,
        fail_test: bool,
        playbook_app: 'MockApp',
    ):
        """Test KeyValue field type with string input.

        Args:
            playbook_app (fixture): An instance of MockApp.
        """
        if optional is False:

            class PytestModel(BaseModel):
                """Test Model for Inputs"""

                my_key_value: KeyValue

        else:

            class PytestModel(BaseModel):
                """Test Model for Inputs"""

                my_key_value: Optional[KeyValue]

        self._type_validation(
            PytestModel,
            input_name='my_key_value',
            input_value=input_value,
            input_type='KeyValue',
            expected=expected,
            fail_test=fail_test,
            playbook_app=playbook_app,
        )

    @pytest.mark.parametrize(
        ('nested_reference,nested_value,value,expected_value'),
        [
            (
                '#App:1234:my_ref!Binary',
                b'binary string',
                '#App:1234:my_ref!Binary',
                b'binary string',
            ),
            (
                '#App:1234:my_ref!BinaryArray',
                [b'binary string'],
                '#App:1234:my_ref!BinaryArray',
                [b'binary string'],
            ),
            ('#App:1234:my_ref!String', 'string', '#App:1234:my_ref!String', 'string'),
            (
                '#App:1234:my_ref!StringArray',
                ['string'],
                '#App:1234:my_ref!StringArray',
                ['string'],
            ),
            (
                '#App:1234:my_ref!KeyValue',
                {'key': 'key', 'value': 'value', 'type': 'any'},
                '#App:1234:my_ref!KeyValue',
                {'key': 'key', 'value': 'value', 'type': 'any'},
            ),
            (
                '#App:1234:my_ref!KeyValueArray',
                [{'key': 'key', 'value': 'value', 'type': 'any'}],
                '#App:1234:my_ref!KeyValueArray',
                [{'key': 'key', 'value': 'value', 'type': 'any'}],
            ),
            (
                '#App:1234:my_ref!TCEntity',
                {'id': '1', 'value': '1.1.1.1', 'type': 'Address'},
                '#App:1234:my_ref!TCEntity',
                TCEntity(**{'id': '1', 'value': '1.1.1.1', 'type': 'Address'}),
            ),
            (
                '#App:1234:my_ref!TCEntityArray',
                [{'id': '1', 'value': '1.1.1.1', 'type': 'Address'}],
                '#App:1234:my_ref!TCEntityArray',
                [TCEntity(**{'id': '1', 'value': '1.1.1.1', 'type': 'Address'})],
            ),
            # value is string with String variable reference
            (
                '#App:1234:my_ref!String',
                'string',
                'String with nested ref #App:1234:my_ref!String',
                'String with nested ref string',
            ),
            # value is string with StringArray reference
            (
                '#App:1234:my_ref!StringArray',
                ['string'],
                'String with nested ref #App:1234:my_ref!StringArray',
                'String with nested ref ["string"]',
            ),
            # value is string with KeyValue reference
            (
                '#App:1234:my_ref!KeyValue',
                {'key': 'key', 'value': 'value', 'type': 'any'},
                'String with nested ref #App:1234:my_ref!KeyValue',
                'String with nested ref {"key": "key", "value": "value", "type": "any"}',
            ),
            # value is string with KeyValueArray reference
            (
                '#App:1234:my_ref!KeyValueArray',
                [{'key': 'key', 'value': 'value', 'type': 'any'}],
                'String with nested ref #App:1234:my_ref!KeyValueArray',
                'String with nested ref [{"key": "key", "value": "value", "type": "any"}]',
            ),
            # value is string with TCEntity reference
            (
                '#App:1234:my_ref!TCEntity',
                {'id': '1', 'value': '1.1.1.1', 'type': 'Address'},
                'String with nested ref #App:1234:my_ref!TCEntity',
                'String with nested ref {"id": "1", "value": "1.1.1.1", "type": "Address"}',
            ),
            # value is string with TCEntityArray reference
            (
                '#App:1234:my_ref!TCEntityArray',
                [{'id': '1', 'value': '1.1.1.1', 'type': 'Address'}],
                'String with nested ref #App:1234:my_ref!TCEntityArray',
                'String with nested ref [{"id": "1", "value": "1.1.1.1", "type": "Address"}]',
            ),
            # value is string with reference that resolves to None
            # NOTE: need to be able to clear key value store between tests
            (
                '#App:1234:my_ref2!String',
                None,
                'String with nested ref #App:1234:my_ref2!String',
                'String with nested ref <null>',
            ),
            # value is string with reference to binary
            # need to add exception handling in read_embedded
            (
                '#App:1234:my_ref!Binary',
                b'binary string',
                'string with binary reference #App:1234:my_ref!Binary',
                'string with binary reference <binary>',
            ),
        ],
    )
    def test_field_type_key_value_with_nested_reference(
        self,
        nested_reference,
        nested_value,
        value,
        expected_value,
        playbook_app: 'MockApp',
    ):
        """Test KeyValue field type with nested reference.

        Args:
            nested_reference: nested variable reference found within 'value' of KeyValue
            nested_value: the value that nested_reference should resolve to
            value: the 'value' portion of the KeyValue prior to reference resolution
            expected_value: the 'value' portion of the KeyValue after resolution
            playbook_app (fixture): An instance of MockApp.
        """

        class PytestModel(BaseModel):
            """Test Model for Inputs"""

            my_key_value: KeyValue

        config_data = {'my_key_value': '#App:1234:my_key_value!KeyValue'}
        app = playbook_app(config_data=config_data)
        tcex = app.tcex
        self._stage_key_value('my_ref', nested_reference, nested_value, tcex)
        self._stage_key_value(
            'my_key_value',
            '#App:1234:my_key_value!KeyValue',
            {'key': 'my_key', 'value': value, 'type': 'any'},
            tcex,
        )
        tcex.inputs.add_model(PytestModel)

        assert tcex.inputs.model.my_key_value == {
            'key': 'my_key',
            'value': expected_value,
            'type': 'any',
        }
