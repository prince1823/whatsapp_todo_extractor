import re

def clean_message(text):
    if not text or not isinstance(text, str):
        return ""
    
    # Normalize common variations with improved corrections
    replacements = {
        r'\b(send|sen[d]?|bhej|snd)\s*(kr?o?d?o?)\b': 'send',
        r'\b(kr?d?o?|kar?d?o?)\b': '',
        r'\b(pls|plz|kindly|asap)\b': 'please',
        r'\b(kal)\b': 'tomorrow',
        r'\b(aaj)\b': 'today',
        r'\b(shaam)\b': 'evening',
        r'\b(baje)\b': 'o\'clock',
        r'\b(sent|sended)\b': 'sent',
        r'\b(did|done|completed)\b': 'done',
        r'\b(received|got)\b': 'received',
        r'\b(resend|send again)\b': 'resend',
        r'\b(sory|sorry)\b': 'sorry',
        r'\b(diya|diya)\b': 'done',
        r'\b(me)\b': 'me',
        r'\b(u|you)\b': 'you',
        r'\b(plz|pls)\b': 'please',
        r'\b(thx|tnx|thanx)\b': 'thanks',
        r'\b(hav|have)\b': 'have',
        r'\b(hrs|hours)\b': 'hours',
        r'\b(sec|seconds)\b': 'seconds',
        r'\b(min|minutes)\b': 'minutes',
        r'\b(\w+)ing\b': lambda m: m.group(1) + 'ing',  # Fix broken -ing words
        r'\b(chek|chec|chk|chck|cek)\b': 'check',
        r'\b(verfiy|verfy|verifiy|verif)\b': 'verify',
        r'\b(reveiw|revie|revw)\b': 'review',
        r'\b(look in?to?|see|examine|inspect)\b': 'check',
        r'\b(kar (l[ae]?t[ae]? h[uaei]+|karen?g[ae]))\b': 'check',  # Hindi variants
        r'\b(I\'?ll|I will|main|hum)\b': 'I will',
        r'\b(my)\b': 'my'
    }
    
    text = text.lower().strip()
    
    # Apply replacements
    for pattern, replacement in replacements.items():
        if callable(replacement):
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        else:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Fix common spacing issues
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\s([?.!,])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([a-z])\s([a-z])', lambda m: m.group(1) + m.group(2) 
                  if len(m.group(1)+m.group(2)) <= 3 else m.group(1)+' '+m.group(2), text)  # Fix short word splits
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    
    return text