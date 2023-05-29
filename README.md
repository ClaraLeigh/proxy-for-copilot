# Custom Proxy for GitHub Copilot Chat

This custom proxy forwards HTTP requests to their original destination, except when talking to the CoPilot chat endpoints. When it finds that endpoint it modifies the request to use GPT-4 using the main openai endpoint.

## Requirements

- Python 3.6 or higher
- mitmproxy
- python-dotenv

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/custom-proxy.git
cd custom-proxy
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual API key.

## Usage

1. Start the proxy server:

```bash
mitmdump -s proxy.py -p 8090
```

This command starts the proxy server on port 8090.

2. Configure your application to use the proxy server by setting the `HTTP_PROXY` and `HTTPS_PROXY` environment variables to `http://localhost:8090`.

3. Run your application, and the proxy will intercept and modify the specified requests as described.

## License

This project is licensed under the [MIT License](LICENSE).
