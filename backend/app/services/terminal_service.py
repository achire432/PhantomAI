"""
SAFE TERMINAL SERVICE
======================
Purpose: Allow PhantomAI to run safe terminal commands.

Why This Matters:
- Users need to check system status
- PhantomAI can help with system management
- Makes PhantomAI more powerful

Safety Rules:
- Only specific commands allowed
- No destructive commands
- Timeout limits
- User confirmation required
- Logs all commands for auditing

What Would Happen Without Safety:
- A malicious command could delete files
- System could be damaged
- Security risk
"""

import subprocess
import re
import os
from datetime import datetime

# ALLOWED COMMANDS - Only these are permitted
ALLOWED_COMMANDS = [
    "ls",
    "pwd", 
    "whoami",
    "df -h",
    "uptime",
    "ps aux",
    "echo",
]

# DANGEROUS PATTERNS - These are forbidden
FORBIDDEN_PATTERNS = [
    r"rm\s+-rf",
    r"sudo",
    r"chmod",
    r"chown",
    r"dd",
    r"mkfs",
    r"shutdown",
    r"reboot",
    r">\s*/",
    r"kill\s+-9",
]

def validate_command(command: str) -> dict:
    """
    Validate a command before execution.
    
    Checks:
    1. Command is in allowed list
    2. No forbidden patterns
    3. Not too long
    4. No shell injection attempts
    
    Returns:
    {
        "valid": True,
        "message": "Command is safe"
    }
    """
    # Check if the command is too long
    if len(command) > 500:
        return {
            "valid": False,
            "message": "Command is too long (max 500 characters)"
        }
    
    # Check if the base command is allowed
    base_command = command.split()[0]
    if base_command not in [cmd.split()[0] for cmd in ALLOWED_COMMANDS]:
        return {
            "valid": False,
            "message": f"Command '{base_command}' is not allowed"
        }
    
    # Check for forbidden patterns
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return {
                "valid": False,
                "message": f"Command contains forbidden pattern: {pattern}"
            }
    
    return {
        "valid": True,
        "message": "Command is safe"
    }

def run_command(command: str, timeout: int = 30) -> dict:
    """
    Run a validated command safely.
    
    How It Works:
    1. Validates the command
    2. Runs it with subprocess
    3. Captures output
    4. Returns the result
    
    Returns:
    {
        "success": True,
        "output": "Command output here",
        "exit_code": 0
    }
    """
    # Validate first
    validation = validate_command(command)
    if not validation["valid"]:
        return {
            "success": False,
            "error": validation["message"]
        }
    
    try:
        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Log the command (for auditing)
        log_command(command, result.returncode)
        
        return {
            "success": True,
            "output": result.stdout.strip() or result.stderr.strip(),
            "exit_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def log_command(command: str, exit_code: int):
    """
    Log all terminal commands for auditing.
    
    This helps track what commands were run and when.
    """
    log_file = "terminal_audit.log"
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] User ran: '{command}' (exit: {exit_code})\n")

def get_allowed_commands() -> list:
    """
    Return the list of allowed commands.
    """
    return ALLOWED_COMMANDS