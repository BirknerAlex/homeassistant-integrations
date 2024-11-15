# Home Assistant Integration for 1KOMMA5GRAD

## Work in Progress

This integration is still in development and not yet ready for production use.

Feel free to contribute to this project, raise issues or submit pull
requests to improve and help finishing the integration.

## Good to know

The 1KOMMA5GRAD API is not officially documented and may change at any time.
Use mitmproxy or similar tools to intercept the API calls from the official app
to get an idea of the API structure.

## Current state

- [x] Login
- [x] Get all systems (Heartbeat instances)
- [ ] Read current import power pricing
- [ ] Read and manage of heat pumps
- [ ] Read and manage of photovoltaic systems
- [ ] Read and manage of battery systems
- [ ] Read and manage of electric vehicle charging stations

### Development Setup

Documented for macOS, but should be similar for other operating systems.

```bash
brew install python3 autoconf ffmpeg cmake make

pip install -r requirements.txt
```