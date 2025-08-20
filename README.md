# Weather App

A simple weather application written in Python that retrieves and displays current weather information for a given location using a public weather API.

### Languages
![Python](https://img.shields.io/badge/-Python-FFD43B?style=flat&logo=python&logoColor=blue)
## Tools & Libraries

- **Requests:** For making HTTP requests to the weather API.
- **Pillow:** For handling weather-related images.
- **python-dotenv:** For managing environment variables and API keys.
- **OpenWeatherMap API:** Provides current weather data.
- **Command Line Interface:** For user input/output.
- **tkinter:** (Optional) For GUI development.
- **black:** (Optional) For code formatting.
- **flake8:** (Optional) For code linting.


## Features

- Get current weather data for any city or location
- Easy-to-use command line interface
- Uses a public weather API (e.g., OpenWeatherMap)
- Clean, beginner-friendly code

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Requests library (`pip install requests`)
- An API key from [OpenWeatherMap](https://openweathermap.org/api) 

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/arrexha/weather-app.git
    cd weather-app
    ```

2. Install dependencies:
    ```bash
    pip install requests
    ```

3. Add your API key:
    - Open `Weather App.py` and replace `API_KEY` with your actual API key.

### Usage

Run the app from the terminal:
```bash
python "Weather App.py"
```
- Enter the city name when prompted.
- View the current weather information.

## Example Output

```
Enter city name: London
Weather in London:
Temperature: 18°C
Humidity: 65%
Condition: Clear sky
```

## Customization

- You can change the weather API or add more features such as forecast, error handling, or a GUI.

## Contributing

Pull requests are welcome! Please open an issue or submit a PR for suggestions or improvements.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/)
- Python requests library
- Pillow
- python-dotenv
