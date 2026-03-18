"""
Core prediction models for March Madness simulation
Combines Kenpom + Torvik efficiency ratings
"""
import pandas as pd

# D1 Averages for calculations
D1_AVERAGES_KENPOM = {
    'tempo': 67.3,
    'def_efficiency': 109.4,
}

D1_AVERAGES_TORVIK = {
    'tempo': 67.3,
    'def_efficiency': 109.1,
}

# Spread to win probability lookup table
SPREAD_TO_WIN_PROB = {
    -40.0: 0.9990, -39.5: 0.9990, -39.0: 0.9990, -38.5: 0.9990, -38.0: 0.9990,
    -37.5: 0.9990, -37.0: 0.9990, -36.5: 0.9990, -36.0: 0.9990, -35.5: 0.9990,
    -35.0: 0.9989, -34.5: 0.9988, -34.0: 0.9987, -33.5: 0.9986, -33.0: 0.9985,
    -32.5: 0.9984, -32.0: 0.9983, -31.5: 0.9982, -31.0: 0.9981, -30.5: 0.9980,
    -30.0: 0.9979, -29.5: 0.9977, -29.0: 0.9975, -28.5: 0.9973, -28.0: 0.9971,
    -27.5: 0.9969, -27.0: 0.9967, -26.5: 0.9964, -26.0: 0.9961, -25.5: 0.9958,
    -25.0: 0.9954, -24.5: 0.9950, -24.0: 0.9946, -23.5: 0.9941, -23.0: 0.9936,
    -22.5: 0.9930, -22.0: 0.9924, -21.5: 0.9917, -21.0: 0.9909, -20.5: 0.9900,
    -20.0: 0.9788, -19.5: 0.9775, -19.0: 0.9759, -18.5: 0.9741, -18.0: 0.9720,
    -17.5: 0.9695, -17.0: 0.9665, -16.5: 0.9629, -16.0: 0.9585, -15.5: 0.9528,
    -15.0: 0.9454, -14.5: 0.9414, -14.0: 0.9369, -13.5: 0.9315, -13.0: 0.9251,
    -12.5: 0.9175, -12.0: 0.9082, -11.5: 0.8964, -11.0: 0.8811, -10.5: 0.8607,
    -10.0: 0.8316, -9.5: 0.8221, -9.0: 0.8113, -8.5: 0.7988, -8.0: 0.7849,
    -7.5: 0.7691, -7.0: 0.7506, -6.5: 0.7354, -6.0: 0.7175, -5.5: 0.6979,
    -5.0: 0.6753, -4.5: 0.6622, -4.0: 0.6466, -3.5: 0.6310, -3.0: 0.6139,
    -2.5: 0.5935, -2.0: 0.5708, -1.5: 0.5475, -1.0: 0.5192, -0.5: 0.5098,
    0.0: 0.5000,
    0.5: 0.4902, 1.0: 0.4808, 1.5: 0.4525, 2.0: 0.4292, 2.5: 0.4065,
    3.0: 0.3861, 3.5: 0.3690, 4.0: 0.3534, 4.5: 0.3378, 5.0: 0.3247,
    5.5: 0.3021, 6.0: 0.2825, 6.5: 0.2646, 7.0: 0.2494, 7.5: 0.2309,
    8.0: 0.2151, 8.5: 0.2012, 9.0: 0.1887, 9.5: 0.1779, 10.0: 0.1684,
    10.5: 0.1393, 11.0: 0.1189, 11.5: 0.1036, 12.0: 0.0918, 12.5: 0.0825,
    13.0: 0.0749, 13.5: 0.0685, 14.0: 0.0631, 14.5: 0.0586, 15.0: 0.0546,
    15.5: 0.0472, 16.0: 0.0415, 16.5: 0.0371, 17.0: 0.0335, 17.5: 0.0305,
    18.0: 0.0280, 18.5: 0.0259, 19.0: 0.0241, 19.5: 0.0225, 20.0: 0.0212,
    20.5: 0.0100, 21.0: 0.0091, 21.5: 0.0083, 22.0: 0.0076, 22.5: 0.0070,
    23.0: 0.0064, 23.5: 0.0059, 24.0: 0.0054, 24.5: 0.0050, 25.0: 0.0046,
    25.5: 0.0042, 26.0: 0.0039, 26.5: 0.0036, 27.0: 0.0033, 27.5: 0.0031,
    28.0: 0.0029, 28.5: 0.0027, 29.0: 0.0025, 29.5: 0.0023, 30.0: 0.0021,
    30.5: 0.0020, 31.0: 0.0019, 31.5: 0.0018, 32.0: 0.0017, 32.5: 0.0016,
    33.0: 0.0015, 33.5: 0.0014, 34.0: 0.0013, 34.5: 0.0012, 35.0: 0.0011,
    35.5: 0.0010, 36.0: 0.0010, 36.5: 0.0010, 37.0: 0.0010, 37.5: 0.0010,
    38.0: 0.0010, 38.5: 0.0010, 39.0: 0.0010, 39.5: 0.0010, 40.0: 0.0010
}


def get_team_data(df: pd.DataFrame, team: str) -> pd.Series:
    """
    Get team data from DataFrame, handling play-in format
    
    Parameters:
    df: DataFrame with team stats
    team: Team name (may include "/" for play-in teams or "(seed)" prefix)
    
    Returns:
    Team's data row as a Series
    """
    # Strip seed number if present: "(1) Duke" → "Duke"
    if ")" in team:
        team = team.split(") ")[1]
    
    # Handle 'Team1/Team2' play-in format by using first team
    if '/' in team:
        team = team.split('/')[0]
    
    team_data = df[df['Team'] == team]
    
    if len(team_data) == 0:
        raise ValueError(f"Team '{team}' not found in tournament data")
    
    return team_data.iloc[0]


def calculate_kenpom_score(kenpom_data: pd.DataFrame, team: str, opponent: str) -> float:
    """
    Calculate predicted score using Kenpom formula (neutral court)
    
    Formula: (Team AdjO * Opponent AdjD * Tempo) / (D1_avg_def * 100)
    """
    team_data = get_team_data(kenpom_data, team)
    opp_data = get_team_data(kenpom_data, opponent)
    
    # Calculate tempo
    tempo = (team_data['AdjT'] * opp_data['AdjT']) / D1_AVERAGES_KENPOM['tempo']
    
    # Calculate score
    score = (team_data['AdjO'] * opp_data['AdjD'] * tempo) / (D1_AVERAGES_KENPOM['def_efficiency'] * 100)
    
    return score


def calculate_torvik_score(torvik_data: pd.DataFrame, team: str, opponent: str) -> float:
    """
    Calculate predicted score using Torvik formula (neutral court)
    
    Formula: (Team AdjO * Opponent AdjD * Tempo) / (D1_avg_def * 100)
    """
    team_data = get_team_data(torvik_data, team)
    opp_data = get_team_data(torvik_data, opponent)
    
    # Calculate tempo
    tempo = (team_data['AdjT'] * opp_data['AdjT']) / D1_AVERAGES_TORVIK['tempo']
    
    # Calculate score
    score = (team_data['AdjO'] * opp_data['AdjD'] * tempo) / (D1_AVERAGES_TORVIK['def_efficiency'] * 100)
    
    return score


def calculate_combined_score(kenpom_data: pd.DataFrame, torvik_data: pd.DataFrame, 
                             team: str, opponent: str) -> float:
    """
    Combine Kenpom and Torvik predictions (simple average)
    
    Returns: Average of Kenpom and Torvik predicted scores
    """
    kenpom_score = calculate_kenpom_score(kenpom_data, team, opponent)
    torvik_score = calculate_torvik_score(torvik_data, team, opponent)
    
    # Simple average
    combined_score = (kenpom_score + torvik_score) / 2
    
    return combined_score


def round_to_nearest_half(number: float) -> float:
    """Rounds a number to nearest 0.5"""
    return round(number * 2) / 2


def get_spread_implied_probability(spread: float) -> float:
    """
    Get implied win probability from a point spread
    
    Parameters:
    spread: Point spread value (negative for favorite)
    
    Returns:
    Implied win probability (0-1)
    """
    # Round to nearest half-point to match our lookup table
    spread = round_to_nearest_half(spread)
    
    # Get probability from lookup table
    if spread in SPREAD_TO_WIN_PROB:
        return SPREAD_TO_WIN_PROB[spread]
    
    # If spread is outside our range, cap at extremes
    if spread < min(SPREAD_TO_WIN_PROB.keys()):
        return SPREAD_TO_WIN_PROB[min(SPREAD_TO_WIN_PROB.keys())]
    if spread > max(SPREAD_TO_WIN_PROB.keys()):
        return SPREAD_TO_WIN_PROB[max(SPREAD_TO_WIN_PROB.keys())]
    
    # Should not reach here if our table is comprehensive
    return 0.5


def get_win_probability(kenpom_data, torvik_data, team1, team2, disable_16_upsets=True):
    """
    Calculate win probability for team1 vs team2
    
    Parameters:
    kenpom_data: Kenpom efficiency data
    torvik_data: Torvik efficiency data
    team1, team2: Team names (with or without seed numbers)
    disable_16_upsets: If True, 1-seeds automatically beat 16-seeds
    
    Returns:
    team1_win_prob (float 0-1)
    """
    # Extract seed numbers if present
    team1_seed = int(team1.split("(")[1].split(")")[0]) if "(" in team1 else None
    team2_seed = int(team2.split("(")[1].split(")")[0]) if "(" in team2 else None
    
    # Check for 16 vs 1 seed matchup
    # Check for 16 vs 1 seed matchup
    if disable_16_upsets and team1_seed and team2_seed:
        if (team1_seed == 16 and team2_seed == 1):
            return 0.01  # 16-seed has 1% chance (changed from 0.0)
        elif (team1_seed == 1 and team2_seed == 16):
            return 0.99  # 1-seed has 99% chance (changed from 1.0)
    
    # Calculate scores
    team1_score = calculate_combined_score(kenpom_data, torvik_data, team1, team2)
    team2_score = calculate_combined_score(kenpom_data, torvik_data, team2, team1)
    
    # Calculate spread and get win probability
    spread = team1_score - team2_score
    rounded_spread = round_to_nearest_half(spread)
    
    # Negative spread means team1 is favored
    team1_win_prob = get_spread_implied_probability(-rounded_spread)
    
    return team1_win_prob