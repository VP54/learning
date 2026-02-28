from polymarket_dashboard.src.config.enum import NewsCategory


def process_binance_announcments(responses):
    result = []
    for response in responses:
        if not response['success']:
            continue

        catalog = response['data']['catalogs'][0]
        type_event = catalog['catalogName']
        if "listing" in type_event: type_event = NewsCategory.LISTING
        elif "delisting" in type_event: type_event = NewsCategory.DELISTING

        for announcement in catalog['articles']:
            announcement['type_event'] = type_event
            result.append(announcement)

    return result
        
    
if __name__ == "__main__":
    import json
    with open("./sample_data/raw_news_binance.json", "r") as f:
        response_binance = json.load(f)

    responses = process_binance_announcments(response_binance)
    responses[0]

    with open("./sample_data/parsed_news_binance.json", "w") as f:
        json.dump(responses, f)