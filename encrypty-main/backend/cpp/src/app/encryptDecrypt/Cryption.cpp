#include "Cryption.hpp"
#include "../processes/Task.hpp"
#include "../fileHandling/ReadEnv.cpp"
#include <cstdlib>
#include <stdexcept>

int executeCryption(const std::string& taskData) {
    Task task = Task::fromString(taskData);
    ReadEnv env;
    std::string envKey = env.getenv();
    
    // Default encryption key if not found
    int key = 42;
    
    // Try to get key from environment variable first
    const char* envKeyPtr = std::getenv("ENCRYPTION_KEY");
    if (envKeyPtr != nullptr) {
        try {
            key = std::stoi(std::string(envKeyPtr));
        } catch (const std::exception& e) {
            // If conversion fails, use default
            key = 42;
        }
    } else if (!envKey.empty()) {
        // Try to parse from .env file
        try {
            // Remove whitespace from the key string
            envKey.erase(0, envKey.find_first_not_of(" \t\n\r"));
            envKey.erase(envKey.find_last_not_of(" \t\n\r") + 1);
            
            if (!envKey.empty()) {
                key = std::stoi(envKey);
            }
        } catch (const std::exception& e) {
            // If conversion fails, use default
            key = 42;
        }
    }
    if (task.action == Action::ENCRYPT) {
        char ch;
        while (task.f_stream.get(ch)) {
            ch = (ch + key) % 256;
            task.f_stream.seekp(-1, std::ios::cur);
            task.f_stream.put(ch);
        }
        task.f_stream.close();
    } else {
        char ch;
        while (task.f_stream.get(ch)) {
            ch = (ch - key + 256) % 256;
            task.f_stream.seekp(-1, std::ios::cur);
            task.f_stream.put(ch);
        }
        task.f_stream.close();
    }
    return 0;
}