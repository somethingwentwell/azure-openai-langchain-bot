from langchain.callbacks.base import BaseCallbackHandler

class CustomHandler(BaseCallbackHandler):
    def __init__(self, session_id):
        self.session_id = session_id

    def on_llm_new_token(self, token):
        pass

    def on_llm_error(self, error):
        pass

    def on_agent_action(self, action):
        pass

    def on_agent_finish(self, finish):
        pass

    def on_llm_result(self, result):
        pass
# END: 5d7f5f5d5d5dimport json
import psycopg2
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
from typing import Any, Dict, List

class CustomHandler(BaseCallbackHandler):
    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__()


    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        log(self.session_id, "on_llm_start", json.dumps(serialized))
        # print(f"My custom handler, on_llm_start: {json.dumps(serialized, indent=2)}")
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        log(self.session_id, "on_llm_end", json.dumps(response))
        # print(f"My custom handler, on_llm_end: {json.dumps(response, indent=2)}")

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        log(self.session_id, "on_chain_start", json.dumps(serialized))
        # print(f"My custom handler, on_chain_start: {json.dumps(serialized, indent=2)}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        log(self.session_id, "on_chain_end", json.dumps(outputs))
        # print(f"My custom handler, on_chain_end: {json.dumps(outputs, indent=2)}")

    # your other methods here
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        log(self.session_id, "on_tool_start", json.dumps(serialized))
        # print(f"My custom handler, on_tool_start: {json.dumps(serialized, indent=2)}")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        log(self.session_id, "on_tool_end", json.dumps(output))
        # print(f"My custom handler, on_tool_end: {output}")

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        log(self.session_id, "on_agent_action", json.dumps(action))
        # print(f"My custom handler, on_agent_action: {json.dumps(action, indent=2)}")

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        print("on_agent_finish")
        log(self.session_id, "on_agent_finish", json.dumps(finish))
        print(self.session_id)
        # print(f"My custom handler, on_agent_finish: {json.dumps(finish, indent=2)}")

def log(session_id: str, callback_type: str, log_json: str) -> None:
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="chat_history",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO agent_log (session_id, callback_type, log) VALUES (%s, %s, %s)",
        (session_id, callback_type, log_json)
    )
    conn.commit()
    cur.close()
    conn.close()