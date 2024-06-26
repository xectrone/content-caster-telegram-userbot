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
- **Telegram API Credentials**: Obtain API credentials (API ID and API HASH) from [Telegram's website](https://my.telegram.org/auth).
- **Session String**: Generate a session string using the [Session String Creator Userbot](https://github.com/xectrone/session-string-creator-telegram-userbot.git).

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

Create a `.env` file in the root directory and add the following environment variables. You can use a text editor to create and edit this file.

```plaintext
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_STRING=your_session_string
```

- **API_ID**: Your Telegram API ID.
- **API_HASH**: Your Telegram API Hash.
- **SESSION_STRING**: A session string obtained from the Session String Creator Userbot.

To generate a session string, you can use the [Session String Creator Userbot](https://github.com/xectrone/session-string-creator-telegram-userbot.git). Follow the instructions in its README to generate your session string.

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
  
  Example:
  ```bash
  /schedule 123456789 987654321 1 100 2024-06-30-10:00:00 1
  ```
  This command schedules messages from message ID 1 to 100 from chat ID `123456789` to chat ID `987654321`, starting on June 30, 2024, at 10:00 AM, with a 1-hour interval between messages.

- `/info` - Reply to a message to get its message ID and chat ID.

## Contributing

Contributions are welcome! If you have suggestions or want to contribute improvements, please fork the repository and submit a pull request. Feel free to open issues for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.