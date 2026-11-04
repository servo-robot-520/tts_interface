"""tts_interface 的 ROS endpoint 名称辅助函数。"""

from __future__ import annotations

DEFAULT_NODE_FQN = "/audio_tts"

# 下列私有名称仅供 endpoint owner（tts_node 节点自身）创建 endpoint 时使用。
PRIVATE_TOPIC_TEXT = "~/text"
PRIVATE_SERVICE_SYNTHESIZE = "~/synthesize"
PRIVATE_ACTION_SAY = "~/say"
PRIVATE_TOPIC_EVENT = "~/event"

_ASCII_WHITESPACE = " \t\n\r\v\f"


def _normalized_node_fqn(node_fqn: str) -> str:
    """校验并返回去掉尾部 '/' 的 tts_node 节点全名。"""
    trimmed = node_fqn.rstrip("/")
    if (
            not trimmed
            or not trimmed.startswith("/")
            or trimmed == "/"
            or "//" in trimmed
            or any(character in _ASCII_WHITESPACE for character in trimmed)
    ):
        raise ValueError(
            "node_fqn must be an absolute, non-root ROS name without ASCII whitespace"
        )
    return trimmed


def _endpoint_name(node_fqn: str, endpoint_suffix: str) -> str:
    """拼接节点全名与 endpoint 后缀。"""
    return f"{_normalized_node_fqn(node_fqn)}/{endpoint_suffix}"


def topic_text(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回 fire-and-forget 文本话题的绝对名称。"""
    return _endpoint_name(node_fqn, "text")


def service_synthesize(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回只合成服务的绝对名称。"""
    return _endpoint_name(node_fqn, "synthesize")


def action_say(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回长文本播报动作的绝对名称。"""
    return _endpoint_name(node_fqn, "say")


def topic_event(node_fqn: str = DEFAULT_NODE_FQN) -> str:
    """返回 TTS 事件话题的绝对名称。"""
    return _endpoint_name(node_fqn, "event")


__all__ = [
    "DEFAULT_NODE_FQN",
    "PRIVATE_TOPIC_TEXT",
    "PRIVATE_SERVICE_SYNTHESIZE",
    "PRIVATE_ACTION_SAY",
    "PRIVATE_TOPIC_EVENT",
    "topic_text",
    "service_synthesize",
    "action_say",
    "topic_event",
]
