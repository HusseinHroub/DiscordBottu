class SimpleRankExtractor:
   def __init__(self, statType):
    self.statType = statType

   def extract(self, accountId):
     dbutils.