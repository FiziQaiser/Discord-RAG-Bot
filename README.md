# Discord RAG Bot

![Bot Status](https://img.shields.io/badge/status-online-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-yellow)
![Chroma DB](https://img.shields.io/badge/Chroma_DB-Integrated-orange)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Commands](#commands)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)

## Introduction

This bot is an automated customer sales representative designed for Discord servers. It uses a Retrieval-Augmented Generation (RAG) model to answer user queries based on the content of uploaded PDF files. The bot is built using `discord.py`. It is simple to use and provides a seamless experience for server members looking for quick and accurate information.


## Features

- **LLaMA3 Model Integration:** Utilizes the LLaMA3-70B model for generating contextually relevant responses based on PDF content.
- **LangChain Integration:** Leverages LangChain for document processing, text splitting, and chaining responses.
- **ChromaDB:** Stores and retrieves document embeddings using ChromaDB for efficient similarity searches.
- **Automated Support:** Acts as a customer sales representative, providing detailed responses directly from PDFs.
- **Discord Integration:** Built using `discord.py`, making it easy to integrate and use within Discord servers.


## Setup

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Create A Discord Bot and get its token (you can get this from the [Discord Developer Portal](https://discord.com/developers/applications))
- A Groq Api Key (you can get this from [Groq Dashboard](https://console.groq.com/playground))

### Creating a Discord Bot

To use this bot in your Discord server, you'll first need to create a Discord bot through the Discord Developer Portal. Follow these steps to get started:

#### Step 1: Create a New Application

1. **Go to the [Discord Developer Portal](https://discord.com/developers/applications)**.
2. Click on the "New Application" button.
3. Enter a name for your application (e.g., "CSR Bot") and click "Create".

#### Step 2: Configure Bot Permissions
1. Select the bot tab from the menu
2. In the left-hand menu select **Installation**
3. Scroll down to the **Guild Install** section
5. Under **Scopes**, select `bot` and `applications.commands`.
6. Under **Permissions**, select the following permissions:
   - `Attach Files`
   - `Manage Channels`
   - `Manage Messages`
   - `Read Message History`
   - `Send Messages`
   - `Use Slash Commands`
   - `View Channels`
   - `View Audit Log`

   These permissions are essential for the bot to function properly within your server, allowing it to send and manage messages, view channels, and use slash commands.

5. Copy the Install Link open it in a new browser tab.

#### Step 3: Invite the Bot to Your Server

1. Paste the Install Link you copied into your browser and press Enter.
2. Choose the server you want to add the bot to from the dropdown list.
3. Click "Authorize" and complete the CAPTCHA.

#### Step 4: Retrieve Your Bot Token

1. In the **Bot** section, under "Token", click on "Reset Token" to generate a new token.
2. Copy the token to a secure location; this token is your bot's password and should be kept secret.
3. Your bot should be ready to use now.


### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/fiziqaiser/Discord-RAG-Bot.git
    cd Discord-RAG-Bot
    ```

2. **Create a Python 3.11 virtual environment**:

    ```bash
    python3.11 -m venv venv
    ```

3. **Activate the virtual environment**:

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the environment variables**:

    Rename the `example.env` file to `.env` and fill in the following variables:

    ```env
    TOKEN=your_discord_bot_token
    GROQ_API_KEY=your_api_key
    ```

6. **Set up the configuration file**:

    Edit the `config.json` file to match your server's needs. For example:

    ```json
    {
        "bot_name": "CSR",
        "bot_image": "https://cdn.discordapp.com/attachments/1187679514684293181/1272568651563925524/images.png?ex=66bb7369&is=66ba21e9&hm=01cfab7d3ea7ffdde59b6b6b858a59bc277416d5b4aaddf53c61bb5cc21ebafe&",
        "prefix": ">>",
        "support_server_url": "https://discord.gg/kTavknSvrZ",
        "presence_activity": "to your queries.",
        "bot_primary_color": "3c76fa",
        "embed_footer": "Made with love by @fizzy.py"
    }
    ```

7. **Run the bot**:

    ```bash
    python main.py
    ```

## Usage

Once the bot is running, it will automatically sync commands with your Discord server. You can begin uploading PDFs and querying the bot immediately.

## Commands


##### 1. `/upload_file`
- **Description:** Upload a PDF file that the bot will use to answer queries.
- **Usage:** `/upload_file [file]`

##### 2. `/query`
- **Description:** Query the bot with a question. The bot will respond based on the content of the uploaded PDF.
- **Usage:** `/query [your question]`

## Configuration

The bot is highly configurable through the `config.json` file. Here are some key settings:

- `bot_name`: The display name of the bot (default is "CSR").
- `bot_image`: The URL for the bot's thumbnail image.
- `prefix`: The command prefix for the bot (default is `>>`).
- `presence_activity`: The bot's presence status (default is "to your queries.").
- `support_server_url`: Link to your support server for users to join if they need help.
- `bot_primary_color`: The color used in embed messages (default is `3c76fa`).
- `embed_footer`: The footer text displayed in embed messages (default is "Made with love by @fizzy.py").


## Logging

The bot includes a logging system that tracks important events such as when the bot joins or leaves a server. Logs are stored in a dedicated directory and can be customized in the code.

## Contributing

Contributions are welcomed from the community. If you'd like to contribute, please fork the repository and submit a pull request with your changes. Make sure to follow the project's coding standards and conventions.
