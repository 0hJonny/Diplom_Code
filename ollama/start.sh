#!/bin/sh
set -e

# Run serve in the background
/bin/ollama serve &

# Check if mistral and gemma:2b commands have already been executed
if [ ! -f /root/.ollama/commands_executed ]; then
    # Execute the remaining commands
    # /bin/ollama run mistral
    /bin/ollama run openchat
    /bin/ollama run gemma:2b

    # Create a file marker indicating that the commands have been executed
    touch /root/.ollama/commands_executed
fi

wait $!
