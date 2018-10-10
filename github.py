from github3 import login

gh = login('technhbot', 'technehru12')
org = 'PantherTech'

class GitHub():
    def reopen_issue(self, repo, num):
        issue = gh.issue(org, repo, num)
        if issue.is_closed():
            issue.reopen()
            return "Issue reopened!"
        return "Issue already open."


    def comment_issue(self, repo, num, comment):
        issue = gh.issue(org, repo, num)
        issue.create_comment(comment)
        return "Added comment!"


    def close_issue(self, repo, num):
        issue = gh.issue(org, repo, num)
        if(issue.close()):
            return "Issue closed."
        return "Issue already closed."


    def assign_issue(self, repo, num, assignee):
        issue = gh.issue(org, repo, num)
        if(issue.assign(assignee)):
            return "Assigned to " + assignee + "!"
        return "Unable to assign issue."