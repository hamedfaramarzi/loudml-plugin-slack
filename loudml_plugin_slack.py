
import logging
import json
from slacker import Slacker

from loudml.api import (
    Hook,
    Plugin,
)

from voluptuous import (
    All,
    Any,
    Invalid,
    Optional,
    Required,
    Schema,
)


class SlackPlugin(Plugin):
    """
    LoudML Slack plug-in
    """

    # Optional class to be defined if the plug-in requires an initialization
    # on LoudML start up. If no initialization is needed, get rid of it.

    CONFIG_SCHEMA = Schema({
        Required('slack'): Schema({
            Required('token'): str,
            Required('channel'): str,
        }),
    })

    def __init__(self, name, config_dir, *args, **kwargs):

        # Load and validate plug-in configuration from
        # /etc/loudml/plugins.d/<plugin name>.yml
        super().__init__(name, config_dir, *args, **kwargs)

        # ... put here additional initialization actions ...
        self.slack = Slacker(self.config['slack']['token'])



    @classmethod
    def validate(cls, config):
        """
        Validate and sanitize plug-in static configuration
        """

        # Validate configuration against the schema
        config = super().validate(config)

        # ... put here additional validation if needed ...

        # Return sanitized configuration
        return config


class SlackHook(Hook):

    TEMPLATES = {
        'anomaly_start': {
            'color': '#FF0000',
            'content': 'Anomaly detected! date={date} score={score} reason={reason} predicted={predicted} observed={observed}',
        },
        'anomaly_end': {
            'color': '#0000FF',
            'content':  'Anomaly end date={date} score={score}',
        },
    }

    CONFIG_SCHEMA = Schema({
        Optional('templates', default=TEMPLATES): Schema({
            Optional('anomaly_start', default=TEMPLATES['anomaly_start']): {
                Optional('color', default=TEMPLATES['anomaly_start']['color']): str,
                Optional('content', default=TEMPLATES['anomaly_start']['content']): str,
            },
            Optional('anomaly_end', default=TEMPLATES['anomaly_end']): {
                Optional('color', default=TEMPLATES['anomaly_end']['color']): str,
                Optional('content', default=TEMPLATES['anomaly_end']['content']): str,
            },
        }),
    })

    @classmethod
    def validate(cls, config):
        """
        Validate and sanitize hook configuration
        """

        # Validate configuration against the schema
        config = super().validate(config)

        # ... put here additional validation if needed ...

        # Return sanitized configuration
        return config


    def send_msg(self, template_name, *args, **kwargs):
        """
        Build slack message from template and send it
        """

        plugin_cfg = SlackPlugin.instance.config

        slack_instance = SlackPlugin.instance.slack

        if plugin_cfg is None:
            logging.error("slack plug-in is not configured")
            return

        if slack_instance is None:
            logging.error("slack plug-in is not configured")
            return

        channel_cfg = plugin_cfg['slack']['channel']

        template = self.config['templates'][template_name]

        try:
            slack_instance.chat.post_message(channel_cfg, self.model['name'],
                icon_emoji=':echobot:', as_user=False, link_names=True, username='LoudML Bot', attachments= '[{"color": "' + template['color'] + '", "text": "'+ template['content'].strip().format(**kwargs) +'"}]')

            logging.info("sending alert to %s", channel_cfg)

        except Exception as e:
            logging.error("cannot send alert to %s, because %s", channel_cfg, str(e))


    def on_anomaly_start(
        self,
        dt,
        score,
        predicted,
        observed,
        anomalies,
        *args,
        **kwargs
    ):
        # Deal with anomaly notification here
        try:
            self.send_msg(
                'anomaly_start',
                date=str(dt.astimezone()),
                score=score,
                predicted=str(predicted),
                observed=str(observed),
                reason="\n".join(ano_desc),
                **kwargs
            )
        except Exception as e:
            logging.error("Error in anomaly_start.")

    def on_anomaly_end(
        self,
        dt,
        score,
        *args,
        **kwargs
    ):
        # Deal with anomaly notification here
        try:
            if (self.get_object(self.model['name']) == "alert"):
                self.send_msg(
                    'anomaly_end',
                    date=str(dt.astimezone()),
                    score=score,
                    **kwargs
                )
        except Exception as e:
            logging.error("Error in anomaly_end.")
