# Particle Universe

Particle Universe is a project that simulates physics of celestial objects.

## Installation

Download the requirements and the python file and then add your planets and stars as shown in the usage below.

```bash
pip install -r requirements.txt
```

## Usage

```python
from particle_universe import *

star_mass = 1.989 * 10**30
Star = Obj((width // 2, height // 2), star_mass, 696340, color="yellow")

run()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
