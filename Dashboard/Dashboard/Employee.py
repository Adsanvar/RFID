class Employee:
    def __init__(self, id, firstname, lastname, fobid, payrate, cash):
        super().__init__()
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.payrate = payrate
        self.cash = cash
        self.fobid = fobid