# -*- coding: utf-8 -*-
"""Test case template for App testing."""
# flake8: noqa: F401
import os
import sys

% if app_type=='triggerservice':
import paho.mqtt.client as mqtt
% endif

import pytest
from ..profiles import profiles
% if app_type=='organization':
from tcex.testing import TestCaseJob
% elif app_type=='playbook':
from tcex.testing import TestCasePlaybook
% elif app_type=='triggerservice':
from tcex.testing import TestCaseTriggerService
% elif app_type=='webhooktriggerservice':
from tcex.testing import TestCaseWebhookTriggerService
% endif


from .custom_feature import CustomFeature  # pylint: disable=E0402
from .validate_feature import ValidateFeature  # pylint: disable=E0402

# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)  # noqa: F821; pylint: disable=E0602
    sys.setdefaultencoding('utf-8')  # pylint: disable=no-member

# get profile names
profile_names = profiles(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profiles.d'))

# TODO: move this
# instance of custom
custom = CustomFeature()


# pylint: disable=W0235,too-many-function-args
% if app_type=='organization':
class TestFeature(TestCaseJob):
% elif app_type=='playbook':
class TestFeature(TestPlaybook):
% elif app_type=='triggerservice':
class TestFeature(TestCaseTriggerService):
% elif app_type=='webhooktriggerservice':
class TestFeature(TestCaseWebhookTriggerService):
% endif
    """TcEx App Testing Template."""

    @classmethod
    def setup_class(cls):
        """Run setup logic before all test cases in this module."""
        super(TestFeature, cls).setup_class()
        if os.getenv('SETUP_CLASS') is None:
            custom.setup_class()

        % if app_type=='triggerservice':
        # uncomment the following line to use static topics
        cls.client_topic = 'client-topic-123'
        cls.server_topic = 'server-topic-123'
        % endif

    def setup_method(self):
        """Run setup logic before test method runs."""
        super(TestFeature, self).setup_method()
        if os.getenv('SETUP_METHOD') is None:
            custom.setup_method(self)

    @classmethod
    def teardown_class(cls):
        """Run setup logic after all test cases in this module."""
        super(TestFeature, cls).teardown_class()
        if os.getenv('TEARDOWN_CLASS') is None:
            custom.teardown_class()

    def teardown_method(self):
        """Run teardown logic after test method completes."""
        super(TestFeature, self).teardown_method()
        if os.getenv('TEARDOWN_METHOD') is None:
            custom.teardown_method(self)

    % if app_type=='triggerservice':
    @pytest.mark.parametrize('profile_name', profile_names)
    def test_profiles(self, profile_name):
        """Run pre-created testing profiles."""

        # profile data
        pd = self.profile(profile_name)

        # publish createConfig
        for config in pd.get('configs'):
            self.publish_create_config(config)

        # trigger custom event
        self.trigger_event(**pd.get('event_data'))

        # publish deleteConfig
        for config in pd.get('configs'):
            self.publish_delete_config(config)

        # run output variable validation
        for context in self.context_tracker:
            self.validator.tcex.default_args.tc_playbook_db_context = context
            trigger_id = self.redis_client.hget(context, '_trigger_id').decode('utf-8')
            output_data = (pd.get('outputs') or {}).get(trigger_id)
            if output_data is not None:
                ValidateFeature(self.validator).validate(output_data)

    def test_shutdown(self):
        """Run shutdown command."""
        self.publish_shutdown()
    % else:
    @pytest.mark.parametrize('profile_name', profile_names)
    def test_profiles(self, profile_name):  # pylint: disable=unused-argument
        """Run pre-created testing profiles."""
        # get profile
        pd = self.profile(profile_name)

        # check profile env
        self.check_environment(pd.get('environments', ['build']))

        # run custom test method
        custom.test_method(self, pd)

        assert self.run_profile(pd) in pd.get('exit_codes', [0])
        ValidateFeature(self.validator).validate(pd.get('outputs'))
        % if app_type=='organization':
        self.validator.threatconnect.batch(
            self.context, self.owner(pd), pd.get('validation_criteria', {})
        )
        % endif
    % endif