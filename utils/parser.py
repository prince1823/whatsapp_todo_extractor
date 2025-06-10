import re
from dateutil import parser

def parse_whatsapp_chat(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Enhanced regex for various WhatsApp formats
    pattern = r'^(\[?\d{1,2}[/-]\d{1,2}[/-]\d{2,4},?\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:am|pm)?\]?)\s?[-\s]\s?([^:]+):\s(.+)$'
    
    for line in lines:
        match = re.match(pattern, line.strip(), re.IGNORECASE)
        if match:
            timestamp, sender, text = match.groups()
            messages.append({
                'timestamp': timestamp.strip('[]'),
                'sender': sender.strip(),
                'text': text.strip()
            })
        elif messages:
            messages[-1]['text'] += ' ' + line.strip()
    
    return messages