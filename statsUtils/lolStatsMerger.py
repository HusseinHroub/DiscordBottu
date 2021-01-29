def mergeGamesStats(results):
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_farms = 0
    kda = 0.0
    sample_count = 0
    for result in results:
        if result != None:
            total_kills += result['kills']
            total_deaths += result['deaths']
            total_assists += result['assists']
            total_farms += result['totalMinionsKilled'] + result['neutralMinionsKilled']
            sample_count += 1
            kda += (result['kills'] + result['assists']) / (result['deaths'] if result['deaths'] > 0 else 1)
    avg_kda = 0.0
    if sample_count != 0:
        avg_kda = kda / sample_count
    return {
        'total_kills': total_kills,
        'total_deaths': total_deaths,
        'total_assists': total_assists,
        'total_farms': total_farms,
        'avg_kda': avg_kda,
        'sample_count': sample_count
    }
