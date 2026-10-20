import math
import re
from urllib.parse import urlparse
import pandas as pd
import numpy as np

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    entropy = 0.0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def extract_url_features(url: str) -> dict:
    parsed = urlparse(url)
    hostname = parsed.netloc or ""
    path = parsed.path or ""
    query = parsed.query or ""

    url_length = len(url)
    hostname_length = len(hostname)
    path_length = len(path)
    num_subdomains = len(hostname.split(".")) - 1 if hostname else 0
    
    # Check IP address as hostname
    is_ip = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else 0
    is_https = 1 if parsed.scheme == "https" else 0
    
    suspicious_chars = sum(url.count(c) for c in ["@", "-", "_", "?", "=", "&", "%"])
    entropy = calculate_entropy(url)

    suspicious_keywords = ["login", "verify", "update", "bank", "crypto", "secure", "kyc", "free", "claim", "bonus", "auth"]
    has_suspicious_kw = 1 if any(kw in url.lower() for kw in suspicious_keywords) else 0

    return {
        "url_length": url_length,
        "hostname_length": hostname_length,
        "path_length": path_length,
        "num_subdomains": num_subdomains,
        "is_ip": is_ip,
        "is_https": is_https,
        "suspicious_chars": suspicious_chars,
        "url_entropy": entropy,
        "has_suspicious_kw": has_suspicious_kw
    }

def extract_features_df(urls: list) -> pd.DataFrame:
    features = [extract_url_features(u) for u in urls]
    return pd.DataFrame(features)
