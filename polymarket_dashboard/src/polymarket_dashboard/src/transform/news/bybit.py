from polymarket_dashboard.src.config.enum import NewsCategory


def is_new_listing(result):
    keyword = "New listings"
    fulltext_keyword = keyword.rstrip("s").lower()
    return (
        fulltext_keyword in str(result).lower()
        or keyword in result['topics']
        or keyword in result['category']['key']
        or keyword in result['category']['title']
    )

def is_delisting(result):
    keyword = "Delistings"
    fulltext_keyword = keyword.rstrip("s").lower()
    return (
        fulltext_keyword in str(result).lower()
        or keyword in result['topics']
        or keyword in result['category']['key']
        or keyword in result['category']['title']
    )


def process_bybit_announcments(responses):
    lst = []
    for response in responses:
        if not response['ret_msg']:
            continue
        results = response['result']['hits']
        for result in results:
            if "Derivatives" in result['topics']:
                print("=="*100)
                if is_new_listing(result):
                    type_event = NewsCategory.LISTING

                if is_delisting(result):
                    type_event = NewsCategory.DELISTING

                lst.append(
                    {
                        "type_event": type_event,
                        "releaseDate": result['start_date_timestamp'],
                        "id": result['objectID'],
                        "title": result['title']
                    }
                )    
                

            else:
                continue
    return lst


if __name__ == "__main__":
    import json
    with open("./sample_data/response_bybit.json", "r") as f:
        response_bybit = json.load(f)
    responses = process_bybit_announcments(response_bybit)
    print(responses)

    with open("./responses_bybit.json", "w") as f:
        json.dump(responses, f)