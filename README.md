# MorningRodComponent
Custom Component for MorningRod

files need to be saved to {home assistant config directory}/custom_component/morning_rod


:Usage in configuration.yaml
```yaml
cover:
  - platform: morning_rod
    covers:
      blind0:
        code: <token_string for blind0>
        name: blind_name
      blind1:
        code: <token_string for blind1>
        name: blind_name
```
