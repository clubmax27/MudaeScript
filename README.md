# Mudae Logger and Sniper

This project aims to log and automatically respond to Mudae bot events in Discord. It includes functionality for logging character rolls, tracking prices, and responding to specific events like marrying characters.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file using `pip install -r requirements.txt`.

## Usage

### MudaePrice.py

This script logs and responds to events related to character rolls and prices.

1. Change the constants relative to your needs, like which Kakeras and characters do you wish to snipe
2. Change the constants relative to the userID and channels
3. Run the bot


### MudaeLogger.py

This script logs character rolls and their attributes into a SQLite database. Similar to `MudaePrice.py`, but only does the logging part

### MudaeStats.py

This script generates statistical plots based on character prices and categories from the SQLite database.

## Configuration

Make sure to set up your Discord bot token in the respective Python files:

```python
client.run("YOUR_DISCORD_BOT_TOKEN")
```

## Running the Scripts

Run each script individually using Python:

```bash
python MudaePrice.py
python MudaeLogger.py
python MudaeStats.py
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
