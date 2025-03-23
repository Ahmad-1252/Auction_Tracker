# AuctionTracker
AuctionTracker is a Python-based automation tool designed to register for auctions on the Pickles website and extract detailed auction data. It uses Selenium for web automation and Pandas for data handling. The bot can log in, navigate through auction pages, register for auctions, and extract auction details such as car information, specifications, condition reports, and images.

## Features
Login Automation: Logs into the Pickles website using provided credentials.

Auction Registration: Automatically registers for live auctions by clicking the "Bid Live" button.

Data Extraction: Extracts detailed auction data, including:

Auction time and type

Car details (make, model, etc.)

Car specifications

Condition reports

Image URLs

CSV Export: Saves extracted data to a CSV file (DataFile.csv).

Error Handling: Robust error handling with retries and exception management.

## Requirements
Python 3.x

Selenium

Pandas

Pytz

Freezegun

### Install the required libraries using:

pip install -r requirements.txt

## How It Works
Login: The bot logs into the Pickles website using the provided username and password.

Auction Registration: It navigates through auction pages, clicks the "Bid Live" button, and registers for auctions.

Data Extraction: After registration, the bot extracts detailed auction data, including car specifications, condition reports, and images.

Data Export: The extracted data is saved to a CSV file for further analysis.

## Usage
Clone the repository or download the script.

Install the required dependencies.

Update the username and password variables in the script with your Pickles login credentials.

Run the script:

python Auction_tracker.py

## Functions

### Main Functions

login_to_pickles(driver, username, password): Logs into the Pickles website.

registerAuctions(driver, link): Registers for live auctions.

get_auction_data(driver, link): Extracts auction data and saves it to a CSV file.

### Helper Functions
create_driver(proxy=None, headless=False): Initializes the Selenium WebDriver.

check_verification(driver, xpath=None): Handles verification modals.

extract_auction_details(driver): Extracts auction details.

extract_car_data(driver): Extracts car-specific data.

extract_car_specifications(driver): Extracts car specifications.

extract_condition_report_and_images(driver): Extracts condition reports and image URLs.

## Output
The script generates a CSV file (DataFile.csv) containing the following columns:

Auction Time

Auction Type

Auction Date and Time

Car Details

Car Status

Car Price

Stock Number

Car Specifications

Car Condition Report

Image URLs

### Example CSV Output
Auction Time	Auction Type	Auction Date and Time	Car Details	Car Status	Car Price	Stock Number	Car Specifications	Car Condition Report	Image URLs
10:00 AM	Live Auction	24/03/2024 10:00 AM	Toyota Corolla	Active	$15,000	12345	Make: Toyota...	Part: Engine...	[URL1, URL2]
Limitations
The script relies on the structure of the Pickles website. Changes to the website may break the bot.

Requires a stable internet connection and proper ChromeDriver setup.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [Your Name] at [your.email@example.com].


