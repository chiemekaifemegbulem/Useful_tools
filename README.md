# Advanced Web Scraper

## Overview

This is an advanced web scraping tool built with Python. It is designed to efficiently extract structured data from web pages while handling various challenges like CAPTCHA, dynamic content, and IP blocking.

## Features

- **Proxy Support:** Uses a rotating list of proxies to prevent IP bans.
- **User-Agent Rotation:** Randomized user agents to mimic real users.
- **CAPTCHA Solving:** Integrates with 2Captcha for bypassing CAPTCHA challenges.
- **Tor Integration:** Optionally routes requests through the Tor network.
- **Retries and Timeout Handling:** Ensures resilience against connection failures.
- **JavaScript Rendering Support:** Uses Selenium with undetected ChromeDriver for scraping JavaScript-heavy websites.
- **Multi-threaded Scraping:** Utilizes threading for faster data extraction.
- **Automatic Data Deduplication:** Ensures only new data is stored.
- **JSON Storage:** Saves extracted data in JSON format.

## Installation

### Prerequisites

Ensure you have Python 3 installed. Then, install the required dependencies:

```sh
pip install requests beautifulsoup4 fake-useragent undetected-chromedriver selenium twocaptcha stem
```

### Setting Up Tor (Optional for Anonymity)

1. Install Tor and run it.
2. Add your Tor password to the script.
3. Ensure Tor is listening on port 9051.

## Usage

Run the script with:

```sh
python scraper.py
```

Modify the `base_url` in `main()` to scrape different websites.

## Contributing

We welcome contributions! Here’s how you can help:

- Improve proxy rotation mechanisms.
- Enhance JavaScript rendering efficiency.
- Add support for more CAPTCHA-solving services.
- Extend the scraper to handle more complex data structures.

### How to Contribute

1. Fork this repository.

2. Create a feature branch:

   ```sh
   git checkout -b feature-name
   ```

3. Commit your changes:

   ```sh
   git commit -am 'Add new feature'
   ```

4. Push to the branch:

   ```sh
   git push origin feature-name
   ```

5. Open a Pull Request.

## License

This project is open-source under the MIT License.

## Contact

For suggestions or issues, please open an issue or reach out on GitHub.

