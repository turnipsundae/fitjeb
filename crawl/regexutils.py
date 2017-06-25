import re

"""
Identifies gender, age, height, weight, and completion time
in comment.
"""

# Returns titles e.g. **WORKOUT** from og:description
TITLE_RE = re.compile(r'\*\*(.+)\*\*(?im)')

# Returns the workout's unit of measure from og:description
UOM_RE = re.compile(r'post (.*?) to comment(?im)')

# Returns gender from a comment. Also returns the line containing it.
GENDER_RE = re.compile(r'^.*?([mf](?=\s?\/)|male|female).*$(?im)')

# Returns age from a comment
AGE_RE = re.compile(r"[./]\s?([1-9][0-9])\s?[./]")

# Returns Rx or modified from a comment
RX_RE = re.compile(r"(rx)(?im)")

# Returns time score from a comment
TIME_SCORE_RE = re.compile(r'(\d+:\d{2})(?m)')

# Returns points or reps type of score from a comment
REPS_SCORE_RE = re.compile(r'(\d+)\s?(?:rx|rep|cal|point|pt|round|rd)(?im)')

# keywords for identifying the type of workout e.g. time, reps, wt
STD_UOM_TIME = 0
STD_UOM_REPS = 1

# Returns the proper regex based on uom
def get_score_re(uom):
    TIME_KWS = ['time', 'min', 'mins', 'minute', 'minutes']
    REPS_KWS = ['rep', 'reps', 'repetition', 'repetitions',
                'cal', 'cals', 'calorie', 'calories',
                'pt', 'pts', 'point', 'points',
                'rd', 'rds', 'round', 'rounds']
    for unit in TIME_KWS:
        if unit in uom.lower():
            return TIME_SCORE_RE, STD_UOM_TIME
    for unit in REPS_KWS:
        if unit in uom.lower():
            return REPS_SCORE_RE, STD_UOM_REPS
    return None, None


