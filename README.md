# RAG API Setup Guide

This guide provides instructions for setting up the RAG API project and its associated services.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
   - [Clone the Repository](#clone-the-repository)
   - [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
   - [Install Dependencies](#install-dependencies)
   - [Configure Environment Variables](#configure-environment-variables)
   - [Run Migrations](#run-migrations)
   - [Run the Development Server](#run-the-development-server)
3. [Additional Information](#additional-information)
   - [Uploading Files](#uploading-files)
   - [Querying the API](#querying-the-api)

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Git

## Project Setup

### Clone the Repository

First, clone the project repository:

```bash
git clone https://github.com/iCog-Labs-Dev/RAG-API.git
cd RAG-API
```

### Create and Activate Virtual Environment

Create a virtual environment to manage project dependencies:

```
# On Unix or MacOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

Install the required dependencies:

```
pip install -r requirements.txt
```

### Configure Environment Variables

Create a .env file in the project root directory (where manage.py is located) and set your environment variables. For example:

```
API_KEY=your-api-key
```

Make sure to replace the placeholders with your actual values.

### Run Migrations

Apply database migrations:

```
python manage.py migrate
```

### Run the Development Server

```
Start the development server:
```

The server will start at http://127.0.0.1:8000/.

### Additional Information

## Uploading Files

To upload a .txt file to the server, you can use the /upload/ endpoint. Example using curl:

```
curl -X POST -F "file=@/path/to/your/file.txt" http://127.0.0.1:8000/upload/
```

Replace /path/to/your/file.txt with the path to your file.

### Querying the API

To query the API with a text query and a method (either global or local), use the /query/ endpoint. Example using curl:

```
curl -X POST -d "text_query=your query&method_option=global" http://127.0.0.1:8000/query/
```

Replace your query with your actual query and global with the method option (global or local).