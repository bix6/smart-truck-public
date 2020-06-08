# Smart Truck
This is the code I created while working as an Associate Project Manager at [Filld](https://filld.com/). I was tasked with R&D for the Smart Truck initiative. Engineering was busy so I ordered a Raspberry Pi and figured out how to talk to the Veeder Root EMR3 Fuel Meter via an RS232 Serial Connection with Python. The point of this project was to demonstrate the feasibility of the Smart Truck Concept, which it did. Before leaving, I had a working prototype truck out in the field collecting fuel data and sending it to the Filld Cloud. Initially, I managed the Pi using Linux tools like supervisord but as the project progressed I switched to [Balena](https://www.balena.io/) for better remote management. 

## Layout
- `balena-beta/` holds the most current code that ran on the prototype truck.
    - In particular `balena-beta/src/base/code`
- `experiments/` holds experiments I conducted to figure out how to talk to the Fuel Meter and measure the Pi temp.
- `docs/` holds Fuel Meter docs and a few pictures.
- `setup/` holds instructions for setting up the RasPi and Balena.