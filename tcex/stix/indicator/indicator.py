"""Parser for STIX Indicator Objects.

import stix2
see: https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070633
"""
# standard library
import uuid
from typing import Dict, List, Union
import itertools

# third-party
import stix2
from datetime import datetime
from dendrol import Pattern
from dendrol.lang.STIXPatternListener import STIXPatternListener
from dendrol.lang.STIXPatternParser import STIXPatternParser

# first-party
from tcex.batch import Batch
from tcex.stix import StixModel  # pylint: disable=cyclic-import


class StixIndicator(StixModel):
    """Parser for STIX Indicator Objects.

    see: https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070633
    """

    @staticmethod
    def _add_milliseconds(time):
        new_time = f'''{time.upper().replace('Z', '')}.000'''
        if time.lower().endswith('z'):
            return f'{new_time}Z'
        return new_time

    def produce(self, tc_data: Union[list, dict], **kwargs):
        """Produce a STIX Indicator from a ThreatConnect Indicator.

        Args:
            tc_data: ThreatConnect indicator(s)

        Yields:
            A STIX Indicator.
        """
        if not isinstance(tc_data, list):
            tc_data = [tc_data]

        for data in tc_data:
            _type = kwargs.get('indicator_type') or data.get('type')
            indicator_details = self.indicator_type_details.get(_type.lower())
            if not indicator_details:
                continue
            kwargs = {
                'pattern_type': 'stix',
                'lang': 'en',
                'pattern_version': '2.1',
                'type': 'indicator',
                'created': self._add_milliseconds(data.get('dateAdded')),
                'valid_from': self._add_milliseconds(data.get('dateAdded')),
                'modified': self._add_milliseconds(data.get('lastModified')),
                'name': data.get('summary'),
                'pattern': indicator_details.get('lambda')(data),
                'description': '',
                'indicator_types': ['malicious-activity'],
                'confidence': data.get('confidence', 0),
            }
            if not data.get('active', True):
                kwargs['revoked'] = True
            latest = None
            for tag in data.get('tag', []):
                kwargs.setdefault('labels', []).append(tag.get('name'))
            for security_label in data.get('securityLabel', []):
                security_label = security_label.get('name', '').strip().lower()
                if security_label in self.security_label_map:
                    kwargs.setdefault('object_marking_refs', [])
                    kwargs['object_marking_refs'].append(self.security_label_map.get(security_label))
            for attribute in data.get('attribute', []):
                if attribute.get('type').lower() == 'description':
                    value = attribute.get('value')
                    last_modified = datetime.strptime(attribute.get('lastModified'), '%Y-%m-%dT%H:%M:%SZ')
                    if attribute.get('displayed'):
                        kwargs['description'] = value
                        break
                    if not latest or last_modified > latest:
                        latest = last_modified
                        kwargs['description'] = value

            id_ = f'''{data.get('ownerName').lower()}-{_type.lower()}-{data.get('summary')}'''
            kwargs['id'] = f'indicator--{uuid.uuid5(uuid.NAMESPACE_X500, id_)}'

            # {
            #     "type": "indicator",
            #     "spec_version": "2.1",
            #     "id": "indicator--78e53a5c-9510-4a95-88b1-dbac1ee60ca5",
            #     "created": "2020-09-08T19:16:25.481964Z",
            #     "modified": "2020-09-08T19:16:25.481964Z",
            #     "name": "TCI - kqvri.com",
            #     "description": "visible description",
            #     "indicator_types": [
            #         "malicious-activity"
            #     ],
            #     "pattern": "[domain-name:value = 'kqvri.com']",
            #     "pattern_type": "stix",
            #     "pattern_version": "2.1",
            #     "valid_from": "2020-09-08T19:16:25.481964Z",
            #     "labels": [
            #         "test1"
            #     ]
            # }

            try:
                rating = str(int(data.get('rating')))
                kwargs.setdefault('labels', []).append(self.x_threat_rating_map[rating])
            except Exception:
                pass

            yield kwargs

    def consume_mappings(self, stix_data: dict):
        """Produce ThreatConnect mappings from a STIX 2.1 JSON object.

        Args:
            stix_data: STIX Indicator objects to parse.

        Returns:
            A array of indicator mappings.
        """
        pattern = Pattern(stix_data.get('pattern'))
        s = STIXListener()
        pattern.walk(s)
        mappings = []
        mappings.append(self._default_consume_handler(s.indicators))
        mappings.append(self._ip_consume_handler(s.indicators))
        mappings.append(self._file_consume_handler(s.indicators))
        mappings = list(itertools.chain(*mappings))
        return mappings

    def _file_consume_handler(self, indicators: list[dict]):
        """Produce ThreatConnect file mappings from a list of STIX 2.1 indicators

        Args:
            stix_data: STIX Indicator objects to parse.

        Returns:
            A array of indicator mappings.
        """
        file_indicators = list(filter(lambda i: 'file:hashes' in i.get('path'), indicators))

        sha256_indicators = list(
            filter(lambda i: 'SHA-156' in i.get('path').upper(), file_indicators)
        )
        sha2_indicators = list(filter(lambda i: 'SHA-1' in i.get('path').upper(), file_indicators))
        md5_indicators = list(filter(lambda i: 'MD5' in i.get('path').upper(), file_indicators))

        if len(file_indicators) <= 0:
            return []
        mappings = []
        if (
                len(file_indicators) <= 3
                and len(sha256_indicators) <= 1
                and len(sha2_indicators) <= 1
                and len(md5_indicators) <= 1
        ):
            value = ' : '.join([v.get('value') for v in file_indicators])
            mappings.append(
                {
                    'type': 'File',
                    'summary': value,
                    'confidence': '@.confidence',
                }
            )
        else:
            for i in file_indicators:
                mappings.append(
                    {
                        'type': 'File',
                        'summary': i.get('value'),
                        'confidence': '@.confidence',
                    }
                )
        return mappings

    def _ip_consume_handler(self, indicators: list[dict]):
        """Produce ThreatConnect Address/CIDR mappings from a list of STIX 2.1 indicators

        Args:
            stix_data: STIX Indicator objects to parse.

        Returns:
            A array of indicator mappings.
        """
        mappings = []
        for i in filter(lambda i: i.get('path') in ['ipv4-addr:value', 'ipv6-addr:value'], indicators):
            path = i.get('path')
            value = i.get('value')
            parse_map = None
            if path == 'ipv4-addr:value':
                if '/' in value and value.split('/')[1] != '32':  # this is a CIDR
                    parse_map = {
                        'type': 'CIDR',
                        'summary': value,
                    }
                else:  # this is an address
                    parse_map = {
                        'type': 'Address',
                        'summary': value.split('/')[0],
                    }
            elif path == 'ipv6-addr:value':
                if '/' in value and value.split('/')[1] != '128':  # this is a CIDR
                    parse_map = {
                        'type': 'CIDR',
                        'summary': value,
                    }
                else:  # this is an address
                    parse_map = {
                        'type': 'Address',
                        'summary': value.split('/')[0],
                    }
                parse_map['confidence'] = '@.confidence'
            mappings.append(parse_map)
        return mappings

    def _default_consume_handler(self, indicators: list[dict]):
        """Produce ThreatConnect URL/EmailAddress/Host/ASN mappings from a list of STIX 2.1 indicators

        Args:
            stix_data: STIX Indicator objects to parse.

        Returns:
            A array of indicator mappings.
        """

        type_map = {
            'url:value': 'URL',
            'email-addr:value': 'EmailAddress',
            'domain-name:value': 'Host',
            'autonomous-system:name': 'ASN',
        }

        mappings = []
        for i in filter(lambda i: i.get('path') in type_map.keys(), indicators):
            path = i.get('path')
            value = i.get('value')
            indicator_type = type_map.get(path)

            mappings.append(
                {
                    'type': indicator_type,
                    'summary': value,
                    'confidence': '@.confidence',
                }
            )
        return mappings


class STIXListener(STIXPatternListener):
    """Visitor for the parsed stix pattern."""

    def __init__(self):
        """Visitor for the parsed stix pattern."""
        super().__init__()
        self._indicators = []  # indicators that have been pulled out of this

    def enterPropTestEqual(self, ctx: STIXPatternParser.PropTestEqualContext):
        """Pull out path and value from statements with =.

        Args:
            ctx: the context of the equals statement.
        """
        test = ctx.getText()
        eq_index = test.index('=')
        if eq_index:
            path, value = test[:eq_index], test[(eq_index + 1):]  # noqa: E203

            self._indicators.append({'path': path.strip(), 'value': value.strip()[1:-1]})

    def enterPropTestSet(self, ctx: STIXPatternParser.PropTestParenContext):
        """Pull out path and value from statements with in (...).

        Args:
            ctx: the context of the equals statement.
        """
        text = ctx.getText()
        path, values = text.split('IN')

        path = path.strip()

        values = values[1:-1]  # strip off the surrounding parens.
        values = [v.strip()[1:-1] for v in values.split(',')]  # split on , and strip

        for value in values:
            self._indicators.append({'path': path, 'value': value})

    @property
    def indicators(self):
        """Return the indicators parsed out of this pattern."""
        return self._indicators


