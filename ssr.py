from cmd import *
import prompt_toolkit as pt


if __name__ == '__main__':
    cmds = {
        'info'  : cmd_info,
        'get'   : cmd_get,
        'set'   : cmd_set,
        'start' : cmd_start,
        'kill'  : cmd_kill,
        'help'  : cmd_help,
        'exit'  : cmd_exit
    }
    print_welcome()
    nodes = load_config_file()
    comp = pt.completion.WordCompleter(list(cmds.keys()) + list(nodes.keys()))
    session = pt.PromptSession(history=pt.history.FileHistory('.demo.history'), 
                            auto_suggest=pt.auto_suggest.AutoSuggestFromHistory(), 
                            completer=comp, complete_while_typing=True)
    while True:
        user_input = str(session.prompt('>> ')).strip()
        if not user_input:
            continue
        words = user_input.split()
        func = cmds.get(words[0])
        func(words, nodes) if func else cmd_unknown(words)