class Audit():
    """Audit class to hold all kinds of audits."""
    def __init__(self, id, name, operation, time, description):
        """
        Args:
            id (str): id of the audit
            name (int): the name of the modified data
            operation (int): the operation performed
            time (date): time of creation
            description (str): description of audit
        """
        self.id = id
        self.name = name
        self.operation = operation
        self.time = time
        self.description = description

    def toDict(self):
        return dict(id=self.id, name=self.name, operation=self.operation,time=self.time,description=self.description)
