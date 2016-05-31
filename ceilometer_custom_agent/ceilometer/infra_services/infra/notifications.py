#
# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Handler for producing network counter messages from Neutron notification
   events.

"""

import oslo.messaging
from oslo_config import cfg

from ceilometer.agent import plugin_base
from ceilometer.openstack.common import log
from ceilometer import sample

OPTS = [
    cfg.StrOpt('infraservice_control_exchange',
               default='infraservice',
               help="Exchange name for INFRA notifications."),
]

cfg.CONF.register_opts(OPTS)

LOG = log.getLogger(__name__)


class INFRANotificationBase(plugin_base.NotificationBase):

    resource_name = None

    @staticmethod
    def get_targets(conf):
        """Return a sequence of oslo.messaging.Target

        This sequence is defining the exchange and topics to be connected for
        this plugin.
        """
        LOG.info("get_targets for INFRA Notification Listener")
        return [oslo.messaging.Target(topic=topic,
                                      exchange=conf.infraservice_control_exchange)
                for topic in conf.notification_topics]

class INFRANotification(INFRANotificationBase):

    resource_name = None
    event_types = ['infra$']

    def process_notification(self, message):
        LOG.info('Received INFRA notification: vcpe_id=%(vcpe_id)s' % {'vcpe_id': message['payload']['resource_id']})
        yield sample.Sample.from_notification(
            name='vsg',
            type=sample.TYPE_GAUGE,
            unit='vsg',
            volume=1,
            user_id=message['payload']['user_id'],
            project_id=message['payload']['project_id'],
            resource_id=message['payload']['resource_id'],
            message=message)
