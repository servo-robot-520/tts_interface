if (NOT ROS2_WS_SOURCE_BUILD OR NOT TARGET tts_interface)
    find_package(tts_interface REQUIRED)
endif ()

if (ROS2_WS_SOURCE_BUILD AND TARGET tts_interface)
    # 在源码聚合构建中，依赖包尚未安装到 install/，因此直接使用构建树中的
    # typesupport target 与源码 include 目录。
    rosidl_get_typesupport_target(tts_interface_CPP_TYPESUPPORT_TARGET
            tts_interface
            "rosidl_typesupport_cpp"
    )
    rosidl_get_typesupport_target(tts_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET
            tts_interface
            "rosidl_typesupport_fastrtps_cpp"
    )
    rosidl_get_typesupport_target(tts_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET
            tts_interface
            "rosidl_typesupport_introspection_cpp"
    )
    if (tts_interface_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$"
            OR tts_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$"
            OR tts_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$")
        message(FATAL_ERROR "The in-tree tts_interface target does not provide rosidl typesupport targets.")
    endif ()
    if (NOT DEFINED tts_interface_SOURCE_DIR
            OR NOT IS_DIRECTORY "${tts_interface_SOURCE_DIR}/include")
        message(FATAL_ERROR "The in-tree tts_interface source include directory is unavailable.")
    endif ()
    target_link_libraries(${PROJECT_NAME} PUBLIC
            ${tts_interface_CPP_TYPESUPPORT_TARGET}
    )
    target_include_directories(${PROJECT_NAME} PUBLIC
            "$<BUILD_INTERFACE:${tts_interface_SOURCE_DIR}/include>")
else ()
    ament_target_dependencies(${PROJECT_NAME} tts_interface)
endif ()

if (ROS2_WS_SOURCE_BUILD)
    target_link_libraries(${PROJECT_NAME} PUBLIC
            "-Wl,--no-as-needed"
            ${tts_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET}
            ${tts_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET}
            "-Wl,--as-needed"
    )
endif ()
