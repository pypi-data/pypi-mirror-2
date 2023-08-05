# −*− coding: UTF−8 −*−
from dateutil import rrule
from django.db.models.base import ModelBase
from eventtools.utils import OccurrenceReplacer
import datetime
from django.template.defaultfilters import date as date_filter
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from rules import Rule

"""
An OccurrenceGenerator defines the rules for generating a series of events. For example:
	• One occurrence, Tuesday 18th August 2010, 1500-1600
	• Every Tuesday, starting Tuesday 18th August
	• Every day except during Training Week, starting 17th August, finishing 30th October.
	• etc.

Occurrences which repeat need a repetition Rule (see rules.py for details).

The first_start/end_date/time fields describe the first occurrence. The repetition rule is then applied, to generate all occurrences that start before the `repeat_until` datetime.

Occurrences are NOT normally stored in the database, because there is a potentially infinite number of them, and besides, they can be generated quite quickly. Instead, only the Occurrences that have been edited are stored.

You might want to edit an occurrence if it's an exception to the 'norm'. For example:
	• It has a different start/end date
	• It has a different start/end time
	• It is cancelled
	• It has a more complex variation. This a foreign key to an EventVariation model.
	
See occurrences.py for details.
"""

class OccurrenceGeneratorManager(models.Manager):
        
    def occurrences_between(self, start, end):
        """
        Returns all Occurrences with a start_date/time between two datetimes, sorted. 
        
        This function is placed here because OccurrenceGenerators know the name of the Occurrence model, not currently vice-versa.
        However, we really want to hide this model, so lets make a convenience method in EventBaseManager.
        
        Get all OccurrenceGenerators that have the potential to produce occurrences between these dates.
        Run 'em all, and grab the ones that are in range.
            
        TODO - make this a queryset function too!            
        """
        
        if not isinstance(start, datetime.datetime):
            start = datetime.datetime.combine(start, datetime.time.min)
        
        if not isinstance(end, datetime.datetime):
            end = datetime.datetime.combine(end, datetime.time.max)
        
        
        # relevant generators have
        # the first_start_date before the requested end date AND
        # the end date is NULL or after the requested start date
        potental_occurrence_generators = self.filter(first_start_date__lte=end) & (self.filter(repeat_until__isnull=True) | self.filter(repeat_until__gte=start))
        
        occurrences = []
        for generator in potental_occurrence_generators:
            occurrences += generator.get_occurrences(start, end)
        
        #In case you are pondering returning a queryset, remember that potentially occurrences are not in the database, so no such QS exists.
        
        return sorted(occurrences)



class OccurrenceGeneratorModelBase(ModelBase):
    """
    When we create an OccurrenceGenerator, add to it an occurrence_model_name so it knows what to generate.
    """
    
    def __init__(cls, name, bases, attrs):
        if name != 'OccurrenceGeneratorBase': # This should only fire if this is a subclass
            model_name = name[0:-len("Generator")].lower()
            cls.add_to_class('_occurrence_model_name', model_name)
        super(OccurrenceGeneratorModelBase, cls).__init__(name, bases, attrs)
    
class OccurrenceGeneratorBase(models.Model):
    """
    Defines a set of repetition rules for an event
    """
    
    __metaclass__ = OccurrenceGeneratorModelBase
    objects = OccurrenceGeneratorManager()
    # Injected by EventModelBase:
    # event = models.ForeignKey(somekindofEvent)
    
    # Injected by OccurrenceGeneratorModelBase
    # _occurrence_model_lame = somekindofOccurrence
    
    first_start_date = models.DateField(_('start date of the first occurrence'))
    first_start_time = models.TimeField(_('start time of the first occurrence'))
    first_end_date = models.DateField(_('end date of the first occurrence'), null = True, blank = True, help_text=_("if you leave this blank, the same date as Start Date is assumed.")) 
    first_end_time = models.TimeField(_('start time of the first occurrence'))
    rule = models.ForeignKey(Rule, verbose_name=_("repetition rule"), null = True, blank = True, help_text=_("Select '----' for a one-off event."))
    repeat_until = models.DateTimeField(null = True, blank = True, help_text=_("This date is ignored for one-off events."))
    
    class Meta:
        ordering = ('first_start_date', 'first_start_time')
        abstract = True
        verbose_name = _('occurrence generator')
        verbose_name_plural = _('occurrence generators')

    def _occurrence_model(self):
        return models.get_model(self._meta.app_label, self._occurrence_model_name)
    OccurrenceModel = property(_occurrence_model)
     
    def _create_occurrence(self, start, end=None):
        if end is None:
            end = start + (self.end - self.start)
        occ = self.OccurrenceModel(
            generator=self,
            unvaried_start_date=start.date(),
            unvaried_start_time=start.time(),
            unvaried_end_date=end.date(),
            unvaried_end_time=end.time(),
        )
        return occ
 
    def _end_recurring_period(self):
        return self.repeat_until
    end_recurring_period = property(_end_recurring_period)

    def _get_occurrence_list(self, start, end):
        """
        generates a list of *unexceptional* Occurrences for this event between two datetimes, start and end.
        """
        
        difference = (self.end - self.start)
        if self.rule is not None:
            occurrences = []
            if self.end_recurring_period and self.end_recurring_period < end:
                end = self.end_recurring_period
            rule = self.get_rrule_object()
            o_starts = rule.between(start-difference, end, inc=True)
            for o_start in o_starts:
                o_end = o_start + difference
                occurrences.append(self._create_occurrence(o_start, o_end))
            return occurrences
        else:
            # check if event is in the period
            if self.start < end and self.end >= start:
                return [self._create_occurrence(self.start)]
            else:
                return []
                        
    def _occurrences_after_generator(self, after=None):
        """
        returns a generator that produces unexceptional occurrences after the
        datetime ``after``. For ever, if necessary.
        """

        if after is None:
            after = datetime.datetime.now()
        rule = self.get_rrule_object()
        if rule is None:
            if self.end > after:
                yield self._create_occurrence(self.start, self.end)
            raise StopIteration
        date_iter = iter(rule)
        difference = self.end - self.start
        while True:
            o_start = date_iter.next()
            if o_start > self.end_recurring_period:
                raise StopIteration
            o_end = o_start + difference
            if o_end > after:
                yield self._create_occurrence(o_start, o_end)

    # for backwards compatibility, we construct and deconstruct `start` and `end` datetimes.
    def _get_start(self):
        return datetime.datetime.combine(self.first_start_date, self.first_start_time)
    def _set_start(self, value):
        self.first_start_date = value.date()
        self.first_start_time = value.time()
    start = property(_get_start, _set_start)
    
    def _get_end_time(self):
        return self.first_end_time
    def _set_end_time(self, value):
        self.first_end_time = value
    end_time = property(_get_end_time, _set_end_time)    
        
    def _end(self):
        return datetime.datetime.combine(self.first_end_date or self.first_start_date, self.first_end_time)
    end = property(_end)

    def __unicode__(self):
        date_format = u'l, %s' % ugettext("DATE_FORMAT")
        result = ugettext('%(title)s: %(start)s-%(end)s') % {
            'title': unicode(self.event),
            'start': date_filter(self.start, date_format),
            'end': date_filter(self.end, date_format),
        }
        if self.rule:
            result += " repeating %s until %s" % (self.rule, date_filter(self.repeat_until, date_format))
            
        return result

    def get_occurrences(self, start, end):
        """
        returns a list of occurrences between the datetimes ``start`` and ``end``.
        Includes all of the exceptional Occurrences.
        """
        exceptional_occurrences = self.occurrences.all()
        occ_replacer = OccurrenceReplacer(exceptional_occurrences)
        occurrences = self._get_occurrence_list(start, end)
        final_occurrences = []
        for occ in occurrences:
            # replace occurrences with their exceptional counterparts
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)
                # ...but only if they are within this period
                if p_occ.start < end and p_occ.end >= start:
                    final_occurrences.append(p_occ)
            else:
              final_occurrences.append(occ)
        # then add exceptional occurrences which originated outside of this period but now
        # fall within it
        final_occurrences += occ_replacer.get_additional_occurrences(start, end)

        # import pdb; pdb.set_trace()
        return final_occurrences
        

    def get_rrule_object(self):
        if self.rule is not None:
            if self.rule.complex_rule:
                try:
                    return rrule.rrulestr(str(self.rule.complex_rule),dtstart=self.start)
                except:
                    pass
            params = self.rule.get_params()
            frequency = 'rrule.%s' % self.rule.frequency
            simple_rule = rrule.rrule(eval(frequency), dtstart=self.start, **params)
            set = rrule.rruleset()
            set.rrule(simple_rule)
#             goodfriday = rrule.rrule(rrule.YEARLY, dtstart=self.start, byeaster=-2)
#             christmas = rrule.rrule(rrule.YEARLY, dtstart=self.start, bymonth=12, bymonthday=25)
#             set.exrule(goodfriday)
#             set.exrule(christmas)
            return set
   
    def check_for_exceptions(self, occ):
        """
        Pass in an occurrence, pass out the occurrence, or an exceptional occurrence, if one exists in the db.
        """
        try:
            return self.OccurrenceModel.objects.get(
                generator = self,
                unvaried_start_date = occ.unvaried_start_date,
                unvaried_start_time = occ.unvaried_start_time,
                unvaried_end_date = occ.unvaried_end_date,
                unvaried_end_time = occ.unvaried_end_time,
            )
        except self.OccurrenceModel.DoesNotExist:
            return occ
                
    def get_first_occurrence(self):
        occ = self.OccurrenceModel(
                generator=self,
                unvaried_start_date=self.first_start_date,
                unvaried_start_time=self.first_start_time,
                unvaried_end_date=self.first_end_date,
                unvaried_end_time=self.first_end_time,
            )
        occ = self.check_for_exceptions(occ)
        return occ
    get_one_occurrence = get_first_occurrence

    def get_occurrence(self, date):
        rule = self.get_rrule_object()
        if rule:
            next_occurrence = rule.after(date, inc=True)
        else:
            next_occurrence = self.start
        if next_occurrence == date:
            try:
                return self.OccurrenceModel.objects.get(generator__event = self, unvaried_start_date = date)
            except self.OccurrenceModel.DoesNotExist:
                return self._create_occurrence(next_occurrence)
        # import pdb; pdb.set_trace()

    def occurrences_after(self, after=None):
        """
        returns a generator that produces occurrences after the datetime
        ``after``.	Includes all of the exceptional Occurrences.
        
        TODO: this doesn't bring in occurrences that were originally outside this date range, but now fall within it (or vice versa).
        """
        occ_replacer = OccurrenceReplacer(self.occurrence_set.all())
        generator = self._occurrences_after_generator(after)
        while True:
            next = generator.next()
            yield occ_replacer.get_occurrence(next)