"""Test the TcEx API Snippets."""
# first-party
from tcex.api.tc.v3.tql.tql_operator import TqlOperator
from tests.api.tc.v3.v3_helpers import TestCaseManagement, V3Helper


class TestIndicatorSnippets(TestCaseManagement):
    """Test TcEx API Interface."""

    v3 = None

    def setup_method(self):
        """Configure setup before all tests."""
        print('')  # ensure any following print statements will be on new line
        self.v3_helper = V3Helper('cases')
        self.v3 = self.v3_helper.v3
        self.tcex = self.v3_helper.tcex

        # remove old cases
        indicators = self.tcex.v3.indicators()
        indicators.filter.summary(TqlOperator.EQ, '111.111.111.111')
        for indicator in indicators:
            indicator.delete()

    def test_address_create(self):
        """Test snippet"""
        # Begin Snippet
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )

        indicator.create(params={'owner': 'TCI'})
        # End Snippet

        # Add cleanup
        indicator.delete()

    def test_address_stage_group_associations(self):
        """Test snippet"""
        # Begin Snippet
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )

        # Add attribute
        association = self.tcex.v3.group(name='MyGroup', type='Adversary')
        indicator.stage_associated_group(association)

        indicator.create(params={'owner': 'TCI'})
        # End Snippet

        # Add cleanup
        indicator.delete()

    def test_address_stage_attribute(self):
        """Test snippet"""
        # Begin Snippet
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )

        # Add attribute
        attribute = self.tcex.v3.indicator_attribute(
            value='An example description attribute.',
            type='Description',
        )
        indicator.stage_attribute(attribute)

        indicator.create(params={'owner': 'TCI'})
        # End Snippet

        # Add cleanup
        indicator.delete()

    def test_address_stage_security_label(self):
        """Test snippet"""
        # Begin Snippet
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )

        # Add attribute
        security_label = self.tcex.v3.security_label(name='TLP:WHITE')
        indicator.stage_security_label(security_label)

        indicator.create(params={'owner': 'TCI'})
        # End Snippet

        # Add cleanup
        indicator.delete()

    def test_address_stage_tag(self):
        """Test snippet"""
        # Begin Snippet
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )

        # Add attribute
        tag = self.tcex.v3.tag(name='Example-Tag')
        indicator.stage_tag(tag)

        indicator.create(params={'owner': 'TCI'})
        # End Snippet

        # Add cleanup
        indicator.delete()

    def test_address_delete_by_id(self):
        """Test snippet"""
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )
        indicator.create(params={'owner': 'TCI'})

        # Begin Snippet
        indicator = self.tcex.v3.indicator(id=indicator.model.id)
        indicator.delete(params={'owner': 'TCI'})
        # End Snippet

    def test_address_delete_by_summary(self):
        """Test snippet"""
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )
        indicator.create(params={'owner': 'TCI'})

        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')
        indicator.delete(params={'owner': 'TCI'})
        # End Snippet

    def test_address_delete_attribute(self):
        """Test snippet"""
        indicator = self.v3_helper.create_indicator(
            confidence=74,
            value1='111.111.111.111',
            rating=4,
            type='Address',
            attributes=[
                {
                    'type': 'Description',
                    'value': 'An example description attribute',
                },
                {
                    'type': 'Description',
                    'value': 'Another example description attribute',
                },
            ],
        )
        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')
        for attribute in indicator.attributes:
            if attribute.model.value == 'An example description attribute':
                attribute.delete()
        # End Snippet

    def test_address_remove_associations(self):
        """Test snippet"""
        indicator = self.v3_helper.create_indicator(
            value1='111.111.111.111',
            type='Address',
            associated_groups=[
                {'name': 'MyGroup0', 'type': 'Adversary'},
                {'name': 'MyGroup', 'type': 'Adversary'},
            ],
        )

        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')

        for association in indicator.associated_groups:
            if association.model.name == 'MyGroup':
                # IMPORTANT the "remove()" method will remove the association from the indicator and
                #    the "delete()" method will remove the association from the system.
                association.remove()
        # End Snippet

    def test_address_remove_security_label(self):
        """Test snippet"""
        indicator = self.v3_helper.create_indicator(
            value1='111.111.111.111',
            type='Address',
            security_labels=[
                {'name': 'TLP:WHITE'},
                {'name': 'TLP:GREEN'},
            ],
        )

        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')

        for security_label in indicator.security_labels:
            if security_label.model.name == 'TLP:WHITE':
                # IMPORTANT the "remove()" method will remove the security label from the indicator and
                #    the "delete()" method will remove the security label from the system.
                security_label.remove()
        # End Snippet

    def test_address_remove_tag(self):
        """Test snippet"""
        indicator = self.v3_helper.create_indicator(
            value1='111.111.111.111',
            type='Address',
            tags={'name': 'Example-Tag'},
        )

        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')

        for tag in indicator.tags:
            if tag.model.name == 'Example-Tag':
                # IMPORTANT the "remove()" method will remove the tag from the indicator and
                #    the "delete()" method will remove the tag from the system.
                tag.remove()
        # End Snippet

    def test_address_update(self):
        """Test snippet"""
        indicator = self.tcex.v3.indicator(
            confidence=74,
            ip='111.111.111.111',
            rating=4,
            type='Address',
        )
        indicator.create(params={'owner': 'TCI'})

        # Begin Snippet
        indicator = self.tcex.v3.indicator(summary='111.111.111.111')
        # This will update the confidence to "50"
        indicator.model.confidence = 50
        indicator.update(params={'owner': 'TCI'})
        # End Snippet
