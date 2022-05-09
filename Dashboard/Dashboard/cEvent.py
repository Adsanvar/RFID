class cEvent:
    # def __init__(self, id, title, allDay, start, end, className):
    #     super().__init__()
    #     self.id = id
    #     self.title = title
    #     self.allDay = allDay
    #     self.start = start
    #     self.end = end
    #     self.className = className
    def __init__(self, id, title, className, start, end):
        super().__init__()
        self.id = id
        self.title = title
        self.className = className
        # self.start = "new Date({}, {}, {})".format(year, month, day)
        # self.y = year
        # self.m = month
        # self.d = day
        self.start = start
        self.end = end

    


       

