"""Static reference data for CareNear."""

STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu",
    "FCT (Abuja)", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina",
    "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo",
    "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
]

PLACE_TYPES = {
    "pharmacy": "Pharmacy / Chemist",
    "hospital": "Hospital",
    "clinic": "Clinic",
}

# Rough center point per state capital, used to center the map before any
# report has coordinates or the user shares their location. Approximate —
# just for initial map framing, not used for anything else.
STATE_CENTERS = {
    "Abia": (5.4527, 7.5248), "Adamawa": (9.3265, 12.3984), "Akwa Ibom": (5.0377, 7.9128),
    "Anambra": (6.2209, 6.9370), "Bauchi": (10.3158, 9.8442), "Bayelsa": (4.9267, 6.2676),
    "Benue": (7.7322, 8.5391), "Borno": (11.8333, 13.1500), "Cross River": (4.9517, 8.3417),
    "Delta": (5.5333, 5.8333), "Ebonyi": (6.2649, 8.0137), "Edo": (6.3350, 5.6037),
    "Ekiti": (7.6667, 5.2167), "Enugu": (6.4413, 7.4986), "FCT (Abuja)": (9.0765, 7.3986),
    "Gombe": (10.2904, 11.1673), "Imo": (5.4833, 7.0333), "Jigawa": (12.2280, 9.5616),
    "Kaduna": (10.5167, 7.4333), "Kano": (12.0001, 8.5920), "Katsina": (12.9908, 7.6018),
    "Kebbi": (12.4500, 4.1996), "Kogi": (7.8000, 6.7333), "Kwara": (8.5000, 4.5500),
    "Lagos": (6.5244, 3.3792), "Nasarawa": (8.5000, 8.2000), "Niger": (9.6139, 6.5569),
    "Ogun": (7.1500, 3.3500), "Ondo": (7.2500, 5.2000), "Osun": (7.7667, 4.5667),
    "Oyo": (7.3775, 3.9470), "Plateau": (9.2182, 9.5179), "Rivers": (4.8156, 7.0498),
    "Sokoto": (13.0059, 5.2476), "Taraba": (8.0000, 10.7500), "Yobe": (12.0000, 11.5000),
    "Zamfara": (12.1704, 6.2400),
}
