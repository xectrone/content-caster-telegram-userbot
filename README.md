# Content Caster Userbot

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Pyrogram](https://img.shields.io/badge/pyrogram-1.4.2-blue)

**Content Caster** is a versatile userbot designed to schedule and repost messages from one Telegram chat to another. It offers seamless content management across your Telegram channels and groups.

## Key Features

- **Message Scheduling**: Schedule messages from one chat to be reposted in another chat at specified times.
- **Media Handling**: Supports text, photos, videos, and documents for scheduled posts.
- **Flexible Configuration**: Customize start times, intervals, and destination chats for scheduled messages.
- **Error Handling**: Robust error management to handle interruptions and schedule discrepancies gracefully.

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Dependencies](#2-install-dependencies)
  - [Configuration](#3-configuration)
  - [Running the Userbot](#4-running-the-userbot)
- [Usage](#usage)
  - [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/).
- **Telegram API Credentials**: Obtain API credentials (API ID, API HASH, and phone number) from [Telegram's website](https://my.telegram.org/auth).

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/xectrone/content-caster-telegram-userbot.git
cd content-caster-telegram-userbot
```

### 2. Install Dependencies

Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NO=your_phone_number
```

### 4. Running the Userbot

Start the userbot by running:

```bash
python main.py
```

## Usage

### Commands

- `/start` - Start the userbot and receive a welcome message.
- `/help` - Display available commands and usage instructions.
- `/schedule <src_chat_id> <dest_chat_id> <start_message_id> <end_message_id> <start_time (YYYY-MM-DD-HH:MM:SS)> <interval in hrs>` - Schedule messages from `src_chat_id` to `dest_chat_id` starting from `start_message_id` to `end_message_id` at specified intervals.

## Contributing

Contributions are welcome! If you have suggestions or want to contribute improvements, please fork the repository and submit a pull request. Feel free to open issues for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
