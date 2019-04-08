# -*- coding: utf-8 -*-
"""ThreatConnect TI Generic Mappings Object"""
import json
from tcex.tcex_ti.tcex_ti_tc_request import TiTcRequest
from tcex.tcex_utils import TcExUtils


class TIMappings(object):
    """Common API calls for for Indicators/SecurityLabels/Groups and Victims"""

    def __init__(self, tcex, main_type, api_type, sub_type, api_entity):
        """Initialize Class Properties.

        Args:
            tcex:
            main_type:
            api_type:
            sub_type:
            api_entity:
        """
        self._tcex = tcex
        self._data = {}

        self._type = main_type
        self._api_sub_type = sub_type
        self._api_type = api_type
        self._unique_id = None
        self._api_entity = api_entity

        self._utils = TcExUtils()
        self._tc_requests = TiTcRequest(self._tcex)

    @property
    def type(self):
        """Return main type."""
        return self._type

    @property
    def api_sub_type(self):
        """Return sub type."""
        return self._api_sub_type

    @property
    def unique_id(self):
        """Return unique id."""
        return self._unique_id

    @property
    def tc_requests(self):
        """Return tc request object."""
        return self._tc_requests

    @property
    def api_type(self):
        """Return api type."""
        return self._api_type

    @property
    def api_entity(self):
        """Return api entity."""
        return self._api_entity

    @api_entity.setter
    def api_entity(self, api_entity):
        """
        Sets the Api Entity
        Args:
            api_entity:

        Returns:

        """
        self._api_entity = api_entity

    @api_type.setter
    def api_type(self, api_type):
        """
        Sets the Api Type
        Args:
            api_type:

        Returns:

        """
        self._api_type = api_type

    @tc_requests.setter
    def tc_requests(self, tc_requests):
        """
        Sets the Tc Request Object
        Args:
            tc_requests:

        Returns:

        """
        self._tc_requests = tc_requests

    @api_sub_type.setter
    def api_sub_type(self, sub_type):
        """
        Sets the Api Sub Type
        Args:
            sub_type:

        Returns:

        """
        self._api_sub_type = sub_type

    @unique_id.setter
    def unique_id(self, unique_id):
        """
        Sets the Unique Id
        Args:
            unique_id:

        Returns:

        """
        self._unique_id = unique_id

    @property
    def data(self):
        """Return data."""
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data
        Args:
            data:

        Returns:

        """
        self._data = data

    def create(self, owner):
        """
        Creates the Indicator/Group/Victim or Security Label given Owner

        Args:
            owner: The owner for the created object
        """
        if not self.can_create():
            self._tcex.handle_error(905, [self.type])

        response = self.tc_requests.create(self.api_type, self.api_sub_type, self._data, owner)

        if self.tc_requests.success(response):
            self._set_unique_id(response.json().get('data').get(self.api_entity))

        return response

    def delete(self, owner=None):
        """
        Deletes the Indicator/Group/Victim or Security Label
        """
        if not self.can_delete():
            self._tcex.handle_error(915, [self.type])

        return self.tc_requests.delete(
            self.api_type, self.api_sub_type, self.unique_id, owner=owner
        )

    def update(self, owner=None):
        """
        Updates the Indicator/Group/Victim or Security Label
        """
        if not self.can_update():
            self._tcex.handle_error(905, [self.type])

        return self.tc_requests.update(
            self.api_type, self.api_sub_type, self.unique_id, self._data, owner=owner
        )

    def single(self, owner=None, filters=None, params=None):
        """
        Gets the Indicator/Group/Victim or Security Label
        Args:
            owner:
            filters:
            params: parameters to pass in to get the object

        Returns:

        """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.single(
            self.api_type,
            self.api_sub_type,
            self.unique_id,
            filters=filters,
            owner=owner,
            params=params,
        )

    def many(self, owner=None, filters=None, params=None):
        """
        Gets the Indicator/Group/Victim or Security Labels
        Args:
            filters:
            owner:
            params: parameters to pass in to get the objects

        Yields: A Indicator/Group/Victim json

        """
        for i in self.tc_requests.many(
            self.api_type,
            self.api_sub_type,
            self.api_entity,
            owner=owner,
            filters=filters,
            params=params,
        ):
            yield i

    def request(self, result_limit, result_start, owner=None, filters=None, params=None):
        """
        Gets the Indicator/Group/Victim or Security Labels
        Args:
            filters:
            owner:
            result_limit:
            result_start:
            params: parameters to pass in to get the objects

        Returns:

        """
        return self.tc_requests.request(
            self.api_type,
            self.api_sub_type,
            result_limit,
            result_start,
            owner=owner,
            filters=filters,
            params=params,
        )

    def tags(self, owner=None, filters=None, params=None):
        """
         Gets the tags from a Indicator/Group/Victim/Security Labels
         Args:
             filters:
             owner:
             params: parameters to pass in to get the objects

         Yields: A tag json

         """

        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        for t in self.tc_requests.tags(
            self.api_type,
            self.api_sub_type,
            self.unique_id,
            owner=owner,
            filters=filters,
            params=params,
        ):
            yield t

    def tag(self, name, action='ADD', params=None):
        """
         Adds a tag to a Indicator/Group/Victim/Security Label
         Args:
             params:
             action:
             name: The name of the tag

         """
        if not name:
            self._tcex.handle_error(925, ['name', 'tag', 'name', 'name', name])

        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if action == 'GET':
            return self.tc_requests.tag(
                self.api_type, self.api_sub_type, self.unique_id, name, action=action, params=params
            )

        if action == 'ADD':
            return self.tc_requests.tag(
                self.api_type, self.api_sub_type, self.unique_id, name, action=action
            )

        if action == 'DELETE':
            return self.tc_requests.tag(
                self.api_type, self.api_sub_type, self.unique_id, name, action=action
            )
        self._tcex.handle_error(925, ['action', 'tag', 'action', 'action', action])
        return None

    def add_tag(self, name):
        """
         Adds a tag to a Indicator/Group/Victim/Security Label
         Args:
             name: The name of the tag

         """
        return self.tag(name, action='ADD')

    def get_tag(self, name, params=None):
        """
         Gets a tag from a Indicator/Group/Victim/Security Label
         Args:
             name: The name of the tag
             params:
         """
        return self.tag(name, action='GET', params=params)

    def delete_tag(self, name):
        """
         Deletes a tag from a Indicator/Group/Victim/Security Label
         Args:
             name: The name of the tag
         """

        return self.tag(name, action='DELETE')

    def labels(self, owner=None, filters=None, params=None):
        """
         Gets the security labels from a Indicator/Group/Victim

         Yields: A Security label

         """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        for l in self.tc_requests.labels(
            self.api_type,
            self.api_sub_type,
            self.unique_id,
            owner=owner,
            filters=filters,
            params=params,
        ):
            yield l

    def label(self, label, action='ADD', params=None):
        """
         Adds a Security Label to a Indicator/Group or Victim
         Args:
             params:
             label: The name of the Security Label
             action:

         """

        if params is None:
            params = {}

        if not label:
            self._tcex.handle_error(925, ['label', 'Security Label', 'label', 'label', label])

        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if action == 'GET':
            return self.tc_requests.get_label(
                self.api_type, self.api_sub_type, self.unique_id, label, params=params
            )

        if action == 'ADD':
            return self.tc_requests.add_label(
                self.api_type, self.api_sub_type, self.unique_id, label
            )

        if action == 'DELETE':
            return self.tc_requests.delete_tag(
                self.api_type, self.api_sub_type, self.unique_id, label
            )

        self._tcex.handle_error(925, ['action', 'label', 'action', 'action', action])
        return None

    def add_label(self, label):
        """
         Adds a label to a Indicator/Group/Victim
         Args:
             label: The name of the Security Label
         """
        return self.label(label, action='ADD')

    def get_label(self, label, params=None):
        """
         Gets a security label from a Indicator/Group/Victim
         Args:
             label: The name of the Security Label
             params:
         """
        return self.label(label, action='GET', params=params)

    def delete_label(self, label):
        """
         Deletes a security label from a Indicator/Group/Victim
         Args:
             label: The name of the Security Label
         """
        return self.label(label, action='DELETE')

    def indicator_associations(self, params=None):
        """
         Gets the indicator association from a Indicator/Group/Victim

         Yields: Indicator Association

         """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if params is None:
            params = {}

        for ia in self.tc_requests.indicator_associations(
            self.api_type, self.api_sub_type, self.unique_id, params=params
        ):
            yield ia

    def group_associations(self, params=None):
        """
         Gets the group association from a Indicator/Group/Victim

         Yields: Group Association

         """
        if params is None:
            params = {}

        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        for ga in self.tc_requests.group_associations(
            self.api_type, self.api_sub_type, self.unique_id, params=params
        ):
            yield ga

    def victim_asset_associations(self, params=None):
        """
         Gets the victim asset association from a Indicator/Group/Victim

         Yields: Victim Association json

         """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.victim_asset_associations(
            self.api_type, self.api_sub_type, self.unique_id, params=params
        )

    def indicator_associations_types(
        self, indicator_type, api_entity=None, api_branch=None, params=None
    ):
        """
        Gets the indicator association from a Indicator/Group/Victim

        Args:
            indicator_type:
            api_entity:
            api_branch:
            params:

        Returns:

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        target = self._tcex.ti.indicator(indicator_type)
        for at in self.tc_requests.indicator_associations_types(
            self.api_type,
            self.api_sub_type,
            self.unique_id,
            target,
            api_entity=api_entity,
            api_branch=api_branch,
            params=params,
        ):
            yield at

    def group_associations_types(self, group_type, api_entity=None, api_branch=None, params=None):
        """
        Gets the group association from a Indicator/Group/Victim

        Args:
            group_type:
            api_entity:
            api_branch:
            params:

        Returns:

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        target = self._tcex.ti.group(group_type)

        for gat in self.tc_requests.group_associations_types(
            self.api_type,
            self.api_sub_type,
            self.unique_id,
            target,
            api_entity=api_entity,
            api_branch=api_branch,
            params=params,
        ):
            yield gat

    def victim_asset_associations_type(self, victim_asset_type, params=None):
        """
        Gets the victim association from a Indicator/Group/Victim

        Args:
            victim_asset_type:
            params:

        Returns:

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.victim_asset_associations(
            self.api_type, self.api_sub_type, self.unique_id, victim_asset_type, params=params
        )

    def add_association(self, target, api_type=None, api_sub_type=None, unique_id=None):
        """
        Adds a association to a Indicator/Group/Victim

        Args:
            target:
            api_type:
            api_sub_type:
            unique_id:

        Returns:

        """
        api_type = api_type or target.api_type
        api_sub_type = api_sub_type or target.api_sub_type
        unique_id = unique_id or target.unique_id
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if not target.can_update():
            self._tcex.handle_error(910, [target.type])

        return self.tc_requests.add_association(
            self.api_type, self.api_sub_type, self.unique_id, api_type, api_sub_type, unique_id
        )

    def delete_association(self, target, api_type=None, api_sub_type=None, unique_id=None):
        """
        Deletes a association from a Indicator/Group/Victim

        Args:
            target:
            api_type:
            api_sub_type:
            unique_id:

        Returns:

        """
        api_type = api_type or target.api_type
        api_sub_type = api_sub_type or target.api_sub_type
        unique_id = unique_id or target.unique_id
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if not target.can_update():
            self._tcex.handle_error(910, [target.type])

        return self.tc_requests.delete_association(
            self.api_type, self.api_sub_type, self.unique_id, api_type, api_sub_type, unique_id
        )

    def add_observers(self, count, date_observed):
        """
        Adds a Indicator Observation

        Args:
            count:
            date_observed:

        """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        data = {
            'count': count,
            'dataObserved': self._utils.format_datetime(
                date_observed, date_format='%Y-%m-%dT%H:%M:%SZ'
            ),
        }

        return self.tc_requests.observations(self.api_type, self.api_sub_type, self.unique_id, data)

    def add_false_positive(self):
        """
        Adds a Indicator FalsePositive
        """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.add_false_positive(self.api_type, self.api_sub_type, self.unique_id)

    def attributes(self, params=None):
        """
        Gets the attributes from a Group/Indicator or Victim

        Yields: attribute json

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        for a in self.tc_requests.attributes(
            self.api_type, self.api_sub_type, self.unique_id, params=params
        ):
            yield a

    def attribute(self, attribute_id, action='GET', params=None):
        """
        Gets the attribute from a Group/Indicator or Victim


        Args:
            action:
            params:
            attribute_id:

        Returns: attribute json

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if action == 'GET':
            return self.tc_requests.get_attribute(
                self.api_type, self.api_sub_type, self.unique_id, attribute_id, params=params
            )

        if action == 'DELETE':
            return self.tc_requests.delete_attribute(
                self.api_type, self.api_sub_type, self.unique_id, attribute_id
            )

        self._tcex.handle_error(925, ['action', 'attribute', 'action', 'action', action])
        return None

    def add_attribute(self, attribute_type, attribute_value):
        """
        Adds a attribute to a Group/Indicator or Victim


        Args:
            attribute_type:
            attribute_value:

        Returns: attribute json

        """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.add_attribute(
            self.api_type, self.api_sub_type, self.unique_id, attribute_type, attribute_value
        )

    def attribute_labels(self, attribute_id, params=None):
        """
        Gets the security labels from a attribute

        Yields: Security label json

        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        for al in self.tc_requests.attribute_labels(
            self.api_type, self.api_sub_type, self.unique_id, attribute_id, params=params
        ):
            yield al

    def attribute_label(self, attribute_id, label, action='GET', params=None):
        """
        Gets a security labels from a attribute

        Args:
            attribute_id:
            label:
            action:
            params:

        Returns: Security label json
        """
        if params is None:
            params = {}
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        if action == 'GET':
            return self.tc_requests.get_attribute_label(
                self.api_type, self.api_sub_type, self.unique_id, attribute_id, label, params=params
            )
        if action == 'DELETE':
            return self.tc_requests.delete_attribute_label(
                self.api_type, self.api_sub_type, self.unique_id, attribute_id, label
            )

        self._tcex.handle_error(925, ['action', 'attribute_label', 'action', 'action', action])
        return None

    def add_attribute_label(self, attribute_id, label):
        """
        Adds a security labels to a attribute

        Args:
            attribute_id:
            label:

        Returns: A response json
        """
        if not self.can_update():
            self._tcex.handle_error(910, [self.type])

        return self.tc_requests.add_attribute_label(
            self.api_type, self.api_sub_type, self.unique_id, attribute_id, label
        )

    @property
    def _base_request(self):
        """ Returns: A common dict for requests"""
        return {'unique_id': self.unique_id, 'type': self.api_type, 'sub_type': self.api_sub_type}

    def can_create(self):  # pylint: disable=R0201
        """ Determines if the object can be created. """
        return True

    def can_delete(self):
        """ Determines if the object can be deleted. """
        if self.unique_id:
            return True
        return False

    def can_update(self):
        """ Determines if the object can be updated. """
        if self.unique_id:
            return True
        return False

    @staticmethod
    def is_indicator():
        """ Determines if the object is a Indicator. """
        return False

    @staticmethod
    def is_group():
        """ Determines if the object is a Group. """
        return False

    @staticmethod
    def is_victim():
        """ Determines if the object is a Victim. """
        return False

    @staticmethod
    def is_tag():
        """ Determines if the object is a Tag. """
        return False

    @staticmethod
    def is_security_label():
        """ Determines if the object is a Security Label. """
        return False

    @staticmethod
    def is_task():
        """ Determines if the object is a Task. """
        return False

    def _set_unique_id(self, json_response):
        """ Sets the Unique Id given a json """
        self.unique_id = json_response.get('id', '')

    def __str__(self):
        """Return string representation of object."""
        return json.dumps(self.data, indent=4)
