"""检查 tts_interface 的 Python endpoint helper 与消息/服务/动作字段。"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).parents[1]


def load_ros_msg():
    path = PACKAGE_ROOT / "python" / "tts_interface_msg" / "ros_msg.py"
    spec = importlib.util.spec_from_file_location("tts_interface_msg.ros_msg", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_python_endpoint_helpers() -> None:
    ros_msg = load_ros_msg()
    assert ros_msg.topic_text() == "/audio_tts/text"
    assert ros_msg.service_synthesize() == "/audio_tts/synthesize"
    assert ros_msg.action_say() == "/audio_tts/say"
    assert ros_msg.topic_event() == "/audio_tts/event"
    assert ros_msg.topic_text("/robot_a/audio_tts/") == "/robot_a/audio_tts/text"
    assert ros_msg.qualify_node_fqn("/robot_a") == "/robot_a/audio_tts"
    assert ros_msg.action_say(ros_msg.DEFAULT_NODE_FQN, "/robot_a") == "/robot_a/audio_tts/say"


def test_python_endpoint_helpers_reject_invalid_node_fqn() -> None:
    ros_msg = load_ros_msg()
    for bad in ("", "audio/tts", "/", "/audio//tts", "/audio_tts\t"):
        with pytest.raises(ValueError):
            ros_msg.service_synthesize(bad)


def test_python_private_names_match_cpp_header() -> None:
    ros_msg = load_ros_msg()
    header = (PACKAGE_ROOT / "include" / "tts_interface" / "ros_msg.hpp").read_text(
        encoding="utf-8"
    )
    for private_name in (
            ros_msg.PRIVATE_TOPIC_TEXT,
            ros_msg.PRIVATE_SERVICE_SYNTHESIZE,
            ros_msg.PRIVATE_ACTION_SAY,
            ros_msg.PRIVATE_TOPIC_EVENT,
    ):
        assert f'"{private_name}"' in header


def test_tts_text_fields() -> None:
    text = (PACKAGE_ROOT / "msg" / "TtsText.msg").read_text(encoding="utf-8")
    for field in (
            "string text",
            "string voice_id",
            "string language",
            "float32 rate",
            "float32 pitch",
            "float32 volume",
            "bool play",
            "string group",
    ):
        assert field in text


def test_tts_event_contract() -> None:
    event = (PACKAGE_ROOT / "msg" / "TtsEvent.msg").read_text(encoding="utf-8")
    for constant in (
            "uint8 SYNTHESIZE_STARTED=0",
            "uint8 SYNTHESIZED=1",
            "uint8 CACHE_HIT=2",
            "uint8 PLAY_STARTED=3",
            "uint8 PLAY_FINISHED=4",
            "uint8 FAILED=5",
            "uint8 CANCELED=6",
    ):
        assert constant in event
    for field in ("std_msgs/Header header", "string request_id", "uint8 event",
                  "string audio_uri", "float32 duration", "string error"):
        assert field in event


def test_synthesize_contract() -> None:
    request, response = (PACKAGE_ROOT / "srv" / "Synthesize.srv").read_text(
        encoding="utf-8"
    ).split("---")
    assert "tts_interface/TtsText request" in request
    for field in ("bool success", "string audio_uri", "float32 duration", "string error"):
        assert field in response


def test_say_contract() -> None:
    sections = (PACKAGE_ROOT / "action" / "Say.action").read_text(encoding="utf-8").split("---")
    assert len(sections) == 3
    assert "tts_interface/TtsText text" in sections[0]
    assert "string request_id" in sections[1]
    assert "float32 progress" in sections[2]
    assert "string current_sentence" in sections[2]
