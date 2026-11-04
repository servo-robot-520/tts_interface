#include <stdexcept>
#include <type_traits>

#include <gtest/gtest.h>

#include "tts_interface/ros_msg.hpp"

namespace {

constexpr std::string_view kRobotNodeFqn = "/robot_a/audio_tts";

TEST(RosMsgHelpers, ProvidesPrivateEndpointOwnerNames) {
    EXPECT_EQ(tts_interface::kPrivateTopicText, "~/text");
    EXPECT_EQ(tts_interface::kPrivateServiceSynthesize, "~/synthesize");
    EXPECT_EQ(tts_interface::kPrivateActionSay, "~/say");
    EXPECT_EQ(tts_interface::kPrivateTopicEvent, "~/event");
}

TEST(RosMsgHelpers, BuildsDefaultAbsoluteEndpointNames) {
    EXPECT_EQ(tts_interface::topic_text(), "/audio_tts/text");
    EXPECT_EQ(tts_interface::service_synthesize(), "/audio_tts/synthesize");
    EXPECT_EQ(tts_interface::action_say(), "/audio_tts/say");
    EXPECT_EQ(tts_interface::topic_event(), "/audio_tts/event");
}

TEST(RosMsgHelpers, BuildsNamesForCustomNodeFqn) {
    EXPECT_EQ(tts_interface::topic_text(kRobotNodeFqn), "/robot_a/audio_tts/text");
    EXPECT_EQ(tts_interface::service_synthesize(kRobotNodeFqn),
              "/robot_a/audio_tts/synthesize");
    EXPECT_EQ(tts_interface::action_say(kRobotNodeFqn), "/robot_a/audio_tts/say");
    EXPECT_EQ(tts_interface::topic_event(std::string{kRobotNodeFqn} + "///"),
              "/robot_a/audio_tts/event");
}

TEST(RosMsgHelpers, RejectsInvalidNodeFqn) {
    EXPECT_THROW(static_cast<void>(tts_interface::topic_text("")), std::invalid_argument);
    EXPECT_THROW(static_cast<void>(tts_interface::topic_text("audio/tts")),
                 std::invalid_argument);
    EXPECT_THROW(static_cast<void>(tts_interface::topic_text("/")), std::invalid_argument);
    EXPECT_THROW(static_cast<void>(tts_interface::topic_text("/audio//tts")),
                 std::invalid_argument);
    EXPECT_THROW(static_cast<void>(tts_interface::topic_text("/audio_tts\t")),
                 std::invalid_argument);
}

TEST(RosMsgHelpers, ExposesGeneratedTypeAliases) {
    static_assert(std::is_same_v<tts_interface::MsgTtsText, tts_interface::msg::TtsText>);
    static_assert(std::is_same_v<tts_interface::MsgTtsEvent, tts_interface::msg::TtsEvent>);
    static_assert(std::is_same_v<tts_interface::SrvSynthesize,
                                 tts_interface::srv::Synthesize>);
    static_assert(std::is_same_v<tts_interface::ActionSay, tts_interface::action::Say>);
    static_assert(std::is_same_v<tts_interface::ActionSayGoal,
                                 tts_interface::action::Say::Goal>);
    static_assert(std::is_same_v<tts_interface::ActionSayResult,
                                 tts_interface::action::Say::Result>);
    static_assert(std::is_same_v<tts_interface::ActionSayFeedback,
                                 tts_interface::action::Say::Feedback>);
}

} // namespace
