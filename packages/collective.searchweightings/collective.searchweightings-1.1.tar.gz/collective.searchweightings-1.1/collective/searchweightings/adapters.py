from collective.searchweightings.interfaces import ICatalogSorter
from DateTime.DateTime import DateTime
from Products.ZCatalog.Lazy import LazyMap

def normalize_brains(brains, highest):
    for brain in brains:
        brain.data_record_normalized_score_ = int(100.0 * brain.data_record_score_ / highest)

    res = sorted(brains, key=lambda x: 0-x.data_record_score_)
    return LazyMap(lambda x: x, res)


class DummySorter:
    """ A dummy sorter that does nothing """
    def sorted(self, brains):
        print "Done nothing!"
        return brains

class WeightedDateSorter:
    """ A sorter that weights new items higher """

    # you will need to tweak these values
    weight = 100
    halflife = 100 # days


    def sorted(self, brains):

        weight = self.weight
        halflife = self.halflife
        now = DateTime()


        highest=0
        for brain in brains:
            age = now - brain.modified
            score = brain.data_record_score_
            score += weight*(0.5**(age/halflife))
            brain.data_record_score_ = score
            highest = max(highest, score)
        
        return normalize_brains(brains, highest)
