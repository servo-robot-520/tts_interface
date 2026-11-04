# tts_interface

## 简介

通用 TTS 节点（默认节点全名 `/audio_tts`）的 ROS 2 接口。它只定义消息/服务/动作，
不实现节点，也不直接依赖 `audio_io`：节点把合成结果以 `AudioClip` 交给 `/audio_io` 播放。

`tts_interface` 不出现任何鸭子语义；`chirp`、`coo`、`wheee` 属于 `duck_audio_interface`，
设备播放/音量属于 `audio_io_interface`。

## 接口

| 接口 | 类型 | 语义 |
|---|---|---|
| `~/text` | `msg/TtsText` | fire-and-forget：合成并播放 |
| `~/synthesize` | `srv/Synthesize` | 只合成，返回缓存音频 URI |
| `~/say` | `action/Say` | 长文本：按句合成/提交，进度反馈，可取消 |
| `~/event` | `msg/TtsEvent` | 合成/播放起止、缓存命中、失败、取消 |

`~/synthesize` 的请求字段是 `TtsText request`，与 topic/action 共用同一份参数。

## `TtsText`

```msg
string text
string voice_id
string language
float32 rate
float32 pitch
float32 volume
bool play
string group
```

默认值约定（消息没有 optional，用 0/空串表示“用节点默认”）：

| 字段 | 0/空值含义 |
|---|---|
| `text` | 非法请求，节点拒绝/失败并给出原因 |
| `voice_id` | 节点默认音色 |
| `language` | 节点默认语言或后端自动判断 |
| `rate` | 按 1.0 处理 |
| `pitch` | 按 1.0 处理 |
| `volume` | 节点配置的默认播报音量；> 0 时作为线性增益传给 `AudioClip.gain` |
| `play` | `false` 表示只合成并缓存，不提交播放；`~/synthesize` 忽略该字段 |
| `group` | `tts` |

默认播放策略由节点固定为 `priority = SPEECH`、`policy = REPLACE_SAME_GROUP`、`group = tts`
（除非请求显式给出 `group`），即新一句替换旧一句，但不会压掉 `ALERT`。

## `TtsEvent`

事件常量：`SYNTHESIZE_STARTED=0`、`SYNTHESIZED=1`、`CACHE_HIT=2`、`PLAY_STARTED=3`、
`PLAY_FINISHED=4`、`FAILED=5`、`CANCELED=6`。

```msg
std_msgs/Header header
string request_id
uint8 event
string audio_uri
float32 duration
string error
```

`~/text` 的失败不会通过 service 返回，只能从 `~/event` 的 `FAILED` 看到；长文本的中间进度
由 action feedback 提供。

## 端点约定

- `~/...` 是 endpoint owner（`tts_node` 自身）的私有名称。
- 外部节点必须传递目标节点的完整节点名（FQN），由 helper 生成绝对名称。
- `node_fqn` 必须是非根绝对 ROS 名称，不能包含 ASCII 空白或中间的空路径段；尾部 `/` 会被移除。

默认 FQN 为 `/audio_tts`：

| owner 私有名称 | 外部 helper | 默认绝对名称 |
|---|---|---|
| `~/text` | `topic_text(node_fqn)` | `/audio_tts/text` |
| `~/synthesize` | `service_synthesize(node_fqn)` | `/audio_tts/synthesize` |
| `~/say` | `action_say(node_fqn)` | `/audio_tts/say` |
| `~/event` | `topic_event(node_fqn)` | `/audio_tts/event` |

多机器人时用命名空间：`/robot_a/audio_tts/text`。

## 示例

```bash
# 合成并播放（bool 没有“未设置”，必须显式 play: true）
ros2 topic pub --once -w 0 /audio_tts/text tts_interface/msg/TtsText \
  "{text: '你好，我是小鸭', language: zh-CN, play: true}"

# 只预热缓存（play 缺省为 false）
ros2 topic pub --once -w 0 /audio_tts/text tts_interface/msg/TtsText \
  "{text: '你好，我是小鸭', language: zh-CN}"

# 只合成
ros2 service call /audio_tts/synthesize tts_interface/srv/Synthesize \
  "{request: {text: 'hello', language: en-US, play: false}}"

# 长文本播报
ros2 action send_goal /audio_tts/say tts_interface/action/Say \
  "{text: {text: '第一句。第二句。', play: true}}" --feedback

ros2 topic echo /audio_tts/event
```

## C++ / Python 辅助

- `include/tts_interface/ros_msg.hpp`：私有 endpoint 常量、外部绝对名称 helper、生成类型别名。
- `python/tts_interface_msg/ros_msg.py`：同一组名称 helper。
- `cmake_include.cmake`：供 CLion 源码聚合构建直接使用 in-tree typesupport target。

```cpp
#include "tts_interface/ros_msg.hpp"

auto text = tts_interface::topic_text("/robot_a/audio_tts");
auto say = tts_interface::action_say("/robot_a/audio_tts");
```

```python
from tts_interface_msg.ros_msg import action_say, topic_text

print(topic_text("/robot_a/audio_tts"))  # /robot_a/audio_tts/text
print(action_say())                      # /audio_tts/say
```

## 构建与测试

```bash
source /opt/ros/humble/setup.bash

colcon build --base-paths src --packages-select tts_interface
colcon test --base-paths src --packages-select tts_interface
colcon test-result --test-result-base build/tts_interface/test_results --verbose
```

接口依赖：`builtin_interfaces`、`std_msgs`、`rosidl_default_generators`/`rosidl_default_runtime`。

## 与设计文档的对应

| 文档中的接口 | 本包中的类型 |
|---|---|
| `TtsText` | `msg/TtsText.msg` |
| `~/event` 失败上报 | `msg/TtsEvent.msg` |
| `Synthesize` | `srv/Synthesize.srv` |
| `Say` | `action/Say.action` |

设计见 [`docs/duck-ros2-audio-architecture.zh-CN.md`](../../docs/duck-ros2-audio-architecture.zh-CN.md) 第 7 节。
