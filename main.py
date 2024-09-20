import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "93a1393b-8ef6-4dec-888c-b5b282348172"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-K2KMk": {
    "files": "",
    "input_value": "HI",
    "sender": "User",
    "sender_name": "User",
    "session_id": "History",
    "should_store_message": True
  },
  "ChatOutput-Mf7jU": {
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "BajajBot",
    "session_id": "History",
    "should_store_message": True
  },
  "Prompt-yoKIa": {
    "template": "Context:\n{context}\n\nChat History:\n{chat_history}\n\nYou are a Bajaj  Smart AI chatbot, provide assistance to user regarding the query.\nYou are a very understanding chatbot. \nUse the provided context for answering the question. If the answer does not exist in the context, then respond with \"Well, I am Sorry , I am not aware about this\"\n\nQuestion:\n{question}",
    "question": "",
    "context": "",
    "chat_history": ""
  },
  "Chroma-32s7h": {
    "allow_duplicates": False,
    "chroma_server_cors_allow_origins": "",
    "chroma_server_grpc_port": None,
    "chroma_server_host": "",
    "chroma_server_http_port": None,
    "chroma_server_ssl_enabled": False,
    "collection_name": "Bajaj1",
    "limit": None,
    "number_of_results": 10,
    "persist_directory": "C:\\Users\\ha\\Downloads\\Langflow\\chroma\\Bajaj",
    "search_query": "",
    "search_type": "Similarity"
  },
  "OllamaEmbeddings-jeeaI": {
    "base_url": "http://localhost:11434",
    "model": "nomic-embed-text",
    "temperature": 0.1
  },
  "Chroma-76Dt7": {
    "allow_duplicates": False,
    "chroma_server_cors_allow_origins": "",
    "chroma_server_grpc_port": None,
    "chroma_server_host": "",
    "chroma_server_http_port": None,
    "chroma_server_ssl_enabled": False,
    "collection_name": "Bajaj1",
    "limit": None,
    "number_of_results": 10,
    "persist_directory": "C:\\Users\\ha\\Downloads\\Langflow\\chroma\\Bajaj",
    "search_query": "",
    "search_type": "Similarity"
  },
  "ParseData-PFbKQ": {
    "sep": "\n",
    "template": "{text}"
  },
  "Directory-iCV3N": {
    "depth": 0,
    "load_hidden": False,
    "max_concurrency": 2,
    "path": "C:\\Users\\ha\\Downloads\\New folder\\docs",
    "recursive": False,
    "silent_errors": False,
    "types": [
      ".txt"
    ],
    "use_multithreading": False
  },
  "CohereModel-9COrz": {
    "cohere_api_key": "keyco",
    "input_value": "",
    "stream": False,
    "system_message": "",
    "temperature": 0.5
  }
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=args.endpoint, components=[args.components], tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        api_key=args.api_key
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
