import textwrap

story = '''Welcome to ChronoQuest.

You are a daring time-traveler, stepping into a world where every airport holds
mysteries, and every flight brings you closer to victory. With your player
record stored safely in the ChronoQuest database, your journey begins at your
starting airport. From there, your money, range, and goals determine whether
you can outsmart fate.

At each airport, you are greeted with a message: your current funds, your
remaining travel range, and a chance to open a lootbox. Some airports hide
rewards—points, money, or fuel—that boost your progress. Others may hold
traps, costing you everything if you are unlucky.

Your quest is guided by goals in the database: fly across continents, complete
long-distance flights, visit legendary airports, and earn points to prove your
skill. Along the way, you might even uncover the rare Chrono Diamond, the
ultimate prize of ChronoQuest.

But beware—rumors of bandits and sudden misfortune haunt the airports. A
single wrong step can set you back to zero. To win, you must reach your goals
and return to your starting point with your wealth, range, and victories
intact.

ChronoQuest is not just about flying—it’s about strategy, survival, and
claiming your place in history. Can you complete the goals, outlast the
journey, and return home victorious? The adventure awaits.'''

# Set column width to 80 characters
wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
# Wrap text
word_list = wrapper.wrap(text=story)

def getStory():
    return word_list
