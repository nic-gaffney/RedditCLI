# Imports
import praw
import os
from colorama import Fore


# The intro at the start
def intro():
    return(Fore.YELLOW + '\nWelcome to RedditCLI, a command line interface for a'
           'read-only reddit instance!'
           '\nTo use RedditCLI, start by typing' + Fore.RESET + ' help '
           + Fore.YELLOW + 'in the interface!'
           '\nMade by u/Gaffclant\n' + Fore.RESET)


# The help command
def rhelp():
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
def getPost(sub, type):
    global inSub
    global reddit
    output = ''
    selector = []

    try:
        type = type.lower()
        sub = sub.lower()
        subreddit = reddit.subreddit(sub)
        inSub = subreddit.display_name
        selector = getType(subreddit, type)

        # Turn selector into printable data
        for i in selector:
            t = i[1].title
            title = (t[:65] + '...') if len(t) > 75 else t

            # Initialize the output
            output = (f'{output}' + Fore.LIGHTBLUE_EX + f'{i[0]}. '
                      + Fore.LIGHTRED_EX + f'{title}\n')

        output = f'{output}\nType the number corresponfing to a post'
    except Exception as e:
        output = f'ERROR: {e}'
    finally:
        return output, selector


# Show content in subreddit
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
    selector = []
    inSub = None

    agent = 'PC, MAc, Linux. Reddit from the command line by u/Gaffclant v1.0'
    reddit = praw.Reddit(client_id="BGLk80bE3REJAw",
                         client_secret=None,
                         user_agent=agent
                         )

# Start Program
    print(intro())
    while True:
        result = ''

        # Displays command line as 'SUBREDDIT> '
        cmd = input(Fore.GREEN + f'{inSub}> ' + Fore.RESET)

        # Handle clear and exit commands
        if cmd == 'exit':
            os.system('clear')
            quit()
        elif cmd == 'clear':
            os.system('clear')

        # Split input into readable values
        args = [_ for _ in cmd.split(' ')]
        try:
            arg1 = args[1]
            arg2 = args[2]
        except IndexError:
            arg1 = None
            arg2 = None

        # The commands
        com = {
               'help': rhelp(),
               'intro': intro(),
               'get': getPost(arg1, arg2),
               }

        # Determines how to read the command
        try:
            result, selector = com[args[0]]
        except ValueError:
            result = com[args[0]]
        except KeyError:
            try:
                result = showContent(selector[int(args[0])][1])
            except Exception:
                if cmd == 'clear':
                    continue
                else:
                    print(Fore.RED + f"ERROR: Unkown command.\n{rhelp()}"
                          + Fore.RESET)
        finally:
            print(result)


if __name__ == '__main__':
    main()
