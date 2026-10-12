stats = {
    "total": 0,
    "by_level": {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
    "by_source": {},
    "top_error_sources": [],
    "first_timestamp": None,
    "last_timestamp": None,
    "skipped_invalid": 0,
}


def analyzer(stats, event):
    '''
    stats["total"] += 1
    if stats["first_timestamp"] == None or event["timestamp"] < stats["first_timestamp"]:
        stats["first_timestamp"] = event["timestamp"]
    
    elif stats["last_timestamp"] == None or event["timestamp"] > stats["last_timestamp"]:
            stats["last_timestamp"] = event["timestamp"]
    '''     
    pass