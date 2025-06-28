from ape import project, accounts


def main():
    owner = accounts.load("brave")
    project.Ultramon.deploy(owner, sender=owner, publish=True)
