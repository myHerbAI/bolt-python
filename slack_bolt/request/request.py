from typing import Dict, Optional, List, Union, Any

from slack_bolt.context.context import BoltContext
from slack_bolt.request.internals import (
    parse_query,
    parse_body,
    build_normalized_headers,
    build_context,
    extract_content_type,
)


class BoltRequest:
    raw_body: str
    query: Dict[str, List[str]]
    headers: Dict[str, List[str]]
    content_type: Optional[str]
    body: Dict[str, Any]
    context: BoltContext
    lazy_only: bool
    lazy_function_name: Optional[str]

    def __init__(
        self,
        *,
        body: str,
        query: Optional[Union[str, Dict[str, str], Dict[str, List[str]]]] = None,
        # many framework use Dict[str, str] but the reality is Dict[str, List[str]]
        headers: Optional[Dict[str, Union[str, List[str]]]] = None,
        context: Optional[Dict[str, str]] = None,
    ):
        self.raw_body = body
        self.query = parse_query(query)
        self.headers = build_normalized_headers(headers)
        self.content_type = extract_content_type(self.headers)
        self.body = parse_body(self.raw_body, self.content_type)
        self.context = build_context(BoltContext(context if context else {}), self.body)
        self.lazy_only = self.headers.get("x-slack-bolt-lazy-only", [False])[0]
        self.lazy_function_name = self.headers.get(
            "x-slack-bolt-lazy-function-name", [None]
        )[0]
