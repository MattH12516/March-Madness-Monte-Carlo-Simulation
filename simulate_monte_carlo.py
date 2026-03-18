"""
Monte Carlo Tournament Simulator
Runs thousands of random tournament simulations to calculate advance probabilities
"""
import random
from collections import defaultdict
from models import get_win_probability

# Tournament bracket structure
TOURNAMENT_TEAMS = {
    "East": [
        {"seed": 1, "team": "Duke"}, {"seed": 16, "team": "Siena"},
        {"seed": 8, "team": "Ohio St."}, {"seed": 9, "team": "TCU"},
        {"seed": 5, "team": "St. John's"}, {"seed": 12, "team": "Northern Iowa"},
        {"seed": 4, "team": "Kansas"}, {"seed": 13, "team": "Cal Baptist"},
        {"seed": 6, "team": "Louisville"}, {"seed": 11, "team": "South Florida"},
        {"seed": 3, "team": "Michigan St."}, {"seed": 14, "team": "North Dakota St."},
        {"seed": 7, "team": "UCLA"}, {"seed": 10, "team": "UCF"},
        {"seed": 2, "team": "Connecticut"}, {"seed": 15, "team": "Furman"}
    ],
    "West": [
        {"seed": 1, "team": "Arizona"}, {"seed": 16, "team": "LIU"},
        {"seed": 8, "team": "Villanova"}, {"seed": 9, "team": "Utah St."},
        {"seed": 5, "team": "Wisconsin"}, {"seed": 12, "team": "High Point"},
        {"seed": 4, "team": "Arkansas"}, {"seed": 13, "team": "Hawaii"},
        {"seed": 6, "team": "BYU"}, {"seed": 11, "team": "Texas"},
        {"seed": 3, "team": "Gonzaga"}, {"seed": 14, "team": "Kennesaw St."},
        {"seed": 7, "team": "Miami FL"}, {"seed": 10, "team": "Missouri"},
        {"seed": 2, "team": "Purdue"}, {"seed": 15, "team": "Queens"}
    ],
    "South": [
        {"seed": 1, "team": "Florida"}, {"seed": 16, "team": "Prairie View A&M/Lehigh"},
        {"seed": 8, "team": "Clemson"}, {"seed": 9, "team": "Iowa"},
        {"seed": 5, "team": "Vanderbilt"}, {"seed": 12, "team": "McNeese"},
        {"seed": 4, "team": "Nebraska"}, {"seed": 13, "team": "Troy"},
        {"seed": 6, "team": "North Carolina"}, {"seed": 11, "team": "VCU"},
        {"seed": 3, "team": "Illinois"}, {"seed": 14, "team": "Penn"},
        {"seed": 7, "team": "Saint Mary's"}, {"seed": 10, "team": "Texas A&M"},
        {"seed": 2, "team": "Houston"}, {"seed": 15, "team": "Idaho"}
    ],
    "Midwest": [
        {"seed": 1, "team": "Michigan"}, {"seed": 16, "team": "UMBC"},
        {"seed": 8, "team": "Georgia"}, {"seed": 9, "team": "Saint Louis"},
        {"seed": 5, "team": "Texas Tech"}, {"seed": 12, "team": "Akron"},
        {"seed": 4, "team": "Alabama"}, {"seed": 13, "team": "Hofstra"},
        {"seed": 6, "team": "Tennessee"}, {"seed": 11, "team": "SMU/Miami OH"},
        {"seed": 3, "team": "Virginia"}, {"seed": 14, "team": "Wright St."},
        {"seed": 7, "team": "Kentucky"}, {"seed": 10, "team": "Santa Clara"},
        {"seed": 2, "team": "Iowa St."}, {"seed": 15, "team": "Tennessee St."}
    ]
}


def get_round_64_matchups():
    """
    Generate all Round of 64 matchups with seeds
    
    Returns:
    List of (team1_with_seed, team2_with_seed, region) tuples
    """
    matchups = []
    matchup_pairs = [(1, 16), (8, 9), (5, 12), (4, 13), (6, 11), (3, 14), (7, 10), (2, 15)]
    
    for region, teams in TOURNAMENT_TEAMS.items():
        for seed1, seed2 in matchup_pairs:
            team1_info = next((t for t in teams if t['seed'] == seed1), None)
            team2_info = next((t for t in teams if t['seed'] == seed2), None)
            
            if team1_info and team2_info:
                team1 = team1_info['team']
                team2 = team2_info['team']
                
                # Handle play-in games - for Monte Carlo, just pick first team
                if '/' in team1:
                    team1 = team1.split('/')[0]
                if '/' in team2:
                    team2 = team2.split('/')[0]
                
                # Format with seed
                team1_formatted = f"({seed1}) {team1}"
                team2_formatted = f"({seed2}) {team2}"
                
                matchups.append((team1_formatted, team2_formatted, region))
    
    return matchups


def simulate_game(team1, team2, kenpom_data, torvik_data):
    """
    Simulate a single game and return the winner
    
    Parameters:
    team1, team2: Team names (with seed numbers)
    kenpom_data, torvik_data: Efficiency DataFrames
    
    Returns:
    Winner's name (with seed)
    """
    # Get win probability for team1
    team1_win_prob = get_win_probability(kenpom_data, torvik_data, team1, team2)
    
    # Random outcome based on probability
    if random.random() < team1_win_prob:
        return team1
    else:
        return team2


def create_round_matchups(winners, bracket_structure):
    """
    Create next round matchups from previous round winners
    
    Parameters:
    winners: List of winners from previous round (with regions)
    bracket_structure: Which bracket positions match up
    
    Returns:
    List of (team1, team2, region) tuples for next round
    """
    matchups = []
    
    # Group winners by region
    region_winners = defaultdict(list)
    for winner, region in winners:
        region_winners[region].append(winner)
    
    # Create matchups within each region
    for region, teams in region_winners.items():
        # Pair up teams sequentially (winner 1 vs winner 2, winner 3 vs winner 4, etc.)
        for i in range(0, len(teams), 2):
            if i + 1 < len(teams):
                matchups.append((teams[i], teams[i+1], region))
    
    return matchups


def simulate_single_tournament(kenpom_data, torvik_data):
    """
    Simulate ONE complete random tournament
    
    Returns:
    Dictionary with winners at each round level
    """
    bracket = {
        'Round of 64': [],
        'Round of 32': [],
        'Sweet 16': [],
        'Elite 8': [],
        'Final 4': [],
        'Championship': None
    }
    
    # Round of 64
    round_64_matchups = get_round_64_matchups()
    for team1, team2, region in round_64_matchups:
        winner = simulate_game(team1, team2, kenpom_data, torvik_data)
        bracket['Round of 64'].append((winner, region))
    
    # Round of 32
    round_32_matchups = create_round_matchups(bracket['Round of 64'], None)
    for team1, team2, region in round_32_matchups:
        winner = simulate_game(team1, team2, kenpom_data, torvik_data)
        bracket['Round of 32'].append((winner, region))
    
    # Sweet 16
    sweet_16_matchups = create_round_matchups(bracket['Round of 32'], None)
    for team1, team2, region in sweet_16_matchups:
        winner = simulate_game(team1, team2, kenpom_data, torvik_data)
        bracket['Sweet 16'].append((winner, region))
    
    # Elite 8
    elite_8_matchups = create_round_matchups(bracket['Sweet 16'], None)
    for team1, team2, region in elite_8_matchups:
        winner = simulate_game(team1, team2, kenpom_data, torvik_data)
        bracket['Elite 8'].append((winner, region))
    
    # Final Four - specific region pairings
    final_four_regions = [('East', 'South'), ('Midwest', 'West')]
    final_four_winners = []
    
    for region1, region2 in final_four_regions:
        # Get winner from each region
        team1 = next((team for team, reg in bracket['Elite 8'] if reg == region1), None)
        team2 = next((team for team, reg in bracket['Elite 8'] if reg == region2), None)
        
        if team1 and team2:
            winner = simulate_game(team1, team2, kenpom_data, torvik_data)
            final_four_winners.append(winner)
            bracket['Final 4'].append((winner, "Final Four"))
    
    # Championship
    if len(final_four_winners) == 2:
        champion = simulate_game(final_four_winners[0], final_four_winners[1], 
                                kenpom_data, torvik_data)
        bracket['Championship'] = champion
    
    return bracket


def run_monte_carlo_simulation(kenpom_data, torvik_data, n_sims=10000):
    """
    Run Monte Carlo simulation of tournament
    
    Parameters:
    kenpom_data, torvik_data: Team efficiency DataFrames
    n_sims: Number of simulations to run (default 10,000)
    
    Returns:
    Dictionary with advance probabilities for each team at each round
    """
    print(f"Running {n_sims:,} Monte Carlo simulations...")
    
    # Track how many times each team reaches each round
    advance_counts = defaultdict(lambda: defaultdict(int))
    
    # Run simulations
    for i in range(n_sims):
        if (i + 1) % 1000 == 0:
            print(f"  Completed {i + 1:,}/{n_sims:,} simulations...")
        
        # Simulate one tournament
        bracket = simulate_single_tournament(kenpom_data, torvik_data)
        
        # Count who reached each round
        for team, region in bracket['Round of 64']:
            advance_counts[team]['Round of 32'] += 1
        
        for team, region in bracket['Round of 32']:
            advance_counts[team]['Sweet 16'] += 1
        
        for team, region in bracket['Sweet 16']:
            advance_counts[team]['Elite 8'] += 1
        
        for team, region in bracket['Elite 8']:
            advance_counts[team]['Final 4'] += 1
        
        for team, region in bracket['Final 4']:
            advance_counts[team]['Championship'] += 1
        
        champion = bracket['Championship']
        if champion:
            advance_counts[champion]['Champion'] += 1
    
    # Convert counts to percentages
    probabilities = {}
    for team in advance_counts:
        probabilities[team] = {
            round_name: (count / n_sims) * 100
            for round_name, count in advance_counts[team].items()
        }
    
    print(f"✓ Monte Carlo simulation complete!")
    return probabilities