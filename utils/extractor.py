import re
from datetime import datetime
from dateutil import parser as date_parser
from .cleaner import clean_message

def extract_todos(messages):
    if not messages:
        return []

    todos = []
    completed_actions = {}
    request_history = {}
    
    # Precompute message datetimes
    for msg in messages:
        try:
            msg['datetime'] = date_parser.parse(msg['timestamp'], fuzzy=True)
        except:
            msg['datetime'] = datetime.now()
    
    # First pass: Build request history and track completions
    for i, msg in enumerate(messages):
        text = clean_message(msg['text'])
        sender = msg['sender']
        
        # 1. Detect Requests
        is_request = False
        request_patterns = [
            r'(send|mail|bhej|share|submit|provide|resend|check|verify|review)\s*(me|the)?\s*(.+?)(?:please|pl[sz]|kr?do?|karo)?\b',
            r'(?:can you|could you|please|kindly)\s+(send|forward|submit|prepare|resend|check|verify|review)\s+(.+?)\b',
            r'(report|presentation|document|file|inbox|photos?)\s+(send|submit|bhej|resend|check|verify|review)\b',
            r'\b(kr?do?|karo)\s+(.+?)\b',
            r'\bby\s+(.+?)\s+(send|submit|complete|check|verify|review)\b',
            r'\b(today|tomorrow|kal|aaj|now)\s+(.+?)\s+(send|submit|prepare|check|verify|review)\b',
            r'\b(I\'ll|I will|main|hum)\s+(check|verify|review|look)\s*(into|at|for)?\s*(.+?)\b',
            r'\b(check|verify|review)\s*(kar (l[ae]?t[ae]? h[uaei]+|karen?g[ae]))\b'
        ]
        
        for pattern in request_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                is_request = True
                # Create request signature (sender + first 3 words)
                signature = f"{sender}:{' '.join(text.split()[:3])}"
                
                # Track request
                request_history[signature] = {
                    'timestamp': msg['datetime'],
                    'text': text,
                    'position': i
                }
                break
        
        # 2. Detect Completion Indicators
        is_completion = False
        completion_patterns = [
            r'\b(sent|already sent|sended|bhej diya|bhej di|done|completed|finished)\b',
            r'\b(yesterday|kal|last week|last month|pichle hafte)\b',
            r'\b(i have|i\'ve|main ne|hum ne)\s+(sent|completed|finished)',
            r'\b(ho gaya|ho gya|kar (liya|li|chuka|chuki))\b',
            r'^(?!.*(I\'ll|I will)\s+(check|verify|review))'
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in completion_patterns):
            is_completion = True
            
            # Find matching request in recent history
            for j in range(max(0, i-5), i):
                prev_msg = messages[j]
                prev_text = clean_message(prev_msg['text'])
                prev_sig = f"{prev_msg['sender']}:{' '.join(prev_text.split()[:3])}"
                
                # Check if this request matches the completion
                if prev_sig in request_history:
                    completed_actions[prev_sig] = True
                    break
    
    # Second pass: Extract valid todos
    for i, msg in enumerate(messages):
        text = clean_message(msg['text'])
        sender = msg['sender']
        signature = f"{sender}:{' '.join(text.split()[:3])}"
        
        # Skip if this is a completion indicator
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in [
            r'\b(already sent|sended|bhej diya|done|completed|finished)\b',
            r'\b(yesterday|last week|last month)\b',
            r'\b(i have|i\'ve)\s+(sent|completed)',
            r'\b(ho gaya|ho gya|kar (liya|li|chuka|chuki))\b'
        ]):
            continue
            
        # Skip if marked as completed
        if signature in completed_actions:
            continue
            
        # Skip status inquiries and casual messages
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in [
            r'\b(bhej diya kya|sent\??|done\??|completed\??|finished\??)\b',
            r'\b(ho gaya kya|ho gya kya|kar liya kya)\b',
            r'\b(status|update)\s+(on|for)\b',
            r'\b(kya\s+(bhej|kar)\s+diya\??)\b',
            r'\b(did you|have you|has)\s+(sent|completed|finished)\b\?$',
            r'^(hi|hello|thanks|thank you|ok|hmm|yes|no|okay)$'
        ]):
            continue
            
        # Detect requests and structure them
        for pattern in request_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Format the task
                task_parts = []
                recipient = "someone"  # Default recipient
                action = "send"
                item = ""
                
                for match in matches:
                    if isinstance(match, tuple):
                        # Extract action and item
                        if match[0]:
                            action = match[0]
                        if len(match) > 2 and match[2]:
                            item = match[2]
                        elif len(match) > 1 and match[1]:
                            item = match[1]
                            
                        # Look for recipient indicators
                        if "me" in match:
                            recipient = sender
                        elif "you" in match:
                            # Previous sender is the recipient
                            if i > 0:
                                recipient = messages[i-1]['sender']
                    elif match:
                        item = match
                
                # Special handling for "check" actions
                if "check" in action.lower() or "verify" in action.lower() or "review" in action.lower():
                    # Handle self-assigned checks
                    if "I will" in text:
                        recipient = sender
                    
                    # Auto-complete common items
                    if not item:
                        if "inbox" in text:
                            item = "the inbox"
                        elif "photo" in text:
                            item = "the photos"
                        else:
                            item = "it"
                
                # Structure the todo
                if not item:
                    item = "something"
                    
                # Capitalize and format
                action = action.capitalize()
                item = item.strip()
                
                # Special handling for common items
                if "file" in item:
                    item = "the file"
                elif "report" in item:
                    item = "the report"
                elif "presentation" in item:
                    item = "the presentation"
                elif "document" in item:
                    item = "the document"
                
                # Build structured task
                structured_task = f"{sender} wants {recipient} to {action} {item}"
                
                # For self-assigned tasks, mark recipient as "me"
                if recipient == sender:
                    recipient = "me"
                    structured_task = f"{sender} wants me to {action} {item}"
                
                todos.append({
                    'timestamp': msg['timestamp'],
                    'sender': sender,
                    'recipient': recipient,
                    'task': structured_task
                })
                break
    
    return todos