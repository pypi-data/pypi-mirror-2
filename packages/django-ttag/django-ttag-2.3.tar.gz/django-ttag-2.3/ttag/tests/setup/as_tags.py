from django import template

import ttag

register = template.Library()


class FishAs(ttag.helpers.AsTag):

    def as_value(self, data, context):
        return 'fish'


class AnotherFishAs(FishAs):
    pass


class MaybeAs(ttag.helpers.AsTag):

    class Meta:
        as_required = False

    def as_value(self, data, context):
        return 'maybe'


class OutputAs(ttag.helpers.AsTag):
    value = ttag.Arg()

    class Meta:
        as_required = False

    def as_value(self, data, context):
        return data['value']

    def as_output(self, data, context):
        return 'yes_as'


register.tag(FishAs)
register.tag(AnotherFishAs)
register.tag(MaybeAs)
register.tag(OutputAs)
