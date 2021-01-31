# Imports
import praw
import os
from colorama import Fore


# The intro at the start
def intro(args):
    return(Fore.YELLOW + '\nWelcome to RedditCLI, '
           + 'a command line interface for a'
           'read-only reddit instance!'
           '\nTo use RedditCLI, start by typing' + Fore.RESET + ' help '
           + Fore.YELLOW + 'in the interface!'
           '\nMade by u/Gaffclant\n' + Fore.RESET)


# The help command
def rhelp(args):
    return(Fore.LIGHTRED_EX + '\nCommands for RedditCLI'
           + Fore.CYAN + '\n\thelp:'
           + Fore.MAGENTA + ' Displayes this page'
           + Fore.CYAN
           + '\n\tintro:' + Fore.MAGENTA + ' Displays the intro page again'
           + Fore.CYAN
           + '\n\tget<subreddit><type>:' + Fore.MAGENTA + ' Gets posts'
           + ' from specified subreddit'
           + Fore.MAGENTA + '\n\t\tTYPES: ' + Fore.CYAN + 'new, top, hot,'
           + ' rising, gilded, controversial'
           + Fore.GREEN + '\n\t\tNone>' + Fore.RESET + ' get learnpython new'
           + Fore.MAGENTA
           + '\n\t\tgives you the newest posts from r/learnpython'
           + Fore.CYAN + '\n\texit:'
           + Fore.MAGENTA + ' Quits the program\n'
           + Fore.RESET)


def getType(subreddit, type):
    line = 0
    selector = []

    if type == 'hot':
        for submission in subreddit.hot(limit=10):
            selector.append([line, submission])
            line += 1
    elif type == 'new':
        for submission in subreddit.new(limit=10):
            selector.append([line, submission])
            line += 1
    elif type == 'controversial':
        for submission in subreddit.controversial(limit=10):
            selector.append([line, submission])
            line += 1
    elif type == 'gilded':
        for submission in subreddit.gilded(limit=10):
            selector.append([line, submission])
            line += 1
    elif type == 'rising':
        for submission in subreddit.rising(limit=10):
            selector.append([line, submission])
            line += 1
    elif type == 'top':
        for submission in subreddit.top(limit=10):
            selector.append([line, submission])
            line += 1

    return selector


# Activate subreddit
def getPost(args):
    if (len(args) < 2):
        return 'Get command requires at least 2 arguments!'
    sub = args[0]
    type = args[1]

    global inSub
    global reddit
    output = ''
    submissions = []

    try:
        type = type.lower()
        sub = sub.lower()
        subreddit = reddit.subreddit(sub)
        inSub = subreddit.display_name
        submission = getType(subreddit, type)

        # Turn selector into printable data
        for i in submission:
            t = i[1].title
            title = (t[:65] + '...') if len(t) > 75 else t

            # Initialize the output
            output = (f'{output}' + Fore.LIGHTBLUE_EX + f'{i[0]}. '
                      + Fore.LIGHTRED_EX + f'{title}\n')

        output = f'{output}\nType the number corresponfing to a post'
    except Exception as e:
        output = f'ERROR: {e}'
    finally:
        # This will be run after the command is completed
        def continuationFunction():
            # Getting the post the user would like to view
            postStr = input(Fore.GREEN + f'GET {inSub}> ' + Fore.RESET)

            try:
                # Converting it into a number
                postNum = int(postStr)

                # Making sure post number inputted is within
                # range of the submissions list
                if 0 <= postNum < len(submissions):
                    print(showContent(submissions[postNum][1]))

                # Recurssivly calling continuation function
                # just incase user wants to view more posts
                continuationFunction()
            except ValueError as e:
                print(e)
                # Returning back to previous state if
                # no number is passed
                return
        return (output, continuationFunction)


# Show content in submisision
def showContent(subm):
    output = ''
    isText = subm.is_self
    if isText:
        use = subm.selftext
    else:
        use = subm.url

    author = subm.author
    output = (f'Author: {author.name}\tKarma: {author.link_karma}\n')
    output = (f'{output}{subm.score}\t{subm.title}\n\n{use}')
    return output


# Main loop
def main():
    os.system('clear')
    global inSub
    global reddit
    args = []
    inSub = None

    agent = 'PC, MAc, Linux. Reddit from the command line by u/Gaffclant v1.0'
    reddit = praw.Reddit(client_id="BGLk80bE3REJAw",
                         client_secret=None,
                         user_agent=agent
                         )

# Start Program
    print(intro(None))
    while True:

        # Displays command line as 'GET SUBREDDIT> '
        cmd = input(Fore.GREEN + f'{inSub}> ' + Fore.RESET)

        commands = {
            'quit': lambda args: quit(),
            'clear': lambda args: os.system('clear'),
            'help': rhelp,
            'intro': intro,
            'get': getPost
        }

        # Get command & its arguments
        command = cmd.split(' ')[0].lower()
        args = cmd.split(' ')[1:]

        # Execute function corosponding to the command
        if command in commands:
            func = commands[command]
            res = func(args)

            # Turning the response into a tuple if it isnt already one
            if not type(res) == tuple:
                # Response tuples should always be formatted as
                # (output, continuation function), anything else
                # will be ignored. The continuation function
                # allows for commands to have continued presence
                res = tuple([res])

            # Printing the output (first element in the tuple)
            print(res[0])

            # Running the continuation function
            if len(res) > 1:
                res[1]()


if __name__ == '__main__':
    main()
