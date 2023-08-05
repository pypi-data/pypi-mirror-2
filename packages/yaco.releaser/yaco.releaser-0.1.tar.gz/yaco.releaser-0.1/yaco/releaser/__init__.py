

def sufix_commit_msg(data, msg_key="commit_msg"):
    """ Offer extend commit message"""
    print "Message for next commit is ",
    print "'%s'" % (data[msg_key] % data)
    response = raw_input("Extra text to commit message (view #ticket)?: ").strip()
    if response and response not in ('no', 'n'):
        data[msg_key] = '%s %s' % (data[msg_key], response)

if __name__ == '__main__':
    data = {"commit_msg": "Preparing release %(new_version)s",
            "new_version": "0.3"}
    sufix_commit_msg(data)
    print data["commit_msg"] % data
