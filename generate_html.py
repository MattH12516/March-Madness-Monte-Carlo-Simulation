"""
Generate HTML output for Monte Carlo tournament simulation results
"""
from datetime import datetime

def generate_html(probabilities, n_sims=10000):
    """
    Generate HTML report from Monte Carlo simulation results
    
    Parameters:
    probabilities: Dictionary of {team: {round: probability}} from simulation
    n_sims: Number of simulations run
    
    Returns:
    HTML string
    """
    
    # Sort teams by championship probability
    sorted_teams = sorted(probabilities.items(), 
                         key=lambda x: x[1].get('Champion', 0), 
                         reverse=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>March Madness Monte Carlo Simulation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        
        .methodology {{
            background: #f8f9fa;
            padding: 30px 40px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .methodology h2 {{
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        
        .methodology p {{
            color: #555;
            line-height: 1.8;
            margin-bottom: 10px;
        }}
        
        .methodology ul {{
            margin-left: 20px;
            color: #555;
            line-height: 1.8;
        }}
        
        .controls {{
            padding: 20px 40px;
            background: white;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .search-box {{
            flex: 1;
            max-width: 400px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .table-container {{
            padding: 40px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        
        thead {{
            background: #1e3c72;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        th {{
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }}
        
        th:hover {{
            background: #2a5298;
        }}
        
        th::after {{
            content: ' ⇅';
            opacity: 0.5;
            font-size: 0.8em;
        }}
        
        tbody tr {{
            border-bottom: 1px solid #e0e0e0;
            transition: background 0.2s;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        td {{
            padding: 12px;
        }}
        
        .team-name {{
            font-weight: 600;
            color: #1e3c72;
        }}
        
        /* Seed color coding */
        .seed-1 {{ background: rgba(255, 215, 0, 0.1); }}
        .seed-2 {{ background: rgba(192, 192, 192, 0.1); }}
        .seed-3 {{ background: rgba(205, 127, 50, 0.1); }}
        .seed-4 {{ background: rgba(100, 149, 237, 0.1); }}
        .seed-5 {{ background: rgba(144, 238, 144, 0.1); }}
        .seed-6 {{ background: rgba(255, 182, 193, 0.1); }}
        
        .prob-cell {{
            text-align: center;
            font-weight: 500;
        }}
        
        /* Probability highlighting */
        .prob-high {{ color: #10b981; font-weight: 600; }}
        .prob-med {{ color: #f59e0b; }}
        .prob-low {{ color: #6b7280; }}
        
        footer {{
            padding: 30px 40px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .hidden {{
            display: none;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}
            
            .table-container {{
                padding: 20px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 8px 6px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏀 March Madness Monte Carlo Simulation</h1>
            <div class="subtitle">
                Based on {n_sims:,} simulated tournaments<br>
                Combines Kenpom + Torvik Efficiency Ratings
            </div>
        </header>
        
        <div class="methodology">
            <h2>Methodology</h2>
            <p>
                This simulation uses Monte Carlo methods to model tournament outcomes by:
            </p>
            <ul>
                <li><strong>Running {n_sims:,} random tournaments:</strong> Each simulation plays through the entire bracket using win probabilities derived from team efficiency ratings</li>
                <li><strong>Aggregating results:</strong> Final probabilities represent how often each team reached each round across all simulations</li>
            </ul>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search for team..." autocomplete="off">
            </div>
            <span id="resultCount" style="color: #666;"></span>
        </div>
        
        <div class="table-container">
            <table id="resultsTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Team</th>
                        <th onclick="sortTable(1)">Round of 32</th>
                        <th onclick="sortTable(2)">Sweet 16</th>
                        <th onclick="sortTable(3)">Elite 8</th>
                        <th onclick="sortTable(4)">Final 4</th>
                        <th onclick="sortTable(5)">Championship</th>
                        <th onclick="sortTable(6)">Champion</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
"""
    
    # Generate table rows
    for team, probs in sorted_teams:
        # Extract seed number for styling
        seed = team.split("(")[1].split(")")[0] if "(" in team else "0"
        seed_class = f"seed-{seed}" if seed.isdigit() and int(seed) <= 6 else ""
        
        # Get probabilities for each round
        r32 = probs.get('Round of 32', 0)
        s16 = probs.get('Sweet 16', 0)
        e8 = probs.get('Elite 8', 0)
        ff = probs.get('Final 4', 0)
        champ_game = probs.get('Championship', 0)
        champion = probs.get('Champion', 0)
        
        # Helper function to get probability class
        def get_prob_class(prob):
            if prob >= 20:
                return 'prob-high'
            elif prob >= 5:
                return 'prob-med'
            else:
                return 'prob-low'
        
        # Format probabilities
        def fmt(prob):
            if prob == 0:
                return '—'
            elif prob < 0.05:
                return '<0.1%'
            else:
                return f'{prob:.1f}%'
        
        html += f"""                    <tr class="{seed_class}">
                        <td class="team-name">{team}</td>
                        <td class="prob-cell {get_prob_class(r32)}">{fmt(r32)}</td>
                        <td class="prob-cell {get_prob_class(s16)}">{fmt(s16)}</td>
                        <td class="prob-cell {get_prob_class(e8)}">{fmt(e8)}</td>
                        <td class="prob-cell {get_prob_class(ff)}">{fmt(ff)}</td>
                        <td class="prob-cell {get_prob_class(champ_game)}">{fmt(champ_game)}</td>
                        <td class="prob-cell {get_prob_class(champion)}">{fmt(champion)}</td>
                    </tr>
"""
    
    html += f"""                </tbody>
            </table>
        </div>
        
        <footer>
            <p>Generated on {timestamp}</p>
            <p style="margin-top: 10px;">
                Model combines Kenpom and Torvik efficiency ratings using Monte Carlo simulation.<br>
            </p>
        </footer>
    </div>
    
    <script>
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const tableBody = document.getElementById('tableBody');
        const resultCount = document.getElementById('resultCount');
        const allRows = Array.from(tableBody.getElementsByTagName('tr'));
        
        function updateResultCount() {{
            const visibleRows = allRows.filter(row => !row.classList.contains('hidden')).length;
            resultCount.textContent = `Showing ${{visibleRows}} of ${{allRows.length}} teams`;
        }}
        
        searchInput.addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            
            allRows.forEach(row => {{
                const teamName = row.cells[0].textContent.toLowerCase();
                if (teamName.includes(searchTerm)) {{
                    row.classList.remove('hidden');
                }} else {{
                    row.classList.add('hidden');
                }}
            }});
            
            updateResultCount();
        }});
        
        // Table sorting
        let sortDirection = 1;
        let lastSortColumn = -1;
        
        function sortTable(columnIndex) {{
            const table = document.getElementById('resultsTable');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            
            // Toggle sort direction if clicking same column
            if (columnIndex === lastSortColumn) {{
                sortDirection *= -1;
            }} else {{
                sortDirection = 1;
                lastSortColumn = columnIndex;
            }}
            
            rows.sort((a, b) => {{
                let aValue = a.cells[columnIndex].textContent;
                let bValue = b.cells[columnIndex].textContent;
                
                // Handle percentage values
                if (columnIndex > 0) {{
                    aValue = aValue === '—' || aValue === '<0.1%' ? 0 : parseFloat(aValue);
                    bValue = bValue === '—' || bValue === '<0.1%' ? 0 : parseFloat(bValue);
                    return (aValue - bValue) * sortDirection;
                }}
                
                // String comparison for team names
                return aValue.localeCompare(bValue) * sortDirection;
            }});
            
            // Re-append rows in sorted order
            rows.forEach(row => tbody.appendChild(row));
        }}
        
        // Initialize result count
        updateResultCount();
    </script>
</body>
</html>
"""
    
    return html


def save_html(probabilities, filename='monte_carlo_results.html', n_sims=10000):
    """
    Generate and save HTML report
    
    Parameters:
    probabilities: Dictionary from Monte Carlo simulation
    filename: Output filename
    n_sims: Number of simulations run
    """
    html = generate_html(probabilities, n_sims)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ HTML report saved to {filename}")
    print(f"  Open in browser to view interactive results")