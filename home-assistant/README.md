# EstWarden Home Assistant Integration

Turn your smart home into a security-aware home. Display Baltic threat level on your dashboard, automate lights based on threat changes, get spoken alerts.

## Sensors

### REST Sensor — Threat Level

Add to `configuration.yaml`:

```yaml
rest:
  - resource: https://estwarden.eu/api/threat-index
    scan_interval: 900  # 15 minutes
    sensor:
      - name: "Baltic Threat Level"
        value_template: "{{ value_json.level }}"
        json_attributes:
          - score
          - date

      - name: "Baltic Threat Score"
        value_template: "{{ value_json.score | round(1) }}"
        unit_of_measurement: "/100"

  - resource: https://estwarden.eu/api/today
    scan_interval: 1800
    sensor:
      - name: "Baltic Daily Summary"
        value_template: "{{ value_json.summary[:250] }}"
```

### Template Sensor — Threat Color

```yaml
template:
  - sensor:
      - name: "Baltic Threat Color"
        state: >
          {% set level = states('sensor.baltic_threat_level') %}
          {% if level == 'GREEN' %}#22c55e
          {% elif level == 'YELLOW' %}#eab308
          {% elif level == 'ORANGE' %}#f97316
          {% elif level == 'RED' %}#ef4444
          {% else %}#6b7280{% endif %}
```

## Dashboard Card

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: >
      ## 🛡 Baltic Security
      **{{ states('sensor.baltic_threat_level') }}** — {{ states('sensor.baltic_threat_score') }}/100

      {{ states('sensor.baltic_daily_summary') }}

      [Full Report](https://estwarden.eu)

  - type: gauge
    entity: sensor.baltic_threat_score
    name: Composite Threat Index
    min: 0
    max: 100
    severity:
      green: 0
      yellow: 25
      red: 50
```

## Automations

### Notify on Threat Level Change

```yaml
automation:
  - alias: "Baltic Threat Alert"
    trigger:
      - platform: state
        entity_id: sensor.baltic_threat_level
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state != trigger.from_state.state }}"
    action:
      - service: notify.mobile_app
        data:
          title: "🛡 Baltic Threat Level Changed"
          message: >
            {{ trigger.from_state.state }} → {{ trigger.to_state.state }}
            Score: {{ state_attr('sensor.baltic_threat_level', 'score') }}/100
```

### Red Alert — Flash Lights

```yaml
automation:
  - alias: "Baltic Red Alert"
    trigger:
      - platform: state
        entity_id: sensor.baltic_threat_level
        to: "RED"
    action:
      - service: light.turn_on
        target:
          area_id: living_room
        data:
          color_name: red
          brightness: 255
      - delay: "00:00:03"
      - service: light.turn_on
        target:
          area_id: living_room
        data:
          color_name: white
```

### Daily Briefing via TTS

```yaml
automation:
  - alias: "Morning Baltic Briefing"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: tts.speak
        target:
          entity_id: media_player.kitchen_speaker
        data:
          message: >
            Good morning. Baltic threat level is {{ states('sensor.baltic_threat_level') }},
            score {{ states('sensor.baltic_threat_score') }} out of 100.
            {{ states('sensor.baltic_daily_summary')[:200] }}
```
