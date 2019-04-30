# loudml-plugin-slack

Slack Plugin for LoudML 1.5

# Installation

```bash
./setup.py install
```
# Static configuration

Copy slack.yml file to LoudML configuration directory:

```
cp slack.yml /etc/loudml/plugins.d/
```

Edit `/etc/loudml/plugins.d/slack.yml` to configure the Channel name and Slack API token.

# Hook configuration

Edit `slack.json` for the template.

Create hook on LoudML instance:
 ```
curl -X PUT -H 'Content-Type: application/json' localhost:8077/models/my-model -d @slack.json
```
