import argparse
from . import db


def cmd_init(args):
    db.init_db()
    print('Database initialized.')


def cmd_add(args):
    db.add_note(content=args.content, file_path=args.file, question=args.question,
                question_file=args.question_file, course=args.course,
                chapter=args.chapter, max_cooldown=args.max_cooldown)
    print('Note added.')


def cmd_due(args):
    notes = db.fetch_due_notes()
    for n in notes:
        print(n)


def cmd_inc(args):
    conn_cool = args.increase
    db.update_cooldown(args.note_id, conn_cool)
    print(f'Cooldown updated to {conn_cool}.')


def cmd_reset(args):
    db.update_cooldown(args.note_id, 1)
    print('Cooldown reset to 1.')


def build_parser():
    p = argparse.ArgumentParser(description='Study Manager CLI')
    sub = p.add_subparsers(dest='command')

    init_p = sub.add_parser('init', help='Initialize database')
    init_p.set_defaults(func=cmd_init)

    add_p = sub.add_parser('add', help='Add new note')
    add_p.add_argument('--content')
    add_p.add_argument('--file')
    add_p.add_argument('--question')
    add_p.add_argument('--question-file')
    add_p.add_argument('--course')
    add_p.add_argument('--chapter')
    add_p.add_argument('--max-cooldown', type=int, default=1)
    add_p.set_defaults(func=cmd_add)

    due_p = sub.add_parser('due', help='Show due notes')
    due_p.set_defaults(func=cmd_due)

    inc_p = sub.add_parser('inc', help='Increase cooldown by 1')
    inc_p.add_argument('note_id', type=int)
    inc_p.add_argument('increase', type=int, nargs='?', default=None)
    inc_p.set_defaults(func=cmd_inc)

    reset_p = sub.add_parser('reset', help='Reset cooldown to 1')
    reset_p.add_argument('note_id', type=int)
    reset_p.set_defaults(func=cmd_reset)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

