#!/usr/bin/bash

# Get the home directory for the user
USER_HOME=$(eval echo ~"$1")

# Set environment variables
export PLUGIN_PATH="$USER_HOME/homebrew/plugins"
export LOG_LEVEL=INFO

# Change to the working directory
cd "$USER_HOME/homebrew/services" || exit 1

# Start the PluginLoader
exec "$USER_HOME/homebrew/services/PluginLoader"
