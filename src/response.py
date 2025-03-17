def generate_response(username, analysis):
    """Generate a sassy response based on analysis."""
    if analysis == "larping":
        return f"@{username} is larping harder than a D&D nerd on a Saturday night. Total fraud, and I’m calling it!"
    elif analysis == "genuine":
        return f"@{username}’s the real deal. No larp here—just painfully authentic."
    else:
        return f"@{username}? Couldn’t figure ‘em out. Probably too sneaky for me."