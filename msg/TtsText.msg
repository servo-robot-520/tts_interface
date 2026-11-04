# 一次 TTS 请求。topic、service、action 共用同一份参数。

# 要合成的文本；为空时请求被拒绝/失败，不会静默播放。
string text

# 后端音色标识；为空时使用节点默认音色。
# 取值由后端决定，例如 piper 的 voice name 或 espeak 的 voice variant。
string voice_id

# BCP-47 语言标签，例如 zh-CN、en-US；为空时由后端/节点默认值决定。
string language

# 语速倍率，1.0 为后端默认语速；<= 0 时按 1.0 处理。
float32 rate

# 音高倍率，1.0 为后端默认音高；<= 0 时按 1.0 处理。
float32 pitch

# 线性音量，1.0 为原始音量。
# 0 表示使用节点配置的默认播报音量；> 0 时直接作为 AudioClip.gain 传给 audio_io。
float32 volume

# true：合成后提交 audio_io 播放；false：只合成并缓存。
# 注意 bool 没有“未设置”：~/text 与 ~/say 需要播放时调用方必须显式置 true，
# 否则只会预热缓存。~/synthesize 忽略该字段（该服务始终只合成）。
bool play

# audio_io 的音频焦点组，用于 REPLACE_SAME_GROUP 等策略；为空时取 tts。
string group
