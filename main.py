# Imports
import praw
import pathlib
import os
import requests
from colorama import Fore
# Huge thanks to the contribution made by https://github.com/CatDevz


# DECORATORS
def funcPrint(f):
    def printable(args):
        print(f(args))
        # The intro at the start
    return printable


@funcPrint
def intro(args):
    return(Fore.YELLOW
           + '\nWelcome to RedditCLI, '
           + 'a command line interface for a'
           + 'read-only reddit instance!'
           + '\nTo use RedditCLI, start by typing'
           + Fore.RESET
           + ' help '
           + Fore.YELLOW
           + 'in the interface!'
           + '\nMade by u/Gaffclant\n'
           + Fore.RESET)


# The help command
@funcPrint
def rhelp(args):
    return(Fore.LIGHTRED_EX
           + '\nCommands for RedditCLI'
           + Fore.CYAN
           + '\n\thelp:'
           + Fore.MAGENTA
           + ' Displayes this page'
           + Fore.CYAN
           + '\n\tintro:'
           + Fore.MAGENTA
           + ' Displays the intro page again'
           + Fore.CYAN
           + '\n\tget<subreddit><type>:'
           + Fore.MAGENTA + ' Gets posts'
           + ' from specified subreddit'
           + Fore.MAGENTA + '\n\t\tTYPES: '
           + Fore.CYAN + 'new, top, hot,'
           + ' rising, gilded, controversial'
           + Fore.GREEN
           + '\n\t\tCommand>' + Fore.RESET
           + ' get learnpython new'
           + Fore.MAGENTA
           + '\n\t\tgives you the newest posts from r/learnpython'
           + Fore.CYAN
           + '\n\tquit:'
           + Fore.MAGENTA
           + ' Quits the program'
           + Fore.CYAN
           + '\n\tclear:'
           + Fore.MAGENTA
           + ' Clears the terminal\n'
           + Fore.RESET)


def downloader(url, id):
    if not os.path.exists('Images'):
        os.makedirs('Images')
    download = input(Fore.LIGHTRED_EX
                     + f'Download {url}? [Y/n]: ')
    if download == 'Y':
        down = requests.get(url)
        extenstion = pathlib.Path(url).suffix
        img = os.path.join('Images', id)
        open(f'{img}{extenstion}', 'wb').write(down.content)
    else:
        print(Fore.CYAN + 'Cancled download' + Fore.RESET)


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


# Get the informarion of the comments from the submission
def commentParser(com):
    for comment in com:
        try:
            sample = comment.parent().body[:30] + '...'
        except AttributeError:
            sample = comment.parent().selftext[:30] + '...'
        output = (Fore.RED + '#'*20 + Fore.MAGENTA
                  + '\nReply to: ' + Fore.YELLOW
                  + f'{comment.parent().author}> ' + Fore.CYAN
                  + (sample)
                  + Fore.YELLOW
                  + f'\n{comment.author}> '
                  + Fore.RESET + f'{comment.body}')
        print(output)


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
        submissions = getType(subreddit, type)

        # Turn selector into printable data
        for i in submissions:
            t = i[1].title
            auth = i[1].author
            title = (t[:65] + '...') if len(t) > 75 else t

            # Initialize the output
            output = (f'{output}' + Fore.LIGHTBLUE_EX + f'{i[0]}. '
                      + Fore.LIGHTMAGENTA_EX + f'{title}'
                      + Fore.YELLOW + f'-{auth}\n'
                      )

        output = (f'{output}\n' + Fore.CYAN
                  + 'Type <num to post> <number of comments to show>'
                  + ' or type exit to quit GET mode.'
                  + Fore.RESET)

    except Exception as e:
        output = f'ERROR: {e}'
    finally:
        out = '\n' + Fore.RED + '#'*40 + '\n' + output + Fore.RESET
        # This will be run after the command is completed

        def continuationFunction():
            # Getting the post the user would like to view
            print(out)
            comArg = input(Fore.GREEN + f'GET {inSub}> ' + Fore.RESET)
            args = comArg.split(' ')
            com = args[0].lower()
            if str(com) == ('exit'):
                return
            elif str(com) == ('clear'):
                os.system('clear')
                continuationFunction()
            elif len(args) < 2:
                if str(com) == ('exit'):
                    return
                elif str(com) == ('clear'):
                    os.system('clear')
                print('This takes 2 arguments!')
                continuationFunction()
            try:
                if str(com) == ('exit'):
                    return
                elif str(com) == ('clear'):
                    os.system('clear')
                postStr = args[0]
                comStr = args[1]
            except IndexError:
                if str(com) == ('exit'):
                    return
                elif str(com) == ('clear'):
                    os.system('clear')
                print('This takes 2 arguments!')
                continuationFunction()
            try:
                if str(com) == ('exit'):
                    return
                elif str(com) == ('clear'):
                    os.system('clear')
                if str(com) == ('exit'):
                    return
                # Converting it into a number
                postNum = int(postStr)
                comNum = int(comStr)

                # Making sure post number inputted is within
                # range of the submissions list
                if 0 <= postNum < len(submissions):
                    output = showContent(submissions[postNum][1], comNum)
                    print(output[0])

                    isText = output[1]
                    use = output[2]
                    id = output[3]
                    comments = output[4]
                    if not isText:
                        downloader(use, id)

                    commentParser(comments)

                # Recurssivly calling continuation function
                # just incase user wants to view more posts
                continuationFunction()
            except ValueError:
                if str(com) == ('exit'):
                    return
                elif str(com) == ('clear'):
                    os.system('clear')
                # Returning back to previous state if
                # no number is passed
                return
        return (output, continuationFunction)


# Show content in submisision
def showContent(subm, com):
    subm.comments.replace_more(limit=com)
    comments = subm.comments.list()[:com]

    output = []
    id = subm.id
    author = subm.author
    isText = subm.is_self

    if isText:
        use = subm.selftext
    else:
        use = subm.url

    text = (Fore.LIGHTBLUE_EX
            + 'Author: '
            + Fore.YELLOW
            + f'{author.name}'
            + Fore.LIGHTBLUE_EX
            + '\tKarma: '
            + Fore.YELLOW
            + f'{author.link_karma}\n'
            + Fore.LIGHTCYAN_EX
            + f'{subm.score}'
            + Fore.LIGHTMAGENTA_EX
            + f'\t{subm.title}' + Fore.RESET + f'\n\n{use}\n')

    output = [text, isText, use, id, comments]

    return output


# Main loop
def main():
    os.system('clear')
    global inSub
    global reddit
    args = []
    inSub = None

    agent = ('Windows, MacOS, Linux Reddit from the '
             + 'command line RedditCLI by u/Gaffclant v1.3')
    reddit = praw.Reddit(client_id="BGLk80bE3REJAw",
                         client_secret=None,
                         user_agent=agent
                         )

# Start Program
    intro(None)
    while True:

        # Displays command line as 'GET SUBREDDIT> '
        cmd = input(Fore.GREEN + 'Command> ' + Fore.RESET)

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
            res[0]

            # Running the continuation function
            if len(res) > 1:
                res[1]()


if __name__ == '__main__':
    main()
