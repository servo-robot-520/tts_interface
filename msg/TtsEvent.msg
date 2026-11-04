# TTS 异步事件：合成/播放起止、缓存命中、失败与取消。
# topic 路径没有 service 回执，失败只能从这里的 FAILED 看到。

# 已接受请求，开始调用后端合成。
uint8 SYNTHESIZE_STARTED=0
# 合成完成，音频已落盘或已得到 URI。
uint8 SYNTHESIZED=1
# 命中缓存，未调用后端。
uint8 CACHE_HIT=2
# 已提交 audio_io 播放。
uint8 PLAY_STARTED=3
# audio_io 报告播放结束。
uint8 PLAY_FINISHED=4
# 合成或播放失败；error 说明原因。
uint8 FAILED=5
# 请求被取消（action cancel 或新请求替换了同一焦点组的旧请求）。
uint8 CANCELED=6

std_msgs/Header header

# 与请求关联的标识；由节点生成，返回给 service/action 的发起方。
string request_id

# 取上面常量之一。
uint8 event

# 合成结果 URI；SYNTHESIZED/CACHE_HIT/PLAY_STARTED 时非空。
string audio_uri

# 音频时长，单位秒；未知时为 0。
float32 duration

# 失败原因；其他事件为空。
string error
