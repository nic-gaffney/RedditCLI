# Imports
import praw
from colorama import Fore


# The intro at the start
def intro():
    return(Fore.RED + '''
Welcome to RedditCLI, a command line interface for a read-only reddit instance!
To use RedditCLI, start by typing help in the interface!
Made by u/Gaffclant
    ''')


# The help command
def rhelp():
    return(Fore.CYAN + '\nCommands for RedditCLI'
           + Fore.BLUE + '\n\thelp:' + Fore.MAGENTA + ' Displayes this page'
           + Fore.BLUE
           + '\n\tintro:' + Fore.MAGENTA + ' Displays the intro page again'
           + Fore.BLUE
           + '\n\tget:' + Fore.MAGENTA + ' Gets posts from specified subreddit'
           + Fore.GREEN + '\n\t\tNone>' + Fore.RESET + ' get learnpython new'
           + Fore.MAGENTA
           + '\n\t\tgives you the newst posts from r/learnpython'
           + Fore.BLUE + '\n\texit:' + Fore.MAGENTA + ' Quits the program\n'
           + Fore.RESET)


# Activate subreddit
def getPost(sub, type):
    global inSub
    global reddit
    line = 0
    output = ''
    selector = []

    try:
        type = type.lower()
        sub = sub.lower()
        subreddit = reddit.subreddit(sub)
        inSub = subreddit.display_name
        if type == 'hot':
            for submission in subreddit.hot(limit=10):
                selector.append([line, submission])
                line += 1

        for i in selector:
            t = i[1].title
            title = (t[:75] + '...') if len(t) > 75 else t
            output = f'{output}{i[0]}. {title}\n'
        output = f'{output}\nType the number corresponfing to a post'
    except Exception as e:
        output = f'ERROR: {e}'
    finally:
        return output, selector


def showContent(subm):
    output = ''
    author = subm.author
    output = (f'Author: {author.name}\tKarma: {author.link_karma}\n')
    output = (f'{output}{subm.score}\t{subm.title}\n\n{subm.selftext}')
    return output


# Main loop
def main():
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
        cmd = input(Fore.GREEN + f'{inSub}> ' + Fore.RESET)
        if cmd == 'exit':
            quit()
        args = [_ for _ in cmd.split(' ')]
        try:
            arg1 = args[1]
            arg2 = args[2]
        except IndexError:
            arg1 = None
            arg2 = None

        com = {'help': rhelp(),
               'intro': intro(),
               'get': getPost(arg1, arg2)
               }
        try:
            result, selector = com[args[0]]
        except ValueError:
            result = com[args[0]]
        except KeyError:
            try:
                result = showContent(selector[int(args[0])][1])
            except Exception:
                print(f"Unkown command.\n{rhelp()}")
        finally:
            print(result)


if __name__ == '__main__':
    main()
